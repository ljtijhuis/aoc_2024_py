def valid_combinations(locks, keys):
    n = 0
    for lock in locks:
        for key in keys:
            n += is_valid(lock, key)
    return n

def is_valid(lock, key):
    for i in range(5):
        if lock[i] + key[i] > 5:
            return False
    return True


def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def get_heights(s, input_type):
    heights = []
    for col in range(len(s[0])):
        if input_type == 'lock':
            for row in reversed(range(7)):
                if s[row][col] == '#':
                    heights.append(row)
                    break
        else:
            for row in range(7):
                if s[row][col] == '#':
                    heights.append(6-row)
                    break
    return heights

def parse_input(text):
    key_locks = text.split("\n\n")
    locks = []
    keys = []
    for kl in key_locks:
        s = kl.splitlines()
        if s[0][0] == '#':
            # Lock
            locks.append(get_heights(s, 'lock'))
        else:
            # key
            keys.append(get_heights(s, 'key'))
    return locks, keys

text = read_file('day25.txt')
locks, keys = parse_input(text)

n = valid_combinations(locks, keys)
print(n)