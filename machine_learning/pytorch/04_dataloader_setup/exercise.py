# DataLoader Setup
#
# Create a DataLoader from raw tensors and train a model.
# Create TensorDataset, DataLoader, model, and train.
#
import torch
import torch.nn as nn


def solve(
    X: torch.Tensor,
    y: torch.Tensor,
    batch_size: int = 8,
    epochs: int = 100,
) -> nn.Module:
    pass
