# --- Day 3: Gear Ratios ---
import re

# define some functions
def near_symbol(number_positions, symbol_positions):
    for digit_position in number_positions:
        for symbol_position in symbol_positions:
            if distance_1(digit_position, symbol_position):
                return True
    return False

def distance_1(xy1, xy2):
    x1 = xy1[0]
    y1 = xy1[1]
    x2 = xy2[0]
    y2 = xy2[1]
    if abs(x1-x2) <= 1 and abs(y1-y2) <= 1:
        return True
    return False

# load the input data
with open("input", "r") as input_data:
    # read entries
    engine_schematic = input_data.read().split("\n")

# find the symbol positions
symbol_positions = []
for y_pos, row in enumerate(engine_schematic):
    row_symbols_only = re.sub("[0-9]|\.", "", row)
    for symbol in row_symbols_only:
        x_pos = row.index(symbol)
        row = row.replace(symbol, " ", 1)
        symbol_positions.append([y_pos, x_pos])

# for each number in the engine schematic, determine if it is a part number
# (close to a symbol)
part_numbers = []
for y_pos, row in enumerate(engine_schematic):
    row_digits_only = re.sub("[^0-9]", " ", row)
    # first get the numbers in that row
    numbers = row_digits_only.split()  # works for arbitrary number of spaces
    # then loop over each number to check if it is near symbol
    for number in numbers:
        init_position    = row.index(number)
        number_positions = [[y_pos, x_pos] for x_pos in range(init_position, init_position+len(number))]
        if near_symbol(number_positions, symbol_positions):
            part_numbers.append(int(number))
        row = row.replace(number, " "*len(number), 1)

# the answer to the puzzle is the sum of all the part numbers
answer = sum(part_numbers)

print("Answer:", answer)
