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
from collections import deque
ROOT = Path(__file__).resolve().parent

# %% [markdown]
# ## Day 7
# ### Part 1
# - pretty standard traversal problem, we can model the grid as a graph and do BFS 
# - find the starting point (i.e where `"S"` is), then kick off BFS from there
# - at a particular `(row, col)`
#     - if `grid[row][col] == "."`:
#         - we continue straight down, the "neighbour" in this case is `(row - 1, col)`
#     - else: (it's a splitter)
#         - increment the number of splits
#         - then you have 2 possible paths you should explore: `(row, col - 1)` and `(row, col + 1)`
#         - these 2 become your neighbours 
#     - for each of the neighbour, check if they're inbound and **if they've been visited**
#         - the question was quite specific: "the two splitters create a total of only three tachyon beams, since they are both dumping tachyons into the same place between them"
#     - if the neighbour is good
#         - add them onto the queue, mark them as visited 
# - at the end return the number of splits

# %%
def part1(input_path):
    # the heavy lifting 
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    return count_split(lines)

def count_split(grid):
    m, n = len(grid), len(grid[0])
    queue, visited = deque([]), set()
    start = find_start(grid)
    visited.add(start)
    queue.append(start)
    
    split_count = 0
    while queue:
        row, col = queue.popleft()
        if grid[row][col] == "^":
            # split 
            next_cells = [[row, col - 1], [row, col + 1]]
            split_count += 1
        else:
            next_cells = [[row + 1, col]]

        for nrow, ncol in next_cells:
            if 0 <= nrow < m and 0 <= ncol < n and (nrow, ncol) not in visited:
                visited.add((nrow,ncol))
                queue.append((nrow,ncol))
    return split_count

def find_start(grid):
    m, n = len(grid), len(grid[0])
    queue, visited = deque([]), set()
    for row in range(m):
        for col in range(n):
            if grid[row][col] == "S": 
                return (row, col)
                visited.add((row,col))
                queue.append((row,col))

print(f"The number of tachyon beam split in part 1 is {part1("input.txt")}")

# %% [markdown]
# ### Part 2
# - this question kinda naturally lens itself to DFS since it has a DP shape 
# - kick off DFS from `start`
# - the DFS function: this function counts the number of timelines starting at the given `(row, col)`
#     - parameters
#         - `row` and `col`: the current position on the grid 
#     - base case 
#         - if `row < 0 or row >= m or col < 0 or col >= n`, we're out of bounds 
#             - meaning we've successfully explored a timeline/path, so this counts, return 1
#     - recursive case 
#         - if it's a normal cell:
#             - the next cell to explore is the one directly below it 
#             the result is just `dfs(row + 1, col)`
#         - it's a splitter cell
#             - there are 2 paths/timelines to explore: `(row, col - 1)` and `(row, col + 1)`
#             - need to explore both so `dfs(row, col - 1)` and `dfs(row, col + 1)`
#             - and since both will create their own timelines, sum up their results
#     - resources: if we cache this, then time complexity = space complexity = search space which is $O(n \times m)$
# - kick off the DFS from start and return the result
# %%
def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    return count_timelines(lines)

def count_timelines(grid):
    m, n = len(grid), len(grid[0])
    
    @cache 
    def dfs(row, col):
        if row < 0 or row >= m or col < 0 or col >= n:
            return 1 # stop moving

        num_timelines = 0
        if grid[row][col] == ".":
            num_timelines = dfs(row + 1, col)
        else:
            num_timelines = dfs(row, col - 1) + dfs(row, col + 1)
        return num_timelines

    srow, scol = find_start(grid)
    return dfs(srow, scol)
    
print(f"The number of timelines in part 2 is {part2("input.txt")}")
