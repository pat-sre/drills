# Intuition:
#   Use a stack (or recursion) to explore as deep as possible
#   before backtracking. Visit a node, then immediately visit
#   its first unvisited neighbor, and so on.


def dfs(graph, start):
    """
    Perform depth-first search traversal (iterative).

    Args:
        graph: Dict mapping node -> list of neighbor nodes
        start: Starting node for traversal

    Returns:
        List of nodes in DFS traversal order
    """
    if start not in graph:
        return []

    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        result.append(node)

        # Add neighbors in reverse order so first neighbor is processed first
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)

    return result


# Alternative recursive implementation
def dfs_recursive(graph, start):
    """
    Perform depth-first search traversal (recursive).
    """
    if start not in graph:
        return []

    visited = set()
    result = []

    def helper(node):
        if node in visited:
            return
        visited.add(node)
        result.append(node)
        for neighbor in graph[node]:
            helper(neighbor)

    helper(start)
    return result


if __name__ == "__main__":
    from tests import run_dfs_tests

    run_dfs_tests(dfs)
