# Implement merge sort.
#
# Given a list of numbers, return a new sorted list.
# Do not modify the input list.
#
# Algorithm:
#   1. Base case: if the subarray has 0 or 1 elements, it's already sorted — return.
#   2. Split the array in half at the midpoint.
#   3. Recursively sort the left half and the right half.
#   4. Merge the two sorted halves:
#       - Use two pointers, one for each half.
#       - Compare elements at both pointers, place the smaller one into the result,
#         and advance that pointer.
#       - Copy any remaining elements from whichever half isn't exhausted.
#
def solve(nums: list[int | float]) -> list[int | float]:
    if not nums:
        return []
    nums_copy = nums[:]
    pass
