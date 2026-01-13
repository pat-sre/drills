# DataLoader Setup
#
# Create a DataLoader from raw tensors and train a model.
#
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


def train(
    X: torch.Tensor,
    y: torch.Tensor,
    batch_size: int = 8,
    epochs: int = 100,
) -> nn.Module:
    # 1. Create dataset
    dataset = TensorDataset(X, y)

    # 2. Create DataLoader
    dataloader = DataLoader(dataset, batch_size=batch_size)

    # 3. Create model, loss, optimizer
    model = nn.Linear(1, 1)
    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # 4. Train
    for epoch in range(epochs):
        for X_batch, y_batch in dataloader:
            optimizer.zero_grad()
            output = model(X_batch)
            loss = loss_fn(output, y_batch)
            loss.backward()
            optimizer.step()

    # 5. Return trained model
    return model


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(train)
