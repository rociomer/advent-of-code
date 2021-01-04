# --- Day 1: The Tyranny of the Rocket Equation ---


def get_fuel_requirement(mass : int) -> int:
    """Gets the recursive fuel requirement for a given input mass (i.e. the fuel
    required to transport the input mass will also need to be transported, thus
    requiring additional fuel).
    """
    fuel_weight = mass//3 - 2
    if fuel_weight >= 9:  # anything less than 9 will give a negative number
        fuel_weight += get_fuel_requirement(mass=fuel_weight)
    return fuel_weight

with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    module_mass = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # convert to integers
    module_mass = [int(i) for i in module_mass]

# calculate the fuel requirement for each module based on its mass
fuel_requirements = [get_fuel_requirement(mass=mass) for mass in module_mass]

# the answer to the puzzle is the sum of the recursive fuel requirements
answer = sum(fuel_requirements)

print("Answer:", answer)