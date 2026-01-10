if __package__:
    from ..test_utils import make_tree
    from ..tree import Tree
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from test_utils import make_tree
    from tree import Tree


def run_bfs_tests(bfs_func):
    """
    Reusable test suite for tree BFS algorithm.

    Args:
        bfs_func: A function that takes (root) and returns traversal order
    """
    print(f"Running tests for {bfs_func.__name__}...\n")

    # Test 1: Empty tree
    assert bfs_func(None) == [], "Test 1 failed: empty tree"
    print("Test 1 passed: Empty tree")

    # Test 2: Single node
    assert bfs_func(Tree(1)) == [1], "Test 2 failed: single node"
    print("Test 2 passed: Single node")

    # Test 3: Left child only
    assert bfs_func(make_tree(1, Tree(2))) == [1, 2], "Test 3 failed"
    print("Test 3 passed: Left child only")

    # Test 4: Right child only
    assert bfs_func(make_tree(1, None, Tree(2))) == [1, 2], "Test 4 failed"
    print("Test 4 passed: Right child only")

    # Test 5: Complete binary tree (3 nodes)
    tree = make_tree(1, Tree(2), Tree(3))
    assert bfs_func(tree) == [1, 2, 3], "Test 5 failed"
    print("Test 5 passed: Complete binary tree (3 nodes)")

    # Test 6: Full binary tree (7 nodes)
    #         1
    #        / \
    #       2   3
    #      / \ / \
    #     4  5 6  7
    tree = make_tree(1, make_tree(2, Tree(4), Tree(5)), make_tree(3, Tree(6), Tree(7)))
    assert bfs_func(tree) == [1, 2, 3, 4, 5, 6, 7], "Test 6 failed"
    print("Test 6 passed: Full binary tree (level order)")

    # Test 7: Left-skewed tree
    tree = make_tree(1, make_tree(2, Tree(3)))
    assert bfs_func(tree) == [1, 2, 3], "Test 7 failed"
    print("Test 7 passed: Left-skewed tree")

    # Test 8: Right-skewed tree
    tree = make_tree(1, None, make_tree(2, None, Tree(3)))
    assert bfs_func(tree) == [1, 2, 3], "Test 8 failed"
    print("Test 8 passed: Right-skewed tree")

    # Test 9: Unbalanced tree
    tree = make_tree(1, make_tree(2, make_tree(4, Tree(5))), Tree(3))
    assert bfs_func(tree) == [1, 2, 3, 4, 5], "Test 9 failed"
    print("Test 9 passed: Unbalanced tree (level order)")

    # Test 10: String values
    tree = make_tree("a", Tree("b"), Tree("c"))
    assert bfs_func(tree) == ["a", "b", "c"], "Test 10 failed"
    print("Test 10 passed: String values")

    # Test 11: Mixed depth subtrees
    tree = make_tree(1, Tree(2), make_tree(3, Tree(4), make_tree(5, Tree(6))))
    assert bfs_func(tree) == [1, 2, 3, 4, 5, 6], "Test 11 failed"
    print("Test 11 passed: Mixed depth subtrees")

    # Test 12: Larger tree
    tree = make_tree(
        1, make_tree(2, make_tree(4, Tree(8)), Tree(5)), make_tree(3, Tree(6), Tree(7))
    )
    assert bfs_func(tree) == [1, 2, 3, 4, 5, 6, 7, 8], "Test 12 failed"
    print("Test 12 passed: Larger tree (level order)")

    print("\nAll tests passed!")
