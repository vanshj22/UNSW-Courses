def apply_pattern_to_list(L, pattern='+-', from_start=True):
    poped_elements = {}
    parsed_pattern =list(pattern)
    pattern_len = len(parsed_pattern)

    def check_sign(x, y, pattern_char):
        if pattern_char == '+':
            return x < y
        elif pattern_char == '-':
            return x > y
        else:
            return False

    if from_start:
        index_dict= {i: value for i, value in enumerate(L)}
        i=0

        while i < len(index_dict) - 1:
            keys = list(index_dict.keys())
            pattern_char = parsed_pattern[i % pattern_len]
            key1, key2 = keys[i], keys[i + 1]

            if check_sign(index_dict[key1], index_dict[key2], pattern_char):
                i+=1
            else:
                poped_elements[key2] = index_dict.pop(key2)
                i= max(0, i - 1)

        L[:] = [index_dict[key] for key in sorted(index_dict.keys())]

    else:
        index_dict = {-(len(L) - i): value for i, value in enumerate(L[::-1])}
        original_indices = {-(len(L) - i): -(i + 1) for i in range(len(L))}  
        reversed_pattern = parsed_pattern[::-1]
  
        i=0

        while i < len(index_dict) - 1:
            keys = list(index_dict.keys()) 
            pattern_char = reversed_pattern[i % pattern_len] 
            key1, key2 = keys[i], keys[i + 1]

            if check_sign(index_dict[key1], index_dict[key2], pattern_char):
                i+=1
            else:
                poped_elements[original_indices[key2]] = index_dict.pop(key2)  
                keys = list(index_dict.keys()) 
                i = max(0, i - 1)


        L[:] = [index_dict[key] for key in sorted(index_dict.keys(), reverse=True)]

    return poped_elements



L = [0, -4, 4, 4, 2, -2, 1, 3, -3, -4, -4, -2, -3, 0, 1, 2, -4, 3, -1, 1]
apply_pattern_to_list(L, '-+', False)

print(L)
