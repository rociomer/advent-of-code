# --- Day 3: Crossed Wires ---


def get_path(path : list) -> list:
    """Given an input wire path, outputs a list of all the coordinates that the wire
    passes over (excluding the origin).
    """
    x, y = 0, 0  # start at the origin

    path_coordinates = []  # we will use this list to keep track of visited coordinates
    for instruction in path:

        target_coord = int(instruction[1:])

        if instruction[0] == "R":
            for x_coord in range(x + 1, x + target_coord + 1):
                path_coordinates.append((x_coord, y))
            x += target_coord  # update the state
        elif instruction[0] == "U":
            for y_coord in range(y + 1, y + target_coord + 1):
                path_coordinates.append((x, y_coord))
            y += target_coord  # update the state
        elif instruction[0] == "L":
            for x_coord in range(x - 1, x - target_coord - 1, -1):
                path_coordinates.append((x_coord, y))
            x -= target_coord  # update the state
        elif instruction[0] == "D":
            for y_coord in range(y - 1, y - target_coord - 1, -1):
                path_coordinates.append((x, y_coord))
            y -= target_coord  # update the state

    return path_coordinates


def main():
    with open("input", "r") as input_data:
        # read entries; each entry is separated by a comma
        wire_paths = input_data.read().split("\n")[:-1]

        wire_paths_split = []
        for path in wire_paths:
            split_path = path.split(",")
            wire_paths_split.append(split_path)

    # trace out the paths for each wire, and take the set (we don't need the path in order for this)
    wire_1_path_coordinates = set(get_path(path=wire_paths_split[0]))
    wire_2_path_coordinates = set(get_path(path=wire_paths_split[1]))

    # find the points where the two wires intersect, and calculate the Manhattan distance to the origin
    manhattan_distances = []
    for coordinates in wire_1_path_coordinates:
        if coordinates in wire_2_path_coordinates:  # wires intersect here
            manhattan_distances.append(abs(coordinates[0]) + abs(coordinates[1]))

    # the answer to the puzzle is the minimum Manhattan distance to any intersection
    # point (excluding the origin)
    answer = min(manhattan_distances)

    print("Answer:", answer)


if __name__ == "__main__":
    main()
