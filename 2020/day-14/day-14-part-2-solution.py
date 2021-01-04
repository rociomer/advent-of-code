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
       
        #convert the address to binary
        memory_address_binary = bin(int(memory_address))[2:]
        memory_address_padded = "0" * (len(system_state["mask"]) - len(memory_address_binary)) + memory_address_binary

        # then apply the mask to the binary representation
        memory_address_masked = ""
        for idx, token in enumerate(system_state["mask"]):
            if token == "1":
                memory_address_masked += "1"
            elif token == "0":
                memory_address_masked += memory_address_padded[idx]
            else:
                memory_address_masked += "X"

        # get all possible memory addresses
        possible_memory_addresses = get_possible_memory_addresses(address=memory_address_masked)

        # write the value to memory for each possible memory address
        for address in possible_memory_addresses:
            system_state[address] = int(memory_value)
    
    return system_state


def get_possible_memory_addresses(address : str) -> list:
    """Since floating numbers ("X"s) in the memory address can take on values
    of 0 or 1, this function calculates all possible memory addresses which can
    me made from an address with floating numbers.
    """
    possible_memory_addresses = [address]
    while "X" in possible_memory_addresses[0]:

        # we will keep track of the updated memory addresses in a new list
        updated_memory_addresses = []

        for address in possible_memory_addresses:
            # a note on how replace works:
            # replace(substring to replace, string to replace it with, first nth occurences)
            address_1 = address.replace("X", "0", 1)
            address_2 = address.replace("X", "1", 1)

            # add the updated addresses to `updated_memory_addresses`
            updated_memory_addresses.append(address_1)
            updated_memory_addresses.append(address_2)

        # remove the old version of the addresses, which still have the float, by
        # overwriting with the updated memory addresses
        possible_memory_addresses = updated_memory_addresses
    return possible_memory_addresses


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
        decimal_value = system_state[memory_address]
        memory_sum += decimal_value

    print("Answer:", memory_sum)


if __name__ == "__main__":
    main()
