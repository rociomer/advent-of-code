# --- Day 15: Rambunctious Recitation ---


def main():
    # define the starting numbers for the elf game
    starting_numbers = [0,14,1,3,7,9]

    # convert to a dictionary
    current_indices_dict = {}
    for idx, number in enumerate(starting_numbers):
        current_indices_dict[number] = idx + 1  # add 1 to avoid 0-indexing

    # play the game
    next_number_idx = len(starting_numbers)                                 # this is the index for the "next" number
    last_number = starting_numbers[-1]                                      # 9 was the last number
    last_number_already_spoken = (starting_numbers.count(last_number) > 1)  # False (it was not already spoken)
    while next_number_idx < 30000000:  # we want the 30000000th number spoken
        
        # the line below is equal to 0 if the `last_number` has not occured before, and
        # to the difference between the new and last occurence indices if `last_number` did occur before
        next_number = next_number_idx - current_indices_dict[last_number]
        current_indices_dict[last_number] = next_number_idx

        if next_number not in current_indices_dict:
            # update the indices for the next number (which will be the "last" number in the
            # next round) only if it has not been spoken before; if it HAS been spoken,
            # we don't want to touch this yet so as to not overwrite the previous index
            # needed in order to calculate the index difference above
            current_indices_dict[next_number] = next_number_idx + 1

        # in the next iteration, the `next_number` will become the `last_number`
        next_number_idx += 1
        last_number = next_number

    # the 30000000th number spoken should be the last one in the list
    the_30000000th_number = next_number

    print("Answer:", the_30000000th_number)


if __name__ == "__main__":
    main()
