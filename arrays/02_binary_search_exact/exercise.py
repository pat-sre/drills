# Implement binary search (exact match).
#
# Given a sorted list of integers and a target value, return the index of the
# target if found, or -1 if not present.
#
# Examples:
#   ([1, 3, 5, 7, 9], 5) -> 2
#   ([1, 3, 5, 7, 9], 4) -> -1
#   ([], 1)              -> -1
#
# Template (invariant: if target exists, it's in nums[left..right] inclusive):
#   while left <= right:
#       mid = (left + right) // 2
#       if nums[mid] == target: return mid
#       elif nums[mid] < target: left = mid + 1
#       else: right = mid - 1
#   return -1


def solve(nums: list[int], target: int) -> int:
    pass
