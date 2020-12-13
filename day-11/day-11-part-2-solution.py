# --- Day 12: Seating System ---
# Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!
# 
# By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).
# 
# The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:
# 
# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:
# 
# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.
# Floor (.) never changes; seats don't move, and nobody sits on the floor.
# 
# After one round of these rules, every seat in the example layout becomes occupied:
# 
# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##
# After a second round, the seats with four or more occupied adjacent seats become empty again:
# 
# #.LL.L#.##
# #LLLLLL.L#
# L.L.L..L..
# #LLL.LL.L#
# #.LL.LL.LL
# #.LLLL#.##
# ..L.L.....
# #LLLLLLLL#
# #.LLLLLL.L
# #.#LLLL.##
# This process continues for three more rounds:
# 
# #.##.L#.##
# #L###LL.L#
# L.#.#..#..
# #L##.##.L#
# #.##.LL.LL
# #.###L#.##
# ..#.#.....
# #L######L#
# #.LL###L.L
# #.#L###.##
# #.#L.L#.##
# #LLL#LL.L#
# L.L.L..#..
# #LLL.##.L#
# #.LL.LL.LL
# #.LL#L#.##
# ..L.L.....
# #L#LLLL#L#
# #.LLLLLL.L
# #.#L#L#.##
# #.#L.L#.##
# #LLL#LL.L#
# L.#.L..#..
# #L##.##.L#
# #.#L.LL.LL
# #.#L#L#.##
# ..L.L.....
# #L#L##L#L#
# #.LLLLLL.L
# #.#L#L#.##
# At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.
# 
# Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
#
# --- Part Two ---
# As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!
# 
# Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:
# 
# .......#.
# ...#.....
# .#.......
# .........
# ..#L....#
# ....#....
# .........
# #........
# ...#.....
# The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:
# 
# .............
# .L.L.#.#.#.#.
# .............
# The empty seat below would see no occupied seats:
# 
# .##.##.
# #.#.#.#
# ##...##
# ...L...
# ##...##
# #.#.#.#
# .##.##.
# Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.
# 
# Given the same starting layout as above, these new rules cause the seating area to shift around as follows:
# 
# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##
# #.LL.LL.L#
# #LLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLLL.L
# #.LLLLL.L#
# #.L#.##.L#
# #L#####.LL
# L.#.#..#..
# ##L#.##.##
# #.##.#L.##
# #.#####.#L
# ..#.#.....
# LLL####LL#
# #.L#####.L
# #.L####.L#
# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##LL.LL.L#
# L.LL.LL.L#
# #.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLL#.L
# #.L#LL#.L#
# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.#L.L#
# #.L####.LL
# ..#.#.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#
# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.LL.L#
# #.LLLL#.LL
# ..#.L.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#
# Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.
# 
# Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?

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


def get_visible_seats(row_idx : int, col_idx : int, seat_layout : list) -> list:
    """Get the first visible seats adjacent to the seat indicated by `row_idx` and `col_idx`.
                                                      2 2 2
    -->           123               111
    --> Seat map: 4X5     radius 1: 1X1     radius 2: 2 X 2
    -->           678               111                  
                                                      2 2 2
    """
    adjacent_seat_1 = "."
    radius = 1
    while adjacent_seat_1 == ".":
        adjacent_seat_1 = get_seat(row_idx=(row_idx-radius), col_idx=(col_idx-radius), seat_layout=seat_layout)
        radius += 1

    adjacent_seat_2 = "."
    radius = 1
    while adjacent_seat_2 == ".":
        adjacent_seat_2 = get_seat(row_idx=(row_idx-radius), col_idx=col_idx, seat_layout=seat_layout)
        radius += 1

    adjacent_seat_3 = "."
    radius = 1
    while adjacent_seat_3 == ".":
        adjacent_seat_3 = get_seat(row_idx=(row_idx-radius), col_idx=(col_idx+radius), seat_layout=seat_layout)
        radius += 1

    adjacent_seat_4 = "."
    radius = 1
    while adjacent_seat_4 == ".":
        adjacent_seat_4 = get_seat(row_idx=row_idx, col_idx=(col_idx-radius), seat_layout=seat_layout)
        radius += 1

    adjacent_seat_5 = "."
    radius = 1
    while adjacent_seat_5 == ".":
        adjacent_seat_5 = get_seat(row_idx=row_idx, col_idx=(col_idx+radius), seat_layout=seat_layout)
        radius += 1

    adjacent_seat_6 = "."
    radius = 1
    while adjacent_seat_6 == ".":
        adjacent_seat_6 = get_seat(row_idx=(row_idx+radius), col_idx=(col_idx-radius), seat_layout=seat_layout)
        radius += 1

    adjacent_seat_7 = "."
    radius = 1
    while adjacent_seat_7 == ".":
        adjacent_seat_7 = get_seat(row_idx=(row_idx+radius), col_idx=col_idx, seat_layout=seat_layout)
        radius += 1

    adjacent_seat_8 = "."
    radius = 1
    while adjacent_seat_8 == ".":
        adjacent_seat_8 = get_seat(row_idx=(row_idx+radius), col_idx=(col_idx+radius), seat_layout=seat_layout)
        radius += 1

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
                visible_seats = get_visible_seats(row_idx=seat_row_idx,
                                                  col_idx=seat_idx,
                                                  seat_layout=seat_states)

                # remove any information which is not relevant from `visible_seats`
                while "." in visible_seats:
                    visible_seats.remove(".")

                while False in visible_seats:
                    visible_seats.remove(False)

                if seat == "L" and ("#" not in visible_seats):
                    # need to convert a str to a list to do item assignment, then convert back
                    updated_seat_state = list(updated_seat_states[seat_row_idx])
                    updated_seat_state[seat_idx] = "#"
                    updated_seat_states[seat_row_idx] = "".join(updated_seat_state)
                elif seat == "#" and visible_seats.count("#") >= 5:
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
