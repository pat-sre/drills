if __package__:
    from .graph import GraphNode
else:
    from graph import GraphNode


def make_graph(edges, directed=False):
    """
    Build graph from edge list. Returns dict of {value: node}.

    Args:
        edges: List of tuples. Either (a, b) for unweighted or (a, b, weight) for weighted.
        directed: If False (default), adds edges in both directions.

    Example:
        nodes = make_graph([("A", "B"), ("B", "C")])
        start = nodes["A"]
    """
    nodes = {}
    for item in edges:
        if len(item) == 2:
            a, b = item
            weight = None
        else:
            a, b, weight = item

        if a not in nodes:
            nodes[a] = GraphNode(a)
        if b not in nodes:
            nodes[b] = GraphNode(b)

        if weight is not None:
            nodes[a].neighbors.append((nodes[b], weight))
            if not directed:
                nodes[b].neighbors.append((nodes[a], weight))
        else:
            nodes[a].neighbors.append(nodes[b])
            if not directed:
                nodes[b].neighbors.append(nodes[a])
    return nodes


def single_node(val):
    """Create an isolated node with no neighbors."""
    return GraphNode(val)
