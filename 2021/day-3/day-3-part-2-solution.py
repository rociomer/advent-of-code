# --- Day 3: Binary Diagnostic ---
from copy import deepcopy
from statistics import mode


def find_most_matching_number(which_rating : str, list_of_numbers : list) -> str:
    """
    Finds the number from a list of numbers (list of str) which best matches the
    criteria for either the oxygen generator or CO2 scrubber rating, as indi-
    cated by `which_rating` (can be either 'o2' or 'co2').
    """
    possible_numbers = deepcopy(list_of_numbers)
    for bit in range(len(possible_numbers[0])):

        possible_numbers_per_bit = list(zip(*possible_numbers))

        # the number to match will depend on the specific rating to calculate
        number_to_match = ''.join(map(mode, possible_numbers_per_bit))
        if which_rating == 'co2':
            number_to_match = ''.join([str(int(i != '1')) for i in number_to_match])

        # fix ties, if any, which depend on the rating we are trying to calculate
        if possible_numbers_per_bit[bit].count('0') == possible_numbers_per_bit[bit].count('1'):
            if which_rating == 'o2':
                number_to_match = number_to_match[:bit] + '1' + number_to_match[bit+1:]
            elif which_rating == 'co2':
                number_to_match = number_to_match[:bit] + '0' + number_to_match[bit+1:]

        # first figure out which numbers do not match the nth bit
        numbers_to_remove = []
        for number in possible_numbers:
            if number[bit] != number_to_match[bit]:
                numbers_to_remove.append(number)

        # then remove the numbers
        for number in numbers_to_remove:
            possible_numbers.remove(number)

        # when there is only a single number left, that is the most matching number
        if len(possible_numbers) == 1:
            most_matching_number = possible_numbers[0]
            return most_matching_number

# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    diagnostic_report = input_data.read().split("\n")

    # transpose the diagnostic report to get a list of the bits at each position
    diagnostic_report_per_bit = list(zip(*diagnostic_report))

# to determine the oxygen generator rating, find the number which has the
# greatest number of consecutive bits in common with the gamma rate, factoring
# in any possible tie-breaks
oxygen_generator_rating = find_most_matching_number(which_rating='o2',
                                                    list_of_numbers=diagnostic_report)

# to determine the CO2 scrubber rating, find the number which has the
# greatest number of consecutive bits in common with the epsilon rate, factoring
# in any possible tie-breaks
co2_scrubber_rating = find_most_matching_number(which_rating='co2',
                                                list_of_numbers=diagnostic_report)

# calculate the life support rating from the decimal representations of the
# oxygen generator and CO2 scrubber rating
life_support_rating = int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2)

# the answer to the puzzle is the life support rating
answer = life_support_rating

print("Answer:", answer)
