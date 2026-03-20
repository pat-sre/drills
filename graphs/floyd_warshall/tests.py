from test_utils import run_all

INF = float("inf")


def run_tests(solve):
    tests = [
        {
            "name": "single node, no edges",
            "inputs": {"nodes": ["A"], "edges": []},
            "check": lambda r: r == {"A": {"A": 0}},
            "fail_msg": lambda r: f"expected {{'A': {{'A': 0}}}}, got {r}",
        },
        {
            "name": "two nodes, one directed edge",
            "inputs": {"nodes": ["A", "B"], "edges": [("A", "B", 5)]},
            "check": lambda r: r == {
                "A": {"A": 0, "B": 5},
                "B": {"A": INF, "B": 0},
            },
            "fail_msg": lambda r: f"B->A should be inf (no reverse edge). got {r}",
        },
        {
            "name": "linear chain A->B->C",
            "inputs": {
                "nodes": ["A", "B", "C"],
                "edges": [("A", "B", 1), ("B", "C", 2)],
            },
            "check": lambda r: r == {
                "A": {"A": 0, "B": 1, "C": 3},
                "B": {"A": INF, "B": 0, "C": 2},
                "C": {"A": INF, "B": INF, "C": 0},
            },
            "fail_msg": lambda r: f"A->C should be 3 (via B). got {r}",
        },
        {
            "name": "triangle (indirect path beats direct)",
            "inputs": {
                "nodes": ["A", "B", "C"],
                "edges": [("A", "B", 1), ("B", "C", 2), ("A", "C", 10)],
            },
            "check": lambda r: r["A"]["C"] == 3 and r["A"]["B"] == 1,
            "fail_msg": lambda r: (
                f"A->C direct=10, A->B->C=3. expected A->C=3, got {r['A']['C']}"
            ),
        },
        {
            "name": "diamond (two paths to D, pick shorter)",
            "inputs": {
                "nodes": ["A", "B", "C", "D"],
                "edges": [
                    ("A", "B", 1),
                    ("A", "C", 5),
                    ("B", "D", 6),
                    ("C", "D", 1),
                ],
            },
            "check": lambda r: r["A"]["D"] == 6 and r["A"]["B"] == 1 and r["A"]["C"] == 5,
            "fail_msg": lambda r: (
                f"A->B->D=7, A->C->D=6. expected A->D=6, got {r['A']['D']}"
            ),
        },
        {
            "name": "bidirectional edges",
            "inputs": {
                "nodes": ["A", "B", "C"],
                "edges": [
                    ("A", "B", 2),
                    ("B", "A", 3),
                    ("B", "C", 4),
                    ("C", "B", 1),
                ],
            },
            "check": lambda r: (
                r["A"]["C"] == 6
                and r["C"]["A"] == 4
                and r["B"]["A"] == 3
            ),
            "fail_msg": lambda r: (
                f"A->C=6 (via B), C->A=4 (C->B->A). got A->C={r['A']['C']}, C->A={r['C']['A']}"
            ),
        },
        {
            "name": "negative weights (no negative cycle)",
            "inputs": {
                "nodes": ["A", "B", "C"],
                "edges": [("A", "B", 4), ("A", "C", 2), ("C", "B", -3)],
            },
            "check": lambda r: r["A"]["B"] == -1 and r["A"]["C"] == 2,
            "fail_msg": lambda r: (
                f"A->C->B = 2+(-3) = -1. expected A->B=-1, got {r['A']['B']}"
            ),
        },
        {
            "name": "zero-weight edge",
            "inputs": {
                "nodes": ["A", "B", "C"],
                "edges": [("A", "B", 0), ("B", "C", 3)],
            },
            "check": lambda r: r["A"]["B"] == 0 and r["A"]["C"] == 3,
            "fail_msg": lambda r: f"expected A->B=0, A->C=3. got {r}",
        },
        {
            "name": "disconnected nodes (unreachable = inf)",
            "inputs": {
                "nodes": ["A", "B", "C", "D"],
                "edges": [("A", "B", 1), ("C", "D", 2)],
            },
            "check": lambda r: (
                r["A"]["B"] == 1
                and r["C"]["D"] == 2
                and r["A"]["C"] == INF
                and r["A"]["D"] == INF
                and r["C"]["A"] == INF
            ),
            "fail_msg": lambda r: f"disconnected components should have inf distances. got {r}",
        },
        {
            "name": "self-loop with weight (self-distance stays 0)",
            "inputs": {
                "nodes": ["A", "B"],
                "edges": [("A", "A", 5), ("A", "B", 3)],
            },
            "check": lambda r: r["A"]["A"] == 0 and r["A"]["B"] == 3,
            "fail_msg": lambda r: (
                f"self-loop weight should not override dist=0. got A->A={r['A']['A']}"
            ),
        },
        {
            "name": "larger graph (6 nodes)",
            "inputs": {
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "edges": [
                    ("A", "B", 4),
                    ("A", "C", 2),
                    ("C", "B", 1),
                    ("B", "D", 3),
                    ("B", "E", 1),
                    ("C", "D", 5),
                    ("D", "E", 2),
                    ("D", "F", 6),
                    ("E", "F", 3),
                ],
            },
            "check": lambda r: (
                r["A"]["B"] == 3
                and r["A"]["D"] == 6
                and r["A"]["E"] == 4
                and r["A"]["F"] == 7
                and r["E"]["A"] == INF
            ),
            "fail_msg": lambda r: (
                f"expected A->B=3, A->D=6, A->E=4, A->F=7. got {r['A']}"
            ),
        },
    ]

    run_all("floyd_warshall", tests, solve)
