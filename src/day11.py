
def blink(stones):
    new_stones = []

    for stone in stones:
        if stone == 0:
            # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. 
            # The left half of the digits are engraved on the new left stone, and the right half of the digits are 
            # engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
            stone_str = str(stone)
            l = len(stone_str)
            new_stones.append(int(stone_str[:int(l/2)]))
            new_stones.append(int(stone_str[int(l/2):]))
        else:
            # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is 
            # engraved on the new stone.
            new_stones.append(stone * 2024)
    
    return new_stones

def blink_stone_counter(stones, repeats):
    # instead of keeping track of the stones, let's keep track of the kind of stones we have
    # - how many zeroes?
    # - how many with an even number of digits?
    # - other

    # The question then becomes, how do numbers in the other category end up in one of the first two again?
    # - zeroes will only occur if we split a number (case 2) and the right side is just zeroes
    # - when multiplying with 2024, what happens?
    #   - some numbers will have an even number of digits
    #   - others will have an uneven number of digits -> at this point we multiply again with 2024. Is that guaranteed to end up with an even amount? No! (see example)

    # Alternative idea: how many distinct numbers do we get? Should we just keep a map of number to how many times it occurs? (From example it looks to be a lot of different numbers)
    stone_counts = {}
    for stone in stones:
        stone_counts[stone] = stone_counts.get(stone, 0) + 1

    for i in range(repeats):
        new_stone_counts = {}
        for number, count in stone_counts.items():
            if number == 0:
                # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
                new_stone_counts[1] = new_stone_counts.get(1, 0) + count
            elif len(str(number)) % 2 == 0:
                # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. 
                # The left half of the digits are engraved on the new left stone, and the right half of the digits are 
                # engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
                stone_str = str(number)
                l = len(stone_str)

                new_stone_counts[int(stone_str[:int(l/2)])] = new_stone_counts.get(int(stone_str[:int(l/2)]), 0) + count
                new_stone_counts[int(stone_str[int(l/2):])] = new_stone_counts.get(int(stone_str[int(l/2):]), 0) + count
            else:
                # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is 
                # engraved on the new stone.
                new_stone_counts[number * 2024] = new_stone_counts.get(number * 2024, 0) + count
        stone_counts = new_stone_counts

    return sum([count for number, count in stone_counts.items()])    

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    return list(map(int, text.split()))

text = read_file('day11.txt')
# text = "125 17"

stones = parse_input(text)
print(stones)

# blinking 6 times
changed_stones = stones[:]
for i in range(6):
    changed_stones = blink(changed_stones)
    print(changed_stones)

print(len(changed_stones))
print(blink_stone_counter(stones, 6))

#blinking 25 times
changed_stones = stones[:]
for i in range(25):
    changed_stones = blink(changed_stones)
    # print(changed_stones)

print(len(changed_stones))
print(blink_stone_counter(stones, 25))

#blinking 75 times
# changed_stones = stones[:]
# for i in range(75):
#     print(i)
#     print(len(changed_stones))
#     changed_stones = blink(changed_stones)
#     # print(changed_stones)

# print(len(changed_stones))
print(blink_stone_counter(stones, 75))