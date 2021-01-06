# --- Day 4: Secure Container ---
import re


def does_number_meet_password_criteria(number : str) -> int:
    """Checks if the input number meets the specified password criteria. If yes,
    returns 1. Otherwise, returns 0.
    """
    # first condition: be a six-digit number
    # (by default true)

    # second condition: be in the range of the puzzle input
    # (by default true)

    # third condition: two adjacent digits are the same
    if not re.search("(\\d)\\1", number):  # repetition of adjacent digits e.g. 12234 (2 repeats twice)
        return 0

    # fourth condition: going from left to right, the digits never decrease
    digits_increasing = [int(n) >= int(number[idx]) for idx, n in enumerate(number[1:])]
    if not all(digits_increasing):
        return 0

    return 1

def main():
    with open("input", "r") as input_data:
        # read the range of possible passwords
        password_bounds = [int(i) for i in input_data.read().split("\n")[0].split("-")]

    # check how many passwords in the input range meet the criteria
    n_meet_criteria = 0
    for n in range(password_bounds[0], password_bounds[1]+1):
        n_meet_criteria += does_number_meet_password_criteria(number=str(n))

    # the answer to the puzzle is the number of different passwords within the input
    # range which match the criteria
    answer = n_meet_criteria

    print("Answer:", answer)


if __name__ == "__main__":
    main()
