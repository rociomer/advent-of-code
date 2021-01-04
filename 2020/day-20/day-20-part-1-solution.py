# --- Day 20: Jurassic Jigsaw ---
from typing import Tuple
import numpy as np
from functools import reduce


def tiles_list_to_dict(tiles : list) -> dict:
    """Converts the image tiles into a dictionary of numpy arrays.
    """
    image_tiles_dict = {}
    for tile in tiles:
        value_list = []
        for idx, row in enumerate(tile.split("\n")): 
            if idx == 0:
                key = int(row[5:-1])
            elif not row:
                pass  # ignore empty rows
            else:
                value_list.append(np.array(list(row)))
        image_tiles_dict[key] = np.array(value_list)

    return image_tiles_dict


def get_matches(tiles : dict) -> dict:
    """Gets the tile edge matches for each tile, and returns this information as
    a dictionary, where the key is the tile ID and the values are tuples contaning
    the edge ID and the tile IDs which match it.

    Example:
      match_dict[tile_ID_1] = [[tile_ID_2, tile_ID_3]),  # edge 0 (left edge)
                               [tile_ID_4],              # edge 1 (top)
                               [None],                   # edge 2 (right)
                               [tile_ID_5]]              # edge 3 (bottom)
    """
    # create the placeholder `match_dict`
    match_dict = {}
    for key in tiles.keys():
        match_dict[key] = [list(), list(), list(), list()]

    # loop over the tile edges looking for matches
    for tile_ID_1, tile_1 in tiles.items():
        for tile_ID_2, tile_2 in tiles.items():
            if tile_ID_1 != tile_ID_2:
                # get the respective edges for each tile
                # edges = (left_edge, top_edge, right_edge, bottom_edge)
                edges_1 = get_edges(tile=tile_1)
                edges_2 = get_edges(tile=tile_2)
                for idx_edge_1, edge_1 in enumerate(edges_1):
                    for idx_edge_2, edge_2 in enumerate(edges_2):
                        if tile_ID_2 not in match_dict[tile_ID_1][idx_edge_1]:
                            if (edge_1 == edge_2).all():  # compare two np arrays
                                match_dict[tile_ID_1][idx_edge_1].append(tile_ID_2)
                                match_dict[tile_ID_2][idx_edge_2].append(tile_ID_1)
                            elif (edge_1 == np.flip(edge_2)).all():  # compare two np arrays, accounting for that the tiles can rotate
                                match_dict[tile_ID_1][idx_edge_1].append(tile_ID_2)
                                match_dict[tile_ID_2][idx_edge_2].append(tile_ID_1)

    return match_dict 



def get_edges(tile : np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Returns the four edges of the input tile, in the following order:
    left, top, right, bottom.
    """
    left_edge = tile[:, 0]
    top_edge = tile[0, :]
    right_edge = tile[:, -1]
    bottom_edge = tile[-1, :]
    return left_edge, top_edge, right_edge, bottom_edge


def main():
    # load data
    with open("input", "r") as input_data:
        image_tiles = input_data.read().split("\n\n")
    
    # convert the image tiles into a dictionary of numpy arrays
    image_tiles_dict = tiles_list_to_dict(tiles=image_tiles)

    # get the number of edge matches for each tile
    match_dict = get_matches(tiles=image_tiles_dict)

    # the corner tiles are those which only have two matching edges
    corner_tiles = []
    for key, value in match_dict.items():
        n_values = sum([len(row) for row in value])
        if n_values == 2:
            corner_tiles.append(key)

    # the answer to the puzzle is the product of the tile IDs of the four corner tiles
    answer = reduce((lambda x, y: x * y), corner_tiles)

    print("Answer:", answer)


if __name__ == "__main__":
    main()
