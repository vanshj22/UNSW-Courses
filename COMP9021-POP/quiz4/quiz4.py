from math import sqrt
from timeit import timeit

def sieve_of_primes_up_to(n):
    sieve = [True] * (n + 1)
    for p in range(2, round(sqrt(n)) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return (i for i in range(2, n+1) if sieve[i])  # Using generator to save memory

def tri_numbers(n):
    largest_tri_number = None
    largest_decomposition = None
    max_gap = 0
    max_gap_tri_numbers = []

    prime_gen = sieve_of_primes_up_to(round(n / 4))
    prime_list = list(prime_gen)  

    tri_numbers_count = 0
    for i, p1 in enumerate(prime_list):
        if p1 * p1 * p1 > n:
            break
        for j in range(i, len(prime_list)):
            p2 = prime_list[j]
            if p1 * p2 * p2 > n:
                break
            for k in range(j, len(prime_list)):
                p3 = prime_list[k]
                tri_num = p1 * p2 * p3
                if tri_num > n:
                    break
                tri_numbers_count += 1
            
                if largest_tri_number is None or tri_num > largest_tri_number:
                    largest_tri_number = tri_num
                    largest_decomposition = [p1, p2, p3]

                gap = min(p2 - p1, p3 - p2)
                if gap > max_gap:
                    max_gap = gap
                    max_gap_tri_numbers = [(tri_num, [p1, p2, p3])]
                elif gap == max_gap:
                    max_gap_tri_numbers.append((tri_num, [p1, p2, p3]))


    if tri_numbers_count == 1:
        print(f'There is {tri_numbers_count} trinumber at most equal to {n}.')
    else:
        print(f'There are {tri_numbers_count} trinumbers at most equal to {n}.')

    if largest_tri_number:
        print(f'The largest one is {largest_tri_number}, equal to {largest_decomposition[0]} x {largest_decomposition[1]} x {largest_decomposition[2]}.\n')

    print(f'The maximum gap in decompositions is {max_gap}.')
    print("It is achieved with:")
    for tri_number, primes in max_gap_tri_numbers:
        print(f"  {tri_number} = {primes[0]} x {primes[1]} x {primes[2]}")

    return tri_numbers_count

# print(timeit("tri_numbers(90_000_000)", globals=globals(), number=1))
