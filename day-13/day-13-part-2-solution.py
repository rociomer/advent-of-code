# --- Day 13: Shuttle Search ---
import math

def lcm(a : int, b : int) -> int:
    """Returns the least common multiple of two integers.
    """
    return abs(a*b) // math.gcd(a, b)

def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        bus_schedule_notes = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # find the available buses
    available_buses_str = bus_schedule_notes[1].split(",")
    
    # convert available buses to int
    available_buses = []
    for bus in available_buses_str:
        if bus == "x":
            available_buses.append(0)
        else:
            available_buses.append(int(bus))

    # for speed-up purposes, find the "rarest" bus runnign in the timetable
    rarest_bus_idx = available_buses.index(max(available_buses))

    # search for the earliest timestamp such that the first bus ID departs at that
    # time and each subsequent listed bus ID departs at that subsequent minute

    # set the initial timestep to the period of the first bus
    timestep = available_buses[0]

    # the first possible timestamp is when the first bus departs
    possible_timestamp = timestep

    # loop over all the buses and check that they satisfy the "remainder" criteria
    for idx, bus in enumerate(available_buses):
        if bus:  # if bus is not 0 (i.e. "x")
            while (possible_timestamp + idx) % bus:  # while "remainder" criteria remain unsatisfied
                possible_timestamp += timestep
            # update the timestep with the lowest common multiple (LCM) of the 
            # current bus and the current timestep
            timestep = lcm(timestep, bus)

    print("Answer:", possible_timestamp)


if __name__ == "__main__":
    main()
