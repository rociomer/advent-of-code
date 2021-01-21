# --- Day 5: Sunny with a Chance of Asteroids ---
from copy import deepcopy


def run_program(program_memory : list, input_value : int) -> int:
    """Runs an intcode program. The output is the result of the diagnostic tests.
    """
    memory = deepcopy(program_memory)
    diagnostic_tests_output = []  # keep track of diagnostic test outputs (optcode 4)
    instruction_pointer = 0       # the address at the current instruction
    while memory[instruction_pointer] != 99:

        instruction = str(memory[instruction_pointer])
        if len(instruction) < 5:
            instruction = "0" * (5 - len(instruction)) + instruction

        two_digit_optcode = int(instruction[3:])
        mode_of_1st_param = int(instruction[2])
        mode_of_2nd_param = int(instruction[1])
        mode_of_3rd_param = int(instruction[0])  # will never be in position mode e.g. always be 0

        if two_digit_optcode in [1, 2, 7, 8]:
            # determine the values for the three integers following the instruction
            if mode_of_1st_param == 0:
                int1_address = memory[instruction_pointer + 1]
                int1 = memory[int1_address]
            elif mode_of_1st_param == 1:
                int1 = memory[instruction_pointer + 1]

            if mode_of_2nd_param == 0:
                int2_address = memory[instruction_pointer + 2]
                int2 = memory[int2_address]
            elif mode_of_2nd_param == 1:
                int2 = memory[instruction_pointer + 2]

            if mode_of_3rd_param == 0:
                new_address = memory[instruction_pointer + 3]
            elif mode_of_3rd_param == 1:
                raise ValueError

            # carry out the optcode instruction
            if two_digit_optcode == 1:
                memory[new_address] = int1 + int2
            elif two_digit_optcode == 2:
                memory[new_address] = int1 * int2
            elif two_digit_optcode == 7:
                memory[new_address] = int(int1 < int2)
            elif two_digit_optcode == 8:
                memory[new_address] = int(int1 == int2)

            instruction_pointer += 4
        elif two_digit_optcode in [3, 4]:
            # determine the values for the single integer following the instruction
            new_address = memory[instruction_pointer + 1]

            # carry out the optcode instruction
            if two_digit_optcode == 3:
                memory[new_address] = input_value
            elif two_digit_optcode == 4:
                output_value = memory[new_address]
                diagnostic_tests_output.append(output_value)

            instruction_pointer += 2
        elif two_digit_optcode in [5, 6]:
            # determine the values for the two integers following the instruction
            if mode_of_1st_param == 0:
                int1_address = memory[instruction_pointer + 1]
                int1 = memory[int1_address]
            elif mode_of_1st_param == 1:
                int1 = memory[instruction_pointer + 1]

            if mode_of_2nd_param == 0:
                int2_address = memory[instruction_pointer + 2]
                int2 = memory[int2_address]
            elif mode_of_2nd_param == 1:
                int2 = memory[instruction_pointer + 2]

            # carry out the optcode instruction
            if two_digit_optcode == 5 and int1:
                instruction_pointer = int2
            elif two_digit_optcode == 6 and not int1:
                instruction_pointer = int2
            else:
                instruction_pointer += 3

    # program ran successfully, this is the output
    return diagnostic_tests_output


def main():
    with open("input", "r") as input_data:
        # load the input program
        diagnostic_program = input_data.read().split(",")
        diagnostic_program[-1] = diagnostic_program[-1][:-1]  # remove the last trailing whitespace
        diagnostic_program = [int(i) for i in diagnostic_program]

    # run the program
    diagnostis_tests_results = run_program(program_memory=diagnostic_program, input_value=5)

    # the answer to the puzzle is the diagnostic code, which is the only number
    # output by the program before the halt instruction
    diagnostic_code = diagnostis_tests_results[0]

    print("Answer:", diagnostic_code)


if __name__ == "__main__":
    main()
