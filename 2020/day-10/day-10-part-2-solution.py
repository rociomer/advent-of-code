# --- Day 10: Adapter Array ---
import math
from functools import reduce


def binomial(x : int, y : int) -> int:
    try:
        return math.factorial(x) // math.factorial(y) // math.factorial(x - y)
    except ValueError:
        return 0

def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        output_joltages = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

        # convert list of strings to list of integers
        output_joltages = [int(i) for i in output_joltages]

    # add the device's built-in joltage (the max adapter joltage + 3)
    output_joltages.append(max(output_joltages) + 3)

    # sort the adapters
    output_joltages.sort()

    # loop through the joltages and calculate the joltage differences
    jolt_differences = [output_joltages[0]]
    # note: skip the first adapter, since its value is already the jolt difference
    for idx, joltage in enumerate(output_joltages[1:]):
        jolt_differences.append(joltage - output_joltages[idx])

    # get the size of all contiguous 1-jolt differences in `jolt_differences`
    contiguous_one_jolt_sequences = []
    jolt_differences_str = "".join([str(i) for i in jolt_differences])
    for n in range(len(jolt_differences), 1, -1):
        sequence = "1" * n
        if sequence in jolt_differences_str:
            contiguous_one_jolt_sequences += [n] * jolt_differences_str.count(sequence)
            # remove the sequence from the string of jolt differences
            jolt_differences_str = jolt_differences_str.replace(sequence, "")

    # for each sequence of adapters of contiguous 1-jolt differences, 
    # get the number which can be removed *independently* (just subtract one 
    # because the final one in the sequence cannot be removed)
    n_which_can_be_removed = [n - 1 for n in contiguous_one_jolt_sequences]

    # the max number of adapters which can be removed at once are 2 adapters
    # such that for any contiguous 1-jolt sequence containing n > 2 adapters,
    # the number of possible removal combinations are:
    #  binomial(n, 0) + binomial(n, 1) + binomial(n, 2)
    n_removal_combinations = []
    for n in n_which_can_be_removed:
        combinations = 0
        for k in range(0, min(2, n) + 1):
            combinations += binomial(n, k)
        n_removal_combinations.append(combinations)

    # the number of distinct arrangements is the product of all the removal combinations
    n_distinct_arrangements = reduce((lambda x, y: x * y), n_removal_combinations)

    print("Answer:", n_distinct_arrangements)

if __name__ == "__main__":
    main()
