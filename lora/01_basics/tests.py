import os
import tempfile

import torch
import torch.nn as nn
from peft import PeftModel


class SimpleModel(nn.Module):
    """Simple model with a linear layer for LoRA to target."""

    def __init__(self, in_features: int = 1, out_features: int = 1):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, x):
        return self.linear(x)


def run_tests(func):
    """Test suite for LoRA basics exercise."""
    print(f"Running tests for {func.__name__}...\n")

    # Test 1: Returns a PeftModel
    torch.manual_seed(42)
    model = SimpleModel()
    X = torch.linspace(0, 1, 20).unsqueeze(1)
    y = X * 2

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = os.path.join(tmpdir, "lora_adapters")
        result = func(model, X, y, save_path)

        assert result is not None, "Test 1 failed: function should return a model"
        assert isinstance(result, PeftModel), (
            f"Test 1 failed: should return PeftModel, got {type(result).__name__}"
        )
        print("Test 1 passed: Returns a PeftModel")

    # Test 2: LoRA adapters are saved to disk
    torch.manual_seed(42)
    model = SimpleModel()

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = os.path.join(tmpdir, "lora_adapters")
        func(model, X, y, save_path)

        assert os.path.exists(save_path), (
            f"Test 2 failed: save_path '{save_path}' does not exist"
        )
        adapter_config = os.path.join(save_path, "adapter_config.json")
        assert os.path.exists(adapter_config), (
            "Test 2 failed: adapter_config.json not found in save_path"
        )
        adapter_weights = os.path.join(save_path, "adapter_model.safetensors")
        adapter_weights_bin = os.path.join(save_path, "adapter_model.bin")
        assert os.path.exists(adapter_weights) or os.path.exists(adapter_weights_bin), (
            "Test 2 failed: adapter weights not found in save_path"
        )
        print("Test 2 passed: LoRA adapters saved to disk")

    # Test 3: Model learns the pattern (y = 2x)
    torch.manual_seed(42)
    model = SimpleModel()
    X = torch.linspace(0, 1, 20).unsqueeze(1)
    y = X * 2

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = os.path.join(tmpdir, "lora_adapters")
        peft_model = func(model, X, y, save_path, epochs=100)

        with torch.no_grad():
            pred = peft_model(torch.tensor([[0.5]])).item()

        assert abs(pred - 1.0) < 0.3, (
            f"Test 3 failed: prediction for x=0.5 should be ~1.0, got {pred:.2f}"
        )
        print(f"Test 3 passed: Model learned y=2x (predicts {pred:.2f} for x=0.5)")

    # Test 4: Only LoRA parameters are trainable
    torch.manual_seed(42)
    model = SimpleModel()

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = os.path.join(tmpdir, "lora_adapters")
        peft_model = func(model, X, y, save_path, epochs=1)

        trainable_params = sum(
            p.numel() for p in peft_model.parameters() if p.requires_grad
        )
        total_params = sum(p.numel() for p in peft_model.parameters())

        assert trainable_params < total_params, (
            "Test 4 failed: LoRA should freeze base model parameters"
        )
        print(f"Test 4 passed: Only {trainable_params}/{total_params} params trainable")

    # Test 5: Saved adapters can be loaded
    torch.manual_seed(42)
    model = SimpleModel()

    with tempfile.TemporaryDirectory() as tmpdir:
        save_path = os.path.join(tmpdir, "lora_adapters")
        trained_model = func(model, X, y, save_path, epochs=100)

        # Get prediction from trained model
        with torch.no_grad():
            trained_pred = trained_model(torch.tensor([[0.5]])).item()

        # Load adapters into a fresh model with same weights
        torch.manual_seed(42)
        fresh_model = SimpleModel()
        loaded_model = PeftModel.from_pretrained(fresh_model, save_path)

        with torch.no_grad():
            loaded_pred = loaded_model(torch.tensor([[0.5]])).item()

        assert abs(trained_pred - loaded_pred) < 0.01, (
            f"Test 5 failed: loaded model pred ({loaded_pred:.3f}) != "
            f"trained model pred ({trained_pred:.3f})"
        )
        print("Test 5 passed: Saved adapters can be loaded and produce same output")

    print("\nAll tests passed!")
