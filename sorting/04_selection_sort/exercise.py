# Implement selection sort.
#
# Given a list of numbers, return a new sorted list.
# Do not modify the input list.
#
# On each iteration, find the minimum element from the
# unsorted portion and swap it into the correct position.
#
def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    selection_sort(sorted_vals)
    return sorted_vals


def selection_sort(nums):
    pass
