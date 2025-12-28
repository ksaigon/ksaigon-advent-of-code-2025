# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: py:percent,ipynb
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
# ---

# %% [markdown]
# ## Day 2 Part 1 Sidenote
# - I was looking really hard to find an optimization for part 1
#     - I thought there was some digit DP/math that we can do to not have to loop over all the options
#     - and there is a way an optimized way to **count** how many invalid number there are 
#     - however, the question is asking for the sum of all invalid IDs, meaning you actually need to discover the number and add it to the sum
#         - so brute force is the right way here 
# - but I spent a lot of time looking into the optimized counting version so I'm gonna put it here anyways
# - as a start, for these digit DP problem, it's easier to find the number of invalid numbers starting from 0 -> `num`
#     - so for `count_invalid(start -> end)`, we can instead do `count_invalid(0 -> end) - count_invalid(0 -> start - 1)`
#     - (draw a number line, it'll make sense)
# - so for our function `count_invalid(num)`, we're counting the number of invalid number in the range of `0 -> num`
# - let `n = len(num)` (the number of digits num have)
#     - and we pick a number `x`, `x` can have `L` digits, where `1 <= L <= n` 
#     - we can consider these L cases 
# - if `L < n` 
#     - the digits we pick are not really bounded by the digits of `num` at all 
#     - for example, if `num = 123456`, and `L = 3` &rightarrow; we can pick `x = 999`
#         - because `L < n`, meaning our `x` is a whole digit place smaller we are in risk of exceeding the upper bound 
#         - and hence never bounded by the digits of `num`
#     - if `L` is odd, we can't really even form invalid numbers by definition given
#         - so the number here is just 0 
#     - if `L` is even, we can form invalid numbers 
#         - let `k = L // 2` (so half of `L`)
#         - we can pick these first `k` digits digits freely, and then mirror them 
#         - for example, `num = 123456`, and `L = 4` (so `k = 2`)
#             - we can pick 2 digits to be `99`, and form `x = 9999`
#             - this number is invalid 
#         - for the first digit, you can choose from `1 -> 9` (because no leading 0)
#         - for the remaining `k - 1` digits, you can pick from `0 -> 9`
#         - the math for that is $9 * 10^{k-1}$
#         - so this is the number of valid numbers we can form when `L < n` and `L` is even 
# - if `L == n`
#     - this case is a bit more tricky, but instead of digit DP, we can just do math 
#     - let `h` be the chosen `k` characters (so `len(h) = k`)
#         - i.e. above, `h = 99`, `x = 9999`
#     - mathematically speaking, $x = (h * 10^k) + h$
#     - and since $h \leq n \Longrightarrow (h * 10^k) + h \leq n$ 
#     - after some arithmetic, we get $h \leq \lfloor \dfrac{n}{10^k + 1} \rfloor$
#         - let's call this `Hmax`
#     - so among all `k`-digit `h`, the ones that work are exactly $10^{k-1} \leq h \leq min(10^k - 1, Hmax)$
#     - and the count of that interval is just $\max(0, \min(10^k-1, Hmax) - 10^{k-1} + 1)$

# %%
def count_invalid_upto(n: int) -> int:
    if n <= 0:
        return 0
    s = str(n)
    L = len(s)
    ans = 0

    # shorter even lengths: 2k < L
    for k in range(1, (L // 2) + 1):
        if 2 * k < L:
            ans += 9 * (10 ** (k - 1))

    # same length if L even
    if L % 2 == 0:
        k = L // 2
        lo = 10 ** (k - 1)
        hi = 10 ** k - 1
        max_h = n // (10 ** k + 1)
        ans += max(0, min(hi, max_h) - lo + 1)

    return ans

def count_invalid_in_range(a: int, b: int) -> int:
    return count_invalid_upto(b) - count_invalid_upto(a - 1)
