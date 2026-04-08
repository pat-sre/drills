# Topological Sort — Kahn's Algorithm (BFS-based)
#
# Given a list of nodes and directed edges, return a list of node values
# in topologically sorted order.
#
# Input:
#   nodes — list of node values (e.g. ["A", "B", "C"])
#   edges — list of (from, to) tuples representing directed edges
#
# Output:
#   A list of node values where for every edge (u, v), u appears before v.
#   All nodes must appear exactly once in the result.
#
# Hints:
#   - Compute in-degree for each node
#   - Start with all nodes that have in-degree 0
#   - Use a queue (collections.deque) — process nodes in FIFO order
#   - When you process a node, decrement in-degrees of its neighbors

from collections import defaultdict, deque


def solve(nodes: list, edges: list) -> list:
    pass
