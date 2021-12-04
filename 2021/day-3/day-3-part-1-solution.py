# --- Day 3: Binary Diagnostic ---
from statistics import mode


# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    diagnostic_report = input_data.read().split("\n")

    # transpose the diagnostic report to get a list of the bits at each position
    diagnostic_report_per_bit = list(zip(*diagnostic_report))

# get the gamma rate from the diagnostic report numbers; the gamma rate is
# determined by the most common bit at each position
gamma_rate = ''.join(map(mode, diagnostic_report_per_bit))

# get the epsilon rate from the diagnostic report numbers
epsilon_rate = ''.join([str(int(i != '1')) for i in gamma_rate])

# calculate the power consumption from the decimal representations of each rate
power_consumption = int(gamma_rate, 2) * int(epsilon_rate, 2)

# the answer to the puzzle is the power consumption
answer = power_consumption

print("Answer:", answer)
