if __package__:
    from .tree import Tree
else:
    from tree import Tree


def make_tree(val, left=None, right=None):
    """
    Create a tree node with optional children.

    Args:
        val: The node value
        left: Left child (Tree node or None)
        right: Right child (Tree node or None)

    Example:
        # Build:    1
        #          / \
        #         2   3
        tree = make_tree(1, make_tree(2), make_tree(3))
    """
    node = Tree(val)
    node.left = left
    node.right = right
    return node
