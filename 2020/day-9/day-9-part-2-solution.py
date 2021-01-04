# --- Day 9: Encoding Error ---


def is_sum_of_two_numbers_in_list(number : int, list_of_numbers :list) -> bool:
    """Checks if the input `number` can be the sum of two numbers in `list_of_numbers`.
    """
    for idx_1, number_1 in enumerate(list_of_numbers):
        for number_2 in list_of_numbers[(idx_1 + 1):]:
            if number == (number_1 + number_2):
                return True
    return False


def get_contiguous_range(invalid_number : int, list_of_numbers : list) -> list:
    """Returns a contiguous set of numbers from `list_of_numbers` which
       add up to the `invalid_number`.
    """
    for idx_1, number_1 in enumerate(list_of_numbers):
        # don't even bother to start counting if `number_1` is too large
        if number_1 > invalid_number:
            continue

        # start counting
        contiguous_sum = number_1
        for number_2 in list_of_numbers[(idx_1 + 1):]:

            contiguous_sum += number_2

            # check the sum
            if contiguous_sum > invalid_number:
                break
            elif contiguous_sum == invalid_number:
                # get the index for the final number, +1, to return the contiguous sum
                idx_2 = idx_1 + list_of_numbers[idx_1:].index(number_2) + 1
                return list_of_numbers[idx_1:idx_2]

    # this part of code should never be reached with correct input
    raise ValueError


def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        xmas = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

        # convert list of strings to list of integers
        xmas = [int(i) for i in xmas]

    # loop over the numbers
    for idx, number in enumerate(xmas[25:]):
        is_sum = is_sum_of_two_numbers_in_list(number=number,
                                               list_of_numbers=xmas[idx:(idx + 25)])

        if not is_sum:
            break

    # find contiguous set of numbers that add up to the invalid numbers
    contiguous_numbers = get_contiguous_range(invalid_number=number,
                                              list_of_numbers=xmas)

    # get the encryption weakness
    encryption_weakness = min(contiguous_numbers) + max(contiguous_numbers)

    print("Answer:", encryption_weakness)

if __name__ == "__main__":
    main()
