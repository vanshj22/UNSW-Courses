# COMP9021 19T3 - Rachid Hamadi
# Sample Exam 2


def f(N):
    '''
    >>> f(20)
    Here are your banknotes:
    $20: 1
    >>> f(40)
    Here are your banknotes:
    $20: 2
    >>> f(42)
    Here are your banknotes:
    $2: 1
    $20: 2
    >>> f(43)
    Here are your banknotes:
    $1: 1
    $2: 1
    $20: 2
    >>> f(45)
    Here are your banknotes:
    $5: 1
    $20: 2
    >>> f(2537)
    Here are your banknotes:
    $2: 1
    $5: 1
    $10: 1
    $20: 1
    $100: 25
    '''
    banknote_values = [1, 2, 5, 10, 20, 50, 100]
    banknotes = dict.fromkeys(banknote_values, 0)
    # Insert your code here
    for note in reversed(banknote_values):
        while N:
            if note <= N:
                N=N-note
                banknotes[note]+=1
            else:
                break
    print("Here are your banknotes:")
    for key in sorted(banknotes):
        if banknotes[key]>0:
            print(f'${key}: {banknotes[key]}')
if __name__ == '__main__':
    import doctest
    doctest.testmod()