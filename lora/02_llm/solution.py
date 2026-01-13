# Fine-tune an LLM using LoRA with HuggingFace Trainer.
#
# Steps:
#   1. Load the base model and tokenizer
#   2. Configure LoRA with appropriate target modules
#   3. Wrap the model with get_peft_model()
#   4. Tokenize the dataset
#   5. Train using HuggingFace Trainer
#   6. Save the LoRA adapters
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
    """
    Fine-tune an LLM with LoRA and save the adapters.
    """
    # 1. Load base model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Ensure tokenizer has a pad token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 2. Configure LoRA
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )

    # 3. Wrap model with LoRA adapters
    model = get_peft_model(model, lora_config)

    # 4. Tokenize the dataset
    def tokenize(examples):
        tokens = tokenizer(
            examples["text"],
            max_length=128,
            truncation=True,
            padding="max_length",
        )
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    tokenized_dataset = dataset.map(tokenize, batched=True, remove_columns=["text"])

    # 5. Train using HuggingFace Trainer
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

    # 6. Save the LoRA adapters
    model.save_pretrained(output_dir)

    return model


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train_lora_llm)
