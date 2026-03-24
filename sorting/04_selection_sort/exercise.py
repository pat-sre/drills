# Implement selection sort.
#
# Given a list of numbers, return a new sorted list.
# Do not modify the input list.
#
# Algorithm:
#   1. Iterate i from 0 to n-2. The subarray [0..i-1] contains the final sorted elements.
#   2. Scan the unsorted portion [i..n-1] to find the index of the minimum element.
#   3. Swap the minimum element with the element at position i.
#
def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    selection_sort(sorted_vals)
    return sorted_vals


def selection_sort(nums):
    pass
