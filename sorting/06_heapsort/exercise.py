# Implement heapsort.
#
# Given a list of numbers, return a new sorted list.
# Do not modify the input list.
#
# Algorithm:
#   1. Build a max-heap from the array (start from the last parent and sift down to index 0).
#   2. Repeatedly swap the root (largest element) with the last unsorted element.
#   3. Shrink the heap size by one and sift down the new root to restore the heap property.
#   4. Repeat until the heap size is 1.
#
# sift_down(nums, n, i):
#   Given a heap of size n, sift the element at index i down to its correct position.
#   Compare with children, swap with the largest child if it is greater, and repeat.
#
def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    heapsort(sorted_vals)
    return sorted_vals


def heapsort(nums):
    pass


def sift_down(nums, n, i):
    pass
