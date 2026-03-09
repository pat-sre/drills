import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from test_utils import run_all


def run_tests(solve):
    torch.manual_seed(42)

    # Test 1 setup
    t1_model = nn.Linear(1, 1)
    t1_optimizer = optim.SGD(t1_model.parameters(), lr=0.01)
    t1_X = torch.arange(20).float().unsqueeze(1) / 20
    t1_y = t1_X * 2
    t1_loader = DataLoader(TensorDataset(t1_X, t1_y), batch_size=4)

    # Test 2 setup
    torch.manual_seed(42)
    t2_model = nn.Linear(1, 1)
    t2_optimizer = optim.SGD(t2_model.parameters(), lr=0.1)
    t2_X = torch.arange(50).float().unsqueeze(1) / 50
    t2_y = t2_X * 2
    t2_loader = DataLoader(TensorDataset(t2_X, t2_y), batch_size=10)
    with torch.no_grad():
        t2_initial = sum(
            nn.MSELoss()(t2_model(x), y).item() for x, y in t2_loader
        ) / len(t2_loader)

    # Test 3 setup (uneven batch)
    torch.manual_seed(42)
    t3_model = nn.Linear(1, 1)
    t3_optimizer = optim.SGD(t3_model.parameters(), lr=0.1)
    t3_X = torch.arange(15).float().unsqueeze(1) / 15
    t3_y = t3_X + 0.5
    t3_loader = DataLoader(TensorDataset(t3_X, t3_y), batch_size=7)

    # Test 4 setup (learning check)
    torch.manual_seed(42)
    t4_model = nn.Linear(1, 1)
    t4_optimizer = optim.SGD(t4_model.parameters(), lr=0.1)
    t4_X = torch.arange(50).float().unsqueeze(1) / 50
    t4_y = t4_X * 3
    t4_loader = DataLoader(TensorDataset(t4_X, t4_y), batch_size=10)

    tests = [
        {
            "name": "returns float loss",
            "inputs": {
                "model": t1_model,
                "loss_fn": nn.MSELoss(),
                "optimizer": t1_optimizer,
                "dataloader": t1_loader,
                "epochs": 5,
            },
            "check": lambda r: isinstance(r, float),
            "fail_msg": lambda r: f"expected float, got {type(r).__name__}",
        },
        {
            "name": "loss decreases",
            "inputs": {
                "model": t2_model,
                "loss_fn": nn.MSELoss(),
                "optimizer": t2_optimizer,
                "dataloader": t2_loader,
                "epochs": 50,
            },
            "check": lambda r: r < t2_initial,
            "fail_msg": lambda r: f"expected loss < {t2_initial:.4f}, got {r:.4f}",
        },
        {
            "name": "works with uneven batch size",
            "inputs": {
                "model": t3_model,
                "loss_fn": nn.MSELoss(),
                "optimizer": t3_optimizer,
                "dataloader": t3_loader,
                "epochs": 10,
            },
            "check": lambda r: r >= 0,
            "fail_msg": lambda r: f"expected non-negative loss, got {r}",
        },
        {
            "name": "model learns pattern",
            "inputs": {
                "model": t4_model,
                "loss_fn": nn.MSELoss(),
                "optimizer": t4_optimizer,
                "dataloader": t4_loader,
                "epochs": 100,
            },
            "check": lambda r: abs(t4_model(torch.tensor([[0.5]])).item() - 1.5) < 0.3,
            "fail_msg": lambda r: f"expected prediction ~1.5 for x=0.5",
        },
    ]

    run_all("dataloader_training", tests, solve)
