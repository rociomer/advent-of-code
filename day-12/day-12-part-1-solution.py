# --- Day 12: Rain Risk ---
# Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!

# Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

# The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:

# Action N means to move north by the given value.
# Action S means to move south by the given value.
# Action E means to move east by the given value.
# Action W means to move west by the given value.
# Action L means to turn left the given number of degrees.
# Action R means to turn right the given number of degrees.
# Action F means to move forward by the given value in the direction the ship is currently facing.
# The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)

# For example:

# F10
# N3
# F7
# R90
# F11
# These instructions would be handled as follows:

# F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
# N3 would move the ship 3 units north to east 10, north 3.
# F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
# R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
# F11 would move the ship 11 units south to east 17, south 8.
# At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.

# Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
from typing import Tuple


def navigate(instruction : str, start_position : Tuple[int, int, str]) -> Tuple[int, int, str]:
    """Applies the navigation instruction and returns the ships new position.
    The three indices in the position indicate the following:
        (E(+)/W(-) position, N(+)/S(-) position, N/E/S/W facing)
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
