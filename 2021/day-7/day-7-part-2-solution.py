# --- Day 7: The Treachery of Whales ---

def get_fuel_expense(dist : int) -> int:
    """
    Calculates the expense of the fuel for a crab to travel a distance of
    length `dist`.
    """
    cost_of_each_step = [0] + list(range(1, dist+1))
    return sum(cost_of_each_step)

# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate value in the line
    crab_positions = [int(i) for i in input_data.read().split(",")]

# compute the fuel needed to move to each position
fuel = {}
for position in set(range(min(crab_positions), max(crab_positions))):
    fuel_expense = [
        get_fuel_expense(dist=abs(crab_position - position)) for crab_position in crab_positions
    ]
    fuel[position] = sum(fuel_expense)

# identify which position, if the crabs align to it, requires the least amount
# of fuel to move to
best_position = min(fuel, key=fuel.get)

# the answer to the puzzle is the amount of fuel needed for the crabs to align
# to the best position
answer = fuel[best_position]

print("Answer:", answer)
