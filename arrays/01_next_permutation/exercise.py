# Implement next permutation.
#
# Given a list of integers, return the next lexicographically greater permutation.
# If the list is the last permutation (fully descending), return the first
# permutation (fully ascending).
#
# Do not modify the input list.
#
# Examples:
#   [1, 2, 3] -> [1, 3, 2]
#   [3, 2, 1] -> [1, 2, 3]
#   [1, 1, 5] -> [1, 5, 1]
#
# Algorithm:
#   1. Find the pivot. Scan right-to-left, find the first element where nums[i] < nums[i+1].
#       Everything to the right of this is descending — meaning that suffix is already at its last permutation.
#       There's nothing "next" within it alone.
#   2. Swap pivot with the smallest larger element to its right.
#       Scan right-to-left again from the end, find the first element bigger than pivot.
#       Swap them.
#   3. Reverse the suffix after the pivot's position.
#       The suffix was descending (largest permutation of those digits) — reversing makes it ascending (smallest permutation).
#       This gives the next overall permutation, not some arbitrary larger one.
#
def solve(nums: list[int]) -> list[int]:
    pass
