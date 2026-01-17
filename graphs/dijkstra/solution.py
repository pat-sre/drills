import heapq


def solve(start):
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
