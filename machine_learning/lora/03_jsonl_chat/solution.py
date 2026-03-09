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
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    conversations = []
    with open(jsonl_path, "r") as f:
        for line in f:
            data = json.loads(line.strip())
            conversations.append(data["messages"])

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

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)

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
    model.save_pretrained(output_dir)

    return model
