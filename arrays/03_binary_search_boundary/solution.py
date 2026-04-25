def solve(nums: list[int], predicate) -> int:
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if predicate(nums[mid]):
            right = mid
        else:
            left = mid + 1
    return left
