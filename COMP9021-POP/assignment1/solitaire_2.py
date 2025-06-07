from itertools import chain
from random import seed, shuffle
from collections import defaultdict

import sys
from contextlib import redirect_stdout
import io

SUITS = {
    'hearts': 0x1F0B0,    
    'diamonds': 0x1F0C0,  
    'clubs': 0x1F0D0,      
    'spades': 0x1F0A0    
}

ACES = [chr(_) for _ in [0x1F0B1, 0x1F0C1, 0x1F0D1, 0x1F0A1]]
KINGS = [chr(_) for _ in [0x1F0BE, 0x1F0CE, 0x1F0DE, 0x1F0AE]]
QUEENS = [chr(_) for _ in [0x1F0BD, 0x1F0CD, 0x1F0DD, 0x1F0AD]]
JACKS = [chr(_) for _ in [0x1F0BB, 0x1F0CB, 0x1F0DB, 0x1F0AB]]


# Generates a deck of 52 cards using Unicode playing cards  
def generate_deck():
    deck = []
    for suit in SUITS.values():
        number_cards = [chr(suit + num) for num in range(1, 11)]
        picture_cards = [chr(suit + face) for face in [0xB, 0xD, 0xE]]

        deck.extend(number_cards + picture_cards)
    return deck

def display_deck(deck):
    return "]" * len(deck)

def display_unplaced_cards(unplaced):
    if not unplaced:
        return ""
    return "".join([f'['* (len(unplaced)-1) + f'{unplaced[-1]}'])

def display_stacks(sequence_increasing, sequence_decreasing):
    result = []
    for row in [sequence_increasing, sequence_decreasing]:
        if not row:
            result.append("\n")
        else:
            row_str = "".join([
                f"{'[' * (len(stack) - 1) + f'{stack[-1]}':<15}" if stack else " " * 15 for stack in row]).rstrip()

            if row_str:
                result.append("    " + row_str)
            else:
                result.append(row_str)
    return result[0], result[1]

def check_suits(card1, card2):
    suit_ranges = [(0x1F0A1, 0x1F0AE), (0x1F0B1, 0x1F0BE), (0x1F0C1, 0x1F0CE), (0x1F0D1, 0x1F0DE)]
    unicode1, unicode2 = ord(card1), ord(card2)
    return any(start <= unicode1 <= end and start <= unicode2 <= end for start, end in suit_ranges)

def can_place_card(card, target_card,seq):
    if seq == 1:
        if card in QUEENS and target_card in JACKS:
            return (ord(card) == ord(target_card) + 2) if check_suits(card, target_card) else False
        else:
            return (ord(card) == ord(target_card) + 1) if check_suits(card, target_card) else False
    elif seq == -1:
        if card in JACKS and target_card in QUEENS:
            return (ord(card) == ord(target_card) - 2) if check_suits(card, target_card) else False
        else:
            return (ord(card) == ord(target_card) - 1) if check_suits(card, target_card) else False

def rounds_ordinal(n):
    if n == 1:
        return 'first'
    elif n == 2:
        return 'second'
    elif n == 3:
        return 'third'
    else:
        return f"{n}th"

def simulate(no_of_games, seed_input):

    data = defaultdict(int)

    for i in range(no_of_games):
        f = io.StringIO()  # Create a string buffer to capture output
        with redirect_stdout(f):
            no_of_cards, _, _ = solitaire_game_2(seed_input + i) 
        # print(no_of_cards)
        data[no_of_cards] += 1

    print(f"Number of cards left | Frequency")
    print("--------------------------------")

    for no_of_cards in sorted(data.keys(), reverse = True):
        frequency = ((data[no_of_cards] / no_of_games) * 100)
        print(f"{no_of_cards:>20} | {frequency:>8.2f}%")
    


