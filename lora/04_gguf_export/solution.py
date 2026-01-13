# Export a LoRA fine-tuned model to GGUF format.
#
# Steps:
#   1. Load the base model from HuggingFace
#   2. Load LoRA adapters with PeftModel.from_pretrained()
#   3. Merge adapters into base model with merge_and_unload()
#   4. Save merged model to temporary HuggingFace format
#   5. Convert to GGUF (F16) using llama.cpp convert_hf_to_gguf.py
#   6. Quantize to target format using llama-quantize
#   7. Return path to final GGUF file
#
import os
import subprocess
import tempfile

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def export_to_gguf(
    model_name: str,
    adapter_path: str,
    output_path: str,
    llama_cpp_path: str = "~/llama.cpp",
    quantization: str = "q4_k_m",
) -> str:
    """
    Merge LoRA adapters and export to quantized GGUF format.
    """
    llama_cpp_path = os.path.expanduser(llama_cpp_path)

    # Validate llama.cpp installation
    convert_script = os.path.join(llama_cpp_path, "convert_hf_to_gguf.py")
    if not os.path.exists(convert_script):
        raise FileNotFoundError(
            f"convert_hf_to_gguf.py not found at {convert_script}. "
            f"Please install llama.cpp: git clone https://github.com/ggml-org/llama.cpp {llama_cpp_path}"
        )

    # Find llama-quantize binary
    quantize_bin = None
    for path in [
        os.path.join(llama_cpp_path, "build", "bin", "llama-quantize"),
        os.path.join(llama_cpp_path, "llama-quantize"),
        os.path.join(llama_cpp_path, "quantize"),
    ]:
        if os.path.exists(path):
            quantize_bin = path
            break

    if quantize_bin is None:
        raise FileNotFoundError(
            f"llama-quantize not found in {llama_cpp_path}. "
            "Please build llama.cpp: cd llama.cpp && make"
        )

    # 1. Load base model
    base_model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # 2. Load LoRA adapters
    model = PeftModel.from_pretrained(base_model, adapter_path)

    # 3. Merge adapters into base model
    merged_model = model.merge_and_unload()

    # 4. Save merged model to temporary HuggingFace format
    with tempfile.TemporaryDirectory() as tmpdir:
        merged_path = os.path.join(tmpdir, "merged_model")
        merged_model.save_pretrained(merged_path)
        tokenizer.save_pretrained(merged_path)

        # 5. Convert to GGUF (F16)
        f16_path = f"{output_path}-f16.gguf"
        subprocess.run(
            [
                "python",
                convert_script,
                merged_path,
                "--outtype",
                "f16",
                "--outfile",
                f16_path,
            ],
            check=True,
            capture_output=True,
        )

        # 6. Quantize to target format
        if quantization.lower() == "f16":
            # No quantization needed
            final_path = f16_path
        else:
            final_path = f"{output_path}-{quantization}.gguf"
            subprocess.run(
                [
                    quantize_bin,
                    f16_path,
                    final_path,
                    quantization.upper(),
                ],
                check=True,
                capture_output=True,
            )
            # Clean up F16 intermediate file
            os.remove(f16_path)

    # 7. Return path to final GGUF file
    return final_path


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(export_to_gguf)
