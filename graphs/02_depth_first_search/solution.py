def solve(start):
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
