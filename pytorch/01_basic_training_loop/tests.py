import torch
import torch.nn as nn
import torch.optim as optim

from test_utils import run_all


def run_tests(solve):
    torch.manual_seed(42)

    # Test 1 setup
    t1_model = nn.Linear(1, 1)
    t1_loss_fn = nn.MSELoss()
    t1_optimizer = optim.SGD(t1_model.parameters(), lr=0.0001)
    t1_X = torch.arange(100).float().unsqueeze(1)
    t1_y = t1_X / 2
    with torch.no_grad():
        t1_initial_loss = t1_loss_fn(t1_model(t1_X), t1_y).item()

    # Test 2 setup
    torch.manual_seed(42)
    t2_model = nn.Linear(1, 1)
    t2_initial_weight = t2_model.weight.data.clone()
    t2_optimizer = optim.SGD(t2_model.parameters(), lr=0.001)
    t2_X = torch.arange(50).float().unsqueeze(1)
    t2_y = t2_X * 2 + 1

    # Test 3 setup
    torch.manual_seed(42)
    t3_model = nn.Linear(1, 1)
    t3_optimizer = optim.SGD(t3_model.parameters(), lr=0.001)
    t3_X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0]])
    t3_y = torch.tensor([[2.0], [4.0], [6.0], [8.0], [10.0]])

    # Test 4 setup
    torch.manual_seed(42)
    t4_model = nn.Linear(1, 1)
    t4_optimizer = optim.SGD(t4_model.parameters(), lr=0.01)
    t4_X = torch.tensor([[1.0], [2.0]])
    t4_y = torch.tensor([[1.0], [2.0]])

    # Test 5 setup
    torch.manual_seed(42)
    t5_model = nn.Linear(1, 1)
    t5_optimizer = optim.SGD(t5_model.parameters(), lr=0.01)
    t5_X = torch.arange(10).float().unsqueeze(1)
    t5_y = t5_X

    # Test 6 setup (zero_grad check)
    torch.manual_seed(42)
    t6_model = nn.Linear(1, 1)
    t6_optimizer = optim.SGD(t6_model.parameters(), lr=0.5)
    t6_X = torch.linspace(0, 1, 20).unsqueeze(1)
    t6_y = t6_X * 2

    # Run pre-test training for tests that need state
    solve(t2_model, nn.MSELoss(), t2_optimizer, t2_X, t2_y, epochs=3)
    t2_weight_changed = not torch.allclose(t2_model.weight.data, t2_initial_weight)

    solve(t3_model, nn.MSELoss(), t3_optimizer, t3_X, t3_y, epochs=100)
    with torch.no_grad():
        t3_pred = t3_model(torch.tensor([[3.0]])).item()

    tests = [
        {
            "name": "returns float loss",
            "inputs": {
                "model": t1_model,
                "loss_fn": t1_loss_fn,
                "optimizer": t1_optimizer,
                "X": t1_X,
                "y": t1_y,
                "epochs": 5,
            },
            "check": lambda r: isinstance(r, float) and r < t1_initial_loss,
            "fail_msg": lambda r: f"expected loss < {t1_initial_loss:.4f}, got {r}",
        },
        {
            "name": "model weights change",
            "inputs": {
                "model": nn.Linear(1, 1),
                "loss_fn": nn.MSELoss(),
                "optimizer": optim.SGD([torch.nn.Parameter(torch.zeros(1))], lr=0.01),
                "X": torch.ones(5, 1),
                "y": torch.ones(5, 1),
                "epochs": 1,
            },
            "check": lambda r: t2_weight_changed,
            "fail_msg": "model weights should change after training",
        },
        {
            "name": "model learns y=2x",
            "inputs": {
                "model": nn.Linear(1, 1),
                "loss_fn": nn.MSELoss(),
                "optimizer": optim.SGD([torch.nn.Parameter(torch.zeros(1))], lr=0.01),
                "X": torch.ones(5, 1),
                "y": torch.ones(5, 1),
                "epochs": 1,
            },
            "check": lambda r: abs(t3_pred - 6.0) < 1.0,
            "fail_msg": lambda r: f"expected prediction ~6 for x=3, got {t3_pred:.2f}",
        },
        {
            "name": "works with small dataset",
            "inputs": {
                "model": t4_model,
                "loss_fn": nn.MSELoss(),
                "optimizer": t4_optimizer,
                "X": t4_X,
                "y": t4_y,
                "epochs": 10,
            },
            "check": lambda r: isinstance(r, float) and r >= 0,
            "fail_msg": lambda r: f"expected non-negative loss, got {r}",
        },
        {
            "name": "works with single epoch",
            "inputs": {
                "model": t5_model,
                "loss_fn": nn.MSELoss(),
                "optimizer": t5_optimizer,
                "X": t5_X,
                "y": t5_y,
                "epochs": 1,
            },
            "check": lambda r: r is not None,
            "fail_msg": "should work with single epoch",
        },
        {
            "name": "gradients cleared correctly (zero_grad)",
            "inputs": {
                "model": t6_model,
                "loss_fn": nn.MSELoss(),
                "optimizer": t6_optimizer,
                "X": t6_X,
                "y": t6_y,
                "epochs": 100,
            },
            "check": lambda r: r < 0.01,
            "fail_msg": lambda r: f"loss {r:.4f} > 0.01 after 100 epochs - did you forget zero_grad()?",
        },
    ]

    run_all("basic_training_loop", tests, solve)
