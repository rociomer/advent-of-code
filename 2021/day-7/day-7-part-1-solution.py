# --- Day 7: The Treachery of Whales ---


# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate value in the line
    crab_positions = [int(i) for i in input_data.read().split(",")]

# compute the fuel needed to move to each position
fuel = {}
for position in set(range(min(crab_positions), max(crab_positions))):
    fuel[position] = sum([abs(crab_position - position) for crab_position in crab_positions])

# identify which position, if the crabs align to it, requires the least amount
# of fuel to move to
best_position = min(fuel, key=fuel.get)

# the answer to the puzzle is the amount of fuel needed for the crabs to align
# to the best position
answer = fuel[best_position]

print("Answer:", answer)
