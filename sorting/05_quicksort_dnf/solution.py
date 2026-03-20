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
    pivot_start, pivot_end = dnf_partition(start, end, nums)
    quick_sort(start, pivot_start - 1, nums)
    quick_sort(pivot_end + 1, end, nums)


def dnf_partition(start, end, nums):
    pivot_idx = random.randint(start, end)
    pivot = nums[pivot_idx]
    insert_low = start  # where the next < pivot element goes
    current = start  # element being examined
    insert_high = end  # where the next > pivot element goes
    while current <= insert_high:
        if nums[current] < pivot:
            nums[insert_low], nums[current] = nums[current], nums[insert_low]
            insert_low += 1
            current += 1
        elif nums[current] > pivot:
            nums[current], nums[insert_high] = nums[insert_high], nums[current]
            insert_high -= 1
        else:
            current += 1
    return insert_low, insert_high
