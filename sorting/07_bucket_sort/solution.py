def solve(nums):
    if not nums:
        return []
    n = len(nums)
    buckets = [[] for _ in range(n)]
    for x in nums:
        buckets[int(x * n)].append(x)
    result = []
    for bucket in buckets:
        bucket.sort()
        result.extend(bucket)
    return result
