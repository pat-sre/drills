def solve(root):
    result = []

    def traverse(node):
        if node is None:
            return
        result.append(node)
        traverse(node.left)
        traverse(node.right)

    traverse(root)
    return result
