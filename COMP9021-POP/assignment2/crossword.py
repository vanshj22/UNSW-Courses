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
        self.dictionary = {}  # Words to choose from, organized by length

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
            # Check horizontal words (deterministic order)
            for i in range(self.height):
                current_word = ''
                add_word = True
                for j in range(self.width):
                    char = self.grid[i][j]
                    if char == '':
                        # if len(current_word) > 1 and add_word:
                        #     h_complete_words.append(current_word)
                        current_word = ''
                        add_word = False
                    elif char == '*':
                        if len(current_word) > 1 and add_word:
                            h_complete_words.append(current_word)
                        current_word = ''
                        add_word = True
                    elif char.isalpha() and add_word:
                        current_word += char
                if len(current_word) > 1 and add_word:
                    h_complete_words.append(current_word)
            
            # Check vertical words (deterministic order)
            for j in range(self.width):
                current_word = ''
                add_word = True
                for i in range(self.height):
                    char = self.grid[i][j]
                    if char == '':
                        # if len(current_word) > 1 and add_word:
                        #     v_complete_words.append(current_word)
                        current_word = ''
                        add_word = False
                    elif char == '*':
                        if len(current_word) > 1 and add_word:
                            v_complete_words.append(current_word)
                        current_word = ''
                        add_word = True
                    elif char.isalpha() and add_word:
                        current_word += char
                if len(current_word) > 1 and add_word:
                    v_complete_words.append(current_word)
            
            return h_complete_words, v_complete_words

        try:
            with open(self.tex_file, "r") as file:
                content = file.read()
        except FileNotFoundError:
            print(f"File {self.tex_file} not found!")
            sys.exit()
        
        h_complete_words, v_complete_words = [], []

        h_grid = re.search(r'h=(\d+)', content)
        v_grid = re.search(r'v=(\d+)', content)

        if h_grid and v_grid:
            self.width, self.height = int(h_grid.group(1)), int(v_grid.group(1))
            self.grid = np.full((self.height, self.width), '', dtype=str)

        blackcases_count = self.blackcase_count(content)

        # Process horizontal words deterministically
        h_words_match = re.search(r'\\words\[h\]{([^}]*)}', content)
        if h_words_match:
            h_words = h_words_match.group(1).strip().split(',')  # Sort for deterministic processing
            for entry in h_words:
                word_match = re.search(r'(\d+\s*/\s*\d+\s*/\s*[A-Z]+)\s*(?:,|%|$)', entry)
                parts = word_match.group(1).strip().split('/')
                if len(parts) == 3:
                    x, y, word = int(parts[0]), int(parts[1]), parts[2].strip()
                    for i, letter in enumerate(word):
                        if x-1+i < self.width:
                            self.grid[y-1][x-1+i] = letter

        # Process vertical words deterministically
        v_words_match = re.search(r'\\words\[v\]{([^}]*)}', content)
        if v_words_match:
            v_words = v_words_match.group(1).strip().split(',')  # Sort for deterministic processing
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

    def solve(self, output_file, dictionary_file = 'dictionary.txt', fill_with_given_words = False):
        def parse_slots():
            """Extract all empty slots in the grid deterministically."""
            slots = []
            valid_lengths = sorted(set(len(word) for words in self.dictionary.values() for word in words))
            
            # Process horizontal slots first (top to bottom, left to right)
            for i in range(self.height):
                j = 0
                while j < self.width:
                    if self.grid[i][j] != '*':
                        start = (i, j)
                        length = 0
                        while j < self.width and self.grid[i][j] != '*':
                            length += 1
                            j += 1
                        if length > 1 and length in valid_lengths:
                            slots.append((start, length, 'H'))
                    j += 1

            # Process vertical slots second (left to right, top to bottom)
            for j in range(self.width):
                i = 0
                while i < self.height:
                    if self.grid[i][j] != '*':
                        start = (i, j)
                        length = 0
                        while i < self.height and self.grid[i][j] != '*':
                            length += 1
                            i += 1
                        if length > 1 and length in valid_lengths:
                            slots.append((start, length, 'V'))
                    i += 1

            return sorted(slots, key=lambda x: (x[0][0], x[0][1], x[2]))  # Deterministic sort

        def get_initial_domains(slots):
            """Initialize domains deterministically."""
            domains = {}
            for slot in slots:
                start, length, direction = slot
                possible_words = sorted(set(self.dictionary.get(length, [])))  # Sort for deterministic ordering
                
                # Pre-filter based on existing letters
                i, j = start
                for k in range(length):
                    curr_i = i + k if direction == 'V' else i
                    curr_j = j + k if direction == 'H' else j
                    if self.grid[curr_i][curr_j].isalpha():
                        possible_words = sorted([word for word in possible_words 
                                    if word[k] == self.grid[curr_i][curr_j]])
                domains[slot] = possible_words
            return domains

        def count_constraints(slot):
            """Count intersecting constraints deterministically."""
            start, length, direction = slot
            i, j = start
            intersections = []
            
            for k in range(length):
                curr_i = i + k if direction == 'V' else i
                curr_j = j + k if direction == 'H' else j
                
                if direction == 'H':
                    # Count vertical intersections
                    above = below = 0
                    for di in range(curr_i - 1, -1, -1):
                        if self.grid[di][curr_j] == '*': break
                        above += 1
                    for di in range(curr_i + 1, self.height):
                        if self.grid[di][curr_j] == '*': break
                        below += 1
                    if above + below > 0:
                        intersections.append((curr_i, curr_j, above + below))
                else:
                    # Count horizontal intersections
                    left = right = 0
                    for dj in range(curr_j - 1, -1, -1):
                        if self.grid[curr_i][dj] == '*': break
                        left += 1
                    for dj in range(curr_j + 1, self.width):
                        if self.grid[curr_i][dj] == '*': break
                        right += 1
                    if left + right > 0:
                        intersections.append((curr_i, curr_j, left + right))
            
            return len(sorted(intersections, key=lambda x: (x[0], x[1], x[2])))  # Deterministic count

        def select_next_slot(unassigned_slots, domains):
            """Select next slot deterministically."""
            def get_slot_score(slot):
                return (
                    len(domains[slot]),  # Primary: Minimum remaining values
                    -count_constraints(slot),  # Secondary: Maximum constraints
                    slot[0][0],  # Tertiary: Row position
                    slot[0][1],  # Quaternary: Column position
                    slot[2]  # Final: Direction (H/V)
                )
            
            return min(unassigned_slots, key=get_slot_score)

        def update_domains(domains, affected_slots, placement):
            """Update domains deterministically."""
            slot, word = placement
            start, length, direction = slot
            i, j = start
            
            updated_domains = {}
            for affected_slot in sorted(affected_slots, key=lambda x: (x[0][0], x[0][1], x[2])):
                if affected_slot == slot:
                    continue
                    
                astart, alength, adir = affected_slot
                ai, aj = astart
                
                # Find intersection deterministically
                intersection = None
                if direction != adir:
                    for k in range(length):
                        for m in range(alength):
                            curr_i = i + k if direction == 'V' else i
                            curr_j = j + k if direction == 'H' else j
                            acurr_i = ai + m if adir == 'V' else ai
                            acurr_j = aj + m if adir == 'H' else aj
                            
                            if curr_i == acurr_i and curr_j == acurr_j:
                                intersection = (k, m)
                                break
                        if intersection:
                            break
                
                if intersection:
                    k, m = intersection
                    letter = word[k]
                    updated_domains[affected_slot] = sorted([w for w in domains[affected_slot] 
                                                if w[m] == letter])
                
            return updated_domains

        def backtrack(assignment, unassigned_slots, domains):
            """Deterministic backtracking with forward checking."""
            if not unassigned_slots:
                return True

            slot = select_next_slot(unassigned_slots, domains)
            unassigned_slots.remove(slot)

            for word in sorted(domains[slot]):  # Sort for deterministic word selection
                valid = True
                start, length, direction = slot
                i, j = start
                
                # Validity check
                for k in range(length):
                    curr_i = i + k if direction == 'V' else i
                    curr_j = j + k if direction == 'H' else j
                    if self.grid[curr_i][curr_j].isalpha() and self.grid[curr_i][curr_j] != word[k]:
                        valid = False
                        break
                
                if valid:
                    # Save state
                    old_grid = [row.copy() for row in self.grid]
                    
                    # Place word
                    for k in range(length):
                        if direction == 'H':
                            self.grid[i][j + k] = word[k]
                        else:
                            self.grid[i + k][j] = word[k]
                    
                    # Update domains
                    old_domains = {s: domains[s][:] for s in unassigned_slots}
                    new_domains = update_domains(domains, unassigned_slots, (slot, word))
                    domains.update(new_domains)
                    
                    if all(domains[s] for s in unassigned_slots):
                        assignment[slot] = word
                        if backtrack(assignment, unassigned_slots, domains):
                            return True
                    
                    # Restore state
                    self.grid = [row.copy() for row in old_grid]
                    domains.update(old_domains)
                    assignment.pop(slot, None)
            
            unassigned_slots.append(slot)
            return False

        # Load dictionary if not already loaded
        try:
            with open(dictionary_file, "r") as file:
                self.dictionary = file.read().split("\n")
                self.dictionary = {length: [word for word in self.dictionary 
                                        if (len(word) == length and len(word) > 0)] 
                                for length in set(map(len, self.dictionary))}
        except FileNotFoundError:
            print("Dictionary not found!")
            return False

        # Initialize puzzle state
        self.analyse_grid()
        self.slots = parse_slots()
        
        if not self.slots:

            print("Hey, it can't be solved!") if not fill_with_given_words else print("Hey, it can't be filled with these words!")
            return False
            
        # Initialize solving structures
        domains = get_initial_domains(self.slots)
        unassigned_slots = [slot for slot in self.slots if slot not in domains or domains[slot]]
        assignment = {}
        
        grid_filled = all(all(cell.isalpha() or cell == '*' for cell in row) for row in self.grid)

        if unassigned_slots and not grid_filled:
            # Solve puzzle
            if backtrack(assignment, unassigned_slots, domains) and all(all(cell.isalpha() or cell == '*' for cell in row) for row in self.grid):
                # Save solution
                try:
                    print(f"I {'solved' if not fill_with_given_words else 'filled'} it!\nResult captured in {output_file}.")
                    with open(output_file, 'w') as f:
                        f.write(r'\documentclass{standalone}' + '\n')
                        f.write(r'\usepackage{pas-crosswords}' + '\n')
                        f.write(r'\usepackage{tikz}' + '\n\n')
                        f.write(r'\begin{document}' + '\n')
                        f.write(r'\begin{tikzpicture}' + '\n')
                        first_row = self.grid[0]
                        f.write(r'\gridcross{'+''.join(cell  for cell in first_row) + ',%\n')

                        for row in self.grid[1:-1]:
                            f.write(' '*11 + ''.join(cell  for cell in row) + ',%\n')
                        
                        # Handle the last row separately to avoid trailing comma
                        last_row = self.grid[-1]
                        f.write(' '*11 + ''.join(cell for cell in last_row) + '%\n'+' '*10 + '}\n')

                        f.write(r'\end{tikzpicture}' + '\n')
                        f.write(r'\end{document}' + '\n')

                except IOError:
                    print(f"Error writing to {output_file}")

            else:
                print("Hey, it can't be solved!") if not fill_with_given_words else print("Hey, it can't be filled with these words!")
        else:
            print("Hey, it can't be solved!") if not fill_with_given_words else print("Hey, it can't be filled with these words!")



    def fill_with_given_words(self, dictionary_file, output_file):

        solved = self.solve(output_file, dictionary_file, True)
        print(self.tex_file,output_file, dictionary_file,)


