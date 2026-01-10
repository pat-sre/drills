# Implement a basic PyTorch training loop.
#
# Training loop steps (per sample):
#   1. zero_grad  - clear accumulated gradients
#   2. forward    - compute model output
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
    epochs: int = 10,
) -> float:
    """
    Train the model and return the average loss of the final epoch.
    """
    dataset_size = len(X)
    final_epoch_loss = 0.0

    for epoch in range(epochs):
        epoch_loss = 0.0
        for i in range(dataset_size):
            # 1. zero_grad - clear accumulated gradients
            optimizer.zero_grad()

            # 2. forward - compute model output
            input_data = X[i].unsqueeze(0).float()
            output = model(input_data)

            # 3. loss - compute loss between output and target
            target = y[i].unsqueeze(0).float()
            loss = loss_fn(output, target)
            epoch_loss += loss.item()

            # 4. backward - compute gradients
            loss.backward()

            # 5. step - update weights
            optimizer.step()

        final_epoch_loss = epoch_loss / dataset_size

    return final_epoch_loss


if __name__ == "__main__":
    if __package__:
        from .tests import run_train_tests
    else:
        from tests import run_train_tests

    run_train_tests(train)
