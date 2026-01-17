from graphs.test_utils import make_graph, single_node
from test_utils import run_all


def run_tests(solve):
    # Build test graphs
    g3 = make_graph([("A", "B")])
    g4 = make_graph([("A", "B"), ("B", "C"), ("C", "D")])
    g5 = make_graph([("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")])
    g6 = make_graph([("A", "B"), ("B", "C"), ("C", "A")])
    g9 = make_graph([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F")])
    g10 = make_graph([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")])
    g11 = make_graph(
        [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D")]
    )
    g12 = make_graph([(1, 2), (1, 3)])

    # Self-loop node
    self_loop = single_node("A")
    self_loop.neighbors = [self_loop, single_node("B")]
    self_loop.neighbors[1].neighbors = [self_loop]

    tests = [
        {
            "name": "None input",
            "inputs": {"start": None},
            "check": lambda r: r == [],
            "fail_msg": lambda r: f"expected [], got {r}",
        },
        {
            "name": "single node",
            "inputs": {"start": single_node("A")},
            "check": lambda r: r == ["A"],
            "fail_msg": lambda r: f"expected ['A'], got {r}",
        },
        {
            "name": "two connected nodes",
            "inputs": {"start": g3["A"]},
            "check": lambda r: r == ["A", "B"],
            "fail_msg": lambda r: f"expected ['A', 'B'], got {r}",
        },
        {
            "name": "linear graph",
            "inputs": {"start": g4["A"]},
            "check": lambda r: r == ["A", "B", "C", "D"],
            "fail_msg": lambda r: f"expected ['A', 'B', 'C', 'D'], got {r}",
        },
        {
            "name": "tree structure (depth-first)",
            "inputs": {"start": g5["A"]},
            "check": lambda r: (
                r[0] == "A"
                and len(r) == 5
                and r.index("B") < r.index("D")
                and r.index("B") < r.index("E")
            ),
            "fail_msg": "D and E should come after B in DFS",
        },
        {
            "name": "graph with cycle",
            "inputs": {"start": g6["A"]},
            "check": lambda r: len(r) == 3
            and r[0] == "A"
            and set(r) == {"A", "B", "C"},
            "fail_msg": lambda r: f"expected 3 nodes starting with A, got {r}",
        },
        {
            "name": "node with no neighbors",
            "inputs": {"start": single_node("A")},
            "check": lambda r: r == ["A"],
            "fail_msg": lambda r: f"expected ['A'], got {r}",
        },
        {
            "name": "self-loop handled",
            "inputs": {"start": self_loop},
            "check": lambda r: r == ["A", "B"],
            "fail_msg": lambda r: f"expected ['A', 'B'], got {r}",
        },
        {
            "name": "long path traversal",
            "inputs": {"start": g9["A"]},
            "check": lambda r: r == ["A", "B", "C", "D", "E", "F"],
            "fail_msg": lambda r: f"expected ['A', 'B', 'C', 'D', 'E', 'F'], got {r}",
        },
        {
            "name": "diamond graph",
            "inputs": {"start": g10["A"]},
            "check": lambda r: r[0] == "A"
            and len(r) == 4
            and set(r) == {"A", "B", "C", "D"},
            "fail_msg": lambda r: f"expected 4 nodes starting with A, got {r}",
        },
        {
            "name": "no duplicates in complete graph",
            "inputs": {"start": g11["A"]},
            "check": lambda r: len(r) == len(set(r)) == 4,
            "fail_msg": "should have no duplicate visits",
        },
        {
            "name": "numeric values",
            "inputs": {"start": g12[1]},
            "check": lambda r: r[0] == 1 and len(r) == 3,
            "fail_msg": lambda r: f"expected 3 nodes starting with 1, got {r}",
        },
    ]

    run_all("depth_first_search", tests, solve)
