# --- 3: Toboggan Trajectory ---


with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    tree_map = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

n_trees_encountered = 0
n_right_steps = 0
for line in tree_map:

    # get the idx for the square where currently standing
    idx = n_right_steps % len(line)  # correct by 1 because it is an index

    # get the square that this corresponds to on the line, if contains a tree, add 1
    map_square = line[idx]
    n_trees_encountered += map_square.count("#")
    
    # shift over 3 steps
    n_right_steps += 3

print("Answer:", n_trees_encountered)
