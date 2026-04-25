from test_utils import run_all


def run_tests(LRUCache):
    def run_scenario(capacity, ops):
        cache = LRUCache(capacity)
        results = []
        for op in ops:
            if op[0] == "put":
                cache.put(op[1], op[2])
            elif op[0] == "get":
                results.append(cache.get(op[1]))
        return results

    tests = [
        {
            "name": "basic put and get",
            "inputs": {
                "capacity": 2,
                "ops": [("put", 1, 1), ("put", 2, 2), ("get", 1), ("get", 2)],
            },
            "check": lambda r: r == [1, 2],
            "fail_msg": lambda r: f"expected [1, 2], got {r}",
        },
        {
            "name": "evicts LRU on overflow",
            "inputs": {
                "capacity": 2,
                "ops": [
                    ("put", 1, 1),
                    ("put", 2, 2),
                    ("get", 1),       # 1 becomes MRU
                    ("put", 3, 3),    # evicts 2
                    ("get", 2),       # -1
                    ("get", 3),       # 3
                ],
            },
            "check": lambda r: r == [1, -1, 3],
            "fail_msg": lambda r: f"expected [1, -1, 3], got {r}",
        },
        {
            "name": "get missing key returns -1",
            "inputs": {
                "capacity": 1,
                "ops": [("get", 99)],
            },
            "check": lambda r: r == [-1],
            "fail_msg": lambda r: f"expected [-1], got {r}",
        },
        {
            "name": "update existing key",
            "inputs": {
                "capacity": 2,
                "ops": [("put", 1, 1), ("put", 1, 10), ("get", 1)],
            },
            "check": lambda r: r == [10],
            "fail_msg": lambda r: f"expected [10], got {r}",
        },
        {
            "name": "update makes key MRU",
            "inputs": {
                "capacity": 2,
                "ops": [
                    ("put", 1, 1),
                    ("put", 2, 2),
                    ("put", 1, 100),  # update 1, now MRU
                    ("put", 3, 3),    # evicts 2
                    ("get", 1),       # 100
                    ("get", 2),       # -1
                ],
            },
            "check": lambda r: r == [100, -1],
            "fail_msg": lambda r: f"expected [100, -1], got {r}",
        },
        {
            "name": "capacity 1 always evicts previous",
            "inputs": {
                "capacity": 1,
                "ops": [("put", 1, 1), ("put", 2, 2), ("get", 1), ("get", 2)],
            },
            "check": lambda r: r == [-1, 2],
            "fail_msg": lambda r: f"expected [-1, 2], got {r}",
        },
        {
            "name": "LRU example from docstring",
            "inputs": {
                "capacity": 2,
                "ops": [
                    ("put", 1, 1),
                    ("put", 2, 2),
                    ("get", 1),
                    ("put", 3, 3),
                    ("get", 2),
                    ("put", 4, 4),
                    ("get", 1),
                    ("get", 3),
                    ("get", 4),
                ],
            },
            "check": lambda r: r == [1, -1, -1, 3, 4],
            "fail_msg": lambda r: f"expected [1, -1, -1, 3, 4], got {r}",
        },
    ]

    run_all("lru_cache", tests, run_scenario)
