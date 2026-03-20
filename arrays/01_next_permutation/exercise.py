# Implement next permutation.
#
# Given a list of integers, return the next lexicographically greater permutation.
# If the list is the last permutation (fully descending), return the first
# permutation (fully ascending).
#
# Do not modify the input list.
#
# Examples:
#   [2, 3, 6, 5, 4, 1] -> [2, 4, 1, 3, 5, 6]
#   [2, 5, 4, 3, 1] -> [3, 1, 2, 4, 5]
#   [1, 3, 5, 4, 2] -> [1, 4, 2, 3, 5]
#
# Algorithm:
#   1. Find the pivot. Scan right-to-left, find the first element where nums[i] < nums[i+1].
#       Everything to the right of this is descending — meaning that suffix is already at its last permutation.
#   2. Scan right-to-left again from the end, find the first element bigger than pivot.
#       Swap them.
#   3. Reverse the suffix after the pivot's position.
#


def solve(nums: list[int]) -> list[int]:
    i = len(nums) - 2
    while i >= 0 and nums[i] > nums[i + 1]:
        i -= 1
    print(nums[i], nums[i + 1])

    nums[i + 1 :] = nums[i + 1 :][::-1]
    return nums
