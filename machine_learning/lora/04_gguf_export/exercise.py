# GGUF Export
#
# Merge LoRA adapters and export to quantized GGUF format.
# Requires llama.cpp with convert_hf_to_gguf.py and llama-quantize.
#
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
    pass
