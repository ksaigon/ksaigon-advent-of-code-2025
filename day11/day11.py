# %% 
# set up 
from collections import defaultdict, deque
from pathlib import Path
from helper import is_dag, build_graph, top_sort, count_num_path_between

ROOT = Path(__file__).resolve().parent

# %% [markdown]
# ## Day 11
# ### Part 1
# - this is a classic graph counting path problem 
#     - the input is essentially given to you as a adjacency list 
# - the question is bit simpler **if the graph was acyclic** (aka a DAG)
#     - this is not explicitly stated in the question 
#     - but I wrote a helper method `is_dag` that you can run to check, it so happens that both the example input and real input are DAGs
#     - so we can just use this fact to our advantage
#     - I guess that you could also infer that "Data only ever flows from a device through its outputs; it can't flow backwards" implies a DAG 
#         - but idk seems weak, because this reads like it won't flow directly backwards, but you can still get cycles from other paths
# - this question lends itself nicely to DFS, you can just do 
#     - `res = sum(dfs(neighbour) for neigbhour in graph[node])`) for every `node`
#     - can apply caching
#     - this works nicely because DFS naturally respects the dependency order — you fully explore children before returning to the parent
#         - i.e. the recursion implicitly gives you reverse topological order
# - but I wanted to try it out with BFS 
#     - for this, you'd need to perform the DP step in **reverse-chronological order**
#         - you need to do this so that when you do `dp[neighbour]`, you know that `dp[neighbour]` is already computed 
#     - so you must first run topological sort to get the valid ordering 
#     - counting path 
#         - you start from the back, you mark `dp[dst] = 1`
#         - for every node (going in reverse chronological order), you do `dp[node] = sum(dp[neighbour] for neighbour in graph[node])`
#         - edges case: since we already set `dp[dst] = 1`, ignore when `node == dst`
#         - at the end, return `dp[src]`
# %%
def part1(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    graph, degrees = build_graph(lines)
    return find_num_paths(graph, degrees)

def find_num_paths(graph, degrees):
    ordering = top_sort(graph, degrees)
    return count_num_path_between("you", "out", ordering, graph)

print(f"The number of different paths from `you` to `out` for part 1 is {part1("input.txt")}")

# %% [markdown]
# ### Part 2
# - this question requires breaking it up a bit 
# - key fact: if `X` and `Y` are on the same **path**, then in topological ordering, `X` or `Y` must come first and that is deterministic 
#     - because along a path, you can't visit both at the same time, one must come first
# - once you know this, you can break up the path into "legs" essentially 
#     - you can find number of ways from `src -> X`
#     - then find number of ways from `X -> Y`
#     - then find number of ways from `Y -> dst`
#     - then naturally, since any path from each leg can be match with any other path from another leg &rightarrow; thus you multiply them together 
# %%
def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    graph, degrees = build_graph(lines)
    return find_num_paths_visit_both(graph, degrees)

def find_num_paths_visit_both(graph, degrees):
    ordering = top_sort(graph, degrees)
    nodes_of_interest = ["svr"] + [x for x in ordering if x == "dac" or x == "fft"] + ["out"]
    res = 1
    for start, end in zip(nodes_of_interest, nodes_of_interest[1:]):
        res *= count_num_path_between(start, end, ordering, graph)
    return res

print(f"The number of different paths from `svr` to `out` that touches both `dac` and `fft` for part 2 is {part2("input.txt")}")