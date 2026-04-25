from test_utils import run_all


def run_tests(solve):
    tests = [
        {"name": "first >= 5 in [1,3,5,7,9]", "inputs": {"nums": [1, 3, 5, 7, 9], "predicate": lambda x: x >= 5}, "check": lambda r: r == 2, "fail_msg": lambda r: f"expected 2, got {r}"},
        {"name": "all satisfy predicate", "inputs": {"nums": [1, 3, 5, 7, 9], "predicate": lambda x: x >= 0}, "check": lambda r: r == 0, "fail_msg": lambda r: f"expected 0, got {r}"},
        {"name": "none satisfy predicate", "inputs": {"nums": [1, 3, 5, 7, 9], "predicate": lambda x: x >= 10}, "check": lambda r: r == 5, "fail_msg": lambda r: f"expected 5, got {r}"},
        {"name": "only last element satisfies", "inputs": {"nums": [1, 3, 5, 7, 9], "predicate": lambda x: x >= 9}, "check": lambda r: r == 4, "fail_msg": lambda r: f"expected 4, got {r}"},
        {"name": "only first element satisfies", "inputs": {"nums": [1, 3, 5, 7, 9], "predicate": lambda x: x >= 1}, "check": lambda r: r == 0, "fail_msg": lambda r: f"expected 0, got {r}"},
        {"name": "single element satisfies", "inputs": {"nums": [5], "predicate": lambda x: x >= 5}, "check": lambda r: r == 0, "fail_msg": lambda r: f"expected 0, got {r}"},
        {"name": "single element does not satisfy", "inputs": {"nums": [5], "predicate": lambda x: x >= 6}, "check": lambda r: r == 1, "fail_msg": lambda r: f"expected 1, got {r}"},
        {"name": "empty list", "inputs": {"nums": [], "predicate": lambda x: x >= 0}, "check": lambda r: r == 0, "fail_msg": lambda r: f"expected 0, got {r}"},
    ]
    run_all("binary_search_boundary", tests, solve)
