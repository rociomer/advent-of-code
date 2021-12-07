# --- Day 6: Lanternfish ---
from copy import deepcopy


# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    fish_internal_timers = [int(i) for i in input_data.read().split(",")]

    # convert to a dict to more efficiently keep track of the fish population
    # keys == timers, values == counts
    fish_tracker = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
    }
    for timer in set(fish_internal_timers):
        fish_tracker[timer] += fish_internal_timers.count(timer)

# simulate the fish
fish_tracker_copy = deepcopy(fish_tracker)
for day in range(256):
    fish_tracker[8] += fish_tracker_copy[0] - fish_tracker_copy[8]
    fish_tracker[7] += fish_tracker_copy[8] - fish_tracker_copy[7]
    fish_tracker[6] += fish_tracker_copy[7] + fish_tracker_copy[0] - fish_tracker_copy[6]
    fish_tracker[5] += fish_tracker_copy[6] - fish_tracker_copy[5]
    fish_tracker[4] += fish_tracker_copy[5] - fish_tracker_copy[4]
    fish_tracker[3] += fish_tracker_copy[4] - fish_tracker_copy[3]
    fish_tracker[2] += fish_tracker_copy[3] - fish_tracker_copy[2]
    fish_tracker[1] += fish_tracker_copy[2] - fish_tracker_copy[1]
    fish_tracker[0] += fish_tracker_copy[1] - fish_tracker_copy[0]
    fish_tracker_copy = deepcopy(fish_tracker)

# the answer to the puzzle is the number of lanternfish present after 256 days
answer = sum([value for value in fish_tracker.values()])

print("Answer:", answer)
