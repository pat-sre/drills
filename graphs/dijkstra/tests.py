from graphs.test_utils import make_graph, single_node
from test_utils import run_all


def run_tests(solve):
    # Build test graphs (weighted)
    g3 = make_graph([("A", "B", 5)])
    g4 = make_graph([("A", "B", 1), ("B", "C", 2), ("C", "D", 3)])
    g5 = make_graph([("A", "B", 1), ("A", "C", 10), ("B", "C", 3)])
    g6 = make_graph([("A", "B", 5)], directed=True)
    g7 = make_graph([("A", "B", 1), ("A", "C", 4), ("B", "D", 1), ("C", "D", 1)])
    g8 = make_graph([("A", "B", 1), ("B", "C", 2), ("C", "A", 10)], directed=True)
    g9 = make_graph([(1, 2, 5), (1, 3, 2), (3, 2, 1)])
    g10 = make_graph([("A", "B", 0), ("A", "C", 5), ("B", "C", 1)])
    g11 = make_graph(
        [
            ("A", "B", 4),
            ("A", "C", 2),
            ("B", "C", 1),
            ("B", "D", 5),
            ("C", "D", 8),
            ("C", "E", 10),
            ("D", "E", 2),
            ("D", "F", 6),
            ("E", "F", 3),
        ]
    )
    g12 = make_graph([("A", "B", 1.5), ("A", "C", 2.5), ("B", "C", 0.5)])
    g13 = make_graph(
        [("center", "a", 1), ("center", "b", 2), ("center", "c", 3), ("center", "d", 4)]
    )

    tests = [
        {
            "name": "None input",
            "inputs": {"start": None},
            "check": lambda r: r == {},
            "fail_msg": lambda r: f"expected {{}}, got {r}",
        },
        {
            "name": "single node",
            "inputs": {"start": single_node("A")},
            "check": lambda r: r == {"A": 0},
            "fail_msg": lambda r: f"expected {{'A': 0}}, got {r}",
        },
        {
            "name": "two connected nodes",
            "inputs": {"start": g3["A"]},
            "check": lambda r: r == {"A": 0, "B": 5},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 5}}, got {r}",
        },
        {
            "name": "linear graph",
            "inputs": {"start": g4["A"]},
            "check": lambda r: r == {"A": 0, "B": 1, "C": 3, "D": 6},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 1, 'C': 3, 'D': 6}}, got {r}",
        },
        {
            "name": "finds shorter path",
            "inputs": {"start": g5["A"]},
            "check": lambda r: r == {"A": 0, "B": 1, "C": 4},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 1, 'C': 4}}, got {r}",
        },
        {
            "name": "directed graph",
            "inputs": {"start": g6["A"]},
            "check": lambda r: r == {"A": 0, "B": 5},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 5}}, got {r}",
        },
        {
            "name": "multiple paths (finds optimal)",
            "inputs": {"start": g7["A"]},
            "check": lambda r: r == {"A": 0, "B": 1, "C": 3, "D": 2},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 1, 'C': 3, 'D': 2}}, got {r}",
        },
        {
            "name": "directed cycle",
            "inputs": {"start": g8["A"]},
            "check": lambda r: r == {"A": 0, "B": 1, "C": 3},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 1, 'C': 3}}, got {r}",
        },
        {
            "name": "numeric node values",
            "inputs": {"start": g9[1]},
            "check": lambda r: r == {1: 0, 2: 3, 3: 2},
            "fail_msg": lambda r: f"expected {{1: 0, 2: 3, 3: 2}}, got {r}",
        },
        {
            "name": "zero weight edge",
            "inputs": {"start": g10["A"]},
            "check": lambda r: r == {"A": 0, "B": 0, "C": 1},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 0, 'C': 1}}, got {r}",
        },
        {
            "name": "larger graph",
            "inputs": {"start": g11["A"]},
            "check": lambda r: r == {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10, "F": 13},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 3, 'C': 2, 'D': 8, 'E': 10, 'F': 13}}, got {r}",
        },
        {
            "name": "float weights",
            "inputs": {"start": g12["A"]},
            "check": lambda r: r == {"A": 0, "B": 1.5, "C": 2.0},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 1.5, 'C': 2.0}}, got {r}",
        },
        {
            "name": "star graph",
            "inputs": {"start": g13["center"]},
            "check": lambda r: r == {"center": 0, "a": 1, "b": 2, "c": 3, "d": 4},
            "fail_msg": lambda r: f"expected {{'center': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4}}, got {r}",
        },
    ]

    run_all("dijkstra", tests, solve)
