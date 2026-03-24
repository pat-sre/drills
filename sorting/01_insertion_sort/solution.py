def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    insertion_sort(sorted_vals)
    return sorted_vals


def insertion_sort(nums):
    # i have :i sorted elements, i need to sort ith
    pass
