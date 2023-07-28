# --- Day 1: Not Quite Lisp ---

# load the input data
with open("input", "r") as input_data:
    # read entries, all on one line
    directions = input_data.read()

# calculate the number of floors to go up
floors_up = directions.count("(")

# calculate the number of floors to go down
floors_down = directions.count(")")

# the answer to the puzzle is the number of depth increases
answer = floors_up - floors_down

print("Answer:", answer)
