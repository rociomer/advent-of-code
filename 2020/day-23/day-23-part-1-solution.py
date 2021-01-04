# --- Day 23: Crab Cups ---
from collections import deque


def crab_move(cups : deque) -> deque:
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

    **Note 1: the input `cups` should always be structured such that the
      "current cup" is positioned at index -1 (i.e. a "reversed" list).
    **Note 2: deque is preferred over lists in the cases where we need quicker
      append and pop operations from both the ends of the container; deque provides
      an O(1) time complexity for append and pop operations as compared to
      lists, which provide O(n) time complexity (source: GeeksForGeeks).
    """
    # action 4  (**note: we do it here so we can do pop() immediately below)
    cups.rotate(1)  # shift the current cup to the end of the queue

    # action 1
    three_cups = [cups.pop() for _ in range(3)]

    # action 2
    destination_cup = cups[0] - 1
    while destination_cup in three_cups or destination_cup < 1:
        destination_cup -= 1
        if destination_cup < 0:
            destination_cup = max(cups)

    destination_cup_idx = cups.index(destination_cup)

    # action 3
    cups.insert(destination_cup_idx, three_cups[0])
    cups.insert(destination_cup_idx, three_cups[1])
    cups.insert(destination_cup_idx, three_cups[2])

    return cups


def main():
    # load data
    with open("input", "r") as input_data:
        cup_labels = input_data.read()[:-1]

    # convert from list of strings to a reversed (for efficiency) deque of integers
    cup_labels = deque(reversed([int(i) for i in cup_labels]))

    # the crab does 100 of his/her "moves"
    for _ in range(100):
        cup_labels = crab_move(cups=cup_labels)

    # convert the deque object back to a list (for slicing below), and un-reverse
    cup_labels = list(reversed(cup_labels))

    # the answer to the puzzle is the order of the cups after the crabs 100 moves,
    # starting clockwise from cup 1 (and excluding cup 1)
    cup_1_idx = cup_labels.index(1)
    cups_starting_from_1 = cup_labels[cup_1_idx:] + cup_labels[:cup_1_idx]
    answer = "".join([str(i) for i in cups_starting_from_1[1:]])

    print("Answer:", answer)


if __name__ == "__main__":
    main()

