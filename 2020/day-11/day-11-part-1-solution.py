# --- Day 12: Seating System ---
from copy import deepcopy


def get_seat(row_idx : int, col_idx : int, seat_layout : list) -> str:
    """Gets if a corresponding pair of indices in a seat layout corresponds to 
    an occupied seat ("#"), an empty seat ("L"), floor ("."), or is out of the
    range of the seat layout (False).
    """
    max_row_length = len(seat_layout)
    max_col_length = len(seat_layout[0])

    if 0 > row_idx or row_idx >= max_row_length:  # `row_idx` out of range
        adjacent_seat = False
    elif 0 > col_idx or col_idx >= max_col_length:  # `col_idx` out of range
        adjacent_seat = False
    else:
        adjacent_seat = seat_layout[row_idx][col_idx]

    return adjacent_seat


def get_adjacent_seats(row_idx : int, col_idx : int, seat_layout : list) -> list:
    """Get all the seats adjacent to the seat indicated by `row_idx` and `col_idx`.
    -->           123
    --> Seat map: 4X5
    -->           678
    """
    # first get all the adjacent seats
    adjacent_seat_1 = get_seat(row_idx=(row_idx-1), col_idx=(col_idx - 1), seat_layout=seat_layout)
    adjacent_seat_2 = get_seat(row_idx=(row_idx-1), col_idx=col_idx, seat_layout=seat_layout)
    adjacent_seat_3 = get_seat(row_idx=(row_idx-1), col_idx=(col_idx + 1), seat_layout=seat_layout)
    adjacent_seat_4 = get_seat(row_idx=row_idx, col_idx=(col_idx - 1), seat_layout=seat_layout)
    adjacent_seat_5 = get_seat(row_idx=row_idx, col_idx=(col_idx + 1), seat_layout=seat_layout)
    adjacent_seat_6 = get_seat(row_idx=(row_idx+1), col_idx=(col_idx - 1), seat_layout=seat_layout)
    adjacent_seat_7 = get_seat(row_idx=(row_idx+1), col_idx=col_idx, seat_layout=seat_layout)
    adjacent_seat_8 = get_seat(row_idx=(row_idx+1), col_idx=(col_idx + 1), seat_layout=seat_layout)

    # collect all the adjacent seats, and remove the irrelevant ones
    adjacent_seats = [adjacent_seat_1, adjacent_seat_2, 
                      adjacent_seat_3, adjacent_seat_4, 
                      adjacent_seat_5, adjacent_seat_6, 
                      adjacent_seat_7, adjacent_seat_8]

    return adjacent_seats


def update_seat_states(seat_states : list) -> list:
    """Updates the seat states based on the following rules:
       1) If a seat is empty (L) and there are no occupied seats adjacent to it,
          the seat becomes occupied.
       2) If a seat is occupied (#) and four or more seats adjacent to it are 
          also occupied, the seat becomes empty.
       3) Otherwise, the seat's state does not change.
    """
    # create a copy of the seat layout, to update
    updated_seat_states = deepcopy(seat_states)

    # loop over every seat
    for seat_row_idx, seat_row in enumerate(seat_states):
        for seat_idx, seat in enumerate(seat_row):
            if seat == ".":
                pass
            else:
                # get the states of the seats adjacent to the current seat
                adjacent_seats = get_adjacent_seats(row_idx=seat_row_idx,
                                                    col_idx=seat_idx,
                                                    seat_layout=seat_states)

                # remove any information which is not relevant from `adjacent_seats`
                while "." in adjacent_seats:
                    adjacent_seats.remove(".")

                while False in adjacent_seats:
                    adjacent_seats.remove(False)

                if seat == "L" and ("#" not in adjacent_seats):
                    # need to convert a str to a list to do item assignment, then convert back
                    updated_seat_state = list(updated_seat_states[seat_row_idx])
                    updated_seat_state[seat_idx] = "#"
                    updated_seat_states[seat_row_idx] = "".join(updated_seat_state)
                elif seat == "#" and adjacent_seats.count("#") >= 4:
                    updated_seat_state = list(updated_seat_states[seat_row_idx])
                    updated_seat_state[seat_idx] = "L"
                    updated_seat_states[seat_row_idx] = "".join(updated_seat_state)

    return updated_seat_states


def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        seat_layout = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # update the seat states until they equilibrate
    equilibrium = False
    current_seat_layout = seat_layout
    while not equilibrium:
        new_seat_layout = update_seat_states(seat_states=current_seat_layout)
        if new_seat_layout == current_seat_layout:
            equilibrium = True
        else:
            current_seat_layout = new_seat_layout

    # count the number of occupied seats after equilibration
    current_seat_layout_str = "".join([seat_row for seat_row in current_seat_layout])
    n_occupied_seats = current_seat_layout_str.count("#")

    print("Answer:", n_occupied_seats)


if __name__ == "__main__":
    main()
