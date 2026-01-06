def run_dfs_tests(dfs_func):
    """
    Reusable test suite for DFS algorithm.

    Args:
        dfs_func: A function that takes (graph, start) and returns traversal order
    """
    print(f"Running tests for {dfs_func.__name__}...\n")

    # Test 1: Empty graph with non-existent start
    graph1 = {}
    result1 = dfs_func(graph1, "A")
    assert result1 == [], f"Test 1 failed: expected [], got {result1}"
    print("Test 1 passed: Empty graph")

    # Test 2: Single node
    graph2 = {"A": []}
    result2 = dfs_func(graph2, "A")
    assert result2 == ["A"], f"Test 2 failed: expected ['A'], got {result2}"
    print("Test 2 passed: Single node")

    # Test 3: Two connected nodes
    graph3 = {"A": ["B"], "B": ["A"]}
    result3 = dfs_func(graph3, "A")
    assert result3 == ["A", "B"], f"Test 3 failed: expected ['A', 'B'], got {result3}"
    print("Test 3 passed: Two connected nodes")

    # Test 4: Linear graph (chain)
    graph4 = {"A": ["B"], "B": ["A", "C"], "C": ["B", "D"], "D": ["C"]}
    result4 = dfs_func(graph4, "A")
    assert result4 == ["A", "B", "C", "D"], f"Test 4 failed: got {result4}"
    print("Test 4 passed: Linear graph")

    # Test 5: Tree structure - verify DFS property (goes deep first)
    #       A
    #      / \
    #     B   C
    #    / \
    #   D   E
    graph5 = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A"],
        "D": ["B"],
        "E": ["B"],
    }
    result5 = dfs_func(graph5, "A")
    assert result5[0] == "A", f"Test 5 failed: should start with A, got {result5}"
    assert len(result5) == 5, f"Test 5 failed: should visit all 5 nodes"
    # Verify DFS property: B should come before C (we go deep before wide)
    b_idx = result5.index("B")
    c_idx = result5.index("C")
    d_idx = result5.index("D")
    e_idx = result5.index("E")
    # D and E should come after B but could be before or after C depending on order
    assert b_idx < d_idx and b_idx < e_idx, "Test 5 failed: D and E should come after B"
    print("Test 5 passed: Tree structure (depth-first property)")

    # Test 6: Graph with cycle
    graph6 = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}
    result6 = dfs_func(graph6, "A")
    assert len(result6) == 3, f"Test 6 failed: expected 3 nodes, got {len(result6)}"
    assert result6[0] == "A", f"Test 6 failed: should start with A"
    assert set(result6) == {"A", "B", "C"}, f"Test 6 failed: got {result6}"
    print("Test 6 passed: Graph with cycle")

    # Test 7: Disconnected component (only traverse connected nodes)
    graph7 = {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"]}
    result7 = dfs_func(graph7, "A")
    assert result7 == ["A", "B"], f"Test 7 failed: expected ['A', 'B'], got {result7}"
    print("Test 7 passed: Disconnected graph (traverse only reachable)")

    # Test 8: Start node not in graph
    graph8 = {"A": ["B"], "B": ["A"]}
    result8 = dfs_func(graph8, "X")
    assert result8 == [], f"Test 8 failed: expected [], got {result8}"
    print("Test 8 passed: Start node not in graph")

    # Test 9: Node with no neighbors
    graph9 = {"A": [], "B": [], "C": []}
    result9 = dfs_func(graph9, "A")
    assert result9 == ["A"], f"Test 9 failed: expected ['A'], got {result9}"
    print("Test 9 passed: Node with no neighbors")

    # Test 10: Larger graph
    graph10 = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }
    result10 = dfs_func(graph10, "A")
    assert len(result10) == 6, f"Test 10 failed: expected 6 nodes, got {len(result10)}"
    assert result10[0] == "A", f"Test 10 failed: should start with A"
    print("Test 10 passed: Larger graph")

    # Test 11: Numeric nodes
    graph11 = {1: [2, 3], 2: [1, 4], 3: [1], 4: [2]}
    result11 = dfs_func(graph11, 1)
    assert result11[0] == 1, f"Test 11 failed: should start with 1"
    assert len(result11) == 4, f"Test 11 failed: expected 4 nodes"
    print("Test 11 passed: Numeric nodes")

    # Test 12: Self-loop (node connected to itself)
    graph12 = {"A": ["A", "B"], "B": ["A"]}
    result12 = dfs_func(graph12, "A")
    assert result12 == ["A", "B"], (
        f"Test 12 failed: expected ['A', 'B'], got {result12}"
    )
    print("Test 12 passed: Self-loop handled correctly")

    # Test 13: Long path (verify deep traversal)
    graph13 = {
        "A": ["B"],
        "B": ["A", "C"],
        "C": ["B", "D"],
        "D": ["C", "E"],
        "E": ["D", "F"],
        "F": ["E"],
    }
    result13 = dfs_func(graph13, "A")
    assert result13 == ["A", "B", "C", "D", "E", "F"], f"Test 13 failed: got {result13}"
    print("Test 13 passed: Long path traversal")

    # Test 14: Diamond graph
    #     A
    #    / \
    #   B   C
    #    \ /
    #     D
    graph14 = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["B", "C"]}
    result14 = dfs_func(graph14, "A")
    assert result14[0] == "A", "Test 14 failed: should start with A"
    assert len(result14) == 4, f"Test 14 failed: expected 4 nodes"
    assert set(result14) == {"A", "B", "C", "D"}, f"Test 14 failed: got {result14}"
    print("Test 14 passed: Diamond graph")

    # Test 15: Verify no duplicate visits
    graph15 = {
        "A": ["B", "C", "D"],
        "B": ["A", "C", "D"],
        "C": ["A", "B", "D"],
        "D": ["A", "B", "C"],
    }
    result15 = dfs_func(graph15, "A")
    assert len(result15) == len(set(result15)), (
        "Test 15 failed: duplicate nodes visited"
    )
    assert len(result15) == 4, f"Test 15 failed: expected 4 nodes"
    print("Test 15 passed: No duplicate visits in complete graph")

    print("\nAll tests passed!")
