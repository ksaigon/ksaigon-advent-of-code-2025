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
from collections import defaultdict

# %%
def top_sort(graph, degrees):
    ordering = [v for v in graph if degrees[v] == 0]
    for node in ordering:
        for neighbour in graph[node]:
            degrees[neighbour] -= 1
            if degrees[neighbour] == 0:
                ordering.append(neighbour)
    return ordering

# %%
def count_num_path_between(src, dst, ordering, graph):
    dp = defaultdict(int) 
    dp[dst] = 1
    for node in reversed(ordering):
        if node != dst:
            dp[node] = sum(dp[neighbour] for neighbour in graph[node])
    return dp[src]

# %%
def build_graph(lines):
    graph = defaultdict(list)
    degrees = defaultdict(int)
    for line in lines:
        node, rest = line.split(": ")
        for neighbour in rest.split(" "):
            graph[node].append(neighbour)
            degrees[neighbour] += 1
    return graph, degrees

# %%
def is_dag(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    
    def dfs(node):
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:  # back edge = cycle
                return False
            if color[neighbor] == WHITE and not dfs(neighbor):
                return False
        color[node] = BLACK
        return True
    
    return all(dfs(node) for node in graph if color[node] == WHITE)
