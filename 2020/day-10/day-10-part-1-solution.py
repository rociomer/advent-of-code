# --- Day 10: Adapter Array ---


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

    # count the number of 1-jolt differences
    n_one_jolt_differences = jolt_differences.count(1)
    
    # count the number of 3-jolt differences
    n_three_jolt_differences = jolt_differences.count(3)

    answer = n_one_jolt_differences * n_three_jolt_differences

    print("Answer:", answer)

if __name__ == "__main__":
    main()
