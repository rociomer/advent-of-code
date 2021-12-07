# --- Day 6: Lanternfish ---


# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    fish_internal_timers = [int(i) for i in input_data.read().split(",")]

# simulate the fish
for day in range(80):
    fish_internal_timers = [timer - 1 for timer in fish_internal_timers]
    num_new_fish = fish_internal_timers.count(-1)
    fish_internal_timers = [6 if timer == -1 else timer for timer in fish_internal_timers]
    fish_internal_timers += [8]*num_new_fish

# the answer to the puzzle is the number of lanternfish present after 80 days
answer = len(fish_internal_timers)

print("Answer:", answer)
