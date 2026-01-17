import random


def solve(nums: list[int | float]) -> list[int | float]:
    if not nums:
        return nums
    nums_copy = nums[:]
    quick_sort(0, len(nums_copy) - 1, nums_copy)
    return nums_copy


def quick_sort(start, end, nums):
    if start >= end:
        return
    pivot_index = partition(start, end, nums)
    quick_sort(start, pivot_index - 1, nums)
    quick_sort(pivot_index + 1, end, nums)


def partition(start, end, nums):
    pivot_idx = random.randint(start, end)
    pivot = nums[pivot_idx]
    nums[end], nums[pivot_idx] = nums[pivot_idx], nums[end]

    low_boundary = start
    for i in range(start, end):
        if nums[i] <= pivot:
            nums[low_boundary], nums[i] = nums[i], nums[low_boundary]
            low_boundary += 1
    nums[low_boundary], nums[end] = nums[end], nums[low_boundary]
    return low_boundary
