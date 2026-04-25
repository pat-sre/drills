# BST Iterator
#
# Implement an iterator over a BST that yields values in ascending (in-order) order.
#
# Example:
#        4
#       / \
#      2   6
#     / \ / \
#    1  3 5  7
#
# it = BSTIterator(root)
# it.has_next()  # True
# it.next()      # 1
# it.next()      # 2
# ...
# it.next()      # 7
# it.has_next()  # False
#
# Constraints:
#   - next() returns the next smallest value
#   - has_next() returns True if there are remaining values
#   - next() is called only when has_next() is True
#   - O(h) memory where h is the tree height
#


class BSTIterator:
    def __init__(self, root):
        pass


solve = BSTIterator
