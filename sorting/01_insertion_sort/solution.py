def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    insertion_sort(sorted_vals)
    return sorted_vals


def insertion_sort(nums):
    # i have :i sorted elements, i need to sort ith
    for i in range(1, len(nums)):
        val = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > val:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = val
