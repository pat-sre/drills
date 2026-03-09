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
    for epoch in range(epochs):
        total_loss = 0.0
        num_batches = 0

        for X_batch, y_batch in dataloader:
            optimizer.zero_grad()
            output = model(X_batch)
            loss = loss_fn(output, y_batch)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            num_batches += 1

        avg_loss = total_loss / num_batches

    return avg_loss
