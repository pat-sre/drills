# LoRA Chat Fine-tuning
#
# Fine-tune an LLM on JSONL chat data with LoRA.
# Use tokenizer.apply_chat_template() for formatting.
#
import json

from datasets import Dataset
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments


def solve(
    model_name: str,
    jsonl_path: str,
    output_dir: str,
    epochs: int = 1,
    batch_size: int = 4,
) -> PeftModel:
    pass
