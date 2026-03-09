def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    insertion_sort(sorted_vals)
    return sorted_vals


def insertion_sort(nums):
    # i have :i sorted elements, i need to sort ith
    for i in range(len(nums)):
        j = i
        # 3 4 5 2
        val = nums[j]
        while j > 0 and nums[j - 1] > val:
            nums[j] = nums[j - 1]
            j -= 1
        nums[j] = val
