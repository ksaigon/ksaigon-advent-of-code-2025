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
from collections import defaultdict, deque
ROOT = Path(__file__).resolve().parent

# %% [markdown]
# ## Day 4
# ### Part 1
# - we can read in the input file as a grid which will translate cleanly
# - function to pay attention to here is `count_accessible_paper` which takes a grid and traverses it and counts all accessible rolls 
# - pretty standard grid traversal
#     - for each cell `(row, col)`, check all 8 neighbouring cells (don't have to check if the "neighbour" is out of bounds)
#     - count the number of adjacent cells that are also rolls of paper &rightarrow; call this `adjacent_count`
#     - if `adjacent_count` < 4, increase the result counter by 1 as this is reachable 
# - at the end just return the result counter
# %%
def part1(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    # lines here actually form a grid, you can access a cell via lines[row][col]
    return count_accessible_paper(lines)

def count_accessible_paper(grid):
    m, n = len(grid), len(grid[0])
    deltas = [ # viz of the 8 directions
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    res = 0
    for row in range(m):
        for col in range(n):
            if grid[row][col] == ".":
                # it's not a roll, ignore
                continue 
            
            # it's a roll - check adjacent cells (watch for out of bounds)
            adjacent_count = 0
            for drow, dcol in deltas:
                nrow, ncol = row + drow, col + dcol
                if 0 <= nrow < m and 0 <= ncol < n and grid[nrow][ncol] == "@":
                    adjacent_count += 1
            if adjacent_count < 4:
                # this roll is reachable
                res += 1
    return res

print(f"The number of reachable rolls in part 1 is: {part1("input.txt")}")

# %% [markdown]
# ### Part 2
# - could run a basic simulation, but what's the fun in that
#     - if you're interested -- see aside.py
# - instead, we'll run topological sort (or Kahn's algorithm)
# - we can model each cell as a node, and every cell that are adjacent to each other as bidirectional edges 
# - we can do a "peeling" type graph algorithm
#     - where we try to peel away nodes that are "good", see how that affect its neighbours, if its neighbour also turn "good", we process them next
# - "good" here are nodes with out degree `< 4` &rightarrow; i.e. `len(graph[cell]) < 4`
# - top-sort is basically just BFS, so we have a `queue` and a `visited` set
#     - `queue` and `visited` are initialized with nodes that was already good (i.e. accessible in the first traversal)
# - then we process the queue 
#     - for every node, we "remove" it from the graph, thus we go to all its neighbours edge list (set), and remove it from there 
#     - if this removal cause the neighbour to become "good", we add them onto the queue 
#         - the neighbour becoming good here means that `len(graph[neighbour]) < 4` AND `neighbour not in visited` because we don't want to revisit
# - note: topo-sort is A LOT more efficient than the simulation path
# %%
def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [list(line.strip()) for line in input.splitlines() if line.strip()]
    return topological_sort(lines)

def topological_sort(grid):
    graph = defaultdict(set)
    m, n = len(grid), len(grid[0])
    deltas = [ # viz of the 8 directions
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]
    for row in range(m):
        for col in range(n):
            if grid[row][col] == ".":
                # it's not a roll, ignore
                continue 

            # it's a roll - check adjacent cells (watch for out of bounds)
            graph[(row, col)]  # ensure key exists even if degree 0
            for drow, dcol in deltas:
                nrow, ncol = row + drow, col + dcol
                if 0 <= nrow < m and 0 <= ncol < n and grid[nrow][ncol] == "@":
                    graph[(row, col)].add((nrow,ncol))
    
    starts = [cell for cell in graph if len(graph[cell]) < 4]
    queue = deque(starts)
    visited = set(starts)
    res = 0
    while queue:
        row, col = queue.popleft()
        res += 1
        for nrow, ncol in graph[(row,col)]:
            graph[(nrow,ncol)].remove((row,col))
            if len(graph[(nrow,ncol)]) < 4 and (nrow,ncol) not in visited:
                visited.add((nrow,ncol))
                queue.append((nrow,ncol))

    return res
    
print(f"The number of reachable rolls in part 2 is: {part2("input.txt")}")
