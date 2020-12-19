# --- Day 17: Conway Cubes ---
import numpy as np
from copy import deepcopy


def get_array(conway_cubes_list : list) -> np.ndarray:
    """Converts the list of strings that is the input `conway_cubes_list` into
    a numpy array of 0s and 1s, where 0s indicate inactive cubes and 1s indicate
    active cubes.
    """
    # first get the list of 0s and 1s
    list_of_0s_and_1s = []
    for row in conway_cubes_list:
        new_row = [int(n == "#") for n in row]
        list_of_0s_and_1s.append(new_row)

    # then convert the list into an array
    conway_cubes_array = np.array(list_of_0s_and_1s)
    return conway_cubes_array


def pad_up_cube_rep(conway_cubes : list, n_cycles : int) -> list:
    """Pads up the cube representation to the size that would contain all possible
    active cubes after `n_cycles`.
    """
    # create an empty Conway Cube
    max_z = 1 + n_cycles * 2
    max_y = len(conway_cubes) + n_cycles * 2
    max_x = len(conway_cubes[0]) + n_cycles * 2

    conway_cubes_padded = np.zeros((max_z, max_y, max_x))

    # get the indices, which we will use to fill in the current state
    current_z = n_cycles
    start_y = n_cycles
    end_y = n_cycles + len(conway_cubes)
    start_x = n_cycles
    end_x = n_cycles + len(conway_cubes)

    # fill in cube with current state
    conway_cubes_padded[current_z, start_y:end_y, start_x:end_x] = conway_cubes

    return conway_cubes_padded


def get_next_cycle_state(initial_states : list) -> list:
    """Gets the states of the next cycle of the Conway Cubes, starting from the
    input initial_states.
    """
    # create a copy of the next state, which we will modify
    next_states = deepcopy(initial_states)

    # loop over all cubes in the current state and count their active neighbors
    # to determine the next states
    for idx_z, z_slice in enumerate(initial_states):
        for idx_y, row in enumerate(z_slice):
            for idx_x, cube in enumerate(row):
                cube_neighborhood_sum = get_neighborhood_sum(cube_idc=(idx_z, idx_y, idx_x), 
                                                             cube_states=initial_states)
                if cube and cube_neighborhood_sum not in [2, 3]:
                    # if cube is active but there are not 2-3 active cubes in 
                    # its vicinity, the cube becomes inactive in the next cycle
                    next_states[idx_z, idx_y, idx_x] = 0
                elif not cube and cube_neighborhood_sum == 3:
                    # if cube was inactive but it has exactly 3 active neighbors,
                    # then it becomes active in the next cycle
                    next_states[idx_z, idx_y, idx_x] = 1
                else:
                    # otherwise the cube state does not change
                    pass

    return next_states


def get_neighborhood_sum(cube_idc : tuple, cube_states : np.ndarray) -> int:
    """Returns the sum of the 26 neighbors of the cube indicated by `cube_idc`.
    """
    cube_neighborhood_sum = 0.0
    for idx_z in range(cube_idc[0] - 1, cube_idc[0] + 2):
        for idx_y in range(cube_idc[1] - 1, cube_idc[1] + 2):
            for idx_x in range(cube_idc[2] - 1, cube_idc[2] + 2):
                try:
                    cube_neighborhood_sum += cube_states[idx_z, idx_y, idx_x]
                except:
                    # just means the indices are out of the range of the padding,
                    # but we can ignore them because they will not contain actives
                    pass

    # don't forget to subtract the state of the center cube, as we only want the
    # sum of its neighbors
    return cube_neighborhood_sum - cube_states[cube_idc[0], cube_idc[1], cube_idc[2]]


def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        conway_cubes_list = input_data.read().split("\n")[:-1]  # throw away the last empty item

    # convert conway cubes into a numpy array of 0s and 1s
    conway_cubes = get_array(conway_cubes_list=conway_cubes_list)

    # pad up the conway cube input states to the size that would contain all
    # the possible active cubes after six cycles
    conway_cubes = pad_up_cube_rep(conway_cubes=conway_cubes, n_cycles=6)

    # loop over all the cycles
    for _ in range(6):
        conway_cubes = get_next_cycle_state(initial_states=conway_cubes)

    # how many cubes are left in the active state after the sixth cycle?
    answer = int(np.sum(conway_cubes))

    print("Answer:", answer)  # 1059 too high


if __name__ == "__main__":
    main()
