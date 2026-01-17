import random

from test_utils import run_all

random.seed(42)
LARGE = [random.randint(-100, 100) for _ in range(1000)]


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
            "inputs": {"nums": [5]},
            "check": lambda r: r == [5],
            "fail_msg": lambda r: f"expected [5], got {r}",
        },
        {
            "name": "two elements sorted",
            "inputs": {"nums": [1, 2]},
            "check": lambda r: r == [1, 2],
            "fail_msg": lambda r: f"expected [1, 2], got {r}",
        },
        {
            "name": "two elements reverse",
            "inputs": {"nums": [2, 1]},
            "check": lambda r: r == [1, 2],
            "fail_msg": lambda r: f"expected [1, 2], got {r}",
        },
        {
            "name": "already sorted",
            "inputs": {"nums": [1, 2, 3, 4, 5]},
            "check": lambda r: r == [1, 2, 3, 4, 5],
            "fail_msg": lambda r: f"expected [1, 2, 3, 4, 5], got {r}",
        },
        {
            "name": "reverse sorted",
            "inputs": {"nums": [5, 4, 3, 2, 1]},
            "check": lambda r: r == [1, 2, 3, 4, 5],
            "fail_msg": lambda r: f"expected [1, 2, 3, 4, 5], got {r}",
        },
        {
            "name": "random with duplicates",
            "inputs": {"nums": [3, 7, 8, 5, 2, 1, 9, 5, 4]},
            "check": lambda r: r == [1, 2, 3, 4, 5, 5, 7, 8, 9],
            "fail_msg": lambda r: f"expected [1, 2, 3, 4, 5, 5, 7, 8, 9], got {r}",
        },
        {
            "name": "all same",
            "inputs": {"nums": [5, 5, 5, 5, 5]},
            "check": lambda r: r == [5, 5, 5, 5, 5],
            "fail_msg": lambda r: f"expected [5, 5, 5, 5, 5], got {r}",
        },
        {
            "name": "negative numbers",
            "inputs": {"nums": [3, -1, -4, 2, -5, 0]},
            "check": lambda r: r == [-5, -4, -1, 0, 2, 3],
            "fail_msg": lambda r: f"expected [-5, -4, -1, 0, 2, 3], got {r}",
        },
        {
            "name": "floats",
            "inputs": {"nums": [3.5, 1.2, 4.8, 2.1, 0.5]},
            "check": lambda r: r == [0.5, 1.2, 2.1, 3.5, 4.8],
            "fail_msg": lambda r: f"expected [0.5, 1.2, 2.1, 3.5, 4.8], got {r}",
        },
        {
            "name": "large random array (1000 elements)",
            "inputs": {"nums": LARGE},
            "check": lambda r: r == sorted(LARGE),
            "fail_msg": "large array not sorted correctly",
        },
    ]

    run_all("merge_sort", tests, solve)
