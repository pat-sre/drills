import json
import os
import tempfile

import torch
from peft import PeftModel

# Use a small model for testing
TEST_MODEL = "Qwen/Qwen2.5-0.5B"


def create_sample_jsonl(path: str):
    """Create a sample JSONL file for testing."""
    samples = [
        {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is 2+2?"},
                {"role": "assistant", "content": "4."},
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Hello!"},
                {"role": "assistant", "content": "Hello! How can I help you?"},
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "You answer concisely."},
                {"role": "user", "content": "Capital of France?"},
                {"role": "assistant", "content": "Paris."},
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "What color is the sky?"},
                {"role": "assistant", "content": "Blue."},
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "You are helpful."},
                {"role": "user", "content": "What is Python?"},
                {"role": "assistant", "content": "A programming language."},
            ]
        },
    ]

    with open(path, "w") as f:
        for sample in samples:
            f.write(json.dumps(sample) + "\n")


def run_tests(func):
    """Test suite for JSONL chat fine-tuning exercise."""
    print(f"Running tests for {func.__name__}...\n")

    # Test 1: Returns a PeftModel
    print("Test 1: Checking return type...")
    with tempfile.TemporaryDirectory() as tmpdir:
        jsonl_path = os.path.join(tmpdir, "train.jsonl")
        create_sample_jsonl(jsonl_path)
        output_dir = os.path.join(tmpdir, "adapters")

        result = func(
            model_name=TEST_MODEL,
            jsonl_path=jsonl_path,
            output_dir=output_dir,
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
        jsonl_path = os.path.join(tmpdir, "train.jsonl")
        create_sample_jsonl(jsonl_path)
        output_dir = os.path.join(tmpdir, "adapters")

        func(
            model_name=TEST_MODEL,
            jsonl_path=jsonl_path,
            output_dir=output_dir,
            epochs=1,
            batch_size=2,
        )

        adapter_config = os.path.join(output_dir, "adapter_config.json")
        assert os.path.exists(adapter_config), (
            "Test 2 failed: adapter_config.json not found in output_dir"
        )

        adapter_weights = os.path.join(output_dir, "adapter_model.safetensors")
        adapter_weights_bin = os.path.join(output_dir, "adapter_model.bin")
        assert os.path.exists(adapter_weights) or os.path.exists(adapter_weights_bin), (
            "Test 2 failed: adapter weights not found in output_dir"
        )
        print("Test 2 passed: LoRA adapters saved to disk")

    # Test 3: Only LoRA parameters are trainable
    print("Test 3: Checking trainable parameters...")
    with tempfile.TemporaryDirectory() as tmpdir:
        jsonl_path = os.path.join(tmpdir, "train.jsonl")
        create_sample_jsonl(jsonl_path)
        output_dir = os.path.join(tmpdir, "adapters")

        peft_model = func(
            model_name=TEST_MODEL,
            jsonl_path=jsonl_path,
            output_dir=output_dir,
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

        jsonl_path = os.path.join(tmpdir, "train.jsonl")
        create_sample_jsonl(jsonl_path)
        output_dir = os.path.join(tmpdir, "adapters")

        peft_model = func(
            model_name=TEST_MODEL,
            jsonl_path=jsonl_path,
            output_dir=output_dir,
            epochs=1,
            batch_size=2,
        )

        tokenizer = AutoTokenizer.from_pretrained(TEST_MODEL)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Format as chat
        messages = [{"role": "user", "content": "Hello!"}]
        input_ids = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        )

        device = next(peft_model.parameters()).device
        input_ids = input_ids.to(device)

        with torch.no_grad():
            outputs = peft_model.generate(
                input_ids,
                max_new_tokens=10,
                pad_token_id=tokenizer.pad_token_id,
            )

        assert outputs.shape[1] > input_ids.shape[1], (
            "Test 4 failed: model should generate new tokens"
        )
        print("Test 4 passed: Model generates after training")

    # Test 5: JSONL parsing handles multi-turn and system messages
    print("Test 5: Checking JSONL parsing...")
    with tempfile.TemporaryDirectory() as tmpdir:
        jsonl_path = os.path.join(tmpdir, "train.jsonl")

        # Create JSONL with varied formats
        samples = [
            # With system message
            {
                "messages": [
                    {"role": "system", "content": "Be concise."},
                    {"role": "user", "content": "Hi"},
                    {"role": "assistant", "content": "Hello!"},
                ]
            },
            # Without system message
            {
                "messages": [
                    {"role": "user", "content": "Bye"},
                    {"role": "assistant", "content": "Goodbye!"},
                ]
            },
            # Multi-turn
            {
                "messages": [
                    {"role": "user", "content": "What is 1+1?"},
                    {"role": "assistant", "content": "2"},
                    {"role": "user", "content": "And 2+2?"},
                    {"role": "assistant", "content": "4"},
                ]
            },
        ]

        with open(jsonl_path, "w") as f:
            for sample in samples:
                f.write(json.dumps(sample) + "\n")

        output_dir = os.path.join(tmpdir, "adapters")

        # Should not raise an error
        result = func(
            model_name=TEST_MODEL,
            jsonl_path=jsonl_path,
            output_dir=output_dir,
            epochs=1,
            batch_size=2,
        )

        assert result is not None, "Test 5 failed: should handle varied JSONL formats"
        print("Test 5 passed: JSONL parsing handles multi-turn and system messages")

    print("\nAll tests passed!")
