# --- Day 3: Crossed Wires ---
from typing import Tuple


def get_path(path : list) -> Tuple[list, dict]:
    """Given an input wire path, outputs a list of all the coordinates that the wire
    passes over (excluding the origin), as well as a dict with the number of steps 
    the wire has traveled in its path up till that point. If a wire has visited
    a given point multiple times, the dictionary will only keep track of the 
    number of steps from the first time it visited that point.
    """
    x, y = 0, 0  # start at the origin

    path_coordinates = []  # we will use this list to keep track of visited coordinates
    steps = {}             # we will use this dictionary to keep track of the number of steps
    n_steps = 0
    for instruction in path:

        target_coord = int(instruction[1:])

        if instruction[0] == "R":
            for x_coord in range(x + 1, x + target_coord + 1):
                n_steps += 1
                path_coordinates.append((x_coord, y))
                if (x_coord, y) not in steps.keys():
                    steps[(x_coord, y)] = n_steps
            x += target_coord  # update the state
        elif instruction[0] == "U":
            for y_coord in range(y + 1, y + target_coord + 1):
                n_steps += 1
                path_coordinates.append((x, y_coord))
                if (x, y_coord) not in steps.keys():
                    steps[(x, y_coord)] = n_steps
            y += target_coord  # update the state
        elif instruction[0] == "L":
            for x_coord in range(x - 1, x - target_coord - 1, -1):
                n_steps += 1
                path_coordinates.append((x_coord, y))
                if (x_coord, y) not in steps.keys():
                    steps[(x_coord, y)] = n_steps
            x -= target_coord  # update the state
        elif instruction[0] == "D":
            for y_coord in range(y - 1, y - target_coord - 1, -1):
                n_steps += 1
                path_coordinates.append((x, y_coord))
                if (x, y_coord) not in steps.keys():
                    steps[(x, y_coord)] = n_steps
            y -= target_coord  # update the state

    return path_coordinates, steps


def main():
    with open("input", "r") as input_data:
        # read entries; each entry is separated by a comma
        wire_paths = input_data.read().split("\n")[:-1]

        wire_paths_split = []
        for path in wire_paths:
            split_path = path.split(",")
            wire_paths_split.append(split_path)

    # trace out the paths for each wire and get the number of steps taken to each point
    wire_1_path_coordinates, wire_1_steps = get_path(path=wire_paths_split[0])
    wire_2_path_coordinates, wire_2_steps = get_path(path=wire_paths_split[1])

    # take the set of the coordinates (we don't care about the order)
    wire_1_path_coordinates = set(wire_1_path_coordinates)
    wire_2_path_coordinates = set(wire_2_path_coordinates)

    # find the points where the two wires intersect
    n_combined_steps = []
    for coordinates in wire_1_path_coordinates:
        if coordinates in wire_2_path_coordinates:  # wires intersect here
            n_combined_steps.append(wire_1_steps[coordinates] + wire_2_steps[coordinates])

    # the answer to the puzzle is the fewest combined steps the wires must take 
    # to reach an intersection
    answer = min(n_combined_steps)

    print("Answer:", answer)


if __name__ == "__main__":
    main()
