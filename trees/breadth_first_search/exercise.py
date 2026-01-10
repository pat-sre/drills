# Tree BFS (Level-Order Traversal)
#
# Visit all nodes level by level, left to right.
#
# Example:
#        1
#       / \
#      2   3
#     / \
#    4   5
#
# BFS order: [1, 2, 3, 4, 5]
#
# Hint: What data structure processes elements in the order they were added?
#
# Node structure: node.val, node.left, node.right
#
def bfs(root: "Tree | None") -> list:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_bfs_tests
    else:
        from tests import run_bfs_tests

    run_bfs_tests(bfs)
