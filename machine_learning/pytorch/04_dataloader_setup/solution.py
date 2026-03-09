import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


def solve(
    X: torch.Tensor,
    y: torch.Tensor,
    batch_size: int = 8,
    epochs: int = 100,
) -> nn.Module:
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=batch_size)

    model = nn.Linear(1, 1)
    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    for epoch in range(epochs):
        for X_batch, y_batch in dataloader:
            optimizer.zero_grad()
            output = model(X_batch)
            loss = loss_fn(output, y_batch)
            loss.backward()
            optimizer.step()

    return model
