import re 

def parse_input(raw_input):
    blocks = raw_input.split("\n\n") # get individual "blocks"
    present_shapes, dimensions = [], []
    colon_pattern = r'^\d+:\n'
    for block in blocks:
        if re.match(colon_pattern, block):
            block = re.sub(colon_pattern, '', block, count=1)
            present_shapes.append(block)
        else:
            dimensions.extend(block.split("\n"))
    
    present_info_list = [parse_present_shapes(present_shape) for present_shape in present_shapes]
    region_info_list = [parse_dimenion_requirements(dimension) for dimension in dimensions]

    return present_info_list, region_info_list

    
class PresentInfo:
    def __init__(self, grid=[], size=0):
        self.grid = grid 
        self.size = size

def parse_present_shapes(input):
    '''
    Given string of the present shape, return an object PresentInfo that has
    the grid version of the shape, and other metadata like size, etc
    '''

    grid = [list(line) for line in input.split("\n")]
    grid = [[1 if grid[row][col] == "#" else 0 for col in range(3)] for row in range(3)]
    size = input.count("#") # they happen to always be 7 but to be safe
    return PresentInfo(grid, size)

class RegionInfo:
    def __init__(self, w=0, l=0, requirements=None):  # Fix
        self.requirements = requirements if requirements is not None else {}
        self.w = w 
        self.l = l 
        self.area = w * l

def parse_dimenion_requirements(input):
    """
    Given a line of str dimension requirement, convert it to its map form
    Ex. "4x4: 0 0 0 0 2 0" -> RegionInfo(w:4, l:4, requirements: {0:0, 1:0, 2:0, 3:0, 4:2, 5:0})
    """
    parts = input.split(": ")

    # handle w x l first 
    dimension_str = parts[0].split("x")
    w, l = int(dimension_str[0]), int(dimension_str[1])

    # then move on to the requirements
    counts = parts[1].split(" ")
    requirements = {}
    for i, count in enumerate(counts):
        requirements[i] = int(count)
    
    return RegionInfo(w, l, requirements)

