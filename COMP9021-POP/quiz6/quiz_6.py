from collections import defaultdict
from random import seed, random
import sys
import numpy as np

dim = 10

def display(grid):
    print('  ', '-' * (2 * dim + 3))
    for row in grid:
        print('   |', *row, '|')
    print('  ', '-' * (2 * dim + 3))

def stripes(width):
    global grid

    new_grid = [[' ' for _ in range(dim)] for _ in range(dim)]
    count = 0
    valid_stripes = []
    max_length = 0
    min_length = dim
    width_stripes = []

    def checking_stripes(x,y):
        length = 0
        for i in range(dim):
            if 0 <= x + i < dim and 0 <= y + i < dim and grid[x + i][y + i] == '*':
                # print(grid[x + i][y + i], x + i,y + i)
                length += 1
            else:
                break
        return length
    
    def valid_width_stripes(width):
        width_stripes = []
        for i in range(dim):
            for j in range(dim):
                if grid[i][j] == ' ':
                    continue
                length = 0
                coordinates = []

                for k in range(width):
                    if i + k < dim and j - k >= 0 and grid[i + k][j - k] == '*':
                        length += 1
                        coordinates.append((i + k, j - k))
                    else:
                        break
                
                if length == width:  # Found a complete stripe of width n
                    width_stripes.append(coordinates)
        return width_stripes

    if width == 1:
        for i in range(dim):
            for j in range(dim):
                if grid[i][j] == ' ':
                    continue
                length = checking_stripes(i,j)
                if length >= 2 and length >= max_length :  # stride need to be length >=2 to be called a stride
                    if length > max_length:
                        max_length = length
                        count = 1
                        valid_stripes = []
                    elif length == max_length:
                        count += 1

                    for offset in range(max_length):
                        if 0 <= i + offset < dim and 0 <= j + offset < dim and grid[i + offset][j + offset] == '*':
                            valid_stripes.append((i + offset, j + offset))
        length = max_length

        for x, y in valid_stripes:
            new_grid[x][y] = '*'

    else:
        # if not width_stripes: 
        width_stripes = valid_width_stripes(width)
        for stripe in width_stripes:
            min_length = dim
            valid = True
            for i,j in stripe:
                length = checking_stripes(i,j)
                if length < 2: # stride need to be length >= 2 to be called a stride
                    valid = False
                    # index = stripe.index((i,j))
                    # for _ in range(index):
                    #     valid_stripes.pop()
                    break

                min_length = min(length, min_length)
                
            if valid and min_length >= max_length:

                if min_length > max_length:
                    max_length = max(max_length, min_length)
                    count = 1
                    valid_stripes = []
                elif min_length == max_length:
                    count += 1      

                current_stripe = []
                for i, j in stripe:
                    for offset in range(max_length):    
                        if 0 <= i + offset < dim and 0 <= j + offset < dim and grid[i + offset][j + offset] == '*':
                            if (i + offset, j + offset) not in valid_stripes:
                                current_stripe.append((i + offset, j + offset))
                if current_stripe:
                    valid_stripes.append(current_stripe)



        for stripe in valid_stripes:
            length = len(stripe)
            if length > max_length:
                max_length = length # 
            for x, y in stripe:
                if new_grid[x][y] == ' ':  # Check if the position is not already occupied
                    new_grid[x][y] = '*'
    
    return count, max_length, new_grid

try:
    for_seed, width, density = input('Input an integer, an integer '
                                     'greater than 0,\n      and '
                                     'a number between 0 and 1: '
                                    ).split()

    for_seed, width, density = int(for_seed), int(width), float(density)
    # for_seed, width, density = 0,2,0.8
    if width < 1 or density < 0 or density > 1:
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

count, max_width, new_grid = stripes(width)
if not count:
    print(f'There are no stripes of width {width} in the grid!')
else:
    print(f'The size of the largest stripes of width is {max_width}.')
    print('There', count == 1 and 'is' or 'are', count,
          count == 1 and 'stripe' or 'stripes',
          'of that size.'
         )
    print('Here', count == 1 and 'it is:\n' or 'they are:')
    display(new_grid)
# 0 1 0.7  working