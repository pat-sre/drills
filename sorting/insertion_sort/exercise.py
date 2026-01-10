# Implement insertion sort.
#
# Given a list of numbers, return a new sorted list.
# Do not modify the input list.
#
def sort(nums: list[int | float]) -> list[int | float]:
    pass


if __name__ == "__main__":
    if __package__:
        from ..tests import run_sort_tests
    else:
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent.parent))
        from tests import run_sort_tests

    run_sort_tests(sort)
