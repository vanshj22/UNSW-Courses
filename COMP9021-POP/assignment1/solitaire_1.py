# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = 'all'

from itertools import chain
from random import seed, shuffle
from collections import defaultdict

import sys
from contextlib import redirect_stdout
import io


# Define Unicode symbols for cards from the playing card block
suits = {
    'hearts': 0x1F0B0,    
    'diamonds': 0x1F0C0,  
    'clubs': 0x1F0D0,      
    'spades': 0x1F0A0    
}

rounds = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    }

# Generates a deck of 52 cards using Unicode playing cards  
def generate_deck():
    deck = []
    
    for suit in suits.values():
        number_cards = [chr(suit + num) for num in range(1, 11)]
        picture_cards = [chr(suit + face) for face in [0xB, 0xD, 0xE]]

        deck.extend(number_cards + picture_cards)
    
    return deck

def display_grid(grid):
    rows = [grid[i:i+4] for i in range(0, 16, 4)]

    for row in rows:
        print("\t" +"\t".join([card if card else "" for card in row]).rstrip())  # Leaves spaces for removed face cards

def removing_pictures(grid):
    # Unicode for picture cards (Jacks, Queens, Kings)
    picture_cards = [chr(suit + offset) for suit in suits.values() for offset in [0xB, 0xD, 0xE]]

    pictures_removed = 0
    pictures = []
    remaining = []
    for card in grid:
        if card in picture_cards:
            pictures_removed += 1
            pictures.append(card)
            remaining.append("")  # Leave a blank space for face cards
        else:
            remaining.append(card)
    return pictures_removed, pictures, remaining


def sort_remaining_cards(original_deck, removed_pictures):

    sorted_remaining = [card for card in original_deck if card not in removed_pictures]
    
    return sorted_remaining


def solitaire_game_1(seed_input=None):

    while seed_input is None:
        try:
            seed_input = int(input("Please enter an integer to feed the seed() function: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    cards_deck = generate_deck() # To create a deck of cards
    
    round_number = 1

    pictures_removed = 0
    total_pictures_removed = 0
    total_pictures = []

    cards_remaining = cards_deck.copy()

    while total_pictures_removed < 12 and round_number < 5: 

        seed(seed_input)
        shuffle(cards_remaining) # To shuffle the deck of cards

        if round_number == 1:
            print("\nDeck shuffled, ready to start!" + "\n" + "]" * len(cards_remaining))
            print("\nStarting first round..." )
        else:
            print(f"\nAfter shuffling, starting {rounds.get(round_number)} round...")

        # Drawing 16 cards
        grid = [card for card in cards_remaining[-1:-17:-1]]
        cards_remaining = cards_remaining[:-16]

        print("\nDrawing and placing 16 cards:" + "\n" + "]" * len(cards_remaining))
        display_grid(grid)
        
        # Removing face cards
        pictures_removed, pictures, cards_played = removing_pictures(grid)

        total_pictures_removed += pictures_removed
        
        while pictures_removed > 0 :

            total_pictures.extend(pictures)

            print(f"\nPutting {pictures_removed} picture{'' if pictures_removed == 1 else 's'} aside:")

            # Displaying grid after removing face cards
            grid = [card for card in cards_played[::]]
            display_grid(grid)

            if total_pictures_removed== 12:
                break

            replacements = cards_remaining[-1:-(pictures_removed+1):-1]
            
            for i in range(len(cards_played)):
                if cards_played[i] == "" and replacements:
                    cards_played[i] = replacements.pop(0) 

            cards_remaining = cards_remaining[:-pictures_removed]
            print(f"\nDrawing and placing {pictures_removed} card{'' if pictures_removed == 1 else 's'}:" + "\n" + "]" * len(cards_remaining))
            display_grid(cards_played)

            pictures_removed, pictures, cards_played = removing_pictures(cards_played)
            total_pictures_removed += pictures_removed
            if pictures_removed== 0:
                break


        cards_remaining.extend(cards_played)
        # cards_remaining = cards_played + cards_remaining
        cards_remaining = sort_remaining_cards(cards_deck, total_pictures)

        round_number += 1
        seed_input += 1

    if total_pictures_removed == 12:
        print("\nYou uncovered all pictures, you won!")

    elif total_pictures_removed > 1 and total_pictures_removed < 12:
        print(f"\nYou uncovered only {total_pictures_removed} pictures, you lost!")
    elif total_pictures_removed == 0:
        print("\nYou uncovered no pictures, you lost!") 
    elif total_pictures_removed == 1:
        print(f"\nYou uncovered only {total_pictures_removed} picture, you lost!")

    return total_pictures_removed

def simulate(no_of_games, seed_input):

    data = defaultdict(int)

    for i in range(no_of_games):
        f = io.StringIO()  # Create a string buffer to capture output
        with redirect_stdout(f):
            no_of_pictures = solitaire_game_1(seed_input+i ) 
        data[no_of_pictures] += 1

    print(f"Number of uncovered pictures | Frequency")
    print("-" * 40)

    for no_of_pictures in sorted(data.keys()):
        frequency = ((data[no_of_pictures] / no_of_games) * 100)
        print(f"{no_of_pictures:>28} | {frequency:>8.2f}%")


if __name__ == "__main__":

    solitaire_game_1()
    # simulate(10,6)
