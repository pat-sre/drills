# Dijkstra's Algorithm — Shortest Paths in a Weighted Graph
#
# Given an edge list and a source node, find the shortest distance
# from source to every reachable node.
#
# Input:
#   edges  — list of (u, v, weight) tuples representing directed edges
#   source — the starting node label (e.g. "A")
#
# Output:
#   A dict mapping each reachable node's value to its shortest distance:
#     {"A": 0, "B": 4, "C": 7}
#
# Hints:
#   - Build an adjacency list from the edge list
#   - Use heapq for a min-priority queue
#   - Skip nodes already processed with a shorter distance
import heapq
from collections import defaultdict


def solve(edges: list, source: str) -> dict:
    pass
