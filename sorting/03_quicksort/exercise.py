# Implement quicksort.
#
# Given a list of numbers, return a new sorted list.
# Do not modify the input list.
#
# Algorithm:
#   1. Base case: if the subarray has 0 or 1 elements, it's already sorted — return.
#   2. Pick a random pivot element and swap it to the end.
#   3. Partition: walk through the subarray with a low_boundary pointer.
#       - If the current element <= pivot, swap it to low_boundary and advance low_boundary.
#       - After the loop, swap the pivot (at end) into low_boundary. Everything left of
#         low_boundary is <= pivot, everything right is > pivot.
#   4. Recursively sort the left partition and the right partition.
#


def solve(nums: list[int | float]) -> list[int | float]:
    pass
