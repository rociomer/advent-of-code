# --- Day 1: Trebuchet?! ---
import re

# load the input data
with open("input", "r") as input_data:
    # read entries
    calibration_lines = input_data.read().split("\n")

# clean up the calibration values
calibration_values_tmp = [re.sub("[^0-9]", "", line) for line in calibration_lines]
calibration_values     = [int(value[0]+value[-1]) for value in calibration_values_tmp]

# the answer to the puzzle is the sum of the calibration values
answer = sum(calibration_values)

print("Answer:", answer)
