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
            elif op[0] == "components":
                results.append(uf.total_components)
            elif op[0] == "size":
                root = uf.find(op[1])
                results.append(uf.size[root])
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
            "name": "total_components tracking",
            "inputs": {
                "n": 5,
                "ops": [
                    ("components",),
                    ("union", 0, 1),
                    ("components",),
                    ("union", 2, 3),
                    ("components",),
                    ("union", 0, 2),
                    ("components",),
                    ("union", 0, 1),  # redundant
                    ("components",),
                ],
            },
            "check": lambda r: r == [5, True, 4, True, 3, True, 2, False, 2],
            "fail_msg": lambda r: (
                f"expected [5, True, 4, True, 3, True, 2, False, 2], got {r}"
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
            "name": "union by size (smaller under larger)",
            "inputs": {
                "n": 7,
                "ops": [
                    # Build size-4 tree A rooted at 0
                    ("union", 0, 1),
                    ("union", 0, 2),
                    ("union", 0, 3),
                    # Build size-2 tree B rooted at 4
                    ("union", 4, 5),
                    # Union B into A — size-based must pick A's root
                    ("union", 4, 0),
                    ("find", 4),
                    ("find", 0),
                    # Verify size of merged component
                    ("size", 0),
                ],
            },
            "check": lambda r: (
                r[5] == r[6]  # same root
                and r[6] == 0  # root is A's root (0), the larger tree
                and r[7] == 6  # merged size
            ),
            "fail_msg": lambda r: (
                f"expected smaller tree under larger, root=0, size=6; got find(4)={r[5]}, find(0)={r[6]}, size={r[7]}"
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
