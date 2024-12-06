

def list_distance(left, right):
    left.sort()
    right.sort()
    total_distance = 0
    for l, r in zip(left, right):
        total_distance += abs(l - r)

    return total_distance

def similarity_score(left, right):
    left.sort()
    right.sort()

    total = 0
    for l in left:
        count = 0
        for r in right:
            if r == l:
                count += 1

        total += l * count
    
    return total


def read_file(f):
    with open(f) as opened_file:
        return opened_file.readlines()

def parse_input(lines):
    pairs = [map(int, line.split()) for line in lines]
    left = []
    right = []
    for l, r in pairs:
        left.append(l)
        right.append(r)
    return (left, right)


lines = read_file('day1.txt')
parsed = parse_input(lines)
distance = list_distance(parsed[0], parsed[1])
similarity = similarity_score(parsed[0], parsed[1])

print(distance)
print(similarity)