# Training Setup
#
# Build a complete training pipeline from scratch.
#
# Given input data X (shape N, 1) and targets y (shape N, 1),
# create and train a model to predict y from X.
#
# You need to:
#   1. Create a model
#   2. Choose a loss function
#   3. Create an optimizer
#   4. Train for the specified number of epochs
#   5. Return the trained model
#
# Args:
#     X: Input data tensor of shape (N, 1)
#     y: Target data tensor of shape (N, 1)
#     epochs: Number of training epochs
#
# Returns:
#     Trained model (nn.Module)
#
import torch
import torch.nn as nn


def train(X: torch.Tensor, y: torch.Tensor, epochs: int = 100) -> nn.Module:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train)
