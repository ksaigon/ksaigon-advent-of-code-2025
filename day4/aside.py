# %% 
# set up
from pathlib import Path
from collections import defaultdict, deque
ROOT = Path(__file__).resolve().parent

# %% [markdown]
# ### Part 2
# - just simulation, the code is very similar to part 1
# - instead, now when we detect an accessible roll, we mark it for removal, and then remove it after 
#     - (I think that you can also remove it as you go, but I wanted to mirror the simluation logic the question had)
#     - we mark cells that are accessible in a set `accessible_rolls`, the size of that is what we return 
# - for the simulation driver code 
#     - we just call `count_accessible_and_remove_paper` until it returns 0, meaning no more cells are accessible, then we stop
# %% 
def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [list(line.strip()) for line in input.splitlines() if line.strip()]
    return simulate(lines)

def simulate(grid):
    def count_accessible_and_remove_paper():
        m, n = len(grid), len(grid[0])
        deltas = [ # viz of the 8 directions
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1),
        ]

        accessible_rolls = set()
        for row in range(m):
            for col in range(n):
                if grid[row][col] == "." or grid[row][col] == "x":
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
                    accessible_rolls.add((row, col))
        
        # remove all accessible rolls
        for row, col in accessible_rolls:
            grid[row][col] = "x"
        return len(accessible_rolls)
    
    res, curr = 0, -1
    while curr:
        curr = count_accessible_and_remove_paper()
        res += curr 
    return res
