# Basic LoRA Training
#
# Apply LoRA adapters to a model, train, and save adapters.
# Use LoraConfig with r=8, lora_alpha=16, target_modules=["linear"]
#
import torch
import torch.nn as nn
from peft import LoraConfig, get_peft_model


def solve(
    model: nn.Module,
    X: torch.Tensor,
    y: torch.Tensor,
    save_path: str,
    epochs: int = 100,
    lr: float = 0.01,
) -> nn.Module:
    pass
