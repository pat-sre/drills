# Intuition:
#   For i = 0,1,2,3,...
#   Insert A[i] into sorted Array[0:i - 1]


# implement insertion sort
#
def sort(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]  # create a copy of input data
    insertion_sort(sorted_vals)
    return sorted_vals


def insertion_sort(nums):
    for i in range(1, len(nums)):
        j = i
        val = nums[i]
        while j and nums[j - 1] > val:
            nums[j] = nums[j - 1]
            j -= 1
        nums[j] = val


if __name__ == "__main__":
    if __package__:
        from ..tests import run_sort_tests
    else:
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent.parent))
        from tests import run_sort_tests

    run_sort_tests(sort)
