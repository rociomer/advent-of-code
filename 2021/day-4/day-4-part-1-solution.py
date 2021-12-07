# --- Day 4: Giant Squid ---
import re
from typing import Union


def parse_board(board : str) -> list:
    """
    Parse the input string, encoding a bingo board, and return a list of lists.
    """
    parsed_board = []
    rows = board.split("\n")
    for row in rows:
        row = re.sub(" +", " ", row)  # remove multiple spaces
        row = re.sub("^\s", "", row)  # remove starting spaces
        parsed_board.append([int(num) for num in row.split(" ")])  # split row where there is 1 space
    return parsed_board

def mark_boards(number : int, bingo_boards : list) -> list:
    """
    Mark the specified number in the bingo boards.
    """
    updated_bingo_boards = []
    for board in bingo_boards:
        marked_board = _mark_board(number=number, board=board)
        updated_bingo_boards.append(marked_board)
    return updated_bingo_boards

def _mark_board(number : int, board : list) -> list:
    """
    Mark a single board with the specified number.
    """
    updated_board = []
    for row in board:
        updated_board.append(["X" if number == num else num for num in row])
    return updated_board

def check_for_winner(bingo_boards : list) -> Union[list, None]:
    """
    Checks for a bingo winner amongst the boards, and, if it exists, returns
    the winning board. Else returns None.
    """
    for board in bingo_boards:
        for row in board:
            if row.count("X") == 5:
                return board
        for column in zip(*board):  # transpose
            if column.count("X") == 5:
                return board
    return None


# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    raw_input = input_data.read().split("\n\n")

    # parse the input
    number_drawing_order = [int(num) for num in raw_input[0].split(",")]
    bingo_boards_raw = raw_input[1:]
    bingo_boards = [parse_board(board) for board in bingo_boards_raw]

# play the game until one board wins
for last_number_drawn in number_drawing_order:
    bingo_boards = mark_boards(number=last_number_drawn, bingo_boards=bingo_boards)
    winning_board = check_for_winner(bingo_boards=bingo_boards)
    if winning_board:
        break

# calculate the sum of the unmarked numbers in the winning bingo board
winning_board = [[0 if num == "X" else num for num in row] for row in winning_board]
sum_of_unmarked_numbers = sum([sum(row) for row in winning_board])

# calculate the score of the winning bingo board
winning_score = sum_of_unmarked_numbers * last_number_drawn

# the answer to the puzzle is the score of the winning bingo board
answer = winning_score

print("Answer:", answer)
