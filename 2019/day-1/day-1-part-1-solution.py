# --- Day 1: The Tyranny of the Rocket Equation ---


with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    module_mass = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # convert to integers
    module_mass = [int(i) for i in module_mass]

# calculate the fuel requirement for each module based on its mass
fuel_requirements = [mass//3 - 2 for mass in module_mass]

# the answer to the puzzle is the sum of the fuel requirements
answer = sum(fuel_requirements)

print("Answer:", answer)