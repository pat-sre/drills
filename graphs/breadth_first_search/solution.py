# Intuition:
#   Use a queue to explore nodes level by level.
#   Start from the source node, visit all neighbors,
#   then visit neighbors of neighbors, etc.

from collections import deque

if __package__:
    from ..graph import GraphNode
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from graph import GraphNode


def bfs(start):
    if start is None:
        return []

    result = []
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in node.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


if __name__ == "__main__":
    if __package__:
        from .tests import run_bfs_tests
    else:
        from tests import run_bfs_tests

    run_bfs_tests(bfs)
