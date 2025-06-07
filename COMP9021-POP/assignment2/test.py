import sys
import numpy as np
import re
import timeit

class Crossword:
    def __init__(self, tex_file):
        self.tex_file = tex_file 
        self.grid = None
        self.width = 0
        self.height = 0
        self.slots = []  # Slots to fill (coordinates and direction)
        self.dictionary = []  # Words to choose from

    def __str__(self):
            
        h_value, v_value, blackcases_count, total_letter_count, h_letter_count, v_letter_count = self.analyse_grid()

        return (f"A grid of width {h_value} and height {v_value}, with {blackcases_count if blackcases_count != 0 else 'no'} blackcase{'s' if blackcases_count != 1 else ''}, filled with {total_letter_count if total_letter_count != 0 else 'no'} letter{'s' if total_letter_count != 1 else ''},\nwith {v_letter_count if v_letter_count != 0 else 'no'} complete vertical word{'s' if v_letter_count != 1 else ''} and {h_letter_count if h_letter_count != 0 else 'no'} complete horizontal word{'s' if h_letter_count != 1 else ''}.")

    def blackcase_count(self, content):
        blackcases_match = re.search(r'\\blackcases{([^}]*)}', content)
        if blackcases_match:
            blackcases = blackcases_match.group(1).strip().split(',') 
            blackcases_count = len(blackcases)  
            for case in blackcases:
                x, y = map(int, case.strip().split('/'))
                self.grid[y-1][x-1] = '*'
        else:
            blackcases_count = 0
        return blackcases_count

    def analyse_grid(self):

        def count_complete_words(self):
            h_complete_words, v_complete_words = [], []
            
            # Check horizontal words
            for i in range(self.height):
                add_word = True
                current_word = ''
                for j in range(self.width):
                    char = self.grid[i][j]
                    if char == '':
                        current_word = ''
                        add_word = False
                        continue
                    elif char == '*' :
                        add_word = True
                        if len(current_word) > 1 and add_word:  # Word must be at least 2 letters
                            h_complete_words.append(current_word)
                        current_word = ''
                    elif char.isalpha() and add_word:
                        current_word += char
                if len(current_word) > 1 and add_word:  # Check word at end of row
                    h_complete_words.append(current_word)
                
            
            # Check vertical words
            for j in range(self.width):
                add_word = True
                current_word = ''
                for i in range(self.height):
                    char = self.grid[i][j]
                    if char == '':
                        current_word = ''
                        add_word = False
                        continue
                    elif char == '*' :
                        add_word = True
                        if len(current_word) > 1 and add_word:  # Word must be at least 2 letters
                            v_complete_words.append(current_word)
                        current_word = ''
                    elif char.isalpha() and add_word:
                        current_word += char
                if len(current_word) > 1 and add_word:  # Check word at end of column
                    v_complete_words.append(current_word)
            
            return h_complete_words, v_complete_words

        try:
            with open(self.tex_file, "r") as file:
                content = file.read()
        except FileNotFoundError:
            sys.exit()


        h_complete_words, v_complete_words = [], []

        h_grid = re.search(r'h=(\d+)', content)
        v_grid = re.search(r'v=(\d+)', content)

        if h_grid and v_grid:
            self.width ,self.height = int(h_grid.group(1)), int(v_grid.group(1))
            self.grid = np.full((self.height, self.width), '', dtype=str)

        blackcases_count = self.blackcase_count(content)

        h_words_match = re.search(r'\\words\[h\]{([^}]*)}', content)
        if h_words_match:
            h_words = h_words_match.group(1).strip().split(',')
            for entry in h_words:
                word_match = re.search(r'(\d+\s*/\s*\d+\s*/\s*[A-Z]+)\s*(?:,|%|$)', entry)  
                parts = word_match.group(1).strip().split('/')
                if len(parts) == 3:
                    x, y, word = int(parts[0]), int(parts[1]), parts[2].strip()
                    for i, letter in enumerate(word):
                        if x-1+i < self.width:
                            self.grid[y-1][x-1+i] = letter

        v_words_match = re.search(r'\\words\[v\]{([^}]*)}', content) # \b[A-Z]+\b
        if v_words_match:
            v_words = v_words_match.group(1).strip().split(',')
            for entry in v_words:
                word_match = re.search(r'(\d+\s*/\s*\d+\s*/\s*[A-Z]+)\s*(?:,|%|$)', entry)  
                parts = word_match.group(1).strip().split('/')
                if len(parts) == 3:
                    x, y, word = int(parts[0]), int(parts[1]), parts[2].strip()
                    for i, letter in enumerate(word):
                        if y-1+i < self.height:
                            self.grid[y-1+i][x-1] = letter
                            
        h_complete_words, v_complete_words = count_complete_words(self)

        letter_count = sum(1 for row in self.grid for char in row if char.isalpha())

        return self.width, self.height, blackcases_count, letter_count, len(h_complete_words), len(v_complete_words)
    
C1 = Crossword('partial_grid_1.tex')
print(C1)