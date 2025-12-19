# %% [markdown]
# ## Day 1
# ### Part 1
# - we can just solve this using brute force
#     - we can do brute force because we actually need to find the number itself to add them, not just count 
#     - if you're interested in the optimal counting algorithm -- see day2/sidenote.py
# - so firstly, do some string parsing, to get the individual lines and `start` and `end` for each line 
# - then, we can loop through every number `num` from `start` to `end` (inclusive)
#     - converting it to string helps here, so `num_str = str(num)`
#     - if `len(num_str)` is odd, we don't really care about this particular number, because we can't create invalid ids from it 
#     - if it's even, then we it might be possible to create invalid ids
#         - let `k = len(num_str) // 2`
#         - and invalid id will have `num_str[0 to k (non-inclusive)] == num_str[k to end]`
#         - so we can check for this, then add it to `res` if it is invalid
# %%
from pathlib import Path
def part1(input):
    lines = [line.strip() for line in input.split(",") if line.strip()]
    res = 0
    for line in lines:
        start_str, end_str = line.split("-")
        start, end = int(start_str), int(end_str)
        for num in range(start, end+1):
            num_str = str(num)
            n = len(num_str)
            if n % 2:
                # only care about even lengths number
                continue
            if num_str[:n//2] == num_str[n//2:]:
                res += num # literally add up the number, not count them
    return res


def part1_driver():
    ROOT = Path(__file__).resolve().parent

    # with open(ROOT / "example_input.txt") as f: 
    #     example_input = f.read()
    #     part1(example_input)
    
    with open(ROOT / "input.txt") as f: 
        input = f.read()
        print("Sum of all invalid IDs in part 1 is: ", part1(input))

# %% [markdown]
# ### Part 2
# - same string parsing to get each line 
# - again, we loop through all numbers `num` in range `start -> end` (inclusive)
#     - but this time, it's not just about splitting the `num_str` in half to create invalid ID
# - we can think of invalid IDs in terms of a "root" 
#     - a "root" is the part of the number that gets repeated to create the invalid IDs 
#     - ex. `123123` is an invalid ID, with `123` being the root 
#     - so it's required that `len(num_str) is divisible by `len(root)` and `root * x == num_str` (`x >= 2`) for it to be invalid 
# - so at a particular `num_str`, we can try out all possible roots 
#     - ex. `num_str = "123456"`, possible roots are `"1", "12", "123", "1234", ...` 
#         - (though we don't have to try past `len(num_str) // 2` because we don't have enough space to duplicate the root i.e. `x < 2`)
#     - so as soon as we find a root that works, we can add `num` to `res` like before 
#         - IMPORTANT: you need to break right away, a particular number should only be considered invalid once even though it might have multiple roots that work 
#         - ex. `num = 111111`, there are many possible roots here, they can be `1` repeated  6 times, or `11` repeated 3 times, or `111` repeated 3 times, etc 
# %%
def part2(input):
    lines = [line.strip() for line in input.split(",") if line.strip()]
    res = 0
    for line in lines:
        start_str, end_str = line.split("-")
        start, end = int(start_str), int(end_str)
        for num in range(start, end+1):
            num_str = str(num)
            curr = ""
            for char in num_str:
                curr += char 
                div, mod = divmod(len(num_str), len(curr))
                if mod == 0 and div >= 2 and curr * div == num_str:
                    res += num
                    break 
    return res

def part2_driver():
    ROOT = Path(__file__).resolve().parent

    with open(ROOT / "input.txt") as f: 
        input = f.read()
        invalid_sum = part2(input)
        print("Sum of all invalid IDs in part 2 is: ", invalid_sum)

if __name__ == "__main__":
    part1_driver()
    part2_driver()

