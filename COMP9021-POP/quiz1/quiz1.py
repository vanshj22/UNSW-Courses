# def picture(m, n):
#     # m - Number of big blocks
#     # n - Number of divisions in each block 
#     i=0
#     j=0
#     for j in range (m):
#         while i<n:
#             print("/\\")
#     print ("space")
# 2,3
def picture(m, n):
    # Line1
    for i in range(1):
        line1 = ''
        for j in range(m):
            line1 += ' ' + '/\\' * n+ ' '
        print(line1.rstrip())

    # Line2
    for j in range(m):
        print('/', end='')
        print(' ' + '_' * (2 * n - 2), end='')
        print(' \\', end='')
    print()

    # Line3
    for j in range(m):
        print('\\' + ' ' * (2 * n) + '/', end='')
    print()

    # Line4
    for i in range(1):
        line4 = ''
        for j in range(m):
            line4 += ' ' + '\\/' * n +' '
        print(line4.rstrip())



picture(2,3)




# //\/\/\/\/\/\/\/\
# /----\

def list_of_tuples(filename):
    result =[] 

    with open(filename, 'r') as file:

        for line in file:     
            line = line.strip()

            col_index =  line.find(':')
            excl_index = line.find('!')

            if col_index != -1 and excl_index != -1:
                a = int(line[:col_index])
                b = int(line[col_index+1:excl_index])
                c = int(line[excl_index+1:])


                if a<b<c:
                    result.append((a, b, c))
    print(result)

    return result

list_of_tuples(r'quiz1\test_2.txt')