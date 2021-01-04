# --- Day 20: Jurassic Jigsaw ---
from typing import Tuple
import numpy as np
from copy import deepcopy
import re


def add_tile_to_image(image : np.ndarray, tile : np.ndarray, coords : tuple) -> np.ndarray:
    """Adds the tile to the image at the specified coordinates.
    """
    x, y = coords
    tile_without_border = tile[1:-1, 1:-1]
    n = len(tile_without_border)
    image[x*n:(x+1)*n, y*n:(y+1)*n] = tile_without_border

    return image


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


def reassemble_image(tiles : dict) -> Tuple[np.ndarray, np.ndarray]:
    """Reassembles the input tiles into an image. This is too long to be a single
    function at the moment and could be further cleaned up, but I already spent
    enough time on this question and need to move on with my life.
    """
    # define some constants
    n_tiles = len(tiles)
    m = int(np.sqrt(n_tiles))  # m = number of tiles that will be placed along each image dimension i.e. the image is an m x m grid

    # get the tile edge matches for each tile
    tile_match_dict = get_matches(tiles=tiles)

    # get the corner pieces, which are the tiles which only have two matching edges
    corner_tiles = []
    for key, value in tile_match_dict.items():
        n_values = sum([len(row) for row in value])
        if n_values == 2:
            corner_tiles.append(key)

    # get the edge pieces, which are the tiles which only have three matching edges
    edge_tiles = []
    for key, value in tile_match_dict.items():
        n_values = sum([len(row) for row in value])
        if n_values == 3:
            edge_tiles.append(key)

    # reassemble the tiles using the tile match info, start from one corner and add all edges:
    reassembled_tiles_IDs = np.zeros((m, m))
    x, y = 0, 0
    first_piece_ID = corner_tiles[0]
    reassembled_tiles_IDs[x, y] = first_piece_ID  # assign the first corner (arbitrarily)

    # make sure to position the first tile (top left corner tile) in a way that
    # the two matching edges are facing the rest of the image; note, the edge indices
    # follow 0:left_edge, 1:top_edge, 2:right_edge, 3:bottom_edge)
    first_corner, first_corner_matching_edges = rotate_tile(tile=tiles[first_piece_ID],
                                                            matching_edges=tile_match_dict[first_piece_ID],
                                                            edges_to_connect_to=[i for i in tile_match_dict[first_piece_ID] if len(i) > 0],
                                                            edges_to_connect_to_idc=[2,3])
    tile_match_dict[first_piece_ID] = first_corner_matching_edges

    # initialize the image as a zero numpy array (we will fill this in as we
    # add the tiles to the image in the correct orientation)
    size_tiles = len(first_corner) - 2                                      # -2 to account for the border
    reassembled_image = np.zeros((m*size_tiles, m*size_tiles), dtype=str)   # placeholder

    # add the 1st corner to the image
    reassembled_image = add_tile_to_image(image=reassembled_image, tile=first_corner, coords=(x,y))

    # start adding the top edge of the image
    while y < m - 2:
        for edge_tile_ID in edge_tiles:
            if edge_tile_ID in tile_match_dict[reassembled_tiles_IDs[x, y]][2]:  # the 2 indicates the right edge
                prev_tile_ID = int(reassembled_tiles_IDs[x, y])
                y += 1
                # add the tile ID to the list of reassembled_tile_IDs
                reassembled_tiles_IDs[x, y] = edge_tile_ID
                # rotate the tile
                next_tile, next_matching_edges = rotate_tile(tile=tiles[edge_tile_ID],
                                                             matching_edges=tile_match_dict[edge_tile_ID],
                                                             edges_to_connect_to=[[prev_tile_ID], []],
                                                             edges_to_connect_to_idc=[0,1])
                tile_match_dict[edge_tile_ID] = next_matching_edges
                # fill it in
                reassembled_image = add_tile_to_image(image=reassembled_image, tile=next_tile, coords=(x,y))

        # remove the edge tile IDs from the list once they've been placed in the image
        for edge_tile_ID in edge_tiles:
           if edge_tile_ID in reassembled_tiles_IDs:
               edge_tiles.remove(edge_tile_ID)


    # then add the 2nd corner, making sure to position the tile (top right corner
    # tile) in a way that the two matching edges are facing the rest of the
    # image (edge indices follow 0:left_edge, 1:top_edge, 2:right_edge, 3:bottom_edge)
    prev_tile_ID = int(reassembled_tiles_IDs[x, y])
    y += 1
    for corner_tile in corner_tiles:
        if [corner_tile] == tile_match_dict[prev_tile_ID][2]:
            second_corner_ID = corner_tile
            break

    reassembled_tiles_IDs[x, y] = second_corner_ID
    second_corner, second_corner_matching_edges = rotate_tile(tile=tiles[second_corner_ID],
                                                              matching_edges=tile_match_dict[second_corner_ID],
                                                              edges_to_connect_to=[[prev_tile_ID], [], []],
                                                              edges_to_connect_to_idc=[0, 1, 2])
    tile_match_dict[second_corner_ID] = second_corner_matching_edges

    reassembled_image = add_tile_to_image(image=reassembled_image, tile=second_corner, coords=(x,y))

    # then add the right edge of the image
    while x < m - 2:
        for edge_tile_ID in edge_tiles:
            if edge_tile_ID in tile_match_dict[reassembled_tiles_IDs[x, y]][3]:  # the 3 indicates the bottom edge
                prev_tile_ID = int(reassembled_tiles_IDs[x, y])
                x += 1
                # add the tile ID to the list of reassembled_tile_IDs
                reassembled_tiles_IDs[x, y] = edge_tile_ID
                # rotate the tile
                next_tile, next_matching_edges = rotate_tile(tile=tiles[edge_tile_ID],
                                                             matching_edges=tile_match_dict[edge_tile_ID],
                                                             edges_to_connect_to=[[prev_tile_ID], []],
                                                             edges_to_connect_to_idc=[1,2])
                tile_match_dict[edge_tile_ID] = next_matching_edges
                # fill it in
                reassembled_image = add_tile_to_image(image=reassembled_image, tile=next_tile, coords=(x,y))

        # remove the edge tile IDs from the list once they've been placed in the image
        for edge_tile_ID in edge_tiles:
           if edge_tile_ID in reassembled_tiles_IDs:
               edge_tiles.remove(edge_tile_ID)

    # then add the 3rd corner, making sure to position the tile (bottom right corner
    # tile) in a way that the two matching edges are facing the rest of the
    # image (edge indices follow 0:left_edge, 1:top_edge, 2:right_edge, 3:bottom_edge)
    prev_tile_ID = int(reassembled_tiles_IDs[x, y])
    x += 1
    for corner_tile in corner_tiles:
        if [corner_tile] == tile_match_dict[prev_tile_ID][3]:
            third_corner_ID = corner_tile
            break

    reassembled_tiles_IDs[x, y] = third_corner_ID
    third_corner, third_corner_matching_edges = rotate_tile(tile=tiles[third_corner_ID],
                                                            matching_edges=tile_match_dict[third_corner_ID],
                                                            edges_to_connect_to=[[prev_tile_ID], [], []],
                                                            edges_to_connect_to_idc=[1, 2, 3])
    tile_match_dict[third_corner_ID] = third_corner_matching_edges

    reassembled_image = add_tile_to_image(image=reassembled_image, tile=third_corner, coords=(x,y))

    # then add the bottom edge of the image
    while y > 1:
        for edge_tile_ID in edge_tiles:
            if edge_tile_ID in tile_match_dict[reassembled_tiles_IDs[x, y]][0]:  # the 0 indicates the left edge
                prev_tile_ID = int(reassembled_tiles_IDs[x, y])
                y -= 1
                # add the tile ID to the list of reassembled_tile_IDs
                reassembled_tiles_IDs[x, y] = edge_tile_ID
                # rotate the tile
                next_tile, next_matching_edges = rotate_tile(tile=tiles[edge_tile_ID],
                                                             matching_edges=tile_match_dict[edge_tile_ID],
                                                             edges_to_connect_to=[[prev_tile_ID], []],
                                                             edges_to_connect_to_idc=[2,3])
                tile_match_dict[edge_tile_ID] = next_matching_edges
                # fill it in
                reassembled_image = add_tile_to_image(image=reassembled_image, tile=next_tile, coords=(x,y))

        # remove the edge tile IDs from the list once they've been placed in the image
        for edge_tile_ID in edge_tiles:
           if edge_tile_ID in reassembled_tiles_IDs:
               edge_tiles.remove(edge_tile_ID)

    # then add the 4th corner, making sure to position the tile (bottom left corner
    # tile) in a way that the two matching edges are facing the rest of the
    # image (edge indices follow 0:left_edge, 1:top_edge, 2:right_edge, 3:bottom_edge)
    prev_tile_ID = int(reassembled_tiles_IDs[x, y])
    y -= 1
    for corner_tile in corner_tiles:
        if [corner_tile] == tile_match_dict[prev_tile_ID][0]:
            fourth_corner_ID = corner_tile
            break

    reassembled_tiles_IDs[x, y] = fourth_corner_ID
    fourth_corner, fourth_corner_matching_edges = rotate_tile(tile=tiles[fourth_corner_ID],
                                                            matching_edges=tile_match_dict[fourth_corner_ID],
                                                            edges_to_connect_to=[[prev_tile_ID], [], []],
                                                            edges_to_connect_to_idc=[2, 3, 0])
    tile_match_dict[fourth_corner_ID] = fourth_corner_matching_edges

    reassembled_image = add_tile_to_image(image=reassembled_image, tile=fourth_corner, coords=(x,y))

    # then add the left edge of the image
    while x > 1:
        for edge_tile_ID in edge_tiles:
            if edge_tile_ID in tile_match_dict[reassembled_tiles_IDs[x, y]][1]:  # the 1 indicates the top edge
                prev_tile_ID = int(reassembled_tiles_IDs[x, y])
                x -= 1
                # add the tile ID to the list of reassembled_tile_IDs
                reassembled_tiles_IDs[x, y] = edge_tile_ID
                # rotate the tile
                next_tile, next_matching_edges = rotate_tile(tile=tiles[edge_tile_ID],
                                                             matching_edges=tile_match_dict[edge_tile_ID],
                                                             edges_to_connect_to=[[prev_tile_ID], []],
                                                             edges_to_connect_to_idc=[3,0])
                tile_match_dict[edge_tile_ID] = next_matching_edges
                # fill it in
                reassembled_image = add_tile_to_image(image=reassembled_image, tile=next_tile, coords=(x,y))

        # remove the edge tile IDs from the list once they've been placed in the image
        for edge_tile_ID in edge_tiles:
           if edge_tile_ID in reassembled_tiles_IDs:
               edge_tiles.remove(edge_tile_ID)

    # finally, add the (remaining) center tiles, which are those which are not already in `reassembled_titles_IDs`
    center_tiles = []
    for tile_ID in tile_match_dict.keys():
        if tile_ID not in reassembled_tiles_IDs:
            center_tiles.append(tile_ID)

    # start adding the tiles from top left to bottom right, going row-by-row left to right
    while center_tiles:
        for center_tile_ID in center_tiles:
            if center_tile_ID in tile_match_dict[reassembled_tiles_IDs[x, y]][2]:  # the 2 indicates the right edge
                prev_tile_ID_1 = int(reassembled_tiles_IDs[x, y])
                prev_tile_ID_2 = int(reassembled_tiles_IDs[x-1, y+1])
                y += 1
                # add the tile ID to the list of reassembled_tile_IDs
                reassembled_tiles_IDs[x, y] = center_tile_ID
                # rotate the tile
                next_tile, next_matching_edges = rotate_tile(tile=tiles[center_tile_ID],
                                                             matching_edges=tile_match_dict[center_tile_ID],
                                                             edges_to_connect_to=[[prev_tile_ID_1], [prev_tile_ID_2]],
                                                             edges_to_connect_to_idc=[0,1])
                tile_match_dict[center_tile_ID] = next_matching_edges
                # fill it in
                reassembled_image = add_tile_to_image(image=reassembled_image, tile=next_tile, coords=(x,y))
                if y == len(next_tile):
                    y = 0
                    x += 1

        # remove the center tile IDs from the list once they've been placed in the image
        for center_tile_ID in center_tiles:
           if center_tile_ID in reassembled_tiles_IDs:
               center_tiles.remove(center_tile_ID)

    return reassembled_tiles_IDs, reassembled_image


