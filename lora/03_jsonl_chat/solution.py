# Fine-tune an LLM on chat data using LoRA with JSONL input.
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
    """
    Fine-tune an LLM on chat data with LoRA and save the adapters.
    """
    # 1. Load base model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 2. Parse JSONL file into list of conversations
    conversations = []
    with open(jsonl_path, "r") as f:
        for line in f:
            data = json.loads(line.strip())
            conversations.append(data["messages"])

    # 3. Apply chat template to format conversations
    def tokenize_conversation(examples):
        tokenized = []
        for messages in examples["messages"]:
            tokens = tokenizer.apply_chat_template(
                messages,
                tokenize=True,
                add_generation_prompt=False,
                max_length=256,
                truncation=True,
                padding="max_length",
                return_tensors=None,
            )
            tokenized.append(tokens)

        return {
            "input_ids": tokenized,
            "attention_mask": [
                [1 if t != tokenizer.pad_token_id else 0 for t in ids]
                for ids in tokenized
            ],
            "labels": tokenized,
        }

    dataset = Dataset.from_dict({"messages": conversations})
    tokenized_dataset = dataset.map(
        tokenize_conversation,
        batched=True,
        remove_columns=["messages"],
    )

    # 4. Configure LoRA
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )

    # 5. Wrap model with LoRA adapters
    model = get_peft_model(model, lora_config)

    # 6. Train using HuggingFace Trainer
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        logging_steps=10,
        save_strategy="no",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )

    trainer.train()

    # 7. Save the LoRA adapters
    model.save_pretrained(output_dir)

    return model


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train_lora_chat)
