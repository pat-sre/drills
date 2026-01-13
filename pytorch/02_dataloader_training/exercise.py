# DataLoader Training
#
# Train a model using mini-batches from a DataLoader.
#
# Instead of processing all data at once, iterate over batches.
# Each batch gets its own forward/backward pass.
#
# The DataLoader yields (X_batch, y_batch) tuples.
#
# Args:
#     model: PyTorch model to train
#     loss_fn: Loss function
#     optimizer: Optimizer
#     dataloader: DataLoader yielding (X_batch, y_batch) tuples
#     epochs: Number of training epochs
#
# Returns:
#     Average loss for the final epoch (float)
#
import torch
import torch.nn as nn
from torch.utils.data import DataLoader


def train(
    model: nn.Module,
    loss_fn: nn.Module,
    optimizer: torch.optim.Optimizer,
    dataloader: DataLoader,
    epochs: int = 1,
) -> float:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train)
