from test_utils import run_all


def run_tests(solve):
    tests = [
        {"name": "found in middle", "inputs": {"nums": [1, 3, 5, 7, 9], "target": 5}, "check": lambda r: r == 2, "fail_msg": lambda r: f"expected 2, got {r}"},
        {"name": "found at left boundary", "inputs": {"nums": [1, 3, 5, 7, 9], "target": 1}, "check": lambda r: r == 0, "fail_msg": lambda r: f"expected 0, got {r}"},
        {"name": "found at right boundary", "inputs": {"nums": [1, 3, 5, 7, 9], "target": 9}, "check": lambda r: r == 4, "fail_msg": lambda r: f"expected 4, got {r}"},
        {"name": "not present (between elements)", "inputs": {"nums": [1, 3, 5, 7, 9], "target": 4}, "check": lambda r: r == -1, "fail_msg": lambda r: f"expected -1, got {r}"},
        {"name": "target smaller than all", "inputs": {"nums": [2, 4, 6], "target": 0}, "check": lambda r: r == -1, "fail_msg": lambda r: f"expected -1, got {r}"},
        {"name": "target larger than all", "inputs": {"nums": [2, 4, 6], "target": 10}, "check": lambda r: r == -1, "fail_msg": lambda r: f"expected -1, got {r}"},
        {"name": "single element match", "inputs": {"nums": [7], "target": 7}, "check": lambda r: r == 0, "fail_msg": lambda r: f"expected 0, got {r}"},
        {"name": "single element no match", "inputs": {"nums": [7], "target": 3}, "check": lambda r: r == -1, "fail_msg": lambda r: f"expected -1, got {r}"},
        {"name": "empty list", "inputs": {"nums": [], "target": 1}, "check": lambda r: r == -1, "fail_msg": lambda r: f"expected -1, got {r}"},
    ]
    run_all("binary_search_exact", tests, solve)
