# implement Dijkstra's shortest path algorithm
#
# Given a weighted graph (adjacency list with weights) and a start node,
# return a dict mapping each reachable node to its shortest distance from start.
#
# Graph format: {node: [(neighbor, weight), ...], ...}
#
def dijkstra(graph: dict[str, list[tuple[str, int]]], start: str) -> dict[str, int]:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(dijkstra)
