# Fine-tune an LLM using LoRA with HuggingFace Trainer.
#
# Apply LoRA adapters to a real language model and fine-tune it
# on a text dataset using the HuggingFace Trainer API.
#
# Steps:
#   1. Load the base model and tokenizer
#   2. Configure LoRA with appropriate target modules
#   3. Wrap the model with get_peft_model()
#   4. Tokenize the dataset
#   5. Train using HuggingFace Trainer
#   6. Save the LoRA adapters
#
# Args:
#     model_name: HuggingFace model ID (e.g., "Qwen/Qwen2.5-0.5B")
#     dataset: A HuggingFace Dataset with a "text" column (e.g., tiny_shakespeare)
#     output_dir: Directory to save the trained LoRA adapters
#     epochs: Number of training epochs (default: 1)
#     batch_size: Training batch size (default: 4)
#
# Returns:
#     The trained PeftModel
#
# Notes:
#     - Use LoraConfig with r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"]
#     - Set task_type="CAUSAL_LM" in LoraConfig
#     - Use lora_dropout=0.05
#     - Tokenize with max_length=128, truncation=True, padding="max_length"
#     - Dataset: load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
#
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments


def train_lora_llm(
    model_name: str,
    dataset: Dataset,
    output_dir: str,
    epochs: int = 1,
    batch_size: int = 4,
):
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train_lora_llm)
