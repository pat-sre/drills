import random


def run_sort_tests(sort_func):
    """
    Reusable test suite for sorting algorithms.

    Args:
        sort_func: A function that takes a list and returns a sorted list
    """
    print(f"Running tests for {sort_func.__name__}...\n")

    # Test 1: Empty array
    test1 = []
    test1 = sort_func(test1)
    assert test1 == [], f"Test 1 failed: expected [], got {test1}"
    print("Test 1 passed: Empty array")

    # Test 2: Single element
    test2 = [5]
    test2 = sort_func(test2)
    assert test2 == [5], f"Test 2 failed: expected [5], got {test2}"
    print("Test 2 passed: Single element")

    # Test 3: Two elements - already sorted
    test3 = [1, 2]
    test3 = sort_func(test3)
    assert test3 == [1, 2], f"Test 3 failed: expected [1, 2], got {test3}"
    print("Test 3 passed: Two elements already sorted")

    # Test 4: Two elements - reverse sorted
    test4 = [2, 1]
    test4 = sort_func(test4)
    assert test4 == [1, 2], f"Test 4 failed: expected [1, 2], got {test4}"
    print("Test 4 passed: Two elements reverse sorted")

    # Test 5: Already sorted array
    test5 = [1, 2, 3, 4, 5]
    test5 = sort_func(test5)
    assert test5 == [1, 2, 3, 4, 5], (
        f"Test 5 failed: expected [1, 2, 3, 4, 5], got {test5}"
    )
    print("Test 5 passed: Already sorted array")

    # Test 6: Reverse sorted array
    test6 = [5, 4, 3, 2, 1]
    test6 = sort_func(test6)
    assert test6 == [1, 2, 3, 4, 5], (
        f"Test 6 failed: expected [1, 2, 3, 4, 5], got {test6}"
    )
    print("Test 6 passed: Reverse sorted array")

    # Test 7: Random order with duplicates
    test7 = [3, 7, 8, 5, 2, 1, 9, 5, 4]
    test7 = sort_func(test7)
    assert test7 == [1, 2, 3, 4, 5, 5, 7, 8, 9], (
        f"Test 7 failed: expected [1, 2, 3, 4, 5, 5, 7, 8, 9], got {test7}"
    )
    print("Test 7 passed: Random order with duplicates")

    # Test 8: All same elements
    test8 = [5, 5, 5, 5, 5]
    test8 = sort_func(test8)
    assert test8 == [5, 5, 5, 5, 5], (
        f"Test 8 failed: expected [5, 5, 5, 5, 5], got {test8}"
    )
    print("Test 8 passed: All same elements")

    # Test 9: Negative numbers
    test9 = [3, -1, -4, 2, -5, 0]
    test9 = sort_func(test9)
    assert test9 == [-5, -4, -1, 0, 2, 3], (
        f"Test 9 failed: expected [-5, -4, -1, 0, 2, 3], got {test9}"
    )
    print("Test 9 passed: Negative numbers")

    # Test 10: Large array
    test10 = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 23, 36, 18, 77]
    test10 = sort_func(test10)
    assert test10 == [11, 12, 18, 22, 23, 25, 34, 36, 45, 50, 64, 77, 88, 90], (
        f"Test 10 failed: got {test10}"
    )
    print("Test 10 passed: Large array")

    # Test 11: Array with many duplicates
    test11 = [5, 2, 8, 2, 9, 1, 5, 5, 2, 8]
    test11 = sort_func(test11)
    assert test11 == [1, 2, 2, 2, 5, 5, 5, 8, 8, 9], f"Test 11 failed: got {test11}"
    print("Test 11 passed: Many duplicates")

    # Test 12: Floats
    test12 = [3.5, 1.2, 4.8, 2.1, 0.5]
    test12 = sort_func(test12)
    assert test12 == [0.5, 1.2, 2.1, 3.5, 4.8], f"Test 12 failed: got {test12}"
    print("Test 12 passed: Floating point numbers")

    # Test 13: Three elements (important edge case)
    test13 = [3, 1, 2]
    test13 = sort_func(test13)
    assert test13 == [1, 2, 3], f"Test 13 failed: got {test13}"
    print("Test 13 passed: Three elements (important edge case)")

    # Test 14: Larger array (1000 elements)
    test14 = [random.randint(-100, 100) for _ in range(1000)]
    expected14 = sorted(test14)
    test14 = sort_func(test14)
    assert test14 == expected14, "Test 14 failed: 1000 elements array"
    print("Test 14 passed: Larger array (1000 elements)")

    # Test 15: Adjacent duplicates
    test15 = [1, 1, 1, 2, 2, 2, 3, 3, 3]
    test15 = sort_func(test15)
    assert test15 == [1, 1, 1, 2, 2, 2, 3, 3, 3], f"Test 15 failed: got {test15}"
    print("Test 15 passed: Adjacent duplicates")

    print("\nAll tests passed!")
