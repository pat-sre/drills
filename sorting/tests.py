import random

SORT_TESTS = [
    ([], [], "empty array"),
    ([5], [5], "single element"),
    ([1, 2], [1, 2], "two elements sorted"),
    ([2, 1], [1, 2], "two elements reverse"),
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], "already sorted"),
    ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5], "reverse sorted"),
    (
        [3, 7, 8, 5, 2, 1, 9, 5, 4],
        [1, 2, 3, 4, 5, 5, 7, 8, 9],
        "random with duplicates",
    ),
    ([5, 5, 5, 5, 5], [5, 5, 5, 5, 5], "all same"),
    ([3, -1, -4, 2, -5, 0], [-5, -4, -1, 0, 2, 3], "negative numbers"),
    (
        [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 23, 36, 18, 77],
        [11, 12, 18, 22, 23, 25, 34, 36, 45, 50, 64, 77, 88, 90],
        "larger array",
    ),
    ([5, 2, 8, 2, 9, 1, 5, 5, 2, 8], [1, 2, 2, 2, 5, 5, 5, 8, 8, 9], "many duplicates"),
    ([3.5, 1.2, 4.8, 2.1, 0.5], [0.5, 1.2, 2.1, 3.5, 4.8], "floats"),
    ([3, 1, 2], [1, 2, 3], "three elements"),
    ([1, 1, 1, 2, 2, 2, 3, 3, 3], [1, 1, 1, 2, 2, 2, 3, 3, 3], "adjacent duplicates"),
]


def run_sort_tests(sort_func):
    """
    Reusable test suite for sorting algorithms.

    Args:
        sort_func: A function that takes a list and returns a sorted list
    """
    print(f"Running tests for {sort_func.__name__}...\n")

    for i, (input_data, expected, desc) in enumerate(SORT_TESTS, 1):
        result = sort_func(list(input_data))
        assert result == expected, (
            f"Test {i} ({desc}): expected {expected}, got {result}"
        )
        print(f"Test {i} passed: {desc}")

    # Large random test
    large = [random.randint(-100, 100) for _ in range(1000)]
    result = sort_func(list(large))
    assert result == sorted(large), "Large array test failed"
    print(f"Test {len(SORT_TESTS) + 1} passed: large random array (1000 elements)")

    print("\nAll tests passed!")
