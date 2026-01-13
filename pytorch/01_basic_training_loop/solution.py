# Implement a basic PyTorch training loop.
#
# Training loop steps (per epoch):
#   1. zero_grad  - clear accumulated gradients
#   2. forward    - compute model output for all inputs
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
    epochs: int = 1,
) -> float:
    """
    Train the model and return the loss of the final epoch.
    """
    for epoch in range(epochs):
        # 1. zero_grad - clear accumulated gradients
        optimizer.zero_grad()

        # 2. forward - compute model output
        output = model(X)

        # 3. loss - compute loss between output and target
        loss = loss_fn(output, y)

        # 4. backward - compute gradients
        loss.backward()

        # 5. step - update weights
        optimizer.step()

    return loss.item()


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train)
