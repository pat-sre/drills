from test_utils import run_all
from trees.test_utils import make_tree
from trees.tree import Tree


def run_tests(solve):
    # Build test trees
    t6 = make_tree(1, make_tree(2, Tree(4), Tree(5)), make_tree(3, Tree(6), Tree(7)))
    t9 = make_tree(1, make_tree(2, make_tree(4, Tree(5))), Tree(3))
    t11 = make_tree(1, Tree(2), make_tree(3, Tree(4), make_tree(5, Tree(6))))
    t12 = make_tree(
        1, make_tree(2, make_tree(4, Tree(8)), Tree(5)), make_tree(3, Tree(6), Tree(7))
    )

    tests = [
        {
            "name": "empty tree",
            "inputs": {"root": None},
            "check": lambda r: r == [],
            "fail_msg": lambda r: f"expected [], got {r}",
        },
        {
            "name": "single node",
            "inputs": {"root": Tree(1)},
            "check": lambda r: r == [1],
            "fail_msg": lambda r: f"expected [1], got {r}",
        },
        {
            "name": "left child only",
            "inputs": {"root": make_tree(1, Tree(2))},
            "check": lambda r: r == [1, 2],
            "fail_msg": lambda r: f"expected [1, 2], got {r}",
        },
        {
            "name": "right child only",
            "inputs": {"root": make_tree(1, None, Tree(2))},
            "check": lambda r: r == [1, 2],
            "fail_msg": lambda r: f"expected [1, 2], got {r}",
        },
        {
            "name": "complete binary tree (3 nodes)",
            "inputs": {"root": make_tree(1, Tree(2), Tree(3))},
            "check": lambda r: r == [1, 2, 3],
            "fail_msg": lambda r: f"expected [1, 2, 3], got {r}",
        },
        {
            "name": "full binary tree (level order)",
            "inputs": {"root": t6},
            "check": lambda r: r == [1, 2, 3, 4, 5, 6, 7],
            "fail_msg": lambda r: f"expected [1, 2, 3, 4, 5, 6, 7], got {r}",
        },
        {
            "name": "left-skewed tree",
            "inputs": {"root": make_tree(1, make_tree(2, Tree(3)))},
            "check": lambda r: r == [1, 2, 3],
            "fail_msg": lambda r: f"expected [1, 2, 3], got {r}",
        },
        {
            "name": "right-skewed tree",
            "inputs": {"root": make_tree(1, None, make_tree(2, None, Tree(3)))},
            "check": lambda r: r == [1, 2, 3],
            "fail_msg": lambda r: f"expected [1, 2, 3], got {r}",
        },
        {
            "name": "unbalanced tree (level order)",
            "inputs": {"root": t9},
            "check": lambda r: r == [1, 2, 3, 4, 5],
            "fail_msg": lambda r: f"expected [1, 2, 3, 4, 5], got {r}",
        },
        {
            "name": "string values",
            "inputs": {"root": make_tree("a", Tree("b"), Tree("c"))},
            "check": lambda r: r == ["a", "b", "c"],
            "fail_msg": lambda r: f"expected ['a', 'b', 'c'], got {r}",
        },
        {
            "name": "mixed depth subtrees",
            "inputs": {"root": t11},
            "check": lambda r: r == [1, 2, 3, 4, 5, 6],
            "fail_msg": lambda r: f"expected [1, 2, 3, 4, 5, 6], got {r}",
        },
        {
            "name": "larger tree (level order)",
            "inputs": {"root": t12},
            "check": lambda r: r == [1, 2, 3, 4, 5, 6, 7, 8],
            "fail_msg": lambda r: f"expected [1, 2, 3, 4, 5, 6, 7, 8], got {r}",
        },
    ]

    run_all("breadth_first_search", tests, solve)
