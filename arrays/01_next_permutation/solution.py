def solve(nums):
    result = nums[:]

    # Step 1: find largest i where result[i] < result[i+1]
    i = len(result) - 2
    while i >= 0 and result[i] >= result[i + 1]:
        i -= 1

    if i >= 0:
        # Step 2: find first larger value than nums[i] from the right
        j = len(result) - 1
        while result[j] <= result[i]:
            j -= 1
        # Step 3: swap
        result[i], result[j] = result[j], result[i]

    # Step 4: reverse suffix starting at i+1
    result[i + 1 :] = result[i + 1 :][::-1]

    return result
