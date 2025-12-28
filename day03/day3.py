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

# %%
# set up
from pathlib import Path
from functools import cache
ROOT = Path(__file__).resolve().parent

# %% [markdown]
# ## Day 3
# ### Part 1
# - at this point I will skip the string parsing
# - let's consider each line/number
# - at a particular `digit` in a line 
#     - we want to try and match it with some other digit **to the right** of it to make a 2 digit joltage
#         - (the other direction works as well)
#     - we can choose from any other index `j` where `j > i` to form `x = (nums[i] * 10) + nums[j]`
#     - obviously, we want `nums[j]` to be **as big as possible**
# - we traverse from **right to left** 
#     - (again, inverse direction works too if you decided to flip the logic earlier)
#     - we keep a running variable where at `i`, `max_to_right` is the maximum number we've seen **to the right** (and not including) i 
#     - so when trying to create `x` using `i`, we will do `x = (nums[i] * 10) + max_to_right`
#     - compare this with the global max 
#     - after we are done, we should update `max_to_right` to include `i` so that it can be used by `i - 1`
# %%
def part1(input_path):
    # set up 
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]

    # actual code
    res = 0
    for line in lines:
        max_to_right = int(line[-1])
        max_joltage = 0
        for char in line[-2::-1]:
            joltage = int(char)
            total_joltage = joltage * 10 + max_to_right
            max_joltage = max(max_joltage, total_joltage)
            max_to_right = max(max_to_right, joltage)
        res += max_joltage
    return res 

print("Total max joltage in part 1 is", part1("input.txt"))

# %% [markdown]
# ### Part 2
# - again, we process each individual each line, let's call the number/string formed by the line to be `num_str`
# - we can write a helper function `get_max_voltage` to find the max voltage we can make from that `num_str`
# - `get_max_voltage` will call a `dfs` helper 
#     - `get_max_voltage` is essentially just the driver code for the DFS
# - `dfs`
#     - commentary 
#         - pretty classic maximum subsequence problem, we can do knapsack aka take vs not take 
#     - parameters:
#         - `i`: the current index within `num_str`
#         - `digits_left`: the number of digits remaining that we have to take 
#     - base case: there are a couple of base case to consider (their order matters)
#         - if `n - i < digits_left`
#             - this means that even if we take every single remaining digit within `nums_str`, we would reach the length 12 required to form a joltage
#             - so this is actually an invalid scenario, we don't want to consider it 
#             - the classic thing to do in these scenario is to return a very small number that our algo will disregard &rightarrow; -1 does the trick since all digits are positive
#         - if `digits_left == 0`
#             - there's nothing else to take, so we don't have to exlpain anymore, just return 0
#         - if `i == n`
#             - being here means that we've reached the end of `num_str` but haven't taken 12 digits yet (else we would have ended up in the other case)
#             - so again, invalid case, return -1
#     - recursive case: we have 2 choices 
#         - don't take the current digit
#             - we do nothing, just call `dfs(i + 1, digits_left)`
#         - take the current digit (it's a little more involved)
#             - call `dfs(i + 1, digits_left - 1)` (because we've this digit, we have 1 less digit to take)
#             - this recursive call we return some number, we need to prepend our current digit to this result 
#                 - ex. if `curr_digit = 9` and `dfs(i + 1, digits_left - 1) = 314`, our result is `9314`
#             - so to do this we need to "fluff" `curr_digit` with 0s, the number of 0s needed is `digits_left - 1`
#             - so the resulting number $x = \text{curr\_digit} + 10^{\text{digits\_left}-1}$
#         - return the maximum of these 2 options 
#     - analysis: the DFS code is actually quite efficient if you apply caching 
#         - if you cache, `time complexity == space complexity == search space` which is $O(n \times 12) = O(n)$
# - call `get_max_voltage` for each line and add them up 

# %%
def part2(input_path):
    # set up 
    with open(ROOT / input_path) as f: 
        pass 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    res = 0
    for line in lines:
        joltage = get_max_voltage(line)
        res += joltage
    return res

def get_max_voltage(num_str):
    n = len(num_str)
    powers = {i: 10**i for i in range(12)}
    @cache 
    def dfs(i, digits_left):
        if n - i < digits_left: return -1 # we can't take exactly 12 
        if digits_left == 0: return 0 
        if i == n: return -1 # reached the end but haven't taken all 12

        curr_digit = int(num_str[i])
        take = (curr_digit * powers[digits_left-1]) + dfs(i + 1, digits_left - 1)
        not_take = dfs(i + 1, digits_left)
        return max(take, not_take)

    return dfs(0, 12)

print("Total max joltage in part 2 is", part2("input.txt"))
