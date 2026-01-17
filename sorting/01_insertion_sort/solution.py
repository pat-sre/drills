def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    insertion_sort(sorted_vals)
    return sorted_vals


def insertion_sort(nums):
    for i in range(1, len(nums)):
        j = i
        val = nums[i]
        while j and nums[j - 1] > val:
            nums[j] = nums[j - 1]
            j -= 1
        nums[j] = val
