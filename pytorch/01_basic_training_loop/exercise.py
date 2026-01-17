# Basic Training Loop
#
# Train a model for the specified number of epochs.
# Return the final loss value (last epoch).
#
# Training loop steps (per epoch):
#   1. zero_grad  - clear accumulated gradients
#   2. forward    - compute model output
#   3. loss       - compute loss between output and target
#   4. backward   - compute gradients
#   5. step       - update weights
#
import torch
import torch.nn as nn


def solve(
    model: nn.Module,
    loss_fn: nn.Module,
    optimizer: torch.optim.Optimizer,
    X: torch.Tensor,
    y: torch.Tensor,
    epochs: int = 1,
) -> float:
    pass
