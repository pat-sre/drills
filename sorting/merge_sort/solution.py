def sort(nums):
    if not nums:
        return nums
    nums2 = nums[:]
    merge_sort(0, len(nums2) - 1, nums2)
    return nums2


def merge_sort(left, right, nums):
    if left >= right:
        return
    m = (right + left) // 2
    merge_sort(left, m, nums)
    merge_sort(m + 1, right, nums)

    merge(left, m, right, nums)


def merge(start, middle, end, nums):
    larr = nums[start : middle + 1]
    rarr = nums[middle + 1 : end + 1]  # [a, b)
    ptr = start
    left = 0
    right = 0

    while left < len(larr) and right < len(rarr):
        if larr[left] <= rarr[right]:
            nums[ptr] = larr[left]
            left += 1
        else:
            nums[ptr] = rarr[right]
            right += 1
        ptr += 1

    while left < len(larr):
        nums[ptr] = larr[left]
        left += 1
        ptr += 1

    while right < len(rarr):
        nums[ptr] = rarr[right]
        right += 1
        ptr += 1


if __name__ == "__main__":
    if __package__:
        from ..tests import run_tests
    else:
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent.parent))
        from tests import run_tests

    run_tests(sort)
