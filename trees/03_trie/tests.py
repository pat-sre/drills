from test_utils import run_all


def run_tests(Trie):
    def run_scenario(ops):
        t = Trie()
        results = []
        for op in ops:
            if op[0] == "insert":
                t.insert(op[1])
            elif op[0] == "search":
                results.append(t.search(op[1]))
            elif op[0] == "starts_with":
                results.append(t.starts_with(op[1]))
        return results

    tests = [
        {
            "name": "search on empty trie returns False",
            "inputs": {"ops": [("search", "hello")]},
            "check": lambda r: r == [False],
            "fail_msg": lambda r: f"expected [False], got {r}",
        },
        {
            "name": "starts_with on empty trie returns False",
            "inputs": {"ops": [("starts_with", "he")]},
            "check": lambda r: r == [False],
            "fail_msg": lambda r: f"expected [False], got {r}",
        },
        {
            "name": "insert and search single word",
            "inputs": {"ops": [("insert", "hello"), ("search", "hello")]},
            "check": lambda r: r == [True],
            "fail_msg": lambda r: f"expected [True], got {r}",
        },
        {
            "name": "search non-existent word returns False",
            "inputs": {"ops": [("insert", "hello"), ("search", "world")]},
            "check": lambda r: r == [False],
            "fail_msg": lambda r: f"expected [False], got {r}",
        },
        {
            "name": "starts_with valid prefix returns True",
            "inputs": {"ops": [("insert", "apple"), ("starts_with", "app")]},
            "check": lambda r: r == [True],
            "fail_msg": lambda r: f"expected [True], got {r}",
        },
        {
            "name": "starts_with invalid prefix returns False",
            "inputs": {"ops": [("insert", "apple"), ("starts_with", "apl")]},
            "check": lambda r: r == [False],
            "fail_msg": lambda r: f"expected [False], got {r}",
        },
        {
            "name": "prefix in path but not a word — search False, starts_with True",
            "inputs": {"ops": [("insert", "apple"), ("search", "app"), ("starts_with", "app")]},
            "check": lambda r: r == [False, True],
            "fail_msg": lambda r: f"expected [False, True], got {r}",
        },
        {
            "name": "insert prefix of existing word — both searchable",
            "inputs": {"ops": [("insert", "apple"), ("insert", "app"), ("search", "app"), ("search", "apple")]},
            "check": lambda r: r == [True, True],
            "fail_msg": lambda r: f"expected [True, True], got {r}",
        },
        {
            "name": "insert multiple words and search each",
            "inputs": {"ops": [("insert", "cat"), ("insert", "car"), ("insert", "card"), ("search", "cat"), ("search", "car"), ("search", "card"), ("search", "care")]},
            "check": lambda r: r == [True, True, True, False],
            "fail_msg": lambda r: f"expected [True, True, True, False], got {r}",
        },
        {
            "name": "starts_with matches shared prefix across words",
            "inputs": {"ops": [("insert", "cat"), ("insert", "car"), ("starts_with", "ca"), ("starts_with", "cat"), ("starts_with", "cb")]},
            "check": lambda r: r == [True, True, False],
            "fail_msg": lambda r: f"expected [True, True, False], got {r}",
        },
        {
            "name": "case sensitivity — Hello and hello are distinct",
            "inputs": {"ops": [("insert", "Hello"), ("search", "Hello"), ("search", "hello"), ("starts_with", "He"), ("starts_with", "he")]},
            "check": lambda r: r == [True, False, True, False],
            "fail_msg": lambda r: f"expected [True, False, True, False], got {r}",
        },
        {
            "name": "longer word not found when only shorter word is stored",
            "inputs": {"ops": [("insert", "do"), ("search", "dog"), ("starts_with", "dog")]},
            "check": lambda r: r == [False, False],
            "fail_msg": lambda r: f"expected [False, False], got {r}",
        },
    ]

    run_all("trie", tests, run_scenario)
