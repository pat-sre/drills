# Tree DFS (Preorder Traversal)
#
# Visit nodes in depth-first order: root -> left subtree -> right subtree.
#
# Example:
#        1
#       / \
#      2   3
#     / \
#    4   5
#
# DFS preorder: [1, 2, 4, 5, 3]
#
# Node structure: node.val, node.left, node.right
#
def dfs(root: "Tree | None") -> list:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(dfs)
