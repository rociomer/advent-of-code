# --- Day 2: 1202 Program Alarm ---


def run_program(program : list) -> list:
    """Runs an intcode program and returns the updated program.
    """
    position = 0
    while program[position] != 99:

        int1_position = program[position + 1]
        int2_position = program[position + 2]
        int1 = program[int1_position]
        int2 = program[int2_position]

        new_position = program[position + 3]

        if program[position] == 1:
            program[new_position] = int1 + int2
        elif program[position] == 2:
            program[new_position] = int1 * int2

        position += 4

    return program


with open("input", "r") as input_data:
    # read entries; each entry is separated by a comma
    gravity_assist_program = input_data.read().split(",")

    # convert to integers
    gravity_assist_program = [int(i) for i in gravity_assist_program]

    # before running the code, restore it to the "1202 program alarm" state
    gravity_assist_program[1] = 12
    gravity_assist_program[2] = 2

    # run the program
    gravity_assist_program = run_program(program=gravity_assist_program)

# the answer to the puzzle is the value at position 0 after the program halts
answer = gravity_assist_program[0]

print("Answer:", answer)