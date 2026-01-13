# Training Setup
#
# Build a complete training pipeline from scratch.
#
import torch
import torch.nn as nn
import torch.optim as optim


def train(X: torch.Tensor, y: torch.Tensor, epochs: int = 100) -> nn.Module:
    # 1. Create model
    model = nn.Linear(1, 1)

    # 2. Choose loss function
    loss_fn = nn.MSELoss()

    # 3. Create optimizer
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # 4. Training loop
    for _ in range(epochs):
        optimizer.zero_grad()
        output = model(X)
        loss = loss_fn(output, y)
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
