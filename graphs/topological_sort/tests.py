from test_utils import run_all


def is_valid_topo(result, nodes, edges):
    if sorted(result) != sorted(nodes):
        return False
    if len(result) != len(set(result)):
        return False
    pos = {v: i for i, v in enumerate(result)}
    return all(pos[u] < pos[v] for u, v in edges)


def run_tests(solve):
    tests = [
        {
            "name": "single node, no edges",
            "inputs": {"nodes": ["A"], "edges": []},
            "check": lambda r: r == ["A"],
            "fail_msg": lambda r: f"expected ['A'], got {r}",
        },
        {
            "name": "two nodes, one edge",
            "inputs": {"nodes": ["A", "B"], "edges": [("A", "B")]},
            "check": lambda r: r == ["A", "B"],
            "fail_msg": lambda r: f"expected ['A', 'B'], got {r}",
        },
        {
            "name": "linear chain A->B->C->D",
            "inputs": {
                "nodes": ["A", "B", "C", "D"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D")],
            },
            "check": lambda r: r == ["A", "B", "C", "D"],
            "fail_msg": lambda r: f"expected ['A', 'B', 'C', 'D'], got {r}",
        },
        {
            "name": "diamond DAG (A->B, A->C, B->D, C->D)",
            "inputs": {
                "nodes": ["A", "B", "C", "D"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")],
            },
            "check": lambda r: is_valid_topo(
                r,
                ["A", "B", "C", "D"],
                [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")],
            ),
            "fail_msg": lambda r: f"not a valid topological order: {r}",
        },
        {
            "name": "disconnected components (A->B, C->D)",
            "inputs": {
                "nodes": ["A", "B", "C", "D"],
                "edges": [("A", "B"), ("C", "D")],
            },
            "check": lambda r: is_valid_topo(
                r, ["A", "B", "C", "D"], [("A", "B"), ("C", "D")]
            ),
            "fail_msg": lambda r: f"not a valid topological order: {r}",
        },
        {
            "name": "isolated nodes only (no edges)",
            "inputs": {"nodes": ["A", "B", "C"], "edges": []},
            "check": lambda r: is_valid_topo(r, ["A", "B", "C"], []),
            "fail_msg": lambda r: f"not a valid topological order: {r}",
        },
        {
            "name": "fan-out (A -> B, C, D, E)",
            "inputs": {
                "nodes": ["A", "B", "C", "D", "E"],
                "edges": [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E")],
            },
            "check": lambda r: is_valid_topo(
                r,
                ["A", "B", "C", "D", "E"],
                [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E")],
            ),
            "fail_msg": lambda r: f"not a valid topological order: {r}",
        },
        {
            "name": "multiple roots (A->C, B->C, C->D)",
            "inputs": {
                "nodes": ["A", "B", "C", "D"],
                "edges": [("A", "C"), ("B", "C"), ("C", "D")],
            },
            "check": lambda r: is_valid_topo(
                r, ["A", "B", "C", "D"], [("A", "C"), ("B", "C"), ("C", "D")]
            ),
            "fail_msg": lambda r: f"not a valid topological order: {r}",
        },
        {
            "name": "deep with branches",
            "inputs": {
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "edges": [
                    ("A", "B"),
                    ("A", "C"),
                    ("B", "D"),
                    ("C", "E"),
                    ("D", "F"),
                    ("E", "F"),
                ],
            },
            "check": lambda r: is_valid_topo(
                r,
                ["A", "B", "C", "D", "E", "F"],
                [
                    ("A", "B"),
                    ("A", "C"),
                    ("B", "D"),
                    ("C", "E"),
                    ("D", "F"),
                    ("E", "F"),
                ],
            ),
            "fail_msg": lambda r: f"not a valid topological order: {r}",
        },
        {
            "name": "numeric node values",
            "inputs": {
                "nodes": [1, 2, 3, 4],
                "edges": [(1, 2), (1, 3), (2, 4), (3, 4)],
            },
            "check": lambda r: is_valid_topo(
                r, [1, 2, 3, 4], [(1, 2), (1, 3), (2, 4), (3, 4)]
            ),
            "fail_msg": lambda r: f"not a valid topological order: {r}",
        },
        {
            "name": "larger DAG (8 nodes)",
            "inputs": {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [
                    ("A", "C"),
                    ("A", "D"),
                    ("B", "D"),
                    ("B", "E"),
                    ("C", "F"),
                    ("D", "F"),
                    ("D", "G"),
                    ("E", "G"),
                    ("F", "H"),
                    ("G", "H"),
                ],
            },
            "check": lambda r: is_valid_topo(
                r,
                ["A", "B", "C", "D", "E", "F", "G", "H"],
                [
                    ("A", "C"),
                    ("A", "D"),
                    ("B", "D"),
                    ("B", "E"),
                    ("C", "F"),
                    ("D", "F"),
                    ("D", "G"),
                    ("E", "G"),
                    ("F", "H"),
                    ("G", "H"),
                ],
            ),
            "fail_msg": lambda r: f"not a valid topological order: {r}",
        },
    ]

    run_all("topological_sort", tests, solve)
