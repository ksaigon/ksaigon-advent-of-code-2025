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
from collections import deque
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np
ROOT = Path(__file__).resolve().parent
# %% [markdown]
# ## Day 10
# ### Part 1
# - the 2 states, on and off, can be easily thought of as **binary digits**
#     - the act of "toggling" can also be recognized as the bitwise XOR operation
# - reduction
#     - we can look at the `light_diagram` as a final binary state that we want to reach 
#     - we start with all light are off, meaning `0b0000` or just `0`
#     - each "move" can be thought of as a **binary mask** i.e. `[0,2,3] = 0b0011` 
# - the problem is now, we have a selection of masks, apply them to get to the final state, we want the minimum number of moves required
#     - to "apply" the mask here is to XOR them 
#     - the nice thing about XOR is that order does not matter, and `a ^ b ^ b = a` so there's naturally a cycle (we can't keep going forever)
#         - as long as we keep track of states well, we don't have to worry about infinite loop 
# - we can do BFS
#     - an entry on the `queue` will have `curr_state` and `move_count` 
#     - if `curr_state == light_digram`
#         - we've reached the end, can return the number of moves this took i.e. `move_count`
#         - because of the nature of BFS, this will be the minimum distance 
#     - we look at all masks that can be applied 
#         - apply `new_mask = curr_mask ^ mask`
#         - add `new_mask` onto the queue if it hasn't been visited before 
# %%
def part1(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    return min_moves_to_turn_on_indicator(lines)

def min_moves_to_turn_on_indicator(lines):
    res = 0
    for line in lines:
        parts = line.split(" ")
        light_diagram, moves = parts[0], parts[1:-1]
        light_diagram_bin, n = parse_light_diagram(light_diagram)
        moves_bin = parse_moves(moves, n)
        res += compute_min_moves(light_diagram_bin, moves_bin)
    return res

def compute_min_moves(light_diagram, moves):
    # given binary representation of the light_diagram, and the move set, compute minimum moves required
    queue = deque([(0, 0)]) # state, move_count
    visited = {0}

    while queue:
        curr_mask, move_count = queue.popleft()
        if curr_mask == light_diagram:
            return move_count

        for move_mask in moves:
            new_mask = curr_mask ^ move_mask
            if new_mask not in visited:
                queue.append((new_mask, move_count + 1))
                visited.add(new_mask)
    return -1

def parse_light_diagram(light_diagram): # turn light diagram string to binary representation
        light_diagram = light_diagram[1:-1] # remove the paratheses and reverse it
        n = len(light_diagram)
        res = 0 # binary representation
        for i in range(len(light_diagram)-1,-1,-1):
            if light_diagram[i] == "#":
                res = res | (1 << (n - i - 1))
        return res, n

def parse_moves(moves, n):
        moves_bin = []
        for move_set in moves:
            move_set = move_set[1:-1] # get rid of brackets 
            indices = [int(idx) for idx in move_set.split(",")]
            move_bin = 0 # binary representation of the moveset
            for idx in indices:
                move_bin = move_bin | (1 << (n - idx - 1))
            moves_bin.append(move_bin)
        return moves_bin
    
print(f"Minimum move to turn on indicator in part 1 is {part1("input.txt")}")

# %% [markdown]
# ### Part 2
# - note: this was hard as fuck 
# - the problem is now no longer in the binary space 
# - instead, it's more of a "coin change" type problem where we have some state that's a tuple, and we can apply a certain move set which will alter this tuple, and we can apply any move any number of time 
#     - again, we can keep track of states and prune 
#     - however, in the worst case, the DFS/BFS appraoch takes $O(\prod{\text{final_state}[i]})$ which in this case is astronomical - will literally take hours
# - so we have to take a mathematical approach
#     - say you have 3 buttons and 4 counters. Each button is a vector showing which counters it increments
#         ```
#         button0 (3)     = [0, 0, 0, 1]  — only increments counter 3
#         button1 (1,3)   = [0, 1, 0, 1]  — increments counters 1 and 3
#         button2 (0,2)   = [1, 0, 1, 0]  — increments counters 0 and 2
#         ```
#     - if you press `button0` $x_0 times, `button1` $x_1$ times, `button2` $x_2$ times, your final state is
#         ```
#         x_0 * [0,0,0,1] + x_1 * [0,1,0,1] + x_2 * [1,0,1,0] = [target]
#         ```
#     - this is just a linear combination of vectors, can be written as 
#         ```
#         A @ x = b
#
#         where:
#             A = button matrix (each column is a button vector)
#             x = [x_0, x_1, x_2, ...] (how many times to press each button)
#             b = target joltages
#         ```
#     - expanded out 
#         ```
#         ┌             ┐   ┌    ┐     ┌   ┐
#         │ 0   0   1   │   │ x₀ │     │ 3 │
#         │ 0   1   0   │ @ │ x₁ │  =  │ 5 │
#         │ 0   0   1   │   │ x₂ │     │ 4 │
#         │ 1   1   0   │   └    ┘     │ 7 │
#         └             ┘              └   ┘
#         ```
#     - we can use linear algebra libraries to solve this quite easily 
#     - you don't just want any solution — you want the one that minimizes x₀ + x₁ + x₂ + ... (total presses), with the constraint that all xᵢ ≥ 0 (can't press negative times) and must be integers
#     - this is exactly what Integer Linear Programming (ILP) solves
# - code walkthrough 
#     - first, we build the $A$ matrix according to `moves`, and then the `b` matrix according to `joltage` (the target)
#     - then we set the objective function `c`
#         - linear programming solvers are designed to minimize (or maximize) a linear function
#         - the standard form is:
#             ```
#             minimize:  c₀x₀ + c₁x₁ + c₂x₂ + ...
#             ```
#             or in vector notation: `minimize c @ x` (dot product of `c` and `x`).
#         - the `c`` vector defines what you're optimizing for, each element `c[i]` is the "cost" or "weight" of variable `x[i]`
#             - since every button cost 1, we set `c = np.ones()`
#         - aside: different c values would optimize for different things
#             ```
#             c = [1, 1, 1, 1]      # minimize total presses (what we want)
#             c = [1, 0, 0, 0]      # minimize only x₀, ignore others
#             c = [1, 2, 1, 1]      # pressing button 1 "costs" twice as much
#             c = [0, 0, 0, 1]      # minimize only x₃
#             ```
#     - the integrality parameter
#         - by default, `milp` treats variables as continuous (can be any real number), the integrality array tells it which variables must be integers
#         - this is an array of the same length as `x`, where:
#             - 0 = continuous (can be 2.5, 3.7, etc.)
#             - 1 = integer (must be 0, 1, 2, 3, ...)
#     - without integrality constraints, the solver might return `x = [2.3, 1.7, 0.5, 3.0]`, which is optimal, but meaningless, because you can't press a button 2.3 times 
#         - you could round, but this might result in suboptimal or not-right answer 
#         - the integrality needs to be baked into the solving process 
#     - putting it all together 
#         - `milp(c, constraints=constraints, bounds=bounds, integrality=integrality)`
#         - this says
#             > "Find values for `x` that satisfy my constraints (`A @ x = b`) and bounds (`x >= 0`), where all `x` values must be integers, and among all such solutions, give me the one that minimizes `c @ x` (the sum of all presses)."
#         - solver returns `result.fun` which is the minimum value of `c @ x`` it found
# %%
def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    res = 0
    for line in lines:
        parts = line.split(" ")
        moves_str, joltage_str = parts[1:-1], parts[-1]
        
        joltage = [int(x) for x in joltage_str.strip("{}").split(",")]
        moves = parse_joltage_moves(moves_str, len(joltage))
        res += compute_min_move_joltage(joltage, moves)
    return res

def compute_min_move_joltage(joltage, moves):
    """
    joltage: target values, e.g. [3, 5, 4, 7]
    moves: list of vectors, e.g. [[0,0,0,1], [0,1,0,1], ...]

    We want to solve:
        A @ x = b
        minimize: sum(x)
        subject to: x >= 0
    """
    num_buttons = len(moves)
    
    # Button matrix (counters × buttons)
    A_eq = np.array(moves).T
    b_eq = np.array(joltage)
    
    # Objective: minimize sum of presses
    c = np.ones(num_buttons)
    
    # Equality constraint: A @ x == b
    constraints = LinearConstraint(A_eq, b_eq, b_eq)
    
    # x >= 0, no upper bound
    bounds = Bounds(lb=0, ub=np.inf)
    
    # All variables must be integers
    integrality = np.ones(num_buttons)  # 1 = integer, 0 = continuous
    
    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
    
    if result.success:
        return int(round(result.fun))
    else:
        return -1
    
def parse_joltage_moves(moves_str, n):
    all_moves = []
    for move_str in moves_str:
        move_str = move_str[1:-1].split(",")
        move = [0] * n
        for i in range(len(move_str)):
            move[int(move_str[i])] = 1
        all_moves.append(move)
    return all_moves

print(f"Minimum move to configure joltage in part 2 is {part2("input.txt")}")
