# --- Day 23: Crab Cups ---
from typing import Tuple


def crab_move(cups : dict, current_cup : int) -> Tuple[dict, int]:
    """Performs a single crab move. Each move, the crab does the following actions:
    1) The crab picks up the three cups that are immediately clockwise of the
       current cup. They are removed from the circle; cup spacing is adjusted as
       necessary to maintain the circle.
    2) The crab selects a destination cup: the cup with a label equal to the
       current cup's label minus one. If this would select one of the cups that
       was just picked up, the crab will keep subtracting one until it finds a
       cup that wasn't just picked up. If at any point in this process the value
       goes below the lowest value on any cup's label, it wraps around to the
       highest value on any cup's label instead.
    3) The crab places the cups it just picked up so that they are immediately
       clockwise of the destination cup. They keep the same order as when they
       were picked up.
    4) The crab selects a new current cup: the cup which is immediately clockwise
       of the current cup.

    Now, the input `cups` dictionary consists of the cup names as the keys, and
    the cup which is next in the circle (clockwise) as the values. For example,
    consider the circle starting from cup (U) and ending with cup {U}:
      (U) U2 U3 U4 U5 ... {U},
    then cups[(U)] = U2, cups[U2] = U3, etc.
    """
    # action 1
    three_cups = [cups[current_cup]]
    for _ in range(2):
        three_cups.append(cups[three_cups[-1]])

    # action 2
    destination_cup = current_cup - 1
    while destination_cup in three_cups or destination_cup < 1:
        destination_cup -= 1
        if destination_cup < 0:
            destination_cup = 1000000  # the largest cup key

    # action 3
    # Using --> (U) X1 X2 X3 [U] U U U* U** U ... {U} below, where {U} connects
    # back to (U), the current cup, and U* is the destination cup
    cups[current_cup] = cups[three_cups[-1]]        # (U) now points to [U]
    cups[three_cups[-1]] = cups[destination_cup]    # X3 now points to U**
    cups[destination_cup] = three_cups[0]           # U* now points to X1

    # action 4
    current_cup = cups[current_cup]

    return cups, current_cup


def main():
    # load data
    with open("input", "r") as input_data:
        cup_labels = input_data.read()[:-1]  # skip the newline at the end
    cup_labels = [int(i) for i in cup_labels]  # list of strs --> list of ints
    cup_labels += [i for i in range(max(cup_labels)+1, 1000001)]

    # using deque objects and profiling the code showed that calling deque.index()
    # was a bottleneck; as such I've rewritten the solution using a dictionary
    next_cup_dict = {}
    for idx, cup in enumerate(cup_labels):
        try:
            # the value is the "next" cup in the circle, going clockwise
            next_cup_dict[cup] = cup_labels[idx+1]
        except IndexError:  # last cup will bug out since `idx+1` is out of rance
            # looping back around, the last cup should point to the first cup
            next_cup_dict[cup] = cup_labels[0]

    # the crab does 10,000,000 of his/her "moves" using the above cups
    n_moves = 10000000           # the number of moves to perform
    current_cup = cup_labels[0]  # the starting cup
    for _ in range(n_moves):
        next_cup_dict, current_cup = crab_move(cups=next_cup_dict, current_cup=current_cup)

    # the answer to the puzzle is the product of the two cup labels
    # immediately clockwise of cup 1
    adjacent_cup_1 = next_cup_dict[1]
    adjacent_cup_2 = next_cup_dict[adjacent_cup_1]
    answer = adjacent_cup_1 * adjacent_cup_2

    print("Answer:", answer)


if __name__ == "__main__":
    main()
