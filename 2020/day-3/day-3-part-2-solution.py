# --- 3: Toboggan Trajectory ---


def traverse_map(tree_map, steps_right, steps_down):
    n_trees_encountered = 0
    n_right_steps = 0
    line_idx = 0
    while line_idx < len(tree_map):

        # get the current line in the tree map
        line =tree_map[line_idx]

        # get the idx for the square where currently standing
        idx = n_right_steps % len(line)  # correct by 1 because it is an index
    
        # get the square that this corresponds to on the line, if contains a tree, add 1
        map_square = line[idx]
        n_trees_encountered += map_square.count("#")
        
        # shift over `steps_right`
        n_right_steps += steps_right

        # shift down `steps_down`
        line_idx += steps_down
    
    return n_trees_encountered


# first read the data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    tree_map = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

# then compute the number of trees traversed for each case:
# Right 1, down 1.
case_1 = traverse_map(tree_map=tree_map, steps_right=1, steps_down=1)

# Right 3, down 1.
case_2 = traverse_map(tree_map=tree_map, steps_right=3, steps_down=1)

# Right 5, down 1.
case_3 = traverse_map(tree_map=tree_map, steps_right=5, steps_down=1)

# Right 7, down 1.
case_4 = traverse_map(tree_map=tree_map, steps_right=7, steps_down=1)

# Right 1, down 2.
case_5 = traverse_map(tree_map=tree_map, steps_right=1, steps_down=2)

# compute the product of the number of trees traversed in each case
product = case_1 * case_2 * case_3 * case_4 * case_5

print("Answer:", product)
