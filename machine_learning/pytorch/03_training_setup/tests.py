import torch
import torch.nn as nn

from test_utils import run_all


def run_tests(solve):
    # Test 1: returns model
    t1_X = torch.tensor([[1.0], [2.0], [3.0]])
    t1_y = torch.tensor([[2.0], [4.0], [6.0]])

    # Test 3: learns pattern
    t3_X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0]])
    t3_y = torch.tensor([[3.0], [5.0], [7.0], [9.0], [11.0]])

    # Test 4: generalizes
    t4_X = torch.arange(1, 11).float().unsqueeze(1)
    t4_y = t4_X * 2

    tests = [
        {
            "name": "returns nn.Module",
            "inputs": {"X": t1_X, "y": t1_y, "epochs": 100},
            "check": lambda r: isinstance(r, nn.Module),
            "fail_msg": lambda r: f"expected nn.Module, got {type(r).__name__}",
        },
        {
            "name": "model produces correct shape",
            "inputs": {"X": t1_X, "y": t1_y, "epochs": 100},
            "check": lambda r: r(torch.tensor([[3.0]])).shape == (1, 1),
            "fail_msg": lambda r: f"expected shape (1, 1), got {r(torch.tensor([[3.0]])).shape}",
        },
        {
            "name": "learns linear pattern",
            "inputs": {"X": t3_X, "y": t3_y, "epochs": 1000},
            "check": lambda r: abs(r(torch.tensor([[3.0]])).item() - 7.0) < 1.0,
            "fail_msg": lambda r: f"expected ~7 for x=3, got {r(torch.tensor([[3.0]])).item():.2f}",
        },
        {
            "name": "generalizes to unseen data",
            "inputs": {"X": t4_X, "y": t4_y, "epochs": 1000},
            "check": lambda r: abs(r(torch.tensor([[15.0]])).item() - 30.0) < 3.0,
            "fail_msg": lambda r: f"expected ~30 for x=15, got {r(torch.tensor([[15.0]])).item():.2f}",
        },
    ]

    run_all("training_setup", tests, solve)
