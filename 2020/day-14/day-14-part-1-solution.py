# --- Day 14: Docking Data ---
from typing import Tuple


def extract_action(instruction : str) -> Tuple[str, str]:
    """Extracts the action from a given instruction from the initialization program.
    """
    if instruction[:3] == "mas":
        action = "mask"
        value = instruction[7:]
    else:
        action = "memory write"
        memory_write_instruction = instruction.split("=")
        value = memory_write_instruction[0][4:-2] + "," + memory_write_instruction[1]

    return action, value

def apply_action(system_state : dict, action : str, value : str) -> dict:
    """Applies the action to the current system state and returns the new system state.
    """
    if action == "mask":  # save the new mask
        system_state["mask"] = value
    else:  # write to memory
        # first get the value to save, and the address
        memory_address, memory_value = value.split(",")

        # convert the value to binary
        memory_value_binary = bin(int(memory_value))[2:]
        memory_value_padded = "0" * (len(system_state["mask"]) - len(memory_value_binary)) + memory_value_binary

        # then apply the mask to the binary representation
        memory_value_masked = ""
        for idx, token in enumerate(system_state["mask"]):
            if token == "1":
                memory_value_masked += "1"
            elif token == "0":
                memory_value_masked += "0"
            else:
                memory_value_masked += memory_value_padded[idx]

        system_state[int(memory_address)] = memory_value_masked
    
    return system_state

def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        initialization_program = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # initialize the state of the system as an empty dictionary
    system_state = {}

    # loop through instructions in the initialization program
    for instruction in initialization_program:
        action, value = extract_action(instruction=instruction)
        system_state = apply_action(system_state=system_state, 
                                    action=action, 
                                    value=value)

    # once the initialization program is complete, sum all the values left in memory
    # and return their decimal form
    memory_sum = 0
    memory_addresses = [i for i in system_state.keys()]
    memory_addresses.remove("mask")  # remove the "mask" key, as it is not an address
    for memory_address in memory_addresses:
        binary_value = system_state[memory_address]
        decimal_value = int("0b" + binary_value, 2)
        memory_sum += decimal_value

    print("Answer:", memory_sum)


if __name__ == "__main__":
    main()
