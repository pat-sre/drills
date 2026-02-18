# Tree BFS (Level-Order Traversal)
#
# Visit all nodes level by level, left to right.
#
# Example:
#        1
#       / \
#      2   3
#     / \
#    4   5
#
# BFS order: [1, 2, 3, 4, 5]
#
# Node structure: node.val, node.left, node.right
#
from collections import deque


def solve(root: "Tree | None") -> list:
    if not root:
        return []
    nodes = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        nodes.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return nodes
