class Tree:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return repr(self.val)

    def __eq__(self, other):
        if isinstance(other, Tree):
            return self.val == other.val
        return self.val == other
