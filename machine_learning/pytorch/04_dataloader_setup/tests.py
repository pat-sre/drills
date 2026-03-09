import torch
import torch.nn as nn

from test_utils import run_all


def run_tests(solve):
    # Test 1 setup
    t1_X = torch.arange(20).float().unsqueeze(1) / 20
    t1_y = t1_X * 2

    # Test 3 setup (small batch)
    t3_X = torch.arange(50).float().unsqueeze(1) / 50
    t3_y = t3_X * 2

    # Test 4 setup (oversized batch)
    t4_X = torch.tensor([[0.1], [0.2], [0.3]])
    t4_y = torch.tensor([[0.2], [0.4], [0.6]])

    # Test 5 setup (uneven batch)
    t5_X = torch.arange(17).float().unsqueeze(1) / 17
    t5_y = t5_X + 0.5

    tests = [
        {
            "name": "returns nn.Module",
            "inputs": {"X": t1_X, "y": t1_y, "batch_size": 4, "epochs": 50},
            "check": lambda r: isinstance(r, nn.Module),
            "fail_msg": lambda r: f"expected nn.Module, got {type(r).__name__}",
        },
        {
            "name": "model produces correct shape",
            "inputs": {"X": t1_X, "y": t1_y, "batch_size": 4, "epochs": 50},
            "check": lambda r: r(torch.tensor([[0.5]])).shape == (1, 1),
            "fail_msg": lambda r: f"expected shape (1, 1)",
        },
        {
            "name": "learns with small batch size",
            "inputs": {"X": t3_X, "y": t3_y, "batch_size": 5, "epochs": 200},
            "check": lambda r: abs(r(torch.tensor([[0.5]])).item() - 1.0) < 0.2,
            "fail_msg": lambda r: f"expected ~1.0 for x=0.5, got {r(torch.tensor([[0.5]])).item():.2f}",
        },
        {
            "name": "works with oversized batch",
            "inputs": {"X": t4_X, "y": t4_y, "batch_size": 100, "epochs": 500},
            "check": lambda r: abs(r(torch.tensor([[0.2]])).item() - 0.4) < 0.1,
            "fail_msg": lambda r: f"expected ~0.4 for x=0.2, got {r(torch.tensor([[0.2]])).item():.2f}",
        },
        {
            "name": "works with uneven batches",
            "inputs": {"X": t5_X, "y": t5_y, "batch_size": 4, "epochs": 200},
            "check": lambda r: abs(r(torch.tensor([[0.5]])).item() - 1.0) < 0.2,
            "fail_msg": lambda r: f"expected ~1.0 for x=0.5, got {r(torch.tensor([[0.5]])).item():.2f}",
        },
    ]

    run_all("dataloader_setup", tests, solve)
