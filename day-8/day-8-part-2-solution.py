# --- Day 8: Handheld Halting ---
from typing import Tuple


def switch_two_states(state_1 : str, state_2 : str, code : list, line_idx : int) -> list:
    """Flip state 1 and state 2 at a specific line in the code.
    """
    if state_1 in code[line_idx]:
        code[line_idx] = state_2 + code[line_idx][3:]
    elif state_2 in code[line_idx]:
        code[line_idx] = state_1 + code[line_idx][3:]
    return code


def does_code_run_successfully(code : str) -> Tuple[bool, int]:
    """Returns True and the accumulator value if code runs successfully. Otherwise
    returns False and the accumulator value before the code fails.
    """
    # create a list of same length as the code to keep track of if a line has been visited before
    times_line_visited = [0] * len(code)

    # initialize some values before starting to loop through the code
    init_state_idx = 0             # the initial code state
    accumulator = 0                # accumulator state
    code_ran_successfully = False  # will switch to True once the code runs successfully

    # loop over the code
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

        # check for indices which point to non-existing lines in the code, in which case exit the loop
        if next_state_idx < 0 or next_state_idx >= len(code):
            break

    # check if the code ran successfully: this means 1) no infinite loops, and
    # 2) the final line should point to the "next" line (e.g. line number +1)
    code_ran_successfully = (
        bool(max(times_line_visited) == 1) and
        next_state_idx == len(code)
    )

    return code_ran_successfully, accumulator


def main():
    # load the data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        code = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # we will solve this problem the brute force way, and try changing each "nop" instruction
    # to "jmp", and vice versa, one by one, until the code runs successfully, with
    # the additional constraint that the final command in `code` must point to the next line
    for state_idx in range(len(code)):

        # change "nop" to "jmp", or vice versa, for the line defined by `state_idx`
        code = switch_two_states(state_1="nop", state_2="jmp", code=code, line_idx=state_idx)

        # now rerun the code with the changed instruction
        code_ran_successfully, accumulator = does_code_run_successfully(code=code)

        # if all the criteria met, break out of the for loop and print the answer
        if code_ran_successfully:
            break

        # otherwise, change "nop" or "jmp" back to what it was originally so we can try again
        code = switch_two_states(state_1="nop", state_2="jmp", code=code, line_idx=state_idx)

    print("Answer:", accumulator)


if __name__ == "__main__":
    main()