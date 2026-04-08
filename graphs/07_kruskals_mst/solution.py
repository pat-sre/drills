def solve(nodes, edges):
    if not nodes:
        return 0

    node_idx = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    edges_sorted = sorted(edges, key=lambda e: e[2])
    total_weight = 0
    edges_used = 0

    for u, v, w in edges_sorted:
        if union(node_idx[u], node_idx[v]):
            total_weight += w
            edges_used += 1
            if edges_used == n - 1:
                break

    if edges_used != n - 1:
        return -1

    return total_weight
