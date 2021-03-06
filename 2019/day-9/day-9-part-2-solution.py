# --- Day 9: Sensor Boost ---


class Intcode_computer():
    """A complete Intcode computer.

    Example usage:
    >> computer = Intcode_computer(memory)
    >> output = computer.run_program(input_value, instruction_pointer)
    """
    def __init__(self, memory : dict) -> None:
        """Initializes Intcode computer.
        """
        self.memory = memory

    def get_memory_address(self, address : int) -> int:
        """Gets the value at the indicated memory address, and if it does not exist,
        it creates it.
        """
        try:
            value = self.memory[address]
        except KeyError:  # address does not exist yet, so create it
            self.memory[address] = 0
            value =self.memory[address]

        return value

    def run_program(self, input_value : int, instruction_pointer : int) -> list:
        """Runs an intcode program. The first time a program is run, the `input_value`
        should be the phase setting. The `instruction_pointer` is the address at the
        current instruction. Output is returned when a program reaches optcode 99.
        """
        relative_base = 0  # for mode 2 (relative mode)
        output =[]         # initialize
        while self.memory[instruction_pointer] != 99:

            instruction = str(self.memory[instruction_pointer])
            if len(instruction) < 5:
                instruction = "0" * (5 - len(instruction)) + instruction

            two_digit_optcode = int(instruction[3:])
            mode_of_1st_param = int(instruction[2])
            mode_of_2nd_param = int(instruction[1])
            mode_of_3rd_param = int(instruction[0])  # will never be in position mode e.g. always be 0

            if two_digit_optcode in [1, 2, 7, 8]:  # optcodes with 3 parameters
                # determine the values for the three integers following the instruction
                if mode_of_1st_param == 0:    # mode 0 (position mode)
                    int1_address = self.memory[instruction_pointer + 1]
                    int1 = self.get_memory_address(address=int1_address)

                elif mode_of_1st_param == 1:  # mode 1 (immediate mode)
                    int1 = self.memory[instruction_pointer + 1]
                elif mode_of_1st_param == 2:  # mode 2 (relative mode)
                    int1_address = self.memory[instruction_pointer + 1] + relative_base
                    int1 = self.get_memory_address(address=int1_address)

                if mode_of_2nd_param == 0:    # mode 0 (position mode)
                    int2_address = self.memory[instruction_pointer + 2]
                    int2 = self.get_memory_address(address=int2_address)
                elif mode_of_2nd_param == 1:  # mode 1 (immediate mode)
                    int2 = self.memory[instruction_pointer + 2]
                elif mode_of_2nd_param == 2:  # mode 2 (relative mode)
                    int2_address = self.memory[instruction_pointer + 2] + relative_base
                    int2 = self.get_memory_address(address=int2_address)

                if mode_of_3rd_param == 0:    # mode 0 (position mode)
                    new_address = self.memory[instruction_pointer + 3]
                elif mode_of_3rd_param == 1:  # mode 1 (immediate mode)
                    raise ValueError
                elif mode_of_3rd_param == 2:  # mode 2 (relative mode)
                    new_address = self.memory[instruction_pointer + 3] + relative_base

                # carry out the optcode instruction
                if two_digit_optcode == 1:
                    self.memory[new_address] = int1 + int2
                elif two_digit_optcode == 2:
                    self.memory[new_address] = int1 * int2
                elif two_digit_optcode == 7:
                    self.memory[new_address] = int(int1 < int2)
                elif two_digit_optcode == 8:
                    self.memory[new_address] = int(int1 == int2)

                instruction_pointer += 4

            elif two_digit_optcode in [3, 4, 9]:  # optcodes with 1 parameter
                # determine the values for the single integer following the instruction
                if mode_of_1st_param == 0:    # mode 0 (position mode)
                    new_address = self.memory[instruction_pointer + 1]
                elif mode_of_1st_param == 1:  # mode 1 (immediate mode)
                    new_address = instruction_pointer + 1
                elif mode_of_1st_param == 2:  # mode 2 (relative mode)
                    new_address = self.memory[instruction_pointer + 1] + relative_base

                # carry out the optcode instruction
                if two_digit_optcode == 3:
                    # the phase setting should only be used as input the 1st
                    # time input is needed, then we use the default input value
                    self.memory[new_address] = input_value
                elif two_digit_optcode == 4:
                    output_value = self.get_memory_address(address=new_address)
                    output.append(output_value)
                elif two_digit_optcode == 9:
                    base_value = self.get_memory_address(address=new_address)
                    relative_base += base_value

                instruction_pointer += 2

            elif two_digit_optcode in [5, 6]:  # optcodes with 2 parameters
                # determine the values for the two integers following the instruction
                if mode_of_1st_param == 0:    # mode 0 (position mode)
                    int1_address = self.memory[instruction_pointer + 1]
                    int1 = self.get_memory_address(address=int1_address)
                elif mode_of_1st_param == 1:  # mode 1 (immediate mode)
                    int1 = self.memory[instruction_pointer + 1]
                elif mode_of_1st_param == 2:  # mode 2 (relative mode)
                    int1_address = self.memory[instruction_pointer + 1] + relative_base
                    int1 = self.get_memory_address(address=int1_address)

                if mode_of_2nd_param == 0:    # mode 0 (position mode)
                    int2_address = self.memory[instruction_pointer + 2]
                    int2 = self.get_memory_address(address=int2_address)
                elif mode_of_2nd_param == 1:  # mode 1 (immediate mode)
                    int2 = self.memory[instruction_pointer + 2]
                elif mode_of_2nd_param == 2:  # mode 2 (relative mode)
                    int2_address = self.memory[instruction_pointer + 2] + relative_base
                    int2 = self.get_memory_address(address=int2_address)

                # carry out the optcode instruction
                if two_digit_optcode == 5 and int1:
                    instruction_pointer = int2
                elif two_digit_optcode == 6 and not int1:
                    instruction_pointer = int2
                else:
                    instruction_pointer += 3

        # program runs until reaching the `halt` instruction
        return output


def main():
    with open("input", "r") as input_data:
        # load the BOOST program
        BOOST_program = input_data.read().split(",")
        BOOST_program[-1] = BOOST_program[-1][:-1] # remove the trailing newline
        BOOST_program = [int(i) for i in BOOST_program]

    # convert the BOOST program into a dictionary
    BOOST_program_dict = dict(zip(range(len(BOOST_program)), BOOST_program))

    # run the program using the input program and the input value of 2 ("sensor boost mode")
    intcode_computer = Intcode_computer(memory=BOOST_program_dict)
    BOOST_keycode = intcode_computer.run_program(input_value=2,
                                                 instruction_pointer=0)

    # the answer to the puzzle is the output (aka the BOOST keycode), which should be the
    # only output of the program if it ran correctly
    answer = BOOST_keycode[0]

    print("Answer:", answer)


if __name__ == "__main__":
    main()
