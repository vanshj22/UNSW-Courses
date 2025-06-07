import unicodedata
from unicodedata import name

while True:
    try:
        a_b = input('Please input two integers a and b with 0 <= a <= b <= 1114111,\n       both integers being separated by ~, with possibly\n       spaces and tabs before and after the numbers:\n'+" " * 7)
        a, b = map(lambda x: int(x.strip()), a_b.split("~"))
        if 0 <= a <= b <= 1114111:
            break
        else:
            raise ValueError
    except (ValueError, TypeError):
        print("\nIncorrect input, try again!")

named_chars = [(i, name(chr(i), None)) for i in range(a, b + 1) if name(chr(i), None)]

if named_chars:
    if len(named_chars) == (b - a + 1):
        if a == b:
            print(f"\n{a} is the code point of a named character.\n") 
        else:

            print(f"\nAll numbers between {a} and {b}\n  are code points of named characters.\n")
    else:
        percent = len(named_chars) / (b - a + 1) * 100
        print(f"\nAmongst the numbers between {a} and {b},\n  {percent:.2f}% are code points of named characters.\n")

    input_string = input("Enter a string: ")

    named_chars = sorted(named_chars, key=lambda x: x[1])

    max_name_length = 0
    for _, name in named_chars:
        if name.startswith(input_string):
            max_name_length = max(max_name_length, len(name))


    results = [f"{name.ljust(max_name_length)}: {chr(cp)}" for cp, name in named_chars if name.startswith(input_string)]

    if not results:
        print(f"\nNone of the characters you want me to consider\n  has a name that starts with {input_string}.")
    else:
        print(f"\nHere are those of the characters under consideration\n  whose name starts with {input_string}:")
        print("\n".join(results))

else:
    if a == b:
        print(f"\n{a} is not the code point of a named character.")
    else:
        print(f"\nNo number between {a} and {b}\n  is the code point of a named character.")
    