def solitaire_game_2(seed_value = None):
    deck = generate_deck()  # To create a deck of cards
    seed(seed_value)
    shuffle(deck)

    output = []
    output.append("Deck shuffled, ready to start!")
    output.append(display_deck(deck))
    output.append("\n")

    rounds = 0
    total_unplaced = 0
    unplaced_output = [] 

        # 0 - Hearts 
        # 1 - Diamonds
        # 2 - Clubs
        # 3 - Spade
    sequence_increasing = [[] for _ in range(4)]
    sequence_decreasing = [[] for _ in range(4)]

    
    while deck:
        rounds += 1
        win_conditon = False
        output.append(f"Starting to draw 3 cards (if possible) again and again for the {rounds_ordinal(rounds)} time...")
        output.extend("\n")
    
        unplaced = []

        while deck:
            drawn_cards = deck[-3:][::-1] # breakpoint -1 for reversing last three or less elements
            unplaced.extend(drawn_cards)
            deck = deck[:-3]
            output.append(display_deck(deck))
            output.append(display_unplaced_cards(unplaced))
            output.extend(display_stacks(sequence_increasing, sequence_decreasing))
            output.extend("\n")

            for card in unplaced[::-1]: # breakpoint
                if card in ACES:  # Ace
                    index = ACES.index(card)
                    sequence_increasing[index].append(card)
                    unplaced.pop()
                    win_conditon = True
                    output.append("Placing one of the base cards!")
                    output.append(display_deck(deck))
                    output.append(display_unplaced_cards(unplaced))
                    output.extend(display_stacks(sequence_increasing, sequence_decreasing))
                    output.extend("\n")

                elif card in KINGS:  # King
                    index = KINGS.index(card)
                    sequence_decreasing[index].append(card)
                    unplaced.pop()
                    win_conditon = True
                    output.append("Placing one of the base cards!")
                    output.append(display_deck(deck))
                    output.append(display_unplaced_cards(unplaced))
                    output.extend(display_stacks(sequence_increasing, sequence_decreasing))
                    output.extend("\n")

                else:
                    placed = False

                    for i in range(4):
                        if sequence_increasing[i] and can_place_card(card, sequence_increasing[i][-1],1):  
                            output.append("Making progress on an increasing sequence!")
                            sequence_increasing[i].append(card)
                            unplaced.pop()
                            placed = True
                            win_conditon = True
                            output.append(display_deck(deck))
                            output.append(display_unplaced_cards(unplaced))
                            output.extend(display_stacks(sequence_increasing, sequence_decreasing))
                            output.extend("\n")
                            break
                        elif sequence_decreasing[i] and can_place_card(card, sequence_decreasing[i][-1], -1) :
                            output.append("Making progress on a decreasing sequence!")
                            sequence_decreasing[i].append(card)
                            unplaced.pop()
                            placed = True
                            win_conditon = True
                            output.append(display_deck(deck))
                            output.append(display_unplaced_cards(unplaced))
                            output.extend(display_stacks(sequence_increasing, sequence_decreasing))
                            output.extend("\n")
                            break
                    if not placed:
                        break

        total_unplaced = len(unplaced) +len(deck)
        deck = unplaced[::-1]  # Prepare for the next round
    
        if not win_conditon:
            break

    output.pop()

    return total_unplaced, win_conditon, output

def main(seed_value = None):
    seed_value = int(input("Please enter an integer to feed the seed() function: "))
    # Hearts, Diamonds, Clubs, Spades
    
    unplaced_cards, win, output_lines= solitaire_game_2(seed_value)
    total_lines = len(output_lines)

    if unplaced_cards == 0 and win:
        print("\nAll cards have been placed, you won!")
    else:
        print(f"\n{unplaced_cards} cards could not be placed, you lost!")

    print(f"\nThere are {total_lines} lines of output; what do you want me to do?")
    
    while True:
        print()
        print ("Enter: q to quit")
        print(f"       a last line number (between 1 and {total_lines})")
        print(f"       a first line number (between -1 and -{total_lines})")
        print(f"       a range of line numbers (of the form m--n with 1 <= m <= n <= {total_lines})")

        user_input = input(" "*7).strip()
        
        if user_input == 'q':
            break

        elif user_input.startswith('-') and user_input[1:].isdigit():
            n = int(user_input)
            if -total_lines <= n <= -1:
                print()
                if output_lines[n-1].strip() == "":  
                    for line in output_lines[n:]:  
                        print(line.rstrip())
                else:
                    for line in output_lines[n-1:]:  
                        print(line.rstrip())

        elif user_input.isdigit():
            n = int(user_input)
            if 1 <= n <= total_lines:
                print()
                for line in output_lines[:n]:
                    print(line.rstrip())

        elif '--' in user_input:
            parts = user_input.split('--')
            if len(parts) == 2:
                m_str, n_str = parts
                m_str = m_str.strip()
                n_str = n_str.strip()
                if m_str.isdigit() and n_str.isdigit():
                    m = int(m_str)
                    n = int(n_str)
                    if 1 <= m <= n <= total_lines:
                        print()
                        if output_lines[m-1].strip() == "":  # Check if the first line is empty 
                            for line in output_lines[m-1:n]:  # Adjusting for 0-based index
                                print(line.rstrip())
                        else:
                            for line in output_lines[m-1:n]:  # If not empty, print from the first line
                                print(line.rstrip())

if __name__ == "__main__":
    main()
    # simulate(10,6)





