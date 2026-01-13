if __package__:
    from ..test_utils import make_graph, single_node
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from test_utils import make_graph, single_node


def run_tests(dfs_func):
    """
    Reusable test suite for DFS algorithm.

    Args:
        dfs_func: A function that takes (start) and returns traversal order
    """
    print(f"Running tests for {dfs_func.__name__}...\n")

    # Test 1: None input
    assert dfs_func(None) == [], "Test 1 failed: None input"
    print("Test 1 passed: None input")

    # Test 2: Single node
    assert dfs_func(single_node("A")) == ["A"], "Test 2 failed: single node"
    print("Test 2 passed: Single node")

    # Test 3: Two connected nodes
    nodes = make_graph([("A", "B")])
    assert dfs_func(nodes["A"]) == ["A", "B"], "Test 3 failed: two nodes"
    print("Test 3 passed: Two connected nodes")

    # Test 4: Linear graph (chain)
    nodes = make_graph([("A", "B"), ("B", "C"), ("C", "D")])
    assert dfs_func(nodes["A"]) == ["A", "B", "C", "D"], "Test 4 failed: linear"
    print("Test 4 passed: Linear graph")

    # Test 5: Tree structure - verify DFS goes deep first
    nodes = make_graph([("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")])
    result = dfs_func(nodes["A"])
    assert result[0] == "A", "Test 5 failed: should start with A"
    assert len(result) == 5, "Test 5 failed: should visit all 5 nodes"
    # D and E should come after B (DFS goes deep)
    b_idx, d_idx, e_idx = result.index("B"), result.index("D"), result.index("E")
    assert b_idx < d_idx and b_idx < e_idx, "Test 5 failed: D and E should come after B"
    print("Test 5 passed: Tree structure (depth-first property)")

    # Test 6: Graph with cycle (triangle)
    nodes = make_graph([("A", "B"), ("B", "C"), ("C", "A")])
    result = dfs_func(nodes["A"])
    assert len(result) == 3 and result[0] == "A", "Test 6 failed: cycle"
    assert set(result) == {"A", "B", "C"}, "Test 6 failed: cycle"
    print("Test 6 passed: Graph with cycle")

    # Test 7: Node with no neighbors
    assert dfs_func(single_node("A")) == ["A"], "Test 7 failed: no neighbors"
    print("Test 7 passed: Node with no neighbors")

    # Test 8: Self-loop
    node = single_node("A")
    node.neighbors = [node, single_node("B")]
    node.neighbors[1].neighbors = [node]
    result = dfs_func(node)
    assert result == ["A", "B"], "Test 8 failed: self-loop"
    print("Test 8 passed: Self-loop handled correctly")

    # Test 9: Long path (verify deep traversal)
    nodes = make_graph([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F")])
    assert dfs_func(nodes["A"]) == ["A", "B", "C", "D", "E", "F"], "Test 9 failed"
    print("Test 9 passed: Long path traversal")

    # Test 10: Diamond graph
    nodes = make_graph([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")])
    result = dfs_func(nodes["A"])
    assert result[0] == "A" and len(result) == 4, "Test 10 failed: diamond"
    assert set(result) == {"A", "B", "C", "D"}, "Test 10 failed: diamond"
    print("Test 10 passed: Diamond graph")

    # Test 11: No duplicate visits (complete graph K4)
    nodes = make_graph(
        [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D")]
    )
    result = dfs_func(nodes["A"])
    assert len(result) == len(set(result)) == 4, "Test 11 failed: duplicates"
    print("Test 11 passed: No duplicate visits in complete graph")

    # Test 12: Numeric values
    nodes = make_graph([(1, 2), (1, 3)])
    result = dfs_func(nodes[1])
    assert result[0] == 1 and len(result) == 3, "Test 12 failed: numeric"
    print("Test 12 passed: Numeric values")

    print("\nAll tests passed!")
