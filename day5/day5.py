# %% 
# set up
from pathlib import Path
from bisect import bisect_left
ROOT = Path(__file__).resolve().parent

# %% [markdown]
# ## Day 4
# ### Part 1
# - from the look of the question, we can guess that it's an interval question 
#     - the ranges naturally form intervals, and we're trying to query if an ID falls within these intervals
# - so first, we should create these intervals 
#     - since the question mentioned that the intervals can overlap, that's not really good for us (hard to reason about) &rightarrow; we should merge them
#     - merging intervals require sorting them first, so sort by start time, and then merge 
#     - idea of merging interval: process interval in order by start time, if start <= last_seen_end, we need to merge these 2 intervals
# - once you've merged the interval, just need to handle the look up portion for each ID
#     - we can do a traversal through the intervals to check
#     - but since the intervals are sorted from our last step &rightarrow; we can instead do **binary search**
# - binary search 
#     - we should search for **the largest start time that's smaller than target ID**
#     - `bisect_left(arr, x)`` -> index of the first element ``>= x`, so largest number `< x` is `bisect_left(arr, x) - 1`
#     - let `insertion_index` be the result of the binary search 
#     - if `insertion_index == 0`, this means that every start time is greater than the target ID, the fruit is for sure spoiled
#     - if not the index we care about is at `insertion_index - 1`
#         - we just have to check here that the ID falls between the range at `insertion_index - 1`
#         - if it's does, our fruit is fresh
# %%
def part1(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    
    part1, part2 = input.strip().split("\n\n")
    fresh_ingredient_ranges = [line.strip() for line in part1.splitlines() if line.strip()]
    fresh_ingredient_list = [line.strip() for line in part2.splitlines() if line.strip()]
    return count_fresh_ingredients(fresh_ingredient_ranges, fresh_ingredient_list)

def count_fresh_ingredients(fresh_ingredient_ranges, fresh_ingredient_list):
    intervals = create_intervals(fresh_ingredient_ranges)
    fresh_count = 0
    for ingredient_id in fresh_ingredient_list:
        ingredient_id = int(ingredient_id)
        # bisect_left(arr, x) -> index of the first element >= x, so largest number < x is bisect_left(arr, x) - 1
        insertion_idx = bisect_left(intervals, [ingredient_id,])
        if not insertion_idx: # for sure spoiled
            continue
        if intervals[insertion_idx - 1][0] <= ingredient_id <= intervals[insertion_idx - 1][1]:
            fresh_count += 1
    return fresh_count

def create_intervals(ranges):
    unmerged_intervals = []
    for range_str in ranges:
        start, end = range_str.split("-")
        unmerged_intervals.append((int(start), int(end)))
    unmerged_intervals.sort()
    
    # merge the intervals 
    intervals = []
    for start, end in unmerged_intervals:
        if not intervals or start > intervals[-1][1]:
            intervals.append([start, end])
        else:
            intervals[-1][1] = max(intervals[-1][1], end)
    return intervals
        
print(f"The number of available fresh ingredient in part 1 is: {part1("input.txt")}")

# %% [markdown]
# ### Part 2
# - part 2 interestingly is easier than part 1
# - again, we can apply our same interval logic above, create those intervals 
# - this question is basically just asking for the total number of space that those intervals cover 
#     - so it's just the sum of the length of each interval
# %% 
def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    
    part1, _ = input.strip().split("\n\n")
    fresh_ingredient_ranges = [line.strip() for line in part1.splitlines() if line.strip()]
    return sum_intervals(fresh_ingredient_ranges)

def sum_intervals(fresh_ingredient_ranges):
    intervals = create_intervals(fresh_ingredient_ranges)
    res = 0
    for start, end in intervals:
        res += (end - start + 1)
    return res

print(f"The number of fresh ingredient in database in part 2 is: {part2("input.txt")}")