def rotate_tile(tile : np.ndarray, matching_edges : np.ndarray, edges_to_connect_to : list, edges_to_connect_to_idc : list) -> np.ndarray:
    """Rotates and/or flips a tile until the "first" existing edge is aligned
    to the input edge index.
    """
    # first check that the tile isn't already in the correct configuration
    matches = sum([int(matching_edges[idx] == edges_to_connect_to[edges_to_connect_to_idc.index(idx)]) for idx in edges_to_connect_to_idc])
    if matches == len(edges_to_connect_to):
        return tile, matching_edges

    # if not, then try rotating/flipping the tile until it is
    for _ in range(4):
        tile = np.rot90(tile)  # rotate the tile
        matching_edges = np.roll(matching_edges, -1)
        matches = sum([int(matching_edges[idx] == edges_to_connect_to[edges_to_connect_to_idc.index(idx)]) for idx in edges_to_connect_to_idc])
        if matches == len(edges_to_connect_to):
            return tile, matching_edges
        else:  # try flipping the tile
            tile = np.flip(tile, axis=1)  # flip along the (arbitrary) x-axis
            matching_edges = np.array([matching_edges[2], matching_edges[1], matching_edges[0], matching_edges[3]])
            matches = sum([int(matching_edges[idx] == edges_to_connect_to[edges_to_connect_to_idc.index(idx)]) for idx in edges_to_connect_to_idc])
            if matches == len(edges_to_connect_to):
                return tile, matching_edges
            else:  # undo the flip
                tile = np.flip(tile, axis=1)
                matching_edges = np.array([matching_edges[2], matching_edges[1], matching_edges[0], matching_edges[3]])


