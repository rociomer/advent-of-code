# --- Day 1: Sonar Sweep ---

# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    depth_measurements = input_data.read().split("\n")

    # convert to integers
    depth_measurements = [int(i) for i in depth_measurements]

# calculate the sliding window sums
sliding_window_sums = []
for ind, _ in enumerate(depth_measurements[:-2]):
    sliding_window_sums.append(sum(depth_measurements[ind:ind+3]))

# calculate the number of increases in the sliding window
n_increases = 0
prev_num = sliding_window_sums[0]
for depth in sliding_window_sums[1:]:
    if depth > prev_num:
        n_increases += 1
    prev_num = depth

# the answer to the puzzle is the number of increases in the sliding window sums
answer = n_increases

print("Answer:", answer)
