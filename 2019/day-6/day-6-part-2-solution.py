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

    # get the path of objects from SAN to COM
    com = orbit_dict["SAN"]
    santa_path = [com]
    while com != "COM":
        com = orbit_dict[com]
        santa_path.append(com)

    # get the number of orbital transfers required to move from the
    # object YOU are orbiting to the first object on SAN's path
    n_orbital_transfers = 0
    com = orbit_dict["YOU"]
    while com not in santa_path:
        com = orbit_dict[com]
        n_orbital_transfers += 1

    # now just add the number of orbital transfers back to SAN from the inter-
    # secting object on SAN's path, which is the same as its index on `santa_path`
    n_orbital_transfers += santa_path.index(com)

    # the answer to the puzzle is the minimum number of orbital transfers required
    # to move from the object YOU are orbiting to the object SAN is orbiting
    print("Answer:", n_orbital_transfers)


if __name__ == "__main__":
    main()
