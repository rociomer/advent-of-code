# --- Day 10: Monitoring Station ---
from typing import Tuple
import math


def reduce_asteroid_positions(x : int, y : int) -> Tuple[int, int]:
    """Reduces the asteroid positions using their greatest common divisor.
    """
    try:
        gcd = math.gcd(x, y)  # the greatest common divisor
        return x//gcd, y//gcd
    except ZeroDivisionError:  # only occurs when both x and y are 0 (i.e. for the relative origin)
        return 0, 0


def get_asteroid_coordinates(asteroid_map : list) -> list:
    """Returns the asteroid coordinates in the input map.
    """
    asteroid_coordinates = []
    for y, map_row in enumerate(asteroid_map):
        for x, position in enumerate(map_row):
            if position == "#":
                asteroid_coordinates.append((x, y))
    return asteroid_coordinates


def find_best_position(coordinates : list) -> Tuple[tuple, int]:
    """Finds the best asteroid on which to build a monitoring station, based on
    how many asteroids can be detected from that position using a direct line of sight.
    """
    max_asteroids_detected = 0
    best_position = (0, 0)  # placeholder

    # loop over all the asteroid coordinates
    for x_ref, y_ref in coordinates:

        # make all positions now relative to `asteroid_ref`
        asteroids_relative_positions = [(x-x_ref, y-y_ref) for x, y in coordinates]

        # redefine all relative positions in terms of their lowest common multiple
        asteroids_reduced_positions = [reduce_asteroid_positions(x, y) for x, y in asteroids_relative_positions]

        # the number of asteroids detected should be the set of the reduced positions
        n_asteroids = len(set(asteroids_reduced_positions)) - 1  # don't forget to subtract 1 for the origin

        if n_asteroids > max_asteroids_detected:
            max_asteroids_detected = n_asteroids
            best_position = (x_ref, y_ref)

    return best_position, max_asteroids_detected

def main():
    with open("input", "r") as input_data:
        # load the asteroid map
        asteroid_map = input_data.read().split("\n")[:-1]

    # get the asteroid coordinates
    asteroid_coordinates = get_asteroid_coordinates(asteroid_map=asteroid_map)

    # determine the best asteroid on which to build a new monitoring station, and
    # how many asteroids can be detected from that position
    best_position, n_asteroids = find_best_position(coordinates=asteroid_coordinates)

    # the answer to the puzzle is how many asteroids can be detedted from that location
    answer = n_asteroids

    print("Answer:", answer)


if __name__ == "__main__":
    main()
