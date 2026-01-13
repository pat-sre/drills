import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


def run_tests(train_func):
    """
    Test suite for DataLoader training.

    Args:
        train_func: A function that takes (model, loss_fn, optimizer, dataloader, epochs)
                   and returns the final epoch's average loss.
    """
    print(f"Running tests for {train_func.__name__}...\n")

    # Test 1: Returns a loss value
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    X = torch.arange(20).float().unsqueeze(1) / 20  # Normalize to [0, 1)
    y = X * 2
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=4)

    final_loss = train_func(model, loss_fn, optimizer, dataloader, epochs=5)

    assert final_loss is not None, "Test 1 failed: function should return a loss value"
    assert isinstance(final_loss, float), "Test 1 failed: loss should be a float"
    print(f"Test 1 passed: Returns a float loss ({final_loss:.4f})")

    # Test 2: Loss decreases with training
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    X = torch.arange(50).float().unsqueeze(1) / 50  # Normalize
    y = X * 2
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=10)

    initial_loss = _compute_avg_loss(model, loss_fn, dataloader)
    final_loss = train_func(model, loss_fn, optimizer, dataloader, epochs=50)

    assert final_loss < initial_loss, (
        f"Test 2 failed: loss should decrease (initial: {initial_loss:.4f}, final: {final_loss:.4f})"
    )
    print(f"Test 2 passed: Loss decreased from {initial_loss:.4f} to {final_loss:.4f}")

    # Test 3: Works with different batch sizes
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    X = torch.arange(15).float().unsqueeze(1) / 15
    y = X + 0.5
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=7)  # Doesn't divide evenly

    final_loss = train_func(model, loss_fn, optimizer, dataloader, epochs=10)

    assert final_loss >= 0, "Test 3 failed: loss should be non-negative"
    print(f"Test 3 passed: Works with uneven batch size ({final_loss:.4f})")

    # Test 4: Model learns the pattern
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    X = torch.arange(50).float().unsqueeze(1) / 50
    y = X * 3
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=10)

    train_func(model, loss_fn, optimizer, dataloader, epochs=100)

    with torch.no_grad():
        pred = model(torch.tensor([[0.5]])).item()  # x=0.5 -> y=1.5

    assert abs(pred - 1.5) < 0.3, (
        f"Test 4 failed: prediction for x=0.5 should be ~1.5, got {pred:.2f}"
    )
    print(f"Test 4 passed: Model learned the pattern (predicts {pred:.2f} for x=0.5)")

    print("\nAll tests passed!")


def _compute_avg_loss(model, loss_fn, dataloader):
    """Helper to compute average loss without training."""
    total_loss = 0.0
    num_batches = 0
    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            output = model(X_batch)
            loss = loss_fn(output, y_batch)
            total_loss += loss.item()
            num_batches += 1
    return total_loss / num_batches
