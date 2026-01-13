import torch
import torch.nn as nn


def run_tests(train_func):
    """
    Test suite for DataLoader setup.

    Args:
        train_func: A function that takes (X, y, batch_size, epochs)
                   and returns a trained model.
    """
    print(f"Running tests for {train_func.__name__}...\n")

    # Test 1: Returns a model
    X = torch.arange(20).float().unsqueeze(1) / 20
    y = X * 2

    model = train_func(X, y, batch_size=4, epochs=50)

    assert model is not None, "Test 1 failed: function should return a model"
    assert isinstance(model, nn.Module), "Test 1 failed: should return nn.Module"
    print("Test 1 passed: Returns an nn.Module")

    # Test 2: Model produces correct output shape
    with torch.no_grad():
        pred = model(torch.tensor([[0.5]]))

    assert pred.shape == (1, 1), (
        f"Test 2 failed: expected shape (1, 1), got {pred.shape}"
    )
    print("Test 2 passed: Model produces correct output shape")

    # Test 3: Model learns with small batch size
    X = torch.arange(50).float().unsqueeze(1) / 50
    y = X * 2

    model = train_func(X, y, batch_size=5, epochs=200)

    with torch.no_grad():
        pred = model(torch.tensor([[0.5]])).item()  # x=0.5 -> y=1.0

    assert abs(pred - 1.0) < 0.2, (
        f"Test 3 failed: prediction for x=0.5 should be ~1.0, got {pred:.2f}"
    )
    print(
        f"Test 3 passed: Model learned with batch_size=5 (predicts {pred:.2f} for x=0.5)"
    )

    # Test 4: Works with batch size larger than dataset
    X = torch.tensor([[0.1], [0.2], [0.3]])
    y = torch.tensor([[0.2], [0.4], [0.6]])

    model = train_func(X, y, batch_size=100, epochs=500)

    with torch.no_grad():
        pred = model(torch.tensor([[0.2]])).item()

    assert abs(pred - 0.4) < 0.1, (
        f"Test 4 failed: prediction for x=0.2 should be ~0.4, got {pred:.2f}"
    )
    print(f"Test 4 passed: Works with oversized batch (predicts {pred:.2f} for x=0.2)")

    # Test 5: Works with uneven batch size
    X = torch.arange(17).float().unsqueeze(1) / 17
    y = X + 0.5

    model = train_func(X, y, batch_size=4, epochs=200)

    with torch.no_grad():
        pred = model(torch.tensor([[0.5]])).item()  # x=0.5 -> y=1.0

    assert abs(pred - 1.0) < 0.2, (
        f"Test 5 failed: prediction for x=0.5 should be ~1.0, got {pred:.2f}"
    )
    print(f"Test 5 passed: Works with uneven batches (predicts {pred:.2f} for x=0.5)")

    print("\nAll tests passed!")
