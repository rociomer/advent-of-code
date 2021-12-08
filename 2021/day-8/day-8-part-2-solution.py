# --- Day 8: Seven Segment Search ---


def get_integer_codes(input : str) -> dict:
    """
    Returns a dictionary which maps each input key to an integer between 1 and 9.
    """
    solutions = {}
    # first solve the easy numbers (1, 7, 4, and 8)
    for key in input:
        if len(key) == 2:
            solutions[key] = 1
        elif len(key) == 3:
            solutions[key] = 7
        elif len(key) == 4:
            solutions[key] = 4
        elif len(key) == 7:
            solutions[key] = 8

    inverse_solutions = {v: k for k, v in solutions.items()}
    for solved_key in solutions.keys():
        input.remove(solved_key)

    # then solve the harder numbers (0, 3, 6, 9)
    for key in input:
        if len(key) == 5:  # 2, 3, or 5
            if set(inverse_solutions[1]).issubset(set(key)):
                solutions[key] = 3

        elif len(key) == 6:  # 0, 6, or 9
            if set(inverse_solutions[4]).issubset(set(key)):
                solutions[key] = 9
            elif set(inverse_solutions[1]).issubset(set(key)):
                solutions[key] = 0
            else:
                solutions[key] = 6

    inverse_solutions = {v: k for k, v in solutions.items()}
    for solved_key in solutions.keys():
        try:
            input.remove(solved_key)
        except ValueError:  # raised for keys for 1, 7, 4, and 8, removed previously
            pass

    # finally solve the hardest numbers (2, 5)
    for key in input:
        if set(key).issubset(set(inverse_solutions[6])):
            solutions[key] = 5
        else:
            solutions[key] = 2

    # sort the key as the codes in the output may be shuffled
    return {"".join(sorted(k)): v for k, v in solutions.items()}

def decode_output(output : list, keys : dict) -> int:
    """
    Decodes the input list of encoded numbers using the provided keys. Sorts
    the codes in the output as they can be shuffled from what's in the keys.
    """
    digits_list = [keys["".join(sorted(key))] for key in output]
    return int("".join([str(i) for i in digits_list]))

# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line
    raw_input = input_data.read().split("\n")

    # parse the input and separate it from the output
    input, output = [], []
    for line in raw_input:
        split_line = line.split(" | ")
        input.append(split_line[0].split(" "))
        output.append(split_line[1].split(" "))

# determine the integer values of the output
decoded_output = []
for idx, line in enumerate(input):
    solution_dict = get_integer_codes(input=line)
    encoded_value = decode_output(output=output[idx], keys=solution_dict)
    decoded_output.append(encoded_value)

# the answer to the puzzle is the sum of the output integers
answer = sum(decoded_output)

print("Answer:", answer)
