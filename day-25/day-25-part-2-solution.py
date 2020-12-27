# --- Day 25: Combo Breaker ---
from typing import Tuple
import math


def transform(subject : int, value : int) -> int:
    """Performs the following:
    1) Sets the value to itself multiplied by the subject number.
    2) Sets the value to the remainder after dividing the value by 20201227.
    """
    value *= subject
    return value % 20201227


def get_loop_size(subject_number : int, door_public_key : int, card_public_key : int) -> Tuple[int, str]:
    """Gets at least one device's loop size by transforming a range of trial numbers
    until the transformed value matches the corresponding public key.
    """
    loop_size = 0  # keep track of the loop size
    value = 1      # and of the ongoing transformed value

    # starting from a value of 1, for the given number of loops, performs the
    # transformation and check if it matches either of the keys
    while True:
        loop_size += 1
        value = transform(subject=subject_number, value=value)
        condition1 = (value == door_public_key)
        condition2 = (value == card_public_key)
        if condition1:
            return loop_size, "door"
        elif condition2:
            return loop_size, "card"


def main():
    # load data
    with open("input", "r") as input_data:
        # the order of the door/card public keys below is irrelevant
        door_public_key, card_public_key = [int(i) for i in input_data.read().split("\n")[:-1]]

    subject_number = 7

    # get each device's loop size, which is a number that, when "transformed" by
    # the subject number, gives the respective public key
    loop_size, which_device = get_loop_size(subject_number=subject_number,
                                            door_public_key=door_public_key,
                                            card_public_key=card_public_key)

    # the encryption key is the card's public key transformed with the door's loop
    # size (or vice-versa) -- we use whichever we found first above
    encryption_key = 1
    if which_device == "door":
        for _ in range(loop_size):
            encryption_key = transform(subject=card_public_key, value=encryption_key)
    elif which_device == "card":
        for _ in range(loop_size):
            encryption_key = transform(subject=door_public_key, value=encryption_key)

    print("Answer:", encryption_key)


if __name__ == "__main__":
    main()

