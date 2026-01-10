# Intuition:
#   Greedy algorithm that always processes the node with smallest
#   known distance. Use a priority queue (min-heap) to efficiently
#   get the next closest unvisited node.

import heapq

if __package__:
    from ..graph import GraphNode
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from graph import GraphNode


def dijkstra(start):
    if start is None:
        return {}

    distances = {start: 0}
    pq = [(0, id(start), start)]

    while pq:
        dist, _, node = heapq.heappop(pq)

        if dist > distances.get(node, float("inf")):
            continue

        for neighbor, weight in node.neighbors:
            new_dist = dist + weight

            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, id(neighbor), neighbor))

    return {node: dist for node, dist in distances.items()}


if __name__ == "__main__":
    if __package__:
        from .tests import run_dijkstra_tests
    else:
        from tests import run_dijkstra_tests

    run_dijkstra_tests(dijkstra)
