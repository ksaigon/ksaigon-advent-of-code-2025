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
# ## Day 1
# ### Part 1
# - holy yap bro get to the point 
# - anyways, the problem is just adding and subtracting, pretty basic string parsing 
# - parsing the instruction as first char is the direction, all remaining char is the number of turns
#     - (edge case: don't just assume the number part is $x$ number of characters, I've been burned on the Ramp interview before)
# - potential tricky part is that we have to handle wrap around &rightarrow; classic use case for mod
#     - so we mod by 100 since that's the wrap around limit
# - after every turn, `+1` if we're at 0

# %%
import os
from pathlib import Path

def count_rotation_at_0_part_1(instructions):
    curr = 50
    MOD = 100
    res = 0
    lines = [line.strip() for line in instructions.splitlines() if line.strip()]
    for instruction in lines:
        direction, count = instruction[0], int(instruction[1:])
        if direction == "R":
            curr = (curr + count) % MOD 
        else:
            curr = (curr - count) % MOD
        if curr == 0:
            res += 1
    return res

# %% [markdown]
# ### Part 2
# - actually a very annoying question, mostly because they have very niche definition of crossing 
# - using `divmod` won't really work because it counts how many times you cross over the boundary, and not the number of times you hit a boundary (minor diff)
# - we can use some basic math to help us outthough
#     - same set up as before, use `curr` to track the wrapped position (so `0 <= curr < 100`)
#     - counting the number of times it takes to hit 0 **the first time**
#         - if `L`: it takes `100 - curr` moves to hit 0 again 
#         - if `R`: it takes `curr` moves to the left to hit 0 again 
#         - edge case: if `curr == 0`, in either direction, it takes a full cycle to hit 0 again (this is what divmod gets wrong I'm pre sure)
#     - after hitting 0 first, the number of times we hit 0 again is the remaining rotations divided by 100
#         - of course this only matters if `count >= rotations_needed_to_hit_0_first`, else we wouldn't even hit the boundary
# - brute force would have worked quite well here as well 

# %%
def count_rotation_at_0_part_2(instructions):
    curr = 50
    MOD = 100
    res = 0

    lines = [line.strip() for line in instructions.splitlines() if line.strip()]
    for instruction in lines:
        direction = instruction[0]
        count = int(instruction[1:])

        # clicks until first time we land on 0
        if direction == "R":
            clicks_to_0 = MOD - curr
            delta = count
        else:  # "L"
            clicks_to_0 = curr
            delta = -count
        if curr == 0:
            # need a fully rotation 
            clicks_to_0 = MOD 

        # after hitting 0, every MOD rotation we hit 0
        if clicks_to_0 <= count:
            res += 1 + (count - clicks_to_0) // MOD

        curr = (curr + delta) % MOD
    
    return res

# %%
# Part 1
ROOT = Path(__file__).resolve().parent
input_path = ROOT / "input.txt"
with open(input_path) as f: 
    input = f.read()

res = count_rotation_at_0_part_1(instructions=input)
print("The password for part 1 is: {}".format(res))

# Part 2 
res = count_rotation_at_0_part_2(instructions=input)
print("The password for part 2 is: {}".format(res))
