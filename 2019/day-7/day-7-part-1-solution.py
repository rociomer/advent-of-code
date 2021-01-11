# --- Day 7: Amplification Circuit ---
from copy import deepcopy
import itertools


def run_program(program_memory : list, input_value : int, phase_setting : int) -> int:
    """Runs an intcode program. The phase setting is a value from 0 to 4.
    The output is the result of the diagnostic tests.
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
            # determine the values for the single integers following the instruction
            new_address = memory[instruction_pointer + 1]

            # carry out the optcode instruction
            if two_digit_optcode == 3:
                memory[new_address] = phase_setting
                # the phase setting should only be used as input the 1st
                # time input is needed, then we use the default input value
                phase_setting = input_value
            elif two_digit_optcode == 4:
                output_value = memory[new_address]
                diagnostic_tests_output.append(output_value)

            instruction_pointer += 2
        elif two_digit_optcode in [5, 6]:
            # determine the values for the single integers following the instruction
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

    # program ran successfully; the output is the final element of
    # `diagnostic_tests_output`
    output = diagnostic_tests_output[-1]
    return output


def main():
    with open("input", "r") as input_data:
        # load the input software
        amplifier_controller_software = input_data.read().split(",")
        amplifier_controller_software[-1] = amplifier_controller_software[-1][:-1] # remove the trailing newline
        amplifier_controller_software = [int(i) for i in amplifier_controller_software]

    # get all possible permutations of [0, 1, 2, 3, 4]
    phase_settings_permutations = list(
        itertools.permutations([0, 1, 2, 3, 4])
    )

    # each amplifier will need to run a copy of the program using a different
    # permutation of the phase settings; we will keep track of the output for
    # each permutation
    output_to_thrusters = []
    for phase_settings in phase_settings_permutations:
        amp_A_output = run_program(program_memory=amplifier_controller_software,
                                   input_value=0,
                                   phase_setting=phase_settings[0])
        amp_B_output = run_program(program_memory=amplifier_controller_software,
                                   input_value=amp_A_output,
                                   phase_setting=phase_settings[1])
        amp_C_output = run_program(program_memory=amplifier_controller_software,
                                   input_value=amp_B_output,
                                   phase_setting=phase_settings[2])
        amp_D_output = run_program(program_memory=amplifier_controller_software,
                                   input_value=amp_C_output,
                                   phase_setting=phase_settings[3])
        amp_E_output = run_program(program_memory=amplifier_controller_software,
                                   input_value=amp_D_output,
                                   phase_setting=phase_settings[4])
        output_to_thrusters.append(amp_E_output)

    # the answer to the puzzle is the largest possible output signal
    # that can be sent to the thrusters
    answer = max(output_to_thrusters)

    print("Answer:", answer)


if __name__ == "__main__":
    main()
