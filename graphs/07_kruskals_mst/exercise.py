# Kruskal's Algorithm — Minimum Spanning Tree
#
# Given a list of nodes and undirected weighted edges, find the total
# weight of the Minimum Spanning Tree (MST).
#
# Input:
#   nodes — list of node labels (e.g. ["A", "B", "C"])
#   edges — list of (u, v, weight) tuples representing undirected edges
#
# Output:
#   The total weight of the MST as an integer.
#   If the graph is disconnected (no spanning tree exists), return -1.
#
# Hints:
#   - Sort all edges by weight (ascending)
#   - Use a Union-Find structure to track connected components
#   - For each edge, if the endpoints are in different components, add it to the MST
#   - Stop early once you have n-1 edges in the MST
#   - If fewer than n-1 edges were added, the graph is disconnected


def solve(nodes: list, edges: list) -> int:
    pass
