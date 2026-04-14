def solve(nums):
    if not nums:
        return nums
    sorted_vals = nums[:]
    heapsort(sorted_vals)
    return sorted_vals


def heapsort(nums):
    n = len(nums)

    # build max-heap: sift down from last parent to root
    for i in range(n // 2 - 1, -1, -1):
        sift_down(nums, n, i)

    # extract max repeatedly
    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(nums, end, 0)


def sift_down(nums, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and nums[left] > nums[largest]:
        largest = left
    if right < n and nums[right] > nums[largest]:
        largest = right

    if largest != i:
        nums[i], nums[largest] = nums[largest], nums[i]
        sift_down(nums, n, largest)
