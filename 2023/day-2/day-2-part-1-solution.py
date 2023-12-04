# --- Day 2: Cube Conundrum ---
import re

# load the input data
with open("input", "r") as input_data:
    # read entries
    games = input_data.read().split("\n")

    # extract the game ID, and the plays
    games_tmp = [line.split(":") for line in games]
    game_ids  = [int(line[0].split(" ")[1]) for line in games_tmp]
    gameplays = [line[1].split("; ") for line in games_tmp]

# if bag had been loaded with...
blues  = 14
reds   = 12
greens = 13

# ... the games possible would have been
possible_game_ids = []
for id, game in enumerate(gameplays):
    possible_play = True
    for idx, play in enumerate(game):
        if idx == 0:
            play = play[1:]
        cubesets = play.split(", ")
        # check each set of drawn cubes
        for cubeset in cubesets:
            n_cubes, cube_color = cubeset.split(" ")
            n_cubes = int(n_cubes)
            if cube_color == "blue" and n_cubes > blues:
                possible_play = False
                break
            if cube_color == "red" and n_cubes > reds:
                possible_play = False
                break
            if cube_color == "green" and n_cubes > greens:
                possible_play = False
                break

    if possible_play:
        possible_game_ids.append(id+1)

# the answer to the puzzle is the sum of the IDs of possible games
answer = sum(possible_game_ids)

print("Answer:", answer)
