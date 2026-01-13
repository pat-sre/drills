# Implement a basic PyTorch training loop.
#
# Given a model, loss function, optimizer, and data (X, y),
# train the model for the specified number of epochs.
#
# Return the final loss value (last epoch).
#
# Training loop steps (per epoch):
#   1. zero_grad  - clear accumulated gradients
#   2. forward    - compute model output for all inputs
#   3. loss       - compute loss between output and target
#   4. backward   - compute gradients
#   5. step       - update weights
#
# Args:
#     model: PyTorch model to train
#     loss_fn: Loss function (e.g., nn.MSELoss())
#     optimizer: Optimizer (e.g., optim.SGD(model.parameters(), lr=0.01))
#     X: Input data tensor of shape (N, features)
#     y: Target data tensor of shape (N, 1)
#     epochs: Number of training epochs
#
# Returns:
#     Loss value for the final epoch (float)
#
import torch
import torch.nn as nn


def train(
    model: nn.Module,
    loss_fn: nn.Module,
    optimizer: torch.optim.Optimizer,
    X: torch.Tensor,
    y: torch.Tensor,
    epochs: int = 1,
) -> float:
    for _ in range(epochs):
        model.zero_grad()
        out = model(X)
        loss = loss_fn(out, y)
        loss.backward()
        optimizer.step()
    return loss.item()


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train)
