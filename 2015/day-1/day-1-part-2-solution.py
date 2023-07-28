# --- Day 1: Not Quite Lisp ---

# load the input data
with open("input", "r") as input_data:
    # read entries, all on one line
    directions = input_data.read()

# find the position of the first character that causes him to enter the basement (floor -1)
floor = 0
for idx, direction in enumerate(directions):
    floor += (int(bool(direction == ")"))*-2 + 1)
    if floor == -1:
        break

# the answer to the puzzle is the position (index + 1)
answer = idx + 1

print("Answer:", answer)
