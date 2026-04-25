from test_utils import run_all
from trees.test_utils import make_tree
from trees.tree import Tree


def run_tests(BSTIterator):
    def run_scenario(root, ops):
        it = BSTIterator(root)
        results = []
        for op in ops:
            if op == "next":
                results.append(it.next())
            elif op == "has_next":
                results.append(it.has_next())
        return results

    #       4
    #      / \
    #     2   6
    #    / \ / \
    #   1  3 5  7
    bst7 = make_tree(4, make_tree(2, Tree(1), Tree(3)), make_tree(6, Tree(5), Tree(7)))

    #     5
    #    / \
    #   3   8
    #  / \   \
    # 1   4   9
    bst6 = make_tree(5, make_tree(3, Tree(1), Tree(4)), make_tree(8, None, Tree(9)))

    tests = [
        {
            "name": "empty tree has_next is False",
            "inputs": {"root": None, "ops": ["has_next"]},
            "check": lambda r: r == [False],
            "fail_msg": lambda r: f"expected [False], got {r}",
        },
        {
            "name": "single node",
            "inputs": {"root": Tree(42), "ops": ["has_next", "next", "has_next"]},
            "check": lambda r: r == [True, 42, False],
            "fail_msg": lambda r: f"expected [True, 42, False], got {r}",
        },
        {
            "name": "full BST in-order",
            "inputs": {"root": bst7, "ops": ["next"] * 7},
            "check": lambda r: r == [1, 2, 3, 4, 5, 6, 7],
            "fail_msg": lambda r: f"expected [1,2,3,4,5,6,7], got {r}",
        },
        {
            "name": "BST with missing nodes",
            "inputs": {"root": bst6, "ops": ["next"] * 6},
            "check": lambda r: r == [1, 3, 4, 5, 8, 9],
            "fail_msg": lambda r: f"expected [1,3,4,5,8,9], got {r}",
        },
        {
            "name": "left-skewed BST",
            "inputs": {"root": make_tree(3, make_tree(2, Tree(1))), "ops": ["next"] * 3},
            "check": lambda r: r == [1, 2, 3],
            "fail_msg": lambda r: f"expected [1,2,3], got {r}",
        },
        {
            "name": "right-skewed BST",
            "inputs": {"root": make_tree(1, None, make_tree(2, None, Tree(3))), "ops": ["next"] * 3},
            "check": lambda r: r == [1, 2, 3],
            "fail_msg": lambda r: f"expected [1,2,3], got {r}",
        },
        {
            "name": "has_next interleaved with next",
            "inputs": {
                "root": make_tree(2, Tree(1), Tree(3)),
                "ops": ["has_next", "next", "has_next", "next", "has_next", "next", "has_next"],
            },
            "check": lambda r: r == [True, 1, True, 2, True, 3, False],
            "fail_msg": lambda r: f"expected [True,1,True,2,True,3,False], got {r}",
        },
    ]

    run_all("bst_iterator", tests, run_scenario)
