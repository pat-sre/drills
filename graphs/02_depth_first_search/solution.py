def solve(start):
    if start is None:
        return []

    result = []
    visited = {start}
    stack = [start]

    while stack:
        node = stack.pop()
        result.append(node)

        for neighbor in reversed(node.neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return result
