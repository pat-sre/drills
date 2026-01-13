# implement breadth-first search
#
# Given a graph (adjacency list) and a start node,
# return a list of nodes in BFS traversal order.
#
def bfs(graph: dict[str, list[str]], start: str) -> list[str]:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(bfs)
