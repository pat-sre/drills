if __package__:
    from ..test_utils import make_graph, single_node
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from test_utils import make_graph, single_node


def run_tests(dijkstra_func):
    """
    Reusable test suite for Dijkstra's algorithm.

    Args:
        dijkstra_func: A function that takes (start) and returns
                       dict of {node_value: shortest_distance}
    """
    print(f"Running tests for {dijkstra_func.__name__}...\n")

    # Test 1: None input
    assert dijkstra_func(None) == {}, "Test 1 failed: None input"
    print("Test 1 passed: None input")

    # Test 2: Single node
    assert dijkstra_func(single_node("A")) == {"A": 0}, "Test 2 failed: single node"
    print("Test 2 passed: Single node")

    # Test 3: Two connected nodes
    nodes = make_graph([("A", "B", 5)])
    assert dijkstra_func(nodes["A"]) == {"A": 0, "B": 5}, "Test 3 failed"
    print("Test 3 passed: Two connected nodes")

    # Test 4: Linear graph (chain)
    nodes = make_graph([("A", "B", 1), ("B", "C", 2), ("C", "D", 3)])
    assert dijkstra_func(nodes["A"]) == {"A": 0, "B": 1, "C": 3, "D": 6}, (
        "Test 4 failed"
    )
    print("Test 4 passed: Linear graph")

    # Test 5: Triangle - finds shorter path (A->B->C = 4, not A->C = 10)
    nodes = make_graph([("A", "B", 1), ("A", "C", 10), ("B", "C", 3)])
    assert dijkstra_func(nodes["A"]) == {"A": 0, "B": 1, "C": 4}, "Test 5 failed"
    print("Test 5 passed: Triangle (finds shorter path)")

    # Test 6: Node with no outgoing edges (directed)
    nodes = make_graph([("A", "B", 5)], directed=True)
    assert dijkstra_func(nodes["A"]) == {"A": 0, "B": 5}, "Test 6 failed"
    print("Test 6 passed: Node with no outgoing edges")

    # Test 7: Multiple paths - A->B->D->C is shorter than A->C
    nodes = make_graph([("A", "B", 1), ("A", "C", 4), ("B", "D", 1), ("C", "D", 1)])
    assert dijkstra_func(nodes["A"]) == {"A": 0, "B": 1, "C": 3, "D": 2}, (
        "Test 7 failed"
    )
    print("Test 7 passed: Multiple paths (finds optimal)")

    # Test 8: Directed graph
    nodes = make_graph([("A", "B", 1), ("B", "C", 2), ("C", "A", 10)], directed=True)
    assert dijkstra_func(nodes["A"]) == {"A": 0, "B": 1, "C": 3}, "Test 8 failed"
    print("Test 8 passed: Directed graph")

    # Test 9: Numeric node values - 1->3->2 is shorter than 1->2
    nodes = make_graph([(1, 2, 5), (1, 3, 2), (3, 2, 1)])
    assert dijkstra_func(nodes[1]) == {1: 0, 2: 3, 3: 2}, "Test 9 failed"
    print("Test 9 passed: Numeric node values")

    # Test 10: Zero weight edge
    nodes = make_graph([("A", "B", 0), ("A", "C", 5), ("B", "C", 1)])
    assert dijkstra_func(nodes["A"]) == {"A": 0, "B": 0, "C": 1}, "Test 10 failed"
    print("Test 10 passed: Zero weight edge")

    # Test 11: Larger graph
    nodes = make_graph(
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
    expected = {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10, "F": 13}
    assert dijkstra_func(nodes["A"]) == expected, "Test 11 failed"
    print("Test 11 passed: Larger graph")

    # Test 12: Float weights
    nodes = make_graph([("A", "B", 1.5), ("A", "C", 2.5), ("B", "C", 0.5)])
    assert dijkstra_func(nodes["A"]) == {"A": 0, "B": 1.5, "C": 2.0}, "Test 12 failed"
    print("Test 12 passed: Float weights")

    # Test 13: Star graph
    nodes = make_graph(
        [("center", "a", 1), ("center", "b", 2), ("center", "c", 3), ("center", "d", 4)]
    )
    expected = {"center": 0, "a": 1, "b": 2, "c": 3, "d": 4}
    assert dijkstra_func(nodes["center"]) == expected, "Test 13 failed"
    print("Test 13 passed: Star graph")

    print("\nAll tests passed!")