if __name__ == "__main__":

        # Part 1
    # C1 = Crossword('empty_grid_1.tex')
    # print(C1)
    # C2 = Crossword('empty_grid_2.tex')
    # print(C2)
    # C3 = Crossword('empty_grid_3.tex')
    # print(C3)
    # C1 = Crossword('partial_grid_1.tex')
    # print(C1)
    # C2 = Crossword('partial_grid_2.tex')    
    # print(C2)
    # C3 = Crossword('partial_grid_3.tex')
    # print(C3)

    # Part 2
    C1 = Crossword('partial_grid_3.tex')
    
    # Part 3
    # C1 = Crossword('partial_grid_3.tex')
    # C1.solve('solved_empty_grid_1.tex')
    # C2 = Crossword('empty_grid_2.tex')
    # C2.solve('solved_empty_grid_2.tex')
    # P1 = Crossword('partial_grid_1.tex')
    # P1.solve('solved_partial_grid_1.tex')
    execution_time = timeit.timeit(lambda: C1.fill_with_given_words('words_2.txt','test.tex'), number=1)
    print(f"Program ran for {execution_time:.2f} seconds")
    # execution_time = timeit.timeit(lambda: C1.solve('test.tex'), number=1)
    # print(f"Program ran for {execution_time:.2f} seconds")
