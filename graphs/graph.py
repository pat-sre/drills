class GraphNode:
    def __init__(self, val):
        self.val = val
        self.neighbors = []

    def __repr__(self):
        return repr(self.val)

    def __eq__(self, other):
        if isinstance(other, GraphNode):
            return self.val == other.val
        return self.val == other

    def __hash__(self):
        return hash(self.val)
