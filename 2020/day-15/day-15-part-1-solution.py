# --- Day 15: Rambunctious Recitation ---


def main():
    # define the starting numbers for the elf game
    starting_numbers = [0,14,1,3,7,9]

    # play the game
    while len(starting_numbers) < 2020:  # we want the 2020th number spoken
        last_number = starting_numbers[-1]
        # if the number has already been spoken, the next number is the difference 
        # between the new index and the index for the number the last time it was spoken
        if starting_numbers.count(last_number) > 1:
            reversed_starting_numbers = list(reversed(starting_numbers))
            reversed_starting_numbers.remove(last_number)
            # the difference between the new and last occurence index is equal to the line below
            next_number = reversed_starting_numbers.index(last_number) + 1
        else:  # otherwise the next number is just 0
            next_number = 0
        starting_numbers.append(next_number)

    # the 2020th number spoken should be the last one in the list
    the_2020th_number = starting_numbers[-1]

    print("Answer:", the_2020th_number)


if __name__ == "__main__":
    main()
