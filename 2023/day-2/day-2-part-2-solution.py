# --- Day 2: Cube Conundrum ---

# load the input data
with open("input", "r") as input_data:
    # read entries
    games = input_data.read().split("\n")

    # extract the game ID, and the plays
    games_tmp = [line.split(":") for line in games]
    game_ids  = [int(line[0].split(" ")[1]) for line in games_tmp]
    gameplays = [line[1].split("; ") for line in games_tmp]

# what are the fewest number of cubes of each color that each game could have been played with?
min_cubes_power = []
for id, game in enumerate(gameplays):
    min_blue  = 0  # placeholder
    min_red   = 0  # placeholder
    min_green = 0  # placeholder
    for idx, play in enumerate(game):
        if idx == 0:
            play = play[1:]
        cubesets = play.split(", ")
        # check each set of drawn cubes
        for cubeset in cubesets:
            n_cubes, cube_color = cubeset.split(" ")
            n_cubes = int(n_cubes)
            if cube_color == "blue" and n_cubes > min_blue:
                min_blue = n_cubes
            if cube_color == "red" and n_cubes > min_red:
                min_red = n_cubes
            if cube_color == "green" and n_cubes > min_green:
                min_green = n_cubes

    min_cubes_power.append(min_blue*min_red*min_green)

# the answer to the puzzle is the sum of the powers of min cubes per game
answer = sum(min_cubes_power)

print("Answer:", answer)
