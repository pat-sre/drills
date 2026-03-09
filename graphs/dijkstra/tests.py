from test_utils import run_all


def run_tests(solve):
    # --- Edge lists ---
    edges_two = [("A", "B", 5)]
    edges_chain = [("A", "B", 1), ("B", "C", 2), ("C", "D", 3)]

    # Triangle: direct A->C costs 10, but A->B->C costs 1+2=3
    edges_triangle = [("A", "B", 1), ("A", "C", 10), ("B", "C", 2)]

    # Diamond: two paths from A to D
    #   A->B->D = 1+6 = 7
    #   A->C->D = 5+1 = 6  (shorter)
    edges_diamond = [("A", "B", 1), ("A", "C", 5), ("B", "D", 6), ("C", "D", 1)]

    # Relaxation: A->B direct=10, but A->C->B = 3+2 = 5 (must update B)
    edges_relax = [("A", "B", 10), ("A", "C", 3), ("C", "B", 2)]

    # Zero-weight edge
    edges_zero = [("A", "B", 0), ("B", "C", 3)]

    # Directed (solve builds a directed graph by default)
    edges_directed = [("A", "B", 1), ("B", "C", 2)]

    # Larger directed graph (6 nodes, 9 edges)
    edges_large = [
        ("A", "B", 4), ("A", "C", 2),
        ("C", "B", 1), ("B", "D", 3), ("B", "E", 1),
        ("C", "D", 5), ("D", "E", 2), ("D", "F", 6),
        ("E", "F", 3),
    ]

    tests = [
        # 1. Edge case: no edges, single source
        {
            "name": "single node (distance to self is 0)",
            "inputs": {"edges": [], "source": "A"},
            "check": lambda r: r == {"A": 0},
            "fail_msg": lambda r: f"expected {{'A': 0}}, got {r}",
        },
        # 2. Simplest weighted edge
        {
            "name": "two nodes",
            "inputs": {"edges": edges_two, "source": "A"},
            "check": lambda r: r == {"A": 0, "B": 5},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 5}}, got {r}",
        },
        # 3. Distances accumulate
        {
            "name": "linear chain (distances accumulate)",
            "inputs": {"edges": edges_chain, "source": "A"},
            "check": lambda r: r == {"A": 0, "B": 1, "C": 3, "D": 6},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 1, 'C': 3, 'D': 6}}, got {r}",
        },
        # 4. Core insight: indirect path can be shorter
        {
            "name": "triangle (indirect path beats direct)",
            "inputs": {"edges": edges_triangle, "source": "A"},
            "check": lambda r: r == {"A": 0, "B": 1, "C": 3},
            "fail_msg": lambda r: (
                f"A->C direct=10, but A->B->C=3. expected {{'A': 0, 'B': 1, 'C': 3}}, got {r}"
            ),
        },
        # 5. Two paths, pick the shorter
        {
            "name": "diamond (two paths to D, pick shorter)",
            "inputs": {"edges": edges_diamond, "source": "A"},
            "check": lambda r: r == {"A": 0, "B": 1, "C": 5, "D": 6},
            "fail_msg": lambda r: (
                f"A->B->D=7, A->C->D=6. expected {{'A': 0, 'B': 1, 'C': 5, 'D': 6}}, got {r}"
            ),
        },
        # 6. Key concept: must relax/update a previously seen distance
        {
            "name": "relaxation (must update B from 10 to 5)",
            "inputs": {"edges": edges_relax, "source": "A"},
            "check": lambda r: r == {"A": 0, "B": 5, "C": 3},
            "fail_msg": lambda r: (
                f"A->B=10 direct, but A->C->B=5. expected {{'A': 0, 'B': 5, 'C': 3}}, got {r}"
            ),
        },
        # 7. Zero-weight edges are valid
        {
            "name": "zero-weight edge",
            "inputs": {"edges": edges_zero, "source": "A"},
            "check": lambda r: r == {"A": 0, "B": 0, "C": 3},
            "fail_msg": lambda r: f"expected {{'A': 0, 'B': 0, 'C': 3}}, got {r}",
        },
        # 8. Directed: some nodes are unreachable
        {
            "name": "directed graph (unreachable nodes excluded)",
            "inputs": {"edges": edges_directed, "source": "B"},
            "check": lambda r: r == {"B": 0, "C": 2},
            "fail_msg": lambda r: f"A is unreachable from B. expected {{'B': 0, 'C': 2}}, got {r}",
        },
        # 9. Can start from any node in chain
        {
            "name": "start from middle of chain",
            "inputs": {"edges": edges_chain, "source": "B"},
            "check": lambda r: r == {"B": 0, "C": 2, "D": 5},
            "fail_msg": lambda r: f"expected {{'B': 0, 'C': 2, 'D': 5}}, got {r}",
        },
        # 10. Larger graph combining multiple concepts
        {
            "name": "larger graph (relaxation + directed + multi-hop)",
            "inputs": {"edges": edges_large, "source": "A"},
            "check": lambda r: r == {"A": 0, "B": 3, "C": 2, "D": 6, "E": 4, "F": 7},
            "fail_msg": lambda r: (
                f"expected {{'A': 0, 'B': 3, 'C': 2, 'D': 6, 'E': 4, 'F': 7}}, got {r}"
            ),
        },
    ]

    run_all("dijkstra", tests, solve)
