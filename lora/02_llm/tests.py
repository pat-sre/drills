import os
import tempfile

import torch
from datasets import Dataset, load_dataset
from peft import PeftModel

# Use a small model for testing
TEST_MODEL = "Qwen/Qwen2.5-0.5B"


def run_tests(train_lora_llm_func):
    """
    Test suite for LLM LoRA fine-tuning exercise.

    Args:
        train_lora_llm_func: A function that takes (model_name, dataset, output_dir, epochs, batch_size)
                            and returns a trained PeftModel.
    """
    print(f"Running tests for {train_lora_llm_func.__name__}...\n")

    # Load wikitext - use a small subset for fast testing
    print("Loading wikitext dataset...")
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train[:100]")
    # Filter out empty/short lines
    dataset = dataset.filter(lambda x: len(x["text"]) > 50)

    # Test 1: Returns a PeftModel
    print("Test 1: Checking return type...")
    with tempfile.TemporaryDirectory() as tmpdir:
        result = train_lora_llm_func(
            model_name=TEST_MODEL,
            dataset=dataset,
            output_dir=tmpdir,
            epochs=1,
            batch_size=2,
        )

        assert result is not None, "Test 1 failed: function should return a model"
        assert isinstance(result, PeftModel), (
            f"Test 1 failed: should return PeftModel, got {type(result).__name__}"
        )
        print("Test 1 passed: Returns a PeftModel")

    # Test 2: LoRA adapters are saved to disk
    print("Test 2: Checking adapters saved...")
    with tempfile.TemporaryDirectory() as tmpdir:
        train_lora_llm_func(
            model_name=TEST_MODEL,
            dataset=dataset,
            output_dir=tmpdir,
            epochs=1,
            batch_size=2,
        )

        adapter_config = os.path.join(tmpdir, "adapter_config.json")
        assert os.path.exists(adapter_config), (
            "Test 2 failed: adapter_config.json not found in output_dir"
        )

        adapter_weights = os.path.join(tmpdir, "adapter_model.safetensors")
        adapter_weights_bin = os.path.join(tmpdir, "adapter_model.bin")
        assert os.path.exists(adapter_weights) or os.path.exists(adapter_weights_bin), (
            "Test 2 failed: adapter weights not found in output_dir"
        )
        print("Test 2 passed: LoRA adapters saved to disk")

    # Test 3: Only LoRA parameters are trainable
    print("Test 3: Checking trainable parameters...")
    with tempfile.TemporaryDirectory() as tmpdir:
        peft_model = train_lora_llm_func(
            model_name=TEST_MODEL,
            dataset=dataset,
            output_dir=tmpdir,
            epochs=1,
            batch_size=2,
        )

        trainable_params = sum(
            p.numel() for p in peft_model.parameters() if p.requires_grad
        )
        total_params = sum(p.numel() for p in peft_model.parameters())

        assert trainable_params < total_params, (
            "Test 3 failed: LoRA should freeze base model parameters"
        )

        trainable_pct = 100 * trainable_params / total_params
        assert trainable_pct < 1.0, (
            f"Test 3 failed: trainable params ({trainable_pct:.2f}%) should be < 1% of total"
        )
        print(
            f"Test 3 passed: {trainable_params:,}/{total_params:,} params trainable ({trainable_pct:.3f}%)"
        )

    # Test 4: Model can generate after training
    print("Test 4: Checking model can generate...")
    with tempfile.TemporaryDirectory() as tmpdir:
        from transformers import AutoTokenizer

        peft_model = train_lora_llm_func(
            model_name=TEST_MODEL,
            dataset=dataset,
            output_dir=tmpdir,
            epochs=1,
            batch_size=2,
        )

        tokenizer = AutoTokenizer.from_pretrained(TEST_MODEL)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Move inputs to same device as model
        device = next(peft_model.parameters()).device
        inputs = tokenizer("Hello", return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = peft_model.generate(
                **inputs,
                max_new_tokens=5,
                pad_token_id=tokenizer.pad_token_id,
            )

        assert outputs.shape[1] > inputs["input_ids"].shape[1], (
            "Test 4 failed: model should generate new tokens"
        )
        print("Test 4 passed: Model generates after training")

    print("\nAll tests passed!")
