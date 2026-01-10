# implement quick sort
import random


def sort(nums):
    if not nums:
        return nums
    nums2 = nums[:]
    quick_sort(0, len(nums2) - 1, nums2)
    return nums2


def quick_sort(l, r, nums):
    if l >= r:
        return

    q = partition(l, r, nums)
    quick_sort(l, q - 1, nums)
    quick_sort(q + 1, r, nums)


def partition(l, r, nums):
    pivot_idx = random.randint(l, r)
    nums[r], nums[pivot_idx] = nums[pivot_idx], nums[r]
    pivot = nums[r]

    boundary = l - 1
    for i in range(l, r):
        if nums[i] <= pivot:
            boundary += 1
            nums[i], nums[boundary] = nums[boundary], nums[i]
    nums[r], nums[boundary + 1] = nums[boundary + 1], nums[r]
    return boundary + 1


if __name__ == "__main__":
    if __package__:
        from ..tests import run_sort_tests
    else:
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent.parent))
        from tests import run_sort_tests

    run_sort_tests(sort)
