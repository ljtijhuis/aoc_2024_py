def corrupt(field, coordinates):
    for col, row in coordinates:
        field[row][col] = '#'

def fastest_path(field):
    queue = [(0, 0, 0)]
    visited = set()
    visited.add((0, 0))

    while len(queue) > 0:
        row, col, steps = queue.pop(0)
        if row == len(field) - 1 and col == len(field[0]) - 1:
            return steps
        
        if cell_accessible(row - 1, col, field, visited):
            queue.append((row - 1, col, steps + 1))
            visited.add((row - 1, col))
        if cell_accessible(row + 1, col, field, visited):
            queue.append((row + 1, col, steps + 1))
            visited.add((row + 1, col))
        if cell_accessible(row, col - 1, field, visited):
            queue.append((row, col - 1, steps + 1))
            visited.add((row, col - 1))
        if cell_accessible(row, col + 1, field, visited):
            queue.append((row, col + 1, steps + 1))
            visited.add((row, col + 1))
    return -1


def cell_accessible(row, col, field, visited):
    return (row >= 0
            and row < len(field)
            and col >= 0
            and col < len(field[0])
            and field[row][col] != '#'
            and not (row, col) in visited)

def path_blocked_by(field, debris):
    for col, row in debris:
        corrupt(field, [(col, row)])
        steps = fastest_path(field)
        if steps == -1:
            return row, col

def print_field(field, r, c):
    for row, row_list in enumerate(field):
        for col, value in enumerate(row_list):
            if r == row and c == col:
                print('@', end='')
            else: 
                print(value, end='')
        print('')

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    field = [list(map(int, line.split(","))) for line in text.splitlines()]
    return field

text = read_file('day18.txt')
debris = parse_input(text)
field = [['.' for _ in range(71)] for _ in range(71)]

# Part 1
corrupt(field, debris[0:1024])
steps = fastest_path(field)
print(steps)

# Part 2
row, col = path_blocked_by(field, debris)
print(str(col) + "," + str(row))