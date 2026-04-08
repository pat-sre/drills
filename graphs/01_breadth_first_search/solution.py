from collections import deque


def solve(start):
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