def get_matches(tiles : dict) -> dict:
    """Gets the tile edge matches for each tile, and returns this information as
    a dictionary, where the key is the tile ID and the values are tuples contaning
    the edge ID and the tile IDs which match it. In this puzzle each tile edge
    has a single match (as I eventually observed) but this function is more general.

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


def find_pattern(image : np.ndarray, pattern : np.ndarray) -> np.ndarray:
    """Finds the pattern in the image and labels all occurences by replacing
    "#"s with "O"s. Keep in mind that the image may need to be rotated in order
    to find the pattern. Also, the pattern should only match the "#"s in the pattern,
    all other characters can be disregarded.
    """
    labeled_image = deepcopy(image)  # create a copy, for labeling with the matching patterns

    # first, replace blank spaces in the pattern with zeros, and the "#"s with 1s,
    # as we will turn the pattern into a mask
    pattern_mask = np.where(pattern == " ", 0, pattern)
    pattern_mask = np.where(pattern_mask == "#", 1, pattern_mask).astype(np.int)

    subarray_shape = pattern.shape

    for _ in range(4):
        n_matches = 0
        for x in range(image.shape[0] - subarray_shape[0] + 1):
            for y in range(image.shape[1] - subarray_shape[1] + 1):
                subarray = image[x:x+subarray_shape[0], y:y+subarray_shape[1]]
                subarray_mask = np.where(subarray == ".", 0, subarray)
                subarray_mask = np.where(subarray_mask == "#", 1, subarray_mask).astype(np.int)
                if (np.multiply(subarray_mask, pattern_mask) == pattern_mask).all():
                    n_matches += 1
                    replace_pattern = np.where(pattern == "#", "O", subarray)
                    labeled_image[x:x+subarray_shape[0], y:y+subarray_shape[1]] = replace_pattern
        if n_matches > 0:
            break
        else:
            image = np.rot90(image)                  # rotate the image 90 degrees counter-clockwise
            labeled_image = np.rot90(labeled_image)  # rotate the copy

    # if there are no matches after all the rotations, then it means the image is
    # flipped, so we can repeat the above process with the flipped image
    if n_matches == 0:

        # flip along the x-axis (although specific axis is irrelevant)
        image = np.flip(image, axis=1)
        labeled_image = np.flip(labeled_image, axis=1)

        for _ in range(4):
            n_matches = 0
            for x in range(image.shape[0] - subarray_shape[0] + 1):
                for y in range(image.shape[1] - subarray_shape[1] + 1):
                    subarray = image[x:x+subarray_shape[0], y:y+subarray_shape[1]]
                    subarray_mask = np.where(subarray == ".", 0, subarray)
                    subarray_mask = np.where(subarray_mask == "#", 1, subarray_mask).astype(np.int)
                    if (np.multiply(subarray_mask, pattern_mask) == pattern_mask).all():
                        n_matches += 1
                        replace_pattern = np.where(pattern == "#", "O", subarray)
                        labeled_image[x:x+subarray_shape[0], y:y+subarray_shape[1]] = replace_pattern
            if n_matches > 0:
                break
            else:
                image = np.rot90(image)                  # rotate the image 90 degrees counter-clockwise
                labeled_image = np.rot90(labeled_image)  # rotate the copy

    return labeled_image


def main():
    # load data
    with open("input", "r") as input_data:
        image_tiles = input_data.read().split("\n\n")

    # convert the image tiles into a dictionary of numpy arrays
    image_tiles_dict = tiles_list_to_dict(tiles=image_tiles)

    # reassemble the original image from the image tiles (144 tiles --> 12x12 grid)
    reassembled_tiles_IDs, reassembled_image = reassemble_image(tiles=image_tiles_dict)


    # define the sea monster pattern as an numpy array (*note* the whitespaces can be any character)
    sea_monsters = np.array([list("                  # "),
                             list("#    ##    ##    ###"),
                             list(" #  #  #  #  #  #   ")])

    # search for the sea monsters in the `reassembled_image`, and replace any
    # "#"s in the matching sea monsters with "O"
    labeled_image = find_pattern(image=reassembled_image, pattern=sea_monsters)

    # the answer to the puzzle is the number of "#" in the image which are not
    # part of sea monsters
    unique, counts = np.unique(labeled_image, return_counts=True)
    answer = counts[np.where(unique == "#")][0]

    print("Answer:", answer)


if __name__ == "__main__":
    main()
