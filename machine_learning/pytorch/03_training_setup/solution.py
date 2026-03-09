import torch
import torch.nn as nn
import torch.optim as optim


def solve(X: torch.Tensor, y: torch.Tensor, epochs: int = 100) -> nn.Module:
    model = nn.Linear(1, 1)
    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    for _ in range(epochs):
        optimizer.zero_grad()
        output = model(X)
        loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()

    return model
