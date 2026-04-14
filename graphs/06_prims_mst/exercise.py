# Prim's Algorithm — Minimum Spanning Tree
#
# Given a list of nodes and undirected weighted edges, find the total
# weight of the Minimum Spanning Tree (MST).
#
# Input:
#   nodes — list of node labels (e.g. ["A", "B", "C"])
#   edges — list of (u, v, weight) tuples representing undirected edges
#
# Hints:
#   - Build an undirected adjacency list from the edge list
#   - Use heapq for a min-priority queue seeded from the first node
#   - Track visited nodes; greedily pick the cheapest edge to an unvisited node
#   - After the loop, check if all nodes were visited
import heapq
from collections import defaultdict


# Output:
#   The total weight of the MST as an integer.
#   If the graph is disconnected (no spanning tree exists), return -1.
def solve(nodes: list, edges: list) -> int:
    pass
