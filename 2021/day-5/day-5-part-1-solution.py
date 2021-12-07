# --- Day 5: Hydrothermal Venture ---


# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    raw_input = input_data.read().split("\n")

    # parse the input
    coordinates = [row.split(" -> ") for row in raw_input]

# create a dictionary of the space, where the keys are the coordinates and the
# values are the number of lines that pass through said point
space = {}
for coord_pair in coordinates:
    line_start = [int(i) for i in coord_pair[0].split(",")]
    line_end   = [int(i) for i in coord_pair[1].split(",")]

    if line_start[0] != line_end[0] and line_start[1] != line_end[1]:
        continue  # skip non-horizontal and non-vertical lines

    # determine a correction term to make the ranges below inclusive
    if line_end[0] < line_start[0]:
        step_x = -1
    else:
        step_x = 1

    if line_end[1] < line_start[1]:
        step_y = -1
    else:
        step_y = 1

    for x in range(line_start[0], line_end[0] + step_x, step_x):
        for y in range(line_start[1], line_end[1] + step_y, step_y):
            if (x,y) in space.keys():
                space[(x,y)] = space[(x,y)] + 1
            else:
                space[(x,y)] = 1

# count the number of points where at least two lines overlap
count = len([value for value in space.values() if value != 1])

# the answer to the puzzle is the number of points where at least two lines overlap
answer = count

print("Answer:", answer)
