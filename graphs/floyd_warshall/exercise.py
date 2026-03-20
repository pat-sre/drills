# Floyd-Warshall Algorithm — All-Pairs Shortest Paths
#
# Given a list of nodes and weighted directed edges, find the shortest
# distance between every pair of nodes.
#
# Input:
#   nodes — list of node values (e.g. ["A", "B", "C"])
#   edges — list of (u, v, weight) tuples representing directed edges
#
# Output:
#   A nested dict {u: {v: dist}} where dist is the shortest distance
#   from u to v. Use float("inf") for unreachable pairs.
#   Distance from a node to itself is always 0.
#
# Hints:
#   - Initialize a dist table: 0 for self, edge weight for direct edges, inf otherwise
#   - For each intermediate node k, try to improve dist[i][j] via k
#   - The key relaxation: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])


def solve(nodes: list, edges: list) -> dict:
    pass
