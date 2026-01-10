# Implement a basic PyTorch training loop.
#
# Given a model, loss function, optimizer, and data (X, y),
# train the model for the specified number of epochs.
#
# Return the final average loss for the last epoch.
#
# Training loop steps (per sample):
#   1. zero_grad  - clear accumulated gradients
#   2. forward    - compute model output
#   3. loss       - compute loss between output and target
#   4. backward   - compute gradients
#   5. step       - update weights
#
import torch
import torch.nn as nn


def train(
    model: nn.Module,
    loss_fn: nn.Module,
    optimizer: torch.optim.Optimizer,
    X: torch.Tensor,
    y: torch.Tensor,
    epochs: int = 10,
) -> float:
    """
    Train the model and return the average loss of the final epoch.

    Args:
        model: PyTorch model to train
        loss_fn: Loss function (e.g., nn.MSELoss())
        optimizer: Optimizer (e.g., optim.SGD(model.parameters(), lr=0.01))
        X: Input data tensor of shape (N,) or (N, features)
        y: Target data tensor of shape (N,)
        epochs: Number of training epochs

    Returns:
        Average loss for the final epoch
    """
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_train_tests
    else:
        from tests import run_train_tests

    run_train_tests(train)
