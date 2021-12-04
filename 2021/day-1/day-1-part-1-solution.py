# --- Day 1: Sonar Sweep ---

# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    depth_measurements = input_data.read().split("\n")

    # convert to integers
    depth_measurements = [int(i) for i in depth_measurements]

# calculate the number of depth increases
n_increases = 0
prev_num = depth_measurements[0]
for depth in depth_measurements[1:]:
    if depth > prev_num:
        n_increases += 1
    prev_num = depth

# the answer to the puzzle is the number of depth increases
answer = n_increases

print("Answer:", answer)
