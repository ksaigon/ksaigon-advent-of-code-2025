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
import operator
ROOT = Path(__file__).resolve().parent

# %% [markdown]
# ## Day 6
# ### Part 1
# - for this question, the string parsing was the hardest part
# - essentially, you had to split the lines by `"\n"`, and then you had to strip the numbers so that there's no white space in each number
# - but after that, the math is fairly straightforward
#     - imagine that you're given a `grid` version of the input, where grid[row][col] is a number 
#     - we traverse **column wise** which is not usual 
#     - for each column `col`, we get the op (which is `grid[last_row][col]`), then collect all the numbers from `grid[row][col]` for `1 <= row < m`
#     - we apply the `op` to all the numbers and add it to the global sum 
# %%
def part1(input_path):
    # the heavy lifting 
    with open(ROOT / input_path) as f: 
        input = f.read()
    grid = [[x for x in line.split()] for line in input.splitlines() if line.strip()]
    return do_cephalopods_hw(grid)
    
def do_cephalopods_hw(grid):
    m, n = len(grid), len(grid[0])
    op_map = {"+": operator.add, "*": operator.mul}
    total_ans = 0
    for col in range(n):
        op = op_map[grid[-1][col]]
        col_ans = int(grid[0][col])
        for row in range(1, m-1):
            col_ans = op(col_ans, int(grid[row][col]))
        total_ans += col_ans
    return total_ans

print(f"The total answer of the cephalopods math homework in part 1 is {part1("input.txt")}")

# %% [markdown]
# ### Part 2
# - the parsing for this was significantly more annoying 
# - essentially, you know that you've hit a deliminator `col` when `grid[row][col] == " "` for all `0 <= row < m`
#     - from the question: "Problems are still separated with a column consisting only of spaces"
#     - so we keep a variable `last_stop` which is the last deliminator column
#         - (initialized to `-1`)
#     - when we find the next deliminator column, the number can be found by `lines[row][last_stop -> col]` for each `row` that's not the op
#         - we can collect all the numbers and the op, then use a helper `compute_question`
#         - sum up the result from `compute_question`
#         - then we can update `last_stop` to be `col`
# - `compute_question`: given a list of number string `nums_str` and an operator string `op_str`
#     - again, we traverse column wise, going **right to left**
#     - we then try to create each number by going top to bottom, each collecting each digit and appending it to the end of the `curr_num`
#         - edge case: for some reason, empty spaces count as nothing and not 0, so we just ignore white space 
#     - once you've collected all your numbers, you can apply the op to them, and return this sum
# %%
def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = input.splitlines()
    return do_cephalopods_hw_proper(lines)

def do_cephalopods_hw_proper(lines):
    lines = [line + " " for line in lines] # add sentinel value
    m, n = len(lines), len(lines[0])
    total_ans = 0
    last_stop = -1
    for col in range(n):
        if all(lines[row][col] == " " for row in range(m)):
            op_str = lines[-1][last_stop+1]
            nums_str = [lines[row][last_stop+1:col] for row in range(m-1)]
            col_ans = compute_question(nums_str, op_str)
            total_ans += col_ans
            last_stop = col
    return total_ans

def compute_question(nums_str, op_str):
    op_map = {"+": operator.add, "*": operator.mul}
    op = op_map[op_str]
    m = len(nums_str)
    n = max([len(num_str) for num_str in nums_str])
    ans = 1 if op_str == "*" else 0

    for col in range(n):
        curr_num = 0
        for row in range(m):
            # EMPTY SPACES ARE NOT 0
            if nums_str[row][col] == " ": continue
            digit = int(nums_str[row][col])
            curr_num = curr_num * 10 + digit 
        ans = op(ans, curr_num)
    return ans

print(f"The proper answer of the cephalopods math homework in part 2 is {part2("input.txt")}")
