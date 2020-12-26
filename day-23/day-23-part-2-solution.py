# --- Day 23: Crab Cups ---
from collections import deque
# import time


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
        if destination_cup < 1:
            destination_cup = 1000000 - three_cups.count(1000000) - three_cups.count(999999) - three_cups.count(999998)
            break
        else:
            destination_cup -= 1

    destination_cup_idx = cups.index(destination_cup)

    # action 3
    cups.insert(destination_cup_idx, three_cups[0])
    cups.insert(destination_cup_idx, three_cups[1])
    cups.insert(destination_cup_idx, three_cups[2])

    return cups


def main():
    # load data
    with open("input", "r") as input_data:
        cup_labels = input_data.read()[:-1]  # skip the \n at the end
    cup_labels = [int(i) for i in cup_labels]  # convert from list of strings to list of integers

    # the above cup label input is incomplete, it should be 1,000,000 cups with
    # labels as follows:
    cup_labels += [i for i in range(max(cup_labels)+1, 1000001)]

    # for efficiency, we will use a reversed deque (double ended queues) instead of a list
    cup_labels = deque(reversed(cup_labels))

    # start = time.time()
    # the crab does 10,000,000 of his/her "moves" using the above cups
    n_moves = 10000000
    for _ in range(n_moves):
        print(_)
        # if _ % 100000 == 0:
        #     end = time.time() - start
        #     print(end)
        cup_labels = crab_move(cups=cup_labels)

    # the answer to the puzzle is the product of the two cup labels
    # immediately clockwise of cup 1
    cup_1_idx = cup_labels.index(1)
    adjacent_cup_idx_1 = (cup_1_idx - 1) % len(cup_labels)
    adjacent_cup_idx_2 = (cup_1_idx - 2) % len(cup_labels)
    answer = cup_labels[adjacent_cup_idx_1] * cup_labels[adjacent_cup_idx_2]

    print("Answer:", answer)


if __name__ == "__main__":
    main()

