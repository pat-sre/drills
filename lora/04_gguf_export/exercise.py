# Export a LoRA fine-tuned model to GGUF format.
#
# Merge LoRA adapters into the base model and convert to GGUF format
# with quantization for efficient inference with llama.cpp.
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
# Args:
#     model_name: HuggingFace model ID (e.g., "Qwen/Qwen2.5-0.5B")
#     adapter_path: Path to saved LoRA adapters directory
#     output_path: Path for the output GGUF file (without extension)
#     llama_cpp_path: Path to llama.cpp directory (default: "~/llama.cpp")
#     quantization: Quantization type (default: "q4_k_m")
#
# Returns:
#     Path to the final quantized GGUF file
#
# Setup:
#     git clone https://github.com/ggml-org/llama.cpp ~/llama.cpp
#     cd ~/llama.cpp && make
#
# Notes:
#     - The llama.cpp directory must contain convert_hf_to_gguf.py
#     - The llama-quantize binary must be built (in build/bin/ or root)
#     - Supported quantization types: q4_k_m, q4_k_s, q5_k_m, q8_0, f16, etc.
#     - Q4_K_M is recommended as a good balance of size and quality
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
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(export_to_gguf)
