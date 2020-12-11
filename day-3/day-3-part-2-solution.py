# --- 3: Toboggan Trajectory ---
# With the toboggan login problems resolved, you set off toward the airport. While travel by toboggan might be easy, it's certainly not safe: there's very minimal steering and the area is covered in trees. You'll need to see which angles will take you near the fewest trees.
# 
# Due to the local geology, trees in this area only grow on exact integer coordinates in a grid. You make a map (your puzzle input) of the open squares (.) and trees (#) you can see. For example:
# 
# ..##.......
# #...#...#..
# .#....#..#.
# ..#.#...#.#
# .#...##..#.
# ..#.##.....
# .#.#.#....#
# .#........#
# #.##...#...
# #...##....#
# .#..#...#.#
# These aren't the only trees, though; due to something you read about once involving arboreal genetics and biome stability, the same pattern repeats to the right many times:
# 
# ..##.........##.........##.........##.........##.........##.......  --->
# #...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
# .#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
# ..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
# .#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
# ..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
# .#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
# .#........#.#........#.#........#.#........#.#........#.#........#
# #.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
# #...##....##...##....##...##....##...##....##...##....##...##....#
# .#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
# You start on the open square (.) in the top-left corner and need to reach the bottom (below the bottom-most row on your map).
# 
# The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers rational numbers); start by counting all the trees you would encounter for the slope right 3, down 1:
# 
# From your starting position at the top-left, check the position that is right 3 and down 1. Then, check the position that is right 3 and down 1 from there, and so on until you go past the bottom of the map.
# 
# The locations you'd check in the above example are marked here with O where there was an open square and X where there was a tree:
# 
# ..##.........##.........##.........##.........##.........##.......  --->
# #..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
# .#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
# ..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
# .#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
# ..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
# .#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
# .#........#.#........X.#........#.#........#.#........#.#........#
# #.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
# #...##....##...##....##...#X....##...##....##...##....##...##....#
# .#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
# In this example, traversing the map using this slope would cause you to encounter 7 trees.
# 
# Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?
#
# --- Part Two ---
# Time to check the rest of the slopes - you need to minimize the probability of a sudden arboreal stop, after all.
# 
# Determine the number of trees you would encounter if, for each of the following slopes, you start at the top-left corner and traverse the map all the way to the bottom:
# 
# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.
# In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s) respectively; multiplied together, these produce the answer 336.
# 
# What do you get if you multiply together the number of trees encountered on each of the listed slopes?

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
