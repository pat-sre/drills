# implement depth-first search
#
# Given a graph (adjacency list) and a start node,
# return a list of nodes in DFS traversal order.
#
def dfs(graph: dict[str, list[str]], start: str) -> list[str]:
    pass


if __name__ == "__main__":
    if __package__:
        from .tests import run_tests
    else:
        from tests import run_tests

    run_tests(dfs)
