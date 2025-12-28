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
from math import prod
import heapq
ROOT = Path(__file__).resolve().parent

class UnionFind():
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.size = [1] * n
        self.components = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return

        # ensure ra is the larger component
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1 # we lost a component (it got merged)
        # optional cleanup: rb is no longer a root
        self.size[rb] = 0

# %% [markdown]
# ## Day 8
# ### Part 1
# - the question is basically talking about **components** of a graph 
#     - each node isits own component at the start, and as you connect them, you're joining the component
#     - these kind of questions lends itself nicely to **UnionFind**
# - so we write a basic Union Find algo and data structure 
#     - we merge by size and not rank this time 
#     - at the end `uf.size` give us the size of all the components
#         - note: to make life easier, the additional cleanup of setting size to 0 for non-root nodes helps us a lot 
#         - at the end, only any non-zero entries in `uf.size` should be considered 
# - need to figure out the order in which to do the connections 
#     - you need to find **all Euclidean distance** in the question 
#     - any box can connect to any other box, so go through all $O(n^2)$ possibilities and calculate their distance 
#     - since we're only interested in the top `k` (in the example it's 10, but in the real question it's 1000), we can keep a k-size heap
#     - at the of this, `distances` (our heap) should have the top `k` closest connection, but sorted backwards, so we need to sort it again 
# - go through the `k` closest distance 
#     - for each `u, v`, make the connection 
# - at the very end, after making all the union operation, check the top 3 largest size in `uf.size`

# %%
def part1(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    coordinates = [list(map(int, line.split(","))) for line in lines]
    return multiply_component(coordinates)

def multiply_component(coordinates):
    distances, k = [], 1000 # distance heap - top 10
    n = len(coordinates)
    for i in range(n):
        x1, y1, z1 = coordinates[i]
        for j in range(i + 1, n):
            x2, y2, z2 = coordinates[j]
            dist = (x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2
            heapq.heappush(distances, (-dist, i, j))
            if len(distances) > k:
                heapq.heappop(distances)

    # a, b, c = min(distances, key=lambda t: -t[0])
    # print(f"pairs: {tuple(coordinates[b]), tuple(coordinates[c])}, dist: {a}")
    distances = sorted([(-dist, i, j) for dist, i, j in distances])
    uf = UnionFind(n)
    for _, u, v in distances:
        uf.union(u, v)
    return prod(sorted(uf.size, reverse=True)[:3])

print(f"The product of the top 3 largest circuit in part 1 is {part1("input.txt")}")

# %% [markdown]
# ### Part 2 
# - very similar to above, except that you don't have to stop at `k` closest connection
# - do the same set up with `UnionFind` and finding `distances`
#     - add a small modification to `UnionFind` which is the `self.component`counter 
#     - `self.component` should start at `n` as we have `n` individial component at the start 
#     - every time we merge 2 components together, we lose a component (since it becomes one)
# - we keep doing the union for every circuit box pair until `uf.component == 1`
#     - this is the first time that everything is connected 
#     - calculate the x-product of the last 2 points, return that 
# %%
def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    coordinates = [list(map(int, line.split(","))) for line in lines]
    return fully_connect_components(coordinates)

def fully_connect_components(coordinates):
    distances = []
    n = len(coordinates)
    for i in range(n):
        x1, y1, z1 = coordinates[i]
        for j in range(i + 1, n):
            x2, y2, z2 = coordinates[j]
            dist = (x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2
            distances.append((dist, i, j))
    distances.sort(reverse=True)

    uf = UnionFind(n)
    last_x_prod = None 
    while uf.components != 1 and distances:
        _, u, v = distances.pop(-1)
        uf.union(u, v)
        last_x_prod = coordinates[u][0] * coordinates[v][0]
    return last_x_prod

print(f"The x-coordinate product of the last 2 connection in part 2 is {part2("input.txt")}")
