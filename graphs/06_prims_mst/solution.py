import heapq
from collections import defaultdict


def solve(nodes, edges):
    if not nodes:
        return 0

    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((w, v))
        graph[v].append((w, u))

    start = nodes[0]
    visited = set()
    min_heap = [(0, start)]
    total_weight = 0

    while min_heap:
        weight, node = heapq.heappop(min_heap)
        if node in visited:
            continue
        visited.add(node)
        total_weight += weight
        for edge_weight, neighbor in graph[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, neighbor))

    if len(visited) != len(nodes):
        return -1

    return total_weight
