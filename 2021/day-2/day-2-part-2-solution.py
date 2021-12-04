# --- Day 2: Dive! ---

# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    navigation_instructions = input_data.read().split("\n")

horizontal_position = 0
depth_position      = 0
aim_position        = 0

# update the position based on the instructions
for instruction in navigation_instructions:
    if "forward" in instruction:
        horizontal_position += int(instruction[8:])
        depth_position      += aim_position * int(instruction[8:])
    elif "down" in instruction:
        aim_position += int(instruction[5:])
    elif "up" in instruction:
        aim_position -= int(instruction[3:])

# the answer to the puzzle is the product of the final horizontal position and depth
answer = depth_position * horizontal_position

print("Answer:", answer)
