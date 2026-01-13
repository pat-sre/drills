# DataLoader Setup
#
# Create a DataLoader from raw tensors and train a model.
#
# Given X and y tensors, you need to:
#   1. Create a TensorDataset from X and y
#   2. Create a DataLoader with the specified batch size
#   3. Create model, loss function, and optimizer
#   4. Train using mini-batches
#   5. Return the trained model
#
# Args:
#     X: Input data tensor of shape (N, 1)
#     y: Target data tensor of shape (N, 1)
#     batch_size: Number of samples per batch
#     epochs: Number of training epochs
#
# Returns:
#     Trained model (nn.Module)
#
import torch
import torch.nn as nn


def train(
    X: torch.Tensor,
    y: torch.Tensor,
    batch_size: int = 8,
    epochs: int = 100,
) -> nn.Module:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train)
