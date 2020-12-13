# --- Day 8: Handheld Halting ---
# Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next to you.
#
# Their handheld game console won't turn on! They ask if you can take a look.
#
# You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should be able to fix it, but first you need to be able to run the code in isolation.
#
# The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).
#
# acc increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the instruction immediately below it is executed next.
# jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
# nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
# For example, consider the following program:
#
# nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6
# These instructions are visited in this order:
#
# nop +0  | 1
# acc +1  | 2, 8(!)
# jmp +4  | 3
# acc +3  | 6
# jmp -3  | 7
# acc -99 |
# acc +1  | 4
# jmp -4  | 5
# acc +6  |
# First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes, setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to continue back at the first acc +1.
#
# This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to run any instruction a second time, you know it will never terminate.
#
# Immediately before the program would run an instruction a second time, the value in the accumulator is 5.
#
# Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?
#
# --- Part Two ---
# After some careful analysis, you believe that exactly one instruction is corrupted.
#
# Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions were harmed in the corruption of this boot code.)
#
# The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.
#
# For example, consider the same program from above:
#
# nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6
# If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find another jmp instruction and loop forever.
#
# However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions are visited in this order:
#
# nop +0  | 1
# acc +1  | 2
# jmp +4  | 3
# acc +3  |
# jmp -3  |
# acc -99 |
# acc +1  | 4
# nop -4  | 5
# acc +6  | 6
# After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).
#
# Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
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