# Implement binary search (boundary / leftmost true).
#
# Given a sorted list and a monotonic predicate (False, False, ..., True, True, ...),
# return the index of the first element where predicate is True.
# If no element satisfies the predicate, return len(nums).
#
# Examples:
#   ([1, 3, 5, 7, 9], lambda x: x >= 5) -> 2
#   ([1, 3, 5, 7, 9], lambda x: x >= 10) -> 5  (len)
#   ([1, 3, 5, 7, 9], lambda x: x >= 0)  -> 0
#
# Template (invariant: answer is in [left, right); predicate is False on [0, left), True on [right, len)):
#   while left < right:
#       mid = (left + right) // 2
#       if predicate(nums[mid]):
#           right = mid       # mid might be the answer, keep in range
#       else:
#           left = mid + 1    # mid is not the answer, discard
#   return left               # left == right, converged on boundary


def solve(nums: list[int], predicate) -> int:
    pass
