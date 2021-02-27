# --- Day 10: Monitoring Station ---
from typing import Tuple
from operator import itemgetter
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


def get_asteroid_vaporization_order(monitoring_station : Tuple[int, int], coordinates : list) -> list:
    """Returns the order in which the asteroids will be destroyed, given that the
    laser starts shooting "up" from the monitoring station and moves clockwise.
    """
    x_ref, y_ref = monitoring_station

    # make all positions now relative to the monitoring station
    # we do this in a way that makes right and up positive on the x and y axes
    asteroids_relative_positions = [(x-x_ref, y_ref-y) for x, y in coordinates]
    asteroids_relative_positions.remove((0, 0))

    # redefine all relative positions as a tuple of angle and distance to the origin,
    # with straight up being 0 degrees
    asteroids_polar_coordinates = [get_polar_coordinates(x, y) for x, y in asteroids_relative_positions]

    # sort by the bond angles, then by the distances
    asteroids_polar_coordinates.sort(key=itemgetter(0, 1))

    # now just loop over the angles
    angle_prev = None
    asteroid_vaporization_order = []
    from copy import deepcopy
    while len(asteroids_polar_coordinates):
        # do a clockwise vaporization
        for angle, distance in asteroids_polar_coordinates:
            if angle != angle_prev:
                asteroid_vaporization_order.append((angle, distance))
                angle_prev = angle
        for vaporized_asteroid in asteroid_vaporization_order:
            try:
                asteroids_polar_coordinates.remove(vaporized_asteroid)
            except:
                pass
        angle_prev = None  # reset

    return asteroid_vaporization_order


def get_polar_coordinates(x : int, y : int) -> Tuple[float, float]:
    """Returns (x, y) in polar coordinates.
    """
    def _get_angle(x : int, y : int) -> float:
        """Gets the angle between a straight line up from the origin, and a line
        drawn from the origin to (x, y). The origin is at (0, 0). The angle is
        defined as 0 for a line going straight up, and increasing going clockwise.
        """
        angle = math.atan2(y, x)  # math.atan2() output is between -pi and pi

        # the lines below are to shift the angle so that it ranges from 0 to 2pi,
        # and that 0 is defined as the angle for a line going straight up
        angle -= math.pi/2
        angle *= -1
        if angle < 0:
            angle += 2* math.pi
        if angle == -0:
            angle = 0
        return angle

    def _get_distance(x : int, y : int) -> float:
        """Gets the distance from the origin to (x, y). The origin is at (0, 0).
        """
        distance = math.sqrt(x**2 + y**2)
        return distance

    angle = _get_angle(x, y)
    distance = _get_distance(x, y)

    return (angle, distance)


def get_cartesian_coordinates(angle : float, distance : float, origin : Tuple[int, int]=(0,0)) -> Tuple[int, int]:
    """Returns (angle, distance) in Cartesian coordinates. As we know
    all the original coordinates were integers, this is accounted for
    before returning.
    """
    angle *= -1
    angle += math.pi/2
    x = origin[0] + distance * math.cos(angle)
    y = origin[1] - distance * math.sin(angle)
    return (math.ceil(x-0.5), math.ceil(y-0.5))


def main():
    with open("input", "r") as input_data:
        # load the asteroid map
        asteroid_map = input_data.read().split("\n")[:-1]

    # get the asteroid coordinates
    asteroid_coordinates = get_asteroid_coordinates(asteroid_map=asteroid_map)

    # determine the best asteroid on which to build a new monitoring station, and
    # how many asteroids can be detected from that position
    best_position, n_asteroids = find_best_position(coordinates=asteroid_coordinates)

    # determine the order in which asteroids will be vaporized
    asteroid_vaporization_order = get_asteroid_vaporization_order(monitoring_station=best_position,
                                                                  coordinates=asteroid_coordinates)

    # we need the coordinates of the 200th asteroid to be vaporized
    angle, distance = asteroid_vaporization_order[199]
    x, y = get_cartesian_coordinates(angle, distance, origin=best_position)

    # the answer to the puzzle is the following:
    answer = x * 100 + y

    print("Answer:", answer)


if __name__ == "__main__":
    main()
