# Fine-tune an LLM on chat data using LoRA with JSONL input.
#
# Load a JSONL dataset in OpenAI fine-tune format, apply chat templates,
# and train the model using LoRA adapters.
#
# Steps:
#   1. Load the base model and tokenizer
#   2. Parse JSONL file into list of conversations
#   3. Apply tokenizer.apply_chat_template() to format conversations
#   4. Configure LoRA with appropriate target modules
#   5. Wrap the model with get_peft_model()
#   6. Train using HuggingFace Trainer
#   7. Save the LoRA adapters
#
# Args:
#     model_name: HuggingFace model ID (e.g., "Qwen/Qwen2.5-0.5B")
#     jsonl_path: Path to JSONL file with OpenAI fine-tune format
#     output_dir: Directory to save the trained LoRA adapters
#     epochs: Number of training epochs (default: 1)
#     batch_size: Training batch size (default: 4)
#
# Returns:
#     The trained PeftModel
#
# JSONL Format (OpenAI fine-tune API):
#     {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
#     {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
#
# Notes:
#     - Use LoraConfig with r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"]
#     - Set task_type="CAUSAL_LM" in LoraConfig
#     - Use lora_dropout=0.05
#     - Use tokenizer.apply_chat_template() with tokenize=True, add_generation_prompt=False
#     - Set max_length=256, truncation=True, padding="max_length" for tokenization
#
import json

from datasets import Dataset
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments


def train_lora_chat(
    model_name: str,
    jsonl_path: str,
    output_dir: str,
    epochs: int = 1,
    batch_size: int = 4,
) -> PeftModel:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train_lora_chat)
