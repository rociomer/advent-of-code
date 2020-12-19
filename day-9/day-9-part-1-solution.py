# --- Day 9: Encoding Error ---


def is_sum_of_two_numbers_in_list(number : int, list_of_numbers :list) -> bool:
    """Checks if the input `number` can be the sum of two numbers in `list_of_numbers`.
    """
    for idx_1, number_1 in enumerate(list_of_numbers):
        for number_2 in list_of_numbers[(idx_1 + 1):]:
            if number == (number_1 + number_2):
                return True
    return False

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
    
    print("Answer:", number)


if __name__ == "__main__":
    main()
