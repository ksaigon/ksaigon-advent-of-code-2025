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
from collections import defaultdict, deque
from pathlib import Path
ROOT = Path(__file__).resolve().parent
# %% [markdown]
# ## Day 9
# ### Part 1
# - we can just do brute force here 
#     - that is, look at every possible pair of points, treat them as the corners, and find the area of the rectangle from there
# - this is a **pairwise optimization** problem so there are no tricks to do this in linear time 
#     - bit more detail: the objective is not separable (max x difference and max y difference independently is insufficient)
#     - that is, the best pair can involve non-extreme points in either dimension, small losses in x can be compensated by large gains in y (and vice versa)
# - so just look through all the pairs and find the max area 
# %%
def part1(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    coordinates = [
        [x, y]
        for line in input.splitlines()
        if line.strip()
        for y, x in [map(int, line.split(","))]
    ]
    return largest_rectangle(coordinates)

def largest_rectangle(coordinates):
    res = 0
    for i in range(len(coordinates)):
        for j in range(i+1, len(coordinates)):
            r1, c1 = coordinates[i]
            r2, c2 = coordinates[j]

            w, l = abs(r2 - r1) + 1, abs(c2 - c1) + 1
            res = max(res, w * l)
    return res

print(f"The largest rectangle you can make in part 1 is {part1("input.txt")}")

# %% [markdown]
# ### Part 2
# - there's a brute force solution that you can take a look at in part2_brute_force.py
#     - for the brute force, we essentially create the bounded space of red and green 
#     - and from there, we check every pair, make sure that they're bounded within our boundary, and then take their area if so
#     - this works, just a little slow because you are operating in real unit space, which can be large based on the input 
#     - (i.e. coordinates can be huge (billions), so you cannot build the full grid)
# - the first optimization we can make is to compress the space 
#     - coordinate compression replaces a huge coordinate space with a small grid **that preserves gemetric relationships that matter**
#     - the key insight: nothing interesting happens in the vast empty stretches between polygon edges
#     - so we only keep rows and columns where 
#         - the polygon edges exist
#         - the “inside vs outside” classification can change
#     - so we turn `(r, c)` to `(r_id, c_id)` which are bounded by **the number of unique rows and columns** there are 
#     - key trick: add +- 1 neighbours 
#         - this helps the compressed grid not collapse on itself 
#     - now the compressed grid has:
#         - boundary rows
#         - interior rows
#         - exterior rows
#     - this preserves:
#         - polygon walls
#         - interior space
#         - exterior space
# - we'll write a helper that converts from `coordinate_space -> collapsed_space`, and we can operate in the collapsed space to keep it simple
# - afterwards, we want to fill the interior like the question did but for the compressed space 
#     - we can do this using classic BFS `flood_fill` on the compressed grid 
#     - say that `flood_fill` returns a grid `forbidden_cells[r][c] = 1 if (r, c) is NOT in our bounded space`
#         - this is a little backwards but it works for our purposes
#         - (trick: start the flood fill from the edges)
# - now, let's look at every pair of coordinates
#     - again, we should convert them to the compressed version 
#     - from these, we can make a `row_start, row_end` and `col_start, col_end`
#     - we just need to traverse the area/cells `(r, c)` covered by these points and make sure `forbidden_cell[r][c] == 0` for all of them 
#     - this could take a while, so we can use DP/prefix sum/precomputation to help us 
#     - the check above is essentially asking, is the rectangle sum of the `forbidden_cell` bounded by `row_start, row_end` and `col_start, col_end` equal to 0?
#         - DP can help us get the rectangle sum quite quickly 
#         - do the classic DP rectangle sum algorithm on `forbidden_cell`
#         - now for every pair of points, we have a $O(1)$ way to check if it's bounded correctly or not 
# - with these optimization, we can once again traverse through all the points and consider their area if they're valid
# %%
def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    
    coordinates = [
        [x, y]
        for line in input.splitlines()
        if line.strip()
        for y, x in [map(int, line.split(","))]
    ]

    return largest_rectangle_in_bounds(coordinates)

def largest_rectangle_in_bounds(coordinates):
    '''
    1. compress the space
    2. flood fill
    3. prefix 2D, use that to check if something is in bounds (lowkey DP)
    4. brute force with optimized check
    '''
    def convert_raw_to_id(point):
        r, c = point
        return row_map[r], col_map[c]
    
    coordinates_n = len(coordinates)
    row_map, col_map, rows, cols = compress_coordinates(coordinates)
    m, n = len(rows), len(cols)
    
    walls = set()
    for i in range(1, len(coordinates) + 1):
        # these are ids, not raw coordinates
        pr_id, pc_id = convert_raw_to_id(coordinates[(i-1) % coordinates_n]) # handle wrap
        r_id, c_id = convert_raw_to_id(coordinates[i % coordinates_n])
        
        row_start, row_end = min(pr_id, r_id), max(pr_id, r_id)
        col_start, col_end = min(pc_id, c_id), max(pc_id, c_id)
        for r_id in range(row_start, row_end+1):
            for c_id in range(col_start, col_end+1):
                walls.add((r_id, c_id))
            
    forbidden_cells = flood_fill(m, n, walls)
    prefix = [[0]*(n+1) for _ in range(m+1)]
    for r in range(m):
        for c in range(n):
            prefix[r+1][c+1] = (
                forbidden_cells[r][c]
                + prefix[r][c+1]
                + prefix[r+1][c]
                - prefix[r][c]
            )
    def sum_forbidden(row_start, col_start, row_end, col_end):
        return (
            prefix[row_end+1][col_end+1]
            - prefix[row_start][col_end+1]
            - prefix[row_end+1][col_start]
            + prefix[row_start][col_start]
        )

    res = 0
    for i in range(len(coordinates)):
        for j in range(i+1, len(coordinates)):
            r1_id, c1_id = convert_raw_to_id(coordinates[i])
            r2_id, c2_id = convert_raw_to_id(coordinates[j])

            row_start, row_end = min(r1_id, r2_id), max(r1_id, r2_id)
            col_start, col_end = min(c1_id, c2_id), max(c1_id, c2_id)
            if sum_forbidden(row_start, col_start, row_end, col_end) == 0:
                r1, c1 = coordinates[i]
                r2, c2 = coordinates[j]

                w, l = abs(r2 - r1) + 1, abs(c2 - c1) + 1
                res = max(res, w * l)
    return res

def compress_coordinates(points):
    """
    points: list of (r, c) integer coordinates (polygon vertices)

    returns:
        r_id: dict mapping original row -> compressed index
        c_id: dict mapping original col -> compressed index
        rs: sorted list of compressed row coordinates
        cs: sorted list of compressed col coordinates
    """

    rows = set()
    cols = set()
    for r, c in points:
        # include the coordinate itself
        rows.add(r)
        cols.add(c)

        # include neighbors so cells don't collapse
        rows.add(r - 1)
        rows.add(r + 1)
        cols.add(c - 1)
        cols.add(c + 1)

    rs = sorted(rows)
    cs = sorted(cols)

    r_id = {r: i for i, r in enumerate(rs)}
    c_id = {c: i for i, c in enumerate(cs)}

    return r_id, c_id, rs, cs

def flood_fill(m, n, walls): # this flood fill is a bit backwards
    forbidden_cells = [[0 for _ in range(n)] for _ in range(m)]
    starts = [(r, c) for r in [0, m-1] for c in range(n)] + [(r, c) for r in range(1,m-1) for c in [0,n-1]] # start at the borders
    queue = deque([])
    for row, col in starts:
        queue.append((row,col))
        forbidden_cells[row][col] = 1
    
    while queue:
        row, col = queue.popleft()
        for nrow, ncol in [[row-1,col], [row+1,col], [row,col-1], [row,col+1]]:
            if 0 <= nrow < m and 0 <= ncol < n and forbidden_cells[nrow][ncol] == 0 and (nrow,ncol) not in walls:
                queue.append((nrow,ncol))
                forbidden_cells[nrow][ncol] = 1

    return forbidden_cells
    
print(f"The largest rectangle in bounds you can make in part 2 is {part2("input.txt")}")
