# Intuition:
#   Use a stack to explore as deep as possible before backtracking.
#   Visit a node, then immediately visit its first unvisited neighbor, and so on.

if __package__:
    from ..graph import GraphNode
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from graph import GraphNode


def dfs(start):
    if start is None:
        return []

    result = []
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node in visited:
            continue
        visited.add(node)
        result.append(node)

        for neighbor in reversed(node.neighbors):
            if neighbor not in visited:
                stack.append(neighbor)

    return result


if __name__ == "__main__":
    if __package__:
        from .tests import run_dfs_tests
    else:
        from tests import run_dfs_tests

    run_dfs_tests(dfs)
