import torch
import torch.nn as nn
import torch.optim as optim


def run_tests(train_func):
    """
    Test suite for basic training loop.

    Args:
        train_func: A function that takes (model, loss_fn, optimizer, X, y, epochs)
                   and returns the final epoch's loss.
    """
    print(f"Running tests for {train_func.__name__}...\n")

    # Test 1: Simple linear regression (y = x/2)
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.0001)

    X = torch.arange(100).float().unsqueeze(1)  # Shape: (100, 1)
    y = X / 2  # Shape: (100, 1)

    initial_loss = _compute_loss(model, loss_fn, X, y)
    final_loss = train_func(model, loss_fn, optimizer, X, y, epochs=5)

    assert final_loss is not None, "Test 1 failed: function should return a loss value"
    assert isinstance(final_loss, float), "Test 1 failed: loss should be a float"
    assert final_loss < initial_loss, (
        f"Test 1 failed: loss should decrease (initial: {initial_loss:.4f}, final: {final_loss:.4f})"
    )
    print(f"Test 1 passed: Loss decreased from {initial_loss:.4f} to {final_loss:.4f}")

    # Test 2: Model weights should change
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    initial_weight = model.weight.data.clone()
    initial_bias = model.bias.data.clone()

    optimizer = optim.SGD(model.parameters(), lr=0.001)
    X = torch.arange(50).float().unsqueeze(1)  # Shape: (50, 1)
    y = X * 2 + 1  # Shape: (50, 1)

    train_func(model, loss_fn, optimizer, X, y, epochs=3)

    weight_changed = not torch.allclose(model.weight.data, initial_weight)
    bias_changed = not torch.allclose(model.bias.data, initial_bias)

    assert weight_changed, "Test 2 failed: model weights should change after training"
    assert bias_changed, "Test 2 failed: model bias should change after training"
    print("Test 2 passed: Model parameters updated during training")

    # Test 3: Training improves predictions
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    optimizer = optim.SGD(model.parameters(), lr=0.001)

    X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0]])  # Shape: (5, 1)
    y = torch.tensor([[2.0], [4.0], [6.0], [8.0], [10.0]])  # y = 2x

    train_func(model, loss_fn, optimizer, X, y, epochs=100)

    # Test prediction on new data
    with torch.no_grad():
        pred = model(torch.tensor([[3.0]])).item()

    assert abs(pred - 6.0) < 1.0, (
        f"Test 3 failed: prediction for x=3 should be ~6, got {pred:.2f}"
    )
    print(f"Test 3 passed: Model learned y=2x (predicts {pred:.2f} for x=3)")

    # Test 4: Works with different dataset sizes
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    X = torch.tensor([[1.0], [2.0]])  # Shape: (2, 1)
    y = torch.tensor([[1.0], [2.0]])

    final_loss = train_func(model, loss_fn, optimizer, X, y, epochs=10)
    assert final_loss >= 0, "Test 4 failed: loss should be non-negative"
    print("Test 4 passed: Works with small dataset")

    # Test 5: Single epoch
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    X = torch.arange(10).float().unsqueeze(1)  # Shape: (10, 1)
    y = X

    final_loss = train_func(model, loss_fn, optimizer, X, y, epochs=1)
    assert final_loss is not None, "Test 5 failed: should work with single epoch"
    print("Test 5 passed: Works with single epoch")

    # Test 6: Catches missing zero_grad()
    # Without zero_grad(), gradients accumulate and prevent proper convergence
    torch.manual_seed(42)
    model = nn.Linear(1, 1)
    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.5)

    X = torch.linspace(0, 1, 20).unsqueeze(1)
    y = X * 2

    final_loss = train_func(model, loss_fn, optimizer, X, y, epochs=100)

    assert final_loss < 0.01, (
        f"Test 6 failed: Loss is {final_loss:.4f} after 100 epochs (expected < 0.01). "
        "Did you forget to call zero_grad()?"
    )
    print("Test 6 passed: Gradients cleared correctly each epoch")

    print("\nAll tests passed!")


def _compute_loss(model, loss_fn, X, y):
    """Helper to compute loss without training."""
    with torch.no_grad():
        output = model(X)
        loss = loss_fn(output, y)
    return loss.item()
