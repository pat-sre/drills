from test_utils import run_all


def run_tests(solve):
    # --- Edge lists ---

    # Triangle: edges 1,2,3 — MST picks 1+2=3
    edges_triangle = [("A", "B", 1), ("B", "C", 2), ("A", "C", 3)]

    # Diamond: A-B=1, A-C=4, B-C=2, B-D=5, C-D=3
    # MST: A-B(1) + B-C(2) + C-D(3) = 6
    edges_diamond = [
        ("A", "B", 1), ("A", "C", 4), ("B", "C", 2),
        ("B", "D", 5), ("C", "D", 3),
    ]

    # Greedy trap: nearest neighbor from A picks A-B(1), A-C(2)
    # but MST is A-B(1), B-C(1) = 2, not 3
    edges_greedy = [("A", "B", 1), ("A", "C", 2), ("B", "C", 1)]

    # Larger graph (6 nodes)
    #   A--2--B--3--C
    #   |     |     |
    #   4     1     5
    #   |     |     |
    #   D--6--E--2--F
    # MST: B-E(1) + A-B(2) + E-F(2) + B-C(3) + A-D(4) = 12
    edges_large = [
        ("A", "B", 2), ("B", "C", 3), ("A", "D", 4),
        ("B", "E", 1), ("C", "F", 5), ("D", "E", 6),
        ("E", "F", 2),
    ]

    tests = [
        # 1. Single node
        {
            "name": "single node (no edges needed)",
            "inputs": {"nodes": ["A"], "edges": []},
            "check": lambda r: r == 0,
            "fail_msg": lambda r: f"expected 0, got {r}",
        },
        # 2. Two nodes, one edge
        {
            "name": "two nodes",
            "inputs": {"nodes": ["A", "B"], "edges": [("A", "B", 7)]},
            "check": lambda r: r == 7,
            "fail_msg": lambda r: f"expected 7, got {r}",
        },
        # 3. Linear chain
        {
            "name": "linear chain (MST is the chain itself)",
            "inputs": {
                "nodes": ["A", "B", "C"],
                "edges": [("A", "B", 3), ("B", "C", 4)],
            },
            "check": lambda r: r == 7,
            "fail_msg": lambda r: f"expected 7, got {r}",
        },
        # 4. Triangle — must skip the heaviest edge
        {
            "name": "triangle (skip heaviest edge)",
            "inputs": {"nodes": ["A", "B", "C"], "edges": edges_triangle},
            "check": lambda r: r == 3,
            "fail_msg": lambda r: f"MST uses edges 1+2=3, got {r}",
        },
        # 5. Diamond — optimal selection across 4 nodes
        {
            "name": "diamond (optimal MST selection)",
            "inputs": {
                "nodes": ["A", "B", "C", "D"],
                "edges": edges_diamond,
            },
            "check": lambda r: r == 6,
            "fail_msg": lambda r: f"MST: A-B(1)+B-C(2)+C-D(3)=6, got {r}",
        },
        # 6. Greedy trap — nearest neighbor from start is suboptimal
        {
            "name": "greedy trap (nearest neighbor fails)",
            "inputs": {"nodes": ["A", "B", "C"], "edges": edges_greedy},
            "check": lambda r: r == 2,
            "fail_msg": lambda r: f"MST: A-B(1)+B-C(1)=2, got {r}",
        },
        # 7. Zero-weight edge
        {
            "name": "zero-weight edge",
            "inputs": {
                "nodes": ["A", "B", "C"],
                "edges": [("A", "B", 0), ("B", "C", 5)],
            },
            "check": lambda r: r == 5,
            "fail_msg": lambda r: f"expected 5 (0+5), got {r}",
        },
        # 8. Disconnected graph
        {
            "name": "disconnected graph (no MST exists)",
            "inputs": {
                "nodes": ["A", "B", "C"],
                "edges": [("A", "B", 1)],
            },
            "check": lambda r: r == -1,
            "fail_msg": lambda r: f"C is unreachable, expected -1, got {r}",
        },
        # 9. All equal weights — any spanning tree works
        {
            "name": "all equal weights",
            "inputs": {
                "nodes": ["A", "B", "C", "D"],
                "edges": [
                    ("A", "B", 3), ("A", "C", 3), ("A", "D", 3),
                    ("B", "C", 3), ("B", "D", 3), ("C", "D", 3),
                ],
            },
            "check": lambda r: r == 9,
            "fail_msg": lambda r: f"3 edges * weight 3 = 9, got {r}",
        },
        # 10. Larger graph combining multiple concepts
        {
            "name": "larger graph (6 nodes, mixed weights)",
            "inputs": {
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "edges": edges_large,
            },
            "check": lambda r: r == 12,
            "fail_msg": lambda r: (
                f"MST: B-E(1)+A-B(2)+E-F(2)+B-C(3)+A-D(4)=12, got {r}"
            ),
        },
    ]

    run_all("prims_mst", tests, solve)
