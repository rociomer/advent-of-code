# --- Day 6: Universal Orbit Map ---


def main():
    with open("input", "r") as input_data:
        # load the input program
        local_orbit_map = input_data.read().split("\n")[:-1]

    # create a dictionary from the local orbit map
    orbit_dict = {}
    for line in local_orbit_map:
        com, orbiter = line.split(")")
        orbit_dict[orbiter] = com

    # get the number of direct and indirect orbits
    n_direct_orbits = 0
    n_indirect_orbits = 0
    for orbiter in orbit_dict.keys():
        com = orbit_dict[orbiter]
        n_direct_orbits += 1
        while com != "COM":
            com = orbit_dict[com]
            n_indirect_orbits += 1

    # the answer to the puzzle is the total number of direct and indirect
    # orbits in the map data
    answer = n_direct_orbits + n_indirect_orbits

    print("Answer:", answer)


if __name__ == "__main__":
    main()
