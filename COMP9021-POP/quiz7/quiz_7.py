# Written by *** for COMP9021
#
# Working with a grid of size 10 x 10, with i and j
# interpreted as follows:
#
#              j
#     1 2 3 4 5 6 7 8 9 10
#   1
#   2
#   3
#   4
# i 5
#   6
#   7
#   8
#   9
#  10
#
# Finds the longest path in the grid starting from (i, j),
# moving up diagonally in the NE direction (↗)
# or moving down diagonally in the SW direction (↙),
# moving SE to change direction.
#
# Moving up to start with.
#
# To make the path unique, we prefer moving in a given direction
# (up or down) for as long as possible.


from random import seed, random
import sys

dim = 10

def display(grid):
    print('  ', '-' * (2 * dim + 3))
    for row in grid:
        print('   |', *row, '|')
    print('  ', '-' * (2 * dim + 3))

def longest_path(i, j, grid):    
    new_grid = [[' ' for _ in range(dim)] for _ in range(dim)]
    direction_up = True # True = NE, False = SW
    
    if grid[i][j] != '*' and direction_up :
        return 0, new_grid
    
    path_length = 1
    cache = {}
    path_cache = {}
    
    def check_path(i, j, direction_up):
        if i < 1 or i > dim or j < 1 or j > dim or grid[i-1][j-1] != '*':
            return 0, []
        
        if (i, j, direction_up) in cache:
            return cache[(i, j, direction_up)], path_cache[(i, j, direction_up)]
        
        current_path = [(i, j, direction_up)]
        
        # moving in the same direction
        if direction_up:
            next_length, next_path = check_path(i - 1, j + 1, direction_up)
        else:
            next_length, next_path = check_path(i + 1, j - 1, direction_up)
        
        length = 1 + next_length
        path = current_path + next_path
        
        # changing direction by moving SE
        if i + 1 <= dim and j + 1 <= dim and grid[i][j] == '*':
            se_length, se_path = check_path(i + 1, j + 1, not direction_up)
            if 1 + se_length > length:
                length = 1 + se_length
                path = current_path + [(i+1, j+1, not direction_up)] + se_path
        
        cache[(i, j, direction_up)] = length
        path_cache[(i, j, direction_up)] = path
        return length, path
    
    path_length, final_path = check_path(i, j, direction_up)

    for x, y, is_up in final_path:
        new_grid[x-1][y-1] = "↗" if is_up else "↙"
    
    return path_length, new_grid

try:
    for_seed, i, j, density = input('Input an integer, two integers between '
                                    f'1 and {dim},\n      '
                                    'and a number between 0 and 1: '
                                   ).split()

    for_seed, i, j, density = int(for_seed), int(i), int(j), float(density)
    if i < 1 or i > dim or j < 1 or j > dim or density < 0 or density > 1:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [['*' if random() < density else ' ' for _ in range(dim)]
             for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display(grid)

path_length, path_in_grid = longest_path(i, j, grid)
if not path_length:
    print(f'There is no special path starting from ({i}, {j}) in the grid!')
else:
    print(f'The longest special path starting from ({i}, {j}) '
          f'has a length of {path_length}.'
          )
    print('Here it is:')
    display(path_in_grid)
