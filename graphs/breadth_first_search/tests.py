if __package__:
    from ..test_utils import make_graph, single_node
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from test_utils import make_graph, single_node


def run_tests(bfs_func):
    """
    Reusable test suite for BFS algorithm.

    Args:
        bfs_func: A function that takes (start) and returns traversal order
    """
    print(f"Running tests for {bfs_func.__name__}...\n")

    # Test 1: None input
    assert bfs_func(None) == [], "Test 1 failed: None input"
    print("Test 1 passed: None input")

    # Test 2: Single node
    assert bfs_func(single_node("A")) == ["A"], "Test 2 failed: single node"
    print("Test 2 passed: Single node")

    # Test 3: Two connected nodes
    nodes = make_graph([("A", "B")])
    assert bfs_func(nodes["A"]) == ["A", "B"], "Test 3 failed: two nodes"
    print("Test 3 passed: Two connected nodes")

    # Test 4: Linear graph (chain)
    nodes = make_graph([("A", "B"), ("B", "C"), ("C", "D")])
    assert bfs_func(nodes["A"]) == ["A", "B", "C", "D"], "Test 4 failed: linear"
    print("Test 4 passed: Linear graph")

    # Test 5: Tree structure (A -> B,C; B -> D,E)
    nodes = make_graph([("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")])
    result = bfs_func(nodes["A"])
    assert result[0] == "A", "Test 5 failed: should start with A"
    assert set(result[1:3]) == {"B", "C"}, "Test 5 failed: level 1"
    assert set(result[3:5]) == {"D", "E"}, "Test 5 failed: level 2"
    print("Test 5 passed: Tree structure (level order)")

    # Test 6: Graph with cycle (triangle)
    nodes = make_graph([("A", "B"), ("B", "C"), ("C", "A")])
    result = bfs_func(nodes["A"])
    assert len(result) == 3 and result[0] == "A", "Test 6 failed: cycle"
    assert set(result) == {"A", "B", "C"}, "Test 6 failed: cycle"
    print("Test 6 passed: Graph with cycle")

    # Test 7: Node with no neighbors
    assert bfs_func(single_node("A")) == ["A"], "Test 7 failed: no neighbors"
    print("Test 7 passed: Node with no neighbors")

    # Test 8: Self-loop
    node = single_node("A")
    node.neighbors = [node, single_node("B")]
    node.neighbors[1].neighbors = [node]
    result = bfs_func(node)
    assert result == ["A", "B"], "Test 8 failed: self-loop"
    print("Test 8 passed: Self-loop handled correctly")

    # Test 9: Star graph
    nodes = make_graph(
        [
            ("center", "a"),
            ("center", "b"),
            ("center", "c"),
            ("center", "d"),
            ("center", "e"),
        ]
    )
    result = bfs_func(nodes["center"])
    assert result[0] == "center", "Test 9 failed: star start"
    assert set(result[1:]) == {"a", "b", "c", "d", "e"}, "Test 9 failed: star leaves"
    print("Test 9 passed: Star graph")

    # Test 10: Diamond graph (A -> B,C -> D)
    nodes = make_graph([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")])
    result = bfs_func(nodes["A"])
    assert result[0] == "A", "Test 10 failed: diamond start"
    assert set(result[1:3]) == {"B", "C"}, "Test 10 failed: diamond level 1"
    assert result[3] == "D", "Test 10 failed: D should be last"
    print("Test 10 passed: Diamond graph")

    # Test 11: Complete graph K4
    nodes = make_graph(
        [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D")]
    )
    result = bfs_func(nodes["A"])
    assert result[0] == "A" and set(result) == {"A", "B", "C", "D"}, "Test 11 failed"
    print("Test 11 passed: Complete graph K4")

    # Test 12: Numeric values
    nodes = make_graph([(1, 2), (1, 3)])
    result = bfs_func(nodes[1])
    assert result[0] == 1 and len(result) == 3, "Test 12 failed: numeric"
    print("Test 12 passed: Numeric values")

    print("\nAll tests passed!")
