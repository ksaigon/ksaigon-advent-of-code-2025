from collections import defaultdict
from pathlib import Path 
ROOT = Path(__file__).resolve().parent

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
    n = len(coordinates)
    row_intervals = defaultdict(set)
    for i in range(1, len(coordinates) + 1):
        pr, pc = coordinates[(i-1) % n] # handle wrap
        r, c = coordinates[i % n]
        for row in range(min(pr, r), max(pr, r)+1):
                row_intervals[row].update([c, pc])
    for row in row_intervals: row_intervals[row] = sorted(list(row_intervals[row]))

    res = 0
    for i in range(len(coordinates)):
        for j in range(i+1, len(coordinates)):
            r1, c1 = coordinates[i]
            r2, c2 = coordinates[j]
            
            bottom_row, top_row = min(r1, r2), max(r1, r2)
            left_col, right_col = min(c1, c2), max(c1, c2)
            is_valid = True 
            for row in range(bottom_row, top_row + 1):
                if left_col < row_intervals[row][0] or right_col > row_intervals[row][-1]:
                    is_valid = False 
                    break 
            if is_valid:
                area = (top_row - bottom_row + 1) * (right_col - left_col + 1)
                res = max(res, area)
    return res