from collections import deque


def solve(root):
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result
