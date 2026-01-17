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
    for epoch in range(epochs):
        optimizer.zero_grad()
        output = model(X)
        loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()

    return loss.item()
