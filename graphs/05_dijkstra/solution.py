import heapq
from collections import defaultdict


def solve(edges, source):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    shortest_dist = {source: 0}
    min_heap = [(0, source)]

    while min_heap:
        curr_dist, curr_node = heapq.heappop(min_heap)
        if curr_dist > shortest_dist[curr_node]:
            continue
        for neighbor, edge_weight in graph[curr_node]:
            new_dist = curr_dist + edge_weight
            if neighbor not in shortest_dist or new_dist < shortest_dist[neighbor]:
                shortest_dist[neighbor] = new_dist
                heapq.heappush(min_heap, (new_dist, neighbor))

    return shortest_dist
