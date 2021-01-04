# --- Day 8: Handheld Halting ---


with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    code = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

# create a list of same length as the code to keep track of if a line has been visited before
times_line_visited = [0] * len(code)

# loop over the code
init_state_idx = 0  # the initial code state
accumulator = 0     # accumulator state

next_state_idx = init_state_idx
while max(times_line_visited) <= 1:  # while still in the first loop

    next_state = code[next_state_idx]        # move to next code state
    times_line_visited[next_state_idx] += 1  # keep track of lines visited

    # get next state index and accumulator value from code instruction
    if "nop" in next_state:
        next_state_idx += 1
        acc_value = 0
    elif "acc" in next_state:
        next_state_idx += 1 
        acc_value = int(next_state[4:])
    elif "jmp" in next_state:
        next_state_idx += int(next_state[4:])
        acc_value = 0
    else:
        raise ValueError

    accumulator += acc_value

# as loop breaks as soon as any instruction is run a second time, the value
# of the accumulator before exiting is the value just before the "invalid" instruction
accumulator_value_before_exiting = accumulator - acc_value

print("Answer:", accumulator_value_before_exiting)