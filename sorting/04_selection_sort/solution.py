def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    selection_sort(sorted_vals)
    return sorted_vals


def selection_sort(nums):
    for i in range(len(nums) - 1):
        min_idx = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[min_idx]:
                min_idx = j
        nums[i], nums[min_idx] = nums[min_idx], nums[i]
