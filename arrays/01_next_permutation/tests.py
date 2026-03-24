from test_utils import run_all


def run_tests(solve):
    tests = [
        {
            "name": "simple ascending [1, 2, 3]",
            "inputs": {"nums": [1, 2, 3]},
            "check": lambda r: r == [1, 3, 2],
            "fail_msg": lambda r: f"expected [1, 3, 2], got {r}",
        },
        {
            "name": "last permutation wraps around [3, 2, 1]",
            "inputs": {"nums": [3, 2, 1]},
            "check": lambda r: r == [1, 2, 3],
            "fail_msg": lambda r: f"expected [1, 2, 3], got {r}",
        },
        {
            "name": "with duplicates [1, 1, 5]",
            "inputs": {"nums": [1, 1, 5]},
            "check": lambda r: r == [1, 5, 1],
            "fail_msg": lambda r: f"expected [1, 5, 1], got {r}",
        },
        {
            "name": "single element [1]",
            "inputs": {"nums": [1]},
            "check": lambda r: r == [1],
            "fail_msg": lambda r: f"expected [1], got {r}",
        },
        {
            "name": "two elements ascending [1, 2]",
            "inputs": {"nums": [1, 2]},
            "check": lambda r: r == [2, 1],
            "fail_msg": lambda r: f"expected [2, 1], got {r}",
        },
        {
            "name": "two elements descending [2, 1]",
            "inputs": {"nums": [2, 1]},
            "check": lambda r: r == [1, 2],
            "fail_msg": lambda r: f"expected [1, 2], got {r}",
        },
        {
            "name": "mid permutation [1, 3, 2]",
            "inputs": {"nums": [1, 3, 2]},
            "check": lambda r: r == [2, 1, 3],
            "fail_msg": lambda r: f"expected [2, 1, 3], got {r}",
        },
        {
            "name": "longer sequence [2, 3, 6, 5, 4, 1]",
            "inputs": {"nums": [2, 3, 6, 5, 4, 1]},
            "check": lambda r: r == [2, 4, 1, 3, 5, 6],
            "fail_msg": lambda r: f"expected [2, 4, 1, 3, 5, 6], got {r}",
        },
        {
            "name": "all same elements [5, 5, 5]",
            "inputs": {"nums": [5, 5, 5]},
            "check": lambda r: r == [5, 5, 5],
            "fail_msg": lambda r: f"expected [5, 5, 5], got {r}",
        },
        {
            "name": "swap at end [1, 2, 3, 5, 4]",
            "inputs": {"nums": [1, 2, 3, 5, 4]},
            "check": lambda r: r == [1, 2, 4, 3, 5],
            "fail_msg": lambda r: f"expected [1, 2, 4, 3, 5], got {r}",
        },
        {
            "name": "duplicates in non-increasing suffix [1, 5, 5, 4, 3]",
            "inputs": {"nums": [1, 5, 5, 4, 3]},
            "check": lambda r: r == [3, 1, 4, 5, 5],
            "fail_msg": lambda r: f"expected [3, 1, 4, 5, 5], got {r}",
        },
        {
            "name": "pivot duplicate in suffix [2, 5, 2, 1]",
            "inputs": {"nums": [2, 5, 2, 1]},
            "check": lambda r: r == [5, 1, 2, 2],
            "fail_msg": lambda r: f"expected [5, 1, 2, 2], got {r}",
        },
    ]

    run_all("next_permutation", tests, solve)
