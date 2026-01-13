# Implement basic LoRA (Low-Rank Adaptation) training with PEFT.
#
# Given a simple model, apply LoRA adapters, train on data,
# and save the adapters to a directory.
#
# Steps:
#   1. Create a LoraConfig targeting the "linear" layer
#   2. Wrap the model with get_peft_model()
#   3. Train the model using a basic training loop
#   4. Save only the LoRA adapters (not the full model)
#
# Args:
#     model: A simple nn.Module with a "linear" layer to adapt
#     X: Input tensor of shape (N, features)
#     y: Target tensor of shape (N, 1)
#     save_path: Directory path to save the LoRA adapters
#     epochs: Number of training epochs (default: 100)
#     lr: Learning rate (default: 0.01)
#
# Returns:
#     The trained PeftModel
#
# Notes:
#     - Use LoraConfig with r=8, lora_alpha=16, target_modules=["linear"]
#     - Use MSELoss and SGD optimizer
#     - The save_path directory will be created if it doesn't exist
#
import torch
import torch.nn as nn
from peft import LoraConfig, get_peft_model


def train_lora(
    model: nn.Module,
    X: torch.Tensor,
    y: torch.Tensor,
    save_path: str,
    epochs: int = 100,
    lr: float = 0.01,
) -> nn.Module:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train_lora)
