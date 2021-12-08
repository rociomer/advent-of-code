# --- Day 8: Seven Segment Search ---


# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line
    raw_input = input_data.read().split("\n")

    # parse the input and separate it from the output
    input, output = [], []
    for line in raw_input:
        split_line = line.split(" | ")
        input.append(split_line[0].split(" "))
        output.append(split_line[1].split(" "))

# count the number of times the digits 1, 4, 7, and 8 appear in the output
count = 0
for line in output:
    for value in line:
        if len(value) in [2, 3, 4, 7]:
            count += 1

# the answer to the puzzle is the number of times the digits 1, 4, 7, and 8 appear
# in the output values
answer = count

print("Answer:", answer)
