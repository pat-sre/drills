import random

from test_utils import run_all

random.seed(42)
LARGE = [random.random() for _ in range(1000)]


def run_tests(solve):
    tests = [
        {
            "name": "empty array",
            "inputs": {"nums": []},
            "check": lambda r: r == [],
            "fail_msg": lambda r: f"expected [], got {r}",
        },
        {
            "name": "single element",
            "inputs": {"nums": [0.5]},
            "check": lambda r: r == [0.5],
            "fail_msg": lambda r: f"expected [0.5], got {r}",
        },
        {
            "name": "already sorted",
            "inputs": {"nums": [0.1, 0.3, 0.5, 0.7, 0.9]},
            "check": lambda r: r == [0.1, 0.3, 0.5, 0.7, 0.9],
            "fail_msg": lambda r: f"expected [0.1, 0.3, 0.5, 0.7, 0.9], got {r}",
        },
        {
            "name": "reverse sorted",
            "inputs": {"nums": [0.9, 0.7, 0.5, 0.3, 0.1]},
            "check": lambda r: r == [0.1, 0.3, 0.5, 0.7, 0.9],
            "fail_msg": lambda r: f"expected [0.1, 0.3, 0.5, 0.7, 0.9], got {r}",
        },
        {
            "name": "duplicates",
            "inputs": {"nums": [0.5, 0.1, 0.5, 0.3, 0.1]},
            "check": lambda r: r == sorted([0.5, 0.1, 0.5, 0.3, 0.1]),
            "fail_msg": lambda r: f"expected {sorted([0.5, 0.1, 0.5, 0.3, 0.1])}, got {r}",
        },
        {
            "name": "all same",
            "inputs": {"nums": [0.4, 0.4, 0.4]},
            "check": lambda r: r == [0.4, 0.4, 0.4],
            "fail_msg": lambda r: f"expected [0.4, 0.4, 0.4], got {r}",
        },
        {
            "name": "values near boundaries",
            "inputs": {"nums": [0.0, 0.999, 0.5, 0.001]},
            "check": lambda r: r == sorted([0.0, 0.999, 0.5, 0.001]),
            "fail_msg": lambda r: f"expected {sorted([0.0, 0.999, 0.5, 0.001])}, got {r}",
        },
        {
            "name": "input not mutated",
            "inputs": {"nums": [0.9, 0.1, 0.5]},
            "check": lambda r: r == [0.1, 0.5, 0.9],
            "fail_msg": lambda r: f"expected [0.1, 0.5, 0.9], got {r}",
        },
        {
            "name": "large random array (1000 elements)",
            "inputs": {"nums": LARGE},
            "check": lambda r: r == sorted(LARGE),
            "fail_msg": "large array not sorted correctly",
        },
    ]

    run_all("bucket_sort", tests, solve)
