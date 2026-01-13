import torch
import torch.nn as nn


def run_tests(train_func):
    """
    Test suite for training setup.

    Args:
        train_func: A function that takes (X, y, epochs) and returns a trained model.
    """
    print(f"Running tests for {train_func.__name__}...\n")

    # Test 1: Returns a model
    X = torch.tensor([[1.0], [2.0], [3.0]])
    y = torch.tensor([[2.0], [4.0], [6.0]])

    model = train_func(X, y, epochs=100)

    assert model is not None, "Test 1 failed: function should return a model"
    assert isinstance(model, nn.Module), "Test 1 failed: should return nn.Module"
    print("Test 1 passed: Returns an nn.Module")

    # Test 2: Model can make predictions with correct shape
    with torch.no_grad():
        pred = model(torch.tensor([[3.0]]))

    assert pred.shape == (1, 1), (
        f"Test 2 failed: expected shape (1, 1), got {pred.shape}"
    )
    print("Test 2 passed: Model produces correct output shape")

    # Test 3: Model learns a linear pattern
    X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0]])
    y = torch.tensor([[3.0], [5.0], [7.0], [9.0], [11.0]])

    model = train_func(X, y, epochs=1000)

    with torch.no_grad():
        pred = model(torch.tensor([[3.0]])).item()

    assert abs(pred - 7.0) < 1.0, (
        f"Test 3 failed: prediction for x=3 should be ~7, got {pred:.2f}"
    )
    print(f"Test 3 passed: Model learned the pattern (predicts {pred:.2f} for x=3)")

    # Test 4: Model generalizes to unseen data
    X = torch.arange(1, 11).float().unsqueeze(1)  # 1 to 10
    y = X * 2  # y = 2x

    model = train_func(X, y, epochs=1000)

    with torch.no_grad():
        # Test on value outside training range
        pred = model(torch.tensor([[15.0]])).item()

    assert abs(pred - 30.0) < 3.0, (
        f"Test 4 failed: prediction for x=15 should be ~30, got {pred:.2f}"
    )
    print(f"Test 4 passed: Model generalizes (predicts {pred:.2f} for x=15)")

    print("\nAll tests passed!")
