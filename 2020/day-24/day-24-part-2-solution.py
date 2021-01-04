# --- Day 24: Lobby Layout ---
from copy import deepcopy
from typing import Tuple


def parse_tile_flips(flipping_instructions : list) -> list:
    """Parses the input tile flipping instructions, converting them from a list of
    strings to a list of integers, where integers are used to denote the tiles as
    folows: 0:e, 1:se, 2:sw, 3:w, 4:nw 5:ne
    """
    flipping_instructions_int = []
    for instructions in flipping_instructions:
        instructions = instructions.replace("se", "1")
        instructions = instructions.replace("sw", "2")
        instructions = instructions.replace("nw", "4")
        instructions = instructions.replace("ne", "5")
        instructions = instructions.replace("e", "0")
        instructions = instructions.replace("w", "3")
        flipping_instructions_int.append([int(i) for i in instructions])

    return flipping_instructions_int


def which_tile(tile_flip_instruction : list, origin : Tuple[int, int]) -> Tuple[int, int]:
    """Returns the tile indicated in the `tile_flip_instruction`, indicated by
    its coordinates. All instructions start from the same tile e.g. the "origin."
    The grid is oriented as follows, with the origin denoted by (0,0), and corresponds
    to the "directions" illustrated to the right:
                ( 0, 1)                    (N) 5      (E)
        (-1, 1)         ( 1, 0)           4         0
                ( 0, 0)                     ( 0, 0)
        (-1, 0)         ( 1,-1)           3         1
                ( 0,-1)               (W)      2 (S)
    """
    x, y = 0, 0
    for direction in tile_flip_instruction:
        if direction == 0:
            x += 1
        elif direction == 1:
            x += 1
            y -= 1
        elif direction == 2:
            y -= 1
        elif direction == 3:
            x -= 1
        elif direction == 4:
            x -= 1
            y += 1
        elif direction == 5:
            y += 1

    # don't forget to correct for the origin, which is not in fact positioned at
    # (0,0) in the floor layout as it has to be at the center of the list of lists
    origin_x, origin_y = origin
    x, y = origin_x - x, origin_y - y

    return x, y


def initialize_tiles(max_size : int) -> Tuple[list, int, int]:
    """Initializes a hexagonal grid of tiles, all facing the white side.
    The grid is oriented as follows, with the origin denoted by (0,0):
                ( 0, 1)
        (-1, 1)         ( 1, 1)
                ( 0, 0)
        (-1, 0)         ( 1,-1)
                ( 0,-1)
    The value of the `floor_pattern` at each coordinate is the tile's state:
    0: white, 1: black.
    """
    multiplier = max_size*2 + 1

    floor_pattern = []
    for _ in range(multiplier):  # create a list of lists
        floor_pattern.append([0]*multiplier)

    origin = (max_size, max_size)

    return floor_pattern, origin


def flip_tile(tile : Tuple[int, int], layout : list):
    """Flips the indicated tile from black to white, and vice versa, returning
    the updated pattern with the flipped tile.
    """
    x, y = tile
    state = layout[x][y]
    layout[x][y] = int(not state)

    return layout


def update_tiles(layout : list) -> list:
    """Updates the input floor tile pattern according to the following rules:
    1) Any black tile with zero or more than 2 black tiles immediately adjacent
       to it is flipped to white.
    2) Any white tile with exactly 2 black tiles immediately adjacent to it is
       flipped to black.
    """
    updated_layout = deepcopy(layout)  # create a copy

    max_len = len(layout[1:-1]) - 1
    for x, row in enumerate(layout[1:-1]):    # skip the border (it's just padding)
        for y, tile in enumerate(row[1:-1]):  # skip the border

            tile_neighbors = get_adjacent_tiles(layout=layout, tile=(x+1,y+1))
            black_neighbors = sum(tile_neighbors)

            if tile == 1 and (x == 0 or y == 0 or x == max_len or y == max_len):
                raise ValueError("Not enough padding!")
            elif tile == 1:  # if tile is black
                if black_neighbors == 0 or black_neighbors > 2:
                    updated_layout[x+1][y+1] = 0
            else:  # if tile is white
                if black_neighbors == 2:
                    updated_layout[x+1][y+1] = 1

    return updated_layout


def get_adjacent_tiles(layout : list, tile : Tuple[int, int]) -> list:
    """Returns the states of the six tiles adjacent to the input tile, where
    `tile` is the coordinates to the input tile.
    """
    x, y = tile
    adj_tile_0 = layout[x+1][y]
    adj_tile_1 = layout[x+1][y-1]
    adj_tile_2 = layout[x][y-1]
    adj_tile_3 = layout[x-1][y]
    adj_tile_4 = layout[x-1][y+1]
    adj_tile_5 = layout[x][y+1]

    adjacent_tiles = [adj_tile_0, adj_tile_1, adj_tile_2, adj_tile_3, adj_tile_4, adj_tile_5]

    return adjacent_tiles


def main():
    # load data
    with open("input", "r") as input_data:
        tiles_to_flip = input_data.read().split("\n")[:-1]

    # parse the instructions, relabeling the six neighbors in the structions using
    # integers as follows: 0:e, 1:se, 2:sw, 3:w, 4:nw 5:ne
    tile_flipping_instructions = parse_tile_flips(flipping_instructions=tiles_to_flip)
    max_instructions_length = max([len(instruction) for instruction in tile_flipping_instructions]) + 50

    # initially, all tiles start off with the white side facing up, black side facing down
    floor_pattern, origin = initialize_tiles(max_size=max_instructions_length)

    # identify the tile to be flipped for each instruction, and flip it
    for instruction in tile_flipping_instructions:
        tile_to_flip = which_tile(tile_flip_instruction=instruction, origin=origin)
        floor_pattern = flip_tile(tile=tile_to_flip, layout=floor_pattern)

    # now we need to update the floor pattern each day for 100 days, according to
    # the rules of the "live art" exhibit
    for _ in range(100):
        print(_)
        floor_pattern = update_tiles(layout=floor_pattern)

    # the answer to this puzzle is how many tiles are left with the black side up
    # since 0 is white and 1 is black, the answer is simply the sum of `floor_pattern`
    answer = sum([sum(row) for row in floor_pattern])

    print("Answer:", answer)  # 2208 too low


if __name__ == "__main__":
    main()

