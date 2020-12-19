# --- Day 13: Shuttle Search ---


def get_earliest_departure_time(bus_id : int, earliest_timestamp : int) -> int:
    """Gets the earliest possible departure time for the bus that departs every
    `bus_id` minutes (since time 0), that is also after the `earliest_timestamp`.
    """
    departure_time = 0
    while departure_time < earliest_timestamp:
        departure_time += bus_id
    return departure_time


def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        bus_schedule_notes = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # the earliest timestamp of departure is the first line of the input
    earliest_timestamp = int(bus_schedule_notes[0])

    # find the available buses
    available_buses = bus_schedule_notes[1].split(",")
    while "x" in available_buses:  # remove the unavailable buses from the list
        available_buses.remove("x")
    available_buses = [int(bus) for bus in available_buses]  # convert from str to int

    # get the earliest departure time for each bus after `earliest_timestamp`
    departure_times = []
    for bus in available_buses:
        earliest_departure_time = get_earliest_departure_time(bus_id=bus,
                                                              earliest_timestamp=earliest_timestamp)
        departure_times.append(earliest_departure_time)

    # find which bus departs first (`earliest_bus_id`), and how long you would 
    # have to wait for it to depart (`wait_minutes`)
    ealiest_bus_departure_timestamp =min(departure_times)
    ealiest_bus_departure_timestamp_idx = departure_times.index(ealiest_bus_departure_timestamp)
    earliest_bus_id = available_buses[ealiest_bus_departure_timestamp_idx]

    wait_minutes = ealiest_bus_departure_timestamp - earliest_timestamp

    # calculate the answer to the puzzle
    answer = earliest_bus_id * wait_minutes

    print("Answer:", answer)


if __name__ == "__main__":
    main()
