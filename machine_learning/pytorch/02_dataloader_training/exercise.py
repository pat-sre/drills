# DataLoader Training
#
# Train a model using mini-batches from a DataLoader.
# The DataLoader yields (X_batch, y_batch) tuples.
#
# Return the average loss for the final epoch.
#
import torch
import torch.nn as nn
from torch.utils.data import DataLoader


def solve(
    model: nn.Module,
    loss_fn: nn.Module,
    optimizer: torch.optim.Optimizer,
    dataloader: DataLoader,
    epochs: int = 1,
) -> float:
    pass
