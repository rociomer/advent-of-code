# --- Day 1: Trebuchet?! ---
import re

# load the input data
with open("input", "r") as input_data:
    # read entries
    calibration_lines = input_data.read().split("\n")

# create a dictionary of digits and their spelled out versions
digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

# replace spelled out digits with integer strings, starting from left to right
not_spelled_out = []
for line in calibration_lines:
    # can skip by two's since new digits are at least 3 characters, and *2 because spelled out digits can overlap
    for i in range(3, len(line)*2, 2):
        for key, value in digits.items():
            if key not in line[:i]:
                continue
            else:
                line = re.sub(key, str(value)+str(key[1:]), line)
                break
    not_spelled_out.append(line)

# clean up the calibration values
calibration_values_tmp = [re.sub("[^0-9]", "", line) for line in not_spelled_out]
calibration_values     = [int(value[0]+value[-1]) for value in calibration_values_tmp]

# the answer to the puzzle is the sum of the calibration values
answer = sum(calibration_values)

print("Answer:", answer)
