from collections import deque, defaultdict


def solve(nodes, edges):
    adj = defaultdict(list)
    in_degree = {node: 0 for node in nodes}

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque(node for node in nodes if in_degree[node] == 0)
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result
