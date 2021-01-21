# --- Day 7: Amplification Circuit ---
from typing import Tuple
from copy import deepcopy
import itertools


def run_program(memory : list,
                input_value : int,
                instruction_pointer : int,
                return_when_input_used : bool=False) -> Tuple[list, int, int]:
    """Runs an intcode program. The first time a program is run, the `input_value`
    should be the phase setting. The `instruction_pointer` is the address at the
    current instruction. Output is returned when a program reaches optcode 4 or 99,
    and it returns the current memory state, the output value, and the current
    instruction pointer (in that order).
    """
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
                # the phase setting should only be used as input the 1st
                # time input is needed, then we use the default input value
                memory[new_address] = input_value
                if return_when_input_used:
                    return memory, False, instruction_pointer + 2
            elif two_digit_optcode == 4:
                output_value = memory[new_address]
                return memory, output_value, instruction_pointer + 2

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

    # program ran until reaching the `halt` instruction
    return memory, False, 0

def run_feedback_loop(shared_memory : list, phase_settings : list) -> int:
    """Runs the Amplifier Controller Software in feedback loop mode. Each
    feedback loop runs until Amp E reaches a halt instruction (optcode 99).
    The output which is then sent to the thrusters is the second to last
    Amp E output, which is what is returned by this function.
    """
    # initialize separate memories for each of the five amplifiers
    amp_A_memory = deepcopy(shared_memory)
    amp_B_memory = deepcopy(shared_memory)
    amp_C_memory = deepcopy(shared_memory)
    amp_D_memory = deepcopy(shared_memory)
    amp_E_memory = deepcopy(shared_memory)

    # initialize the instruction pointers for each amplifier
    amp_A_instruction_pointer = 0
    amp_B_instruction_pointer = 0
    amp_C_instruction_pointer = 0
    amp_D_instruction_pointer = 0
    amp_E_instruction_pointer = 0

    # initially, the phase settings should be used exactly once by each amplifier
    amp_A_memory, amp_A_output, amp_A_instruction_pointer = run_program(
        memory=amp_A_memory,
        input_value=phase_settings[0],
        instruction_pointer=amp_A_instruction_pointer,
        return_when_input_used=True
    )
    amp_B_memory, amp_B_output, amp_B_instruction_pointer = run_program(
        memory=amp_B_memory,
        input_value=phase_settings[1],
        instruction_pointer=amp_B_instruction_pointer,
        return_when_input_used=True
    )
    amp_C_memory, amp_C_output, amp_C_instruction_pointer = run_program(
        memory=amp_C_memory,
        input_value=phase_settings[2],
        instruction_pointer=amp_C_instruction_pointer,
        return_when_input_used=True
    )
    amp_D_memory, amp_D_output, amp_D_instruction_pointer = run_program(
        memory=amp_D_memory,
        input_value=phase_settings[3],
        instruction_pointer=amp_D_instruction_pointer,
        return_when_input_used=True
    )
    amp_E_memory, amp_E_output, amp_E_instruction_pointer = run_program(
        memory=amp_E_memory,
        input_value=phase_settings[4],
        instruction_pointer=amp_E_instruction_pointer,
        return_when_input_used=True
    )

    # then, Amp A should use see 0 as input
    amp_A_memory, amp_A_output, amp_A_instruction_pointer = run_program(
        memory=amp_A_memory,
        input_value=0,
        instruction_pointer=amp_A_instruction_pointer,
    )

    # now, go into the feedback loop, using the output from the previous
    # amplifier as input to the next
    while True:
        amp_B_memory, amp_B_output, amp_B_instruction_pointer = run_program(
            memory=amp_B_memory,
            input_value=amp_A_output,
            instruction_pointer=amp_B_instruction_pointer,
        )
        amp_C_memory, amp_C_output, amp_C_instruction_pointer = run_program(
            memory=amp_C_memory,
            input_value=amp_B_output,
            instruction_pointer=amp_C_instruction_pointer,
        )
        amp_D_memory, amp_D_output, amp_D_instruction_pointer = run_program(
            memory=amp_D_memory,
            input_value=amp_C_output,
            instruction_pointer=amp_D_instruction_pointer,
        )
        amp_E_memory, amp_E_output, amp_E_instruction_pointer = run_program(
            memory=amp_E_memory,
            input_value=amp_D_output,
            instruction_pointer=amp_E_instruction_pointer,
        )

        if amp_E_output == False:
            break

        # otherwise, continue into the next loop
        amp_A_memory, amp_A_output, amp_A_instruction_pointer = run_program(
            memory=amp_A_memory,
            input_value=amp_E_output,
            instruction_pointer=amp_A_instruction_pointer,
        )

        output = amp_E_output

    # the output should be the last Amp E output
    return output


def main():
    with open("input", "r") as input_data:
        # load the input software
        amplifier_controller_software = input_data.read().split(",")
        amplifier_controller_software[-1] = amplifier_controller_software[-1][:-1] # remove the trailing newline
        amplifier_controller_software = [int(i) for i in amplifier_controller_software]

    # get all possible permutations of [5, 6, 7, 8, 9]
    phase_settings_permutations = list(
        itertools.permutations([5, 6, 7, 8, 9])
    )

    # each amplifier will need to run a copy of the program using a different
    # permutation of the phase settings; we will keep track of the output for
    # each permutation in `output_to_thrusters`
    output_to_thrusters = []
    for phase_settings in phase_settings_permutations:
        # now the program runs using the feedback loop arrangement
        output = run_feedback_loop(shared_memory=amplifier_controller_software,
                                   phase_settings=list(phase_settings))
        output_to_thrusters.append(output)

    # the answer to the puzzle is the largest possible output signal
    # that can be sent to the thrusters
    answer = max(output_to_thrusters)

    print("Answer:", answer)


if __name__ == "__main__":
    main()
