from pathlib import Path
from collections import deque
ROOT = Path(__file__).resolve().parent

def part2(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    return min_moves_to_configure_joltage(lines)

def min_moves_to_configure_joltage(lines):
    res = 0
    for line in lines:
        parts = line.split(" ")
        moves_str, joltage_str = parts[1:-1], parts[-1]
        
        joltage = [int(x) for x in joltage_str.strip("{}").split(",")]
        moves = parse_joltage_moves(moves_str, len(joltage))
        res += compute_min_move_joltage(joltage, moves)
    return res

def compute_min_move_joltage(joltage, moves):
    n = len(joltage)
    start_state = [0] * n
    queue, visited = deque([(start_state, 0)]), {tuple(start_state)}
    while queue:
        state, move_count = queue.popleft()
        if state == joltage:
            return move_count 
        for move in moves:
            new_state = list(state)
            for i in range(n):
                new_state[i] += move[i]
                if new_state[i] > joltage[i]:
                    new_state = None # say that we can't take it
                    break
            if new_state and tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                queue.append((new_state, move_count + 1))
    return -1 # never possible to reach final state
        
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