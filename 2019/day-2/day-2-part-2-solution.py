# --- Day 2: 1202 Program Alarm ---
from copy import deepcopy
from typing import Tuple


def run_program(program_memory : list) -> int:
    """Runs an intcode program. The output is the value at memory address 0.
    Modified the variables to use the terminology provided.
    """
    memory = deepcopy(program_memory)
    instruction_pointer = 0  # the address at the current instruction
    while memory[instruction_pointer] != 99:

        int1_address = memory[instruction_pointer + 1]
        int2_address = memory[instruction_pointer + 2]
        int1 = memory[int1_address]
        int2 = memory[int2_address]

        new_address = memory[instruction_pointer + 3]

        if new_address >= len(memory):
            # invalid address
            return None
        elif memory[instruction_pointer] == 1:
            memory[new_address] = int1 + int2
        elif memory[instruction_pointer] == 2:
            memory[new_address] = int1 * int2

        instruction_pointer += 4

        # check if 99 still in memory
        if 99 not in memory:
            # prevent an infinite loop
            return None

    # program ran successfully, this is the output
    return memory[0]  # the output


def find_noun_and_verb(program : list) -> Tuple[int, int]:
    """Tries different values for the noun and verb until the output of the gravity
    assist program is equal to 19690720.
    """
    for noun in range(len(program)):
        for verb in range(len(program)):

            # change the addresses at positions 1 and 2
            program[1] = noun
            program[2] = verb

            # run the program
            output = run_program(program_memory=program)

            if output == 19690720:
                return noun, verb

    # this part should never be reached
    return None, None


def main():
    with open("input", "r") as input_data:
        # read entries; each entry is separated by a comma
        gravity_assist_program = input_data.read().split(",")
    
        # convert to integers
        gravity_assist_program = [int(i) for i in gravity_assist_program]
    
        # find values of the noun and verb which cause the program to output 19690720
        noun, verb = find_noun_and_verb(program=gravity_assist_program)
    
    # the answer to the puzzle is equal to 100 * noun + verb
    answer = 100 * noun + verb
    
    print("Answer:", answer)


if __name__ == "__main__":
    main()
