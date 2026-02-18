from test_utils import run_all


def run_tests(UnionFind):
    def run_scenario(n, ops):
        """Construct UnionFind(n), execute ops, return list of results."""
        uf = UnionFind(n)
        results = []
        for op in ops:
            if op[0] == "find":
                results.append(uf.find(op[1]))
            elif op[0] == "union":
                results.append(uf.union(op[1], op[2]))
            elif op[0] == "parent":
                results.append(uf.parent[op[1]])
        return results

    tests = [
        {
            "name": "single element find",
            "inputs": {"n": 1, "ops": [("find", 0)]},
            "check": lambda r: r == [0],
            "fail_msg": lambda r: f"expected [0], got {r}",
        },
        {
            "name": "two elements are separate",
            "inputs": {"n": 2, "ops": [("find", 0), ("find", 1)]},
            "check": lambda r: r[0] != r[1],
            "fail_msg": lambda r: f"expected different roots, got {r}",
        },
        {
            "name": "basic union",
            "inputs": {
                "n": 2,
                "ops": [("union", 0, 1), ("find", 0), ("find", 1)],
            },
            "check": lambda r: r[0] is True and r[1] == r[2],
            "fail_msg": lambda r: f"expected [True, same, same], got {r}",
        },
        {
            "name": "redundant union returns False",
            "inputs": {
                "n": 2,
                "ops": [("union", 0, 1), ("union", 0, 1)],
            },
            "check": lambda r: r == [True, False],
            "fail_msg": lambda r: f"expected [True, False], got {r}",
        },
        {
            "name": "chain of unions",
            "inputs": {
                "n": 3,
                "ops": [
                    ("union", 0, 1),
                    ("union", 1, 2),
                    ("find", 0),
                    ("find", 1),
                    ("find", 2),
                ],
            },
            "check": lambda r: r[0] is True and r[1] is True and r[2] == r[3] == r[4],
            "fail_msg": lambda r: f"expected all same root, got {r}",
        },
        {
            "name": "separate components",
            "inputs": {
                "n": 4,
                "ops": [
                    ("union", 0, 1),
                    ("union", 2, 3),
                    ("find", 0),
                    ("find", 1),
                    ("find", 2),
                    ("find", 3),
                ],
            },
            "check": lambda r: (
                r[0] is True
                and r[1] is True
                and r[2] == r[3]
                and r[4] == r[5]
                and r[2] != r[4]
            ),
            "fail_msg": lambda r: f"expected two separate components, got {r}",
        },
        {
            "name": "component count",
            "inputs": {
                "n": 5,
                "ops": [
                    ("union", 0, 1),
                    ("union", 2, 3),
                    ("find", 0),
                    ("find", 1),
                    ("find", 2),
                    ("find", 3),
                    ("find", 4),
                ],
            },
            "check": lambda r: len(set(r[2:])) == 3,
            "fail_msg": lambda r: (
                f"expected 3 components, got {len(set(r[2:]))} from roots {r[2:]}"
            ),
        },
        {
            "name": "path compression",
            "inputs": {
                "n": 4,
                "ops": [
                    ("union", 0, 1),
                    ("union", 1, 2),
                    ("union", 2, 3),
                    ("find", 3),
                    ("parent", 3),
                ],
            },
            "check": lambda r: r[3] == r[4],
            "fail_msg": lambda r: (
                f"after find(3), parent[3] should point to root {r[3]}, got {r[4]}"
            ),
        },
        {
            "name": "union by rank (smaller under larger)",
            "inputs": {
                "n": 6,
                "ops": [
                    # Build a tree of rank 1: {0, 1, 2}
                    ("union", 0, 1),
                    ("union", 0, 2),
                    # Single element: {3}
                    # Union single into larger tree
                    ("union", 3, 0),
                    ("find", 3),
                    ("find", 0),
                ],
            },
            "check": lambda r: r[3] == r[4],
            "fail_msg": lambda r: (
                f"expected 3 under 0's root, got find(3)={r[3]}, find(0)={r[4]}"
            ),
        },
        {
            "name": "large n (100 elements)",
            "inputs": {
                "n": 100,
                "ops": (
                    # Chain 0-1-2-...-49 into one component
                    [("union", i, i + 1) for i in range(49)]
                    # Chain 50-51-...-99 into another component
                    + [("union", i, i + 1) for i in range(50, 99)]
                    + [("find", 0), ("find", 49), ("find", 50), ("find", 99)]
                ),
            },
            "check": lambda r: r[-4] == r[-3] and r[-2] == r[-1] and r[-4] != r[-2],
            "fail_msg": lambda r: (
                f"expected two components [0..49] and [50..99], got finds {r[-4:]}"
            ),
        },
        {
            "name": "all connected",
            "inputs": {
                "n": 5,
                "ops": (
                    [("union", i, i + 1) for i in range(4)]
                    + [("find", i) for i in range(5)]
                ),
            },
            "check": lambda r: len(set(r[4:])) == 1,
            "fail_msg": lambda r: f"expected single component, got roots {r[4:]}",
        },
        {
            "name": "idempotent find",
            "inputs": {
                "n": 3,
                "ops": [("union", 0, 1), ("find", 0), ("find", 0), ("find", 0)],
            },
            "check": lambda r: r[1] == r[2] == r[3],
            "fail_msg": lambda r: (
                f"expected same result for repeated find, got {r[1:]}"
            ),
        },
    ]

    run_all("union_find", tests, run_scenario)
