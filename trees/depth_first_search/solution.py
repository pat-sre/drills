# Intuition:
#   Use recursion to explore as deep as possible before backtracking.
#   Visit a node, then immediately visit its left subtree, then right subtree.

if __package__:
    from ..tree import Tree
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from tree import Tree


def dfs(root):
    result = []

    def traverse(node):
        if node is None:
            return
        result.append(node)
        traverse(node.left)
        traverse(node.right)

    traverse(root)
    return result


if __name__ == "__main__":
    if __package__:
        from .tests import run_dfs_tests
    else:
        from tests import run_dfs_tests

    run_dfs_tests(dfs)
