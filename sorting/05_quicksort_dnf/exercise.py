# Implement quicksort using the Dutch National Flag (3-way) partition.
#
# Given a list of numbers, return a new sorted list.
# Do not modify the input list.
#
# The DNF partition splits the array into three regions around a pivot:
#   [ < pivot | == pivot | > pivot ]
#
# This makes quicksort O(n) on arrays with many duplicates,
# since equal elements are never recursed into.
#
# Algorithm:
#   1. Base case: if the subarray has 0 or 1 elements, return.
#   2. Pick a random pivot.
#   3. DNF partition using three pointers — insert_low, current, insert_high:
#       - If nums[current] < pivot: swap with insert_low, advance both insert_low and current.
#       - If nums[current] > pivot: swap with insert_high, decrement insert_high (don't advance
#         current — the swapped-in element hasn't been examined yet).
#       - If nums[current] == pivot: just advance current.
#       - Stop when current > insert_high.
#   4. Recursively sort [start..insert_low-1] and [insert_high+1..end].
#
import random


def solve(nums: list[int | float]) -> list[int | float]:
    if not nums:
        return nums
    nums_copy = nums[:]
    quicksort(0, len(nums_copy) - 1, nums_copy)
    return nums_copy


def quicksort(start, end, nums):
    pass
