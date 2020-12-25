# --- Day 21: Allergen Assessment ---
from typing import Tuple


def play_combat(player_1_deck : list, player_2_deck : list) -> Tuple[list, int]:
    """Returns the outcome of a game of Combat (the winning deck and the winner).
    """
    # play the game until one deck is empty
    while player_1_deck and player_2_deck:
        winning_card = max(player_1_deck[0], player_2_deck[0])
        player_1_wins = bool(winning_card == player_1_deck[0])
        if player_1_wins:
            player_1_deck.remove(winning_card)
            player_1_deck += [winning_card, player_2_deck[0]]
            player_2_deck.remove(player_2_deck[0])
        else:
            player_2_deck.remove(winning_card)
            player_2_deck += [winning_card, player_1_deck[0]]
            player_1_deck.remove(player_1_deck[0])

    # and the winner is...
    if player_1_deck:
        return player_1_deck, 1
    else:
        return player_2_deck, 2


def main():
    # load data
    with open("input", "r") as input_data:
        player_1_deck, player_2_deck = input_data.read().split("\n\n")

    player_1_deck = [int(i) for i in player_1_deck.split("\n")[1:]]
    player_2_deck = [int(i) for i in player_2_deck.split("\n")[1:-1]]

    # play Combat
    winning_deck, _ = play_combat(player_1_deck=player_1_deck, player_2_deck=player_2_deck)

    # the score is the sum of all the card values x (deck length - index) in the winning deck
    deck_length = len(winning_deck)
    scores = [value * (deck_length - idx) for idx, value in enumerate(winning_deck)]
    answer = sum(scores)

    print("Answer:", answer)


if __name__ == "__main__":
    main()
