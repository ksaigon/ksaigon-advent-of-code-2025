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
from helpers import parse_input
from pathlib import Path
ROOT = Path(__file__).resolve().parent

# %% [markdown]
# - this question is super lame 
#     - the question in its purest form is NP-hard (bin packing), the overall solution looks something like 
#         ```python 
#         can_fit(region, remaining_shapes):
#         if remaining_shapes is empty:
#             return True
#         
#         # Pruning: check if remaining area is sufficient
#         if total_cells_needed(remaining_shapes) > empty_cells(region):
#             return False
#         
#         pick a shape from remaining_shapes
#         
#         for each rotation/flip of shape:
#             for each valid position in region:
#                 if shape fits at position without overlap:
#                     place shape
#                     if can_fit(region, remaining_shapes - shape):
#                         return True
#                     remove shape (backtrack)
#         
#         return False
#         ```
#         - this would blow up in complexity with large input, but I think you can still solve this < 3 minutes (which is crazy long)
# - interestingly, for the **real** input, you didn't have to consider the tricky cases at all
#     - i.e. in Example 1 where you had to rotate it properly 
#     - instead, a simple heuristic like `total_area_needed < total_free_area` was good enough 
#     - funny that this shitty solution works on the real input, but not on the example 
#         - so the solution below for all intents and purposes wrong 
# - I think Eric the creator of the calendar ran out of time tbh
#     - this problem required creating custom inputs for everyone, and making custom inputs that has all the edge cases was propably too hard
# - maybe eventually I'll attempt the NP-hard version
# %%
def part1(input_path):
    with open(ROOT / input_path) as f: 
        input = f.read()
    present_info_list, region_info_list = parse_input(input)
    return count_number_that_fits(present_info_list, region_info_list)

def count_number_that_fits(present_info_list, region_info_list):
    can_fit = 0
    for i, region_info in enumerate(region_info_list):
        filled_area = 0    
        for present_id, count in region_info.requirements.items():
            present = present_info_list[present_id]
            filled_area += (present.size * count)
        if filled_area <= region_info.area:
            can_fit += 1
    return can_fit
        
print(f"The number of regions that can fit all the presents are {part1("input.txt")}")
