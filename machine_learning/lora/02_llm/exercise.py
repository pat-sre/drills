# LoRA LLM Fine-tuning
#
# Fine-tune an LLM with LoRA using HuggingFace Trainer.
# Use LoraConfig with r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"]
#
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments


def solve(
    model_name: str,
    dataset: Dataset,
    output_dir: str,
    epochs: int = 1,
    batch_size: int = 4,
):
    pass
