from math import sqrt


def compute_roots(nums):
    result = []
    result_append = result.append
    for n in nums:
        result_append(sqrt(n))
    return result


# Test
nums = range(10_000_000)
for n in range(10):
    r = compute_roots(nums)
