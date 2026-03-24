# Implement insertion sort.
#
# Given a list of numbers, return a new sorted list.
# Do not modify the input list.
#
# Algorithm:
#   1. Iterate through the array from left to right. The subarray [0..i-1] is already sorted.
#   2. Save the current element (nums[i]) and scan backwards through the sorted portion.
#   3. Shift each element that is greater than the saved value one position to the right.
#   4. Insert the saved value into the gap left by the shifting.
#
def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    insertion_sort(sorted_vals)
    return sorted_vals


def insertion_sort(nums):
    pass
