# --- Day 12: Rain Risk ---
from typing import Tuple


def navigate(instruction : str, start_position : Tuple[int, int, str]) -> Tuple[int, int, str]:
    """Applies the navigation instruction and returns the ships new position.
    The three indices in the position indicate the following:
        (N(+)/S(-) position, E(+)/W(-) position, N/E/S/W facing)
    """
    action = instruction[0]
    value = int(instruction[1:])

    if action == "F":
        action = start_position[2]

    if action == "N":
        new_position = (start_position[0] + value, start_position[1], start_position[2])
    elif action == "S":
        new_position = (start_position[0] - value, start_position[1], start_position[2])
    elif action == "E":
        new_position = (start_position[0], start_position[1] + value, start_position[2])
    elif action == "W":
        new_position = (start_position[0], start_position[1] - value, start_position[2])
    elif action == "L":
        if value == 90 and start_position[2] == "N":
            new_direction = "W"
        elif value == 90 and start_position[2] == "W":
            new_direction = "S"
        elif value == 90 and start_position[2] == "S":
            new_direction = "E"
        elif value == 90 and start_position[2] == "E":
            new_direction = "N"
        elif value == 180 and start_position[2] == "N":
            new_direction = "S"
        elif value == 180 and start_position[2] == "W":
            new_direction = "E"
        elif value == 180 and start_position[2] == "S":
            new_direction = "N"
        elif value == 180 and start_position[2] == "E":
            new_direction = "W"
        elif value == 270 and start_position[2] == "N":
            new_direction = "E"
        elif value == 270 and start_position[2] == "W":
            new_direction = "N"
        elif value == 270 and start_position[2] == "S":
            new_direction = "W"
        elif value == 270 and start_position[2] == "E":
            new_direction = "S"
        new_position = (start_position[0], start_position[1], new_direction)
    elif action == "R":
        if value == 90 and start_position[2] == "N":
            new_direction = "E"
        elif value == 90 and start_position[2] == "W":
            new_direction = "N"
        elif value == 90 and start_position[2] == "S":
            new_direction = "W"
        elif value == 90 and start_position[2] == "E":
            new_direction = "S"
        elif value == 180 and start_position[2] == "N":
            new_direction = "S"
        elif value == 180 and start_position[2] == "W":
            new_direction = "E"
        elif value == 180 and start_position[2] == "S":
            new_direction = "N"
        elif value == 180 and start_position[2] == "E":
            new_direction = "W"
        elif value == 270 and start_position[2] == "N":
            new_direction = "W"
        elif value == 270 and start_position[2] == "W":
            new_direction = "S"
        elif value == 270 and start_position[2] == "S":
            new_direction = "E"
        elif value == 270 and start_position[2] == "E":
            new_direction = "N"
        new_position = (start_position[0], start_position[1], new_direction)

    return new_position


def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        navigation_instructions = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # loop over the navigation instructions until achieving the final position
    # the first two coordinates are the ship's coordinates, the third is the 
    # direction the ship is facing
    current_position =(0, 0, "E")
    for instruction in navigation_instructions:
        updated_position = navigate(instruction=instruction, 
                                    start_position=current_position)
        current_position = updated_position

    # calculate the Manhattan distance relative to the original position
    manhattan_distance = abs(current_position[0]) + abs(current_position[1])

    print("Answer:", manhattan_distance)


if __name__ == "__main__":
    main()
