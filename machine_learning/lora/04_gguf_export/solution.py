import os
import subprocess
import tempfile

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def solve(
    model_name: str,
    adapter_path: str,
    output_path: str,
    llama_cpp_path: str = "~/llama.cpp",
    quantization: str = "q4_k_m",
) -> str:
    llama_cpp_path = os.path.expanduser(llama_cpp_path)

    convert_script = os.path.join(llama_cpp_path, "convert_hf_to_gguf.py")
    if not os.path.exists(convert_script):
        raise FileNotFoundError(
            f"convert_hf_to_gguf.py not found at {convert_script}. "
            f"Please install llama.cpp: git clone https://github.com/ggml-org/llama.cpp {llama_cpp_path}"
        )

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

    base_model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = PeftModel.from_pretrained(base_model, adapter_path)
    merged_model = model.merge_and_unload()

    with tempfile.TemporaryDirectory() as tmpdir:
        merged_path = os.path.join(tmpdir, "merged_model")
        merged_model.save_pretrained(merged_path)
        tokenizer.save_pretrained(merged_path)

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

        if quantization.lower() == "f16":
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
            os.remove(f16_path)

    return final_path
