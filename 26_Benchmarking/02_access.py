import math


def compute_roots(nums):
    result = []
    for n in nums:
        result.append(math.sqrt(n))
    return result


# Test
nums = range(10_000_000)
for n in range(10):
    r = compute_roots(nums)
