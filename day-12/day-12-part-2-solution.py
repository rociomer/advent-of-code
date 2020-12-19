# --- Day 12: Rain Risk ---
from typing import Tuple
import math


def navigate(instruction : str, coordinates : Tuple[int, int, int, int]) -> Tuple[int, int, int]:
    """Applies the navigation instruction and returns the ships new position.
    The three indices in the position indicate the following:
        (N(+)/S(-) ship position, E(+)/W(-) ship position, 
         N(+)/S(-) waypoint position, E(+)/W(-) waypoint position)
    """
    action = instruction[0]
    value = int(instruction[1:])

    # actions which move the ship:
    if action == "F":
        new_position = (coordinates[0] + coordinates[2] * value,
                        coordinates[1] + coordinates[3] * value, 
                        coordinates[2], 
                        coordinates[3])
    # actions which move the waypoint:
    elif action == "N":
        new_position = (coordinates[0], coordinates[1], coordinates[2] + value, coordinates[3])
    elif action == "S":
        new_position = (coordinates[0], coordinates[1], coordinates[2] - value, coordinates[3])
    elif action == "E":
        new_position = (coordinates[0], coordinates[1], coordinates[2], coordinates[3] + value)
    elif action == "W":
        new_position = (coordinates[0], coordinates[1], coordinates[2], coordinates[3] - value)
    else:  # rotate the waypoint
        # rotate the waypoint by `value` degrees around ship using rotation matrix
        # negative `value` --> counterclockwise, positive `value` --> clockwise
        # rotation_matrix = [[math.cos(value), -math.sin(value)],
        #                    [math.sin(value),  math.cos(value)]]
        # note: math.cos() and math.sin() take radians as input
        sign = -1 + 2 * int(action == "R")  # sign is (-) if action is "L" and (+) if action is "R"
        value = sign * value * math.pi / 180  # convert to radians
        x = coordinates[2]  # note: waypoint coordinates are already relative to the ship
        y = coordinates[3]  # note: waypoint coordinates are already relative to the ship
        new_position = (coordinates[0], coordinates[1], math.cos(value) * x - math.sin(value) * y, math.sin(value) * x + math.cos(value) * y)

    return new_position


def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        navigation_instructions = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # loop over the navigation instructions until achieving the final position
    # the first two coordinates are the ship's coordinates, the second two are 
    # the waypoint's coordinates
    current_coordinates =(0, 0, 1, 10)
    for instruction in navigation_instructions:
        updated_coordinates = navigate(instruction=instruction, 
                                       coordinates=current_coordinates)
        current_coordinates = updated_coordinates

    # calculate the Manhattan distance relative to the original position
    manhattan_distance = int(abs(current_coordinates[0]) + abs(current_coordinates[1]) + 0.5)  # int(x + 0.5) rounds x to the nearest integer

    print("Answer:", manhattan_distance)


if __name__ == "__main__":
    main()
