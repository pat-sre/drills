# Intuition:
#   Use a queue to explore nodes level by level.
#   Start from the root, visit all nodes at current level,
#   then move to the next level.

from collections import deque

if __package__:
    from ..tree import Tree
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from tree import Tree


def bfs(root):
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(bfs)
