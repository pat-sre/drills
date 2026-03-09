import heapq
from collections import defaultdict


def solve(edges, source):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    min_distance = {source: 0}
    min_heap = [(0, source)]

    while min_heap:
        current_distance, current_node = heapq.heappop(min_heap)
        if current_distance > min_distance[current_node]:
            continue
        for neighbor, weight in graph[current_node]:
            new_distance = current_distance + weight
            if neighbor not in min_distance or new_distance < min_distance[neighbor]:
                min_distance[neighbor] = new_distance
                heapq.heappush(min_heap, (new_distance, neighbor))

    return min_distance
