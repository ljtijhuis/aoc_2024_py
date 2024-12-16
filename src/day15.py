def execute_moves(field, moves):
    (row, col) = find_robot(field)
    for (d_r, d_c) in moves:
        # print((d_r, d_c))
        steps = 1

        while (row + steps * d_r >= 0
               and row + steps * d_r < len(field)
               and col + steps * d_c >= 0
               and col + steps * d_c < len(field[0])):
            
            val = field[row + steps * d_r][col + steps * d_c]
            if val == '#':
                # we cannot move anything
                break
            
            if val == 'O' or val == '@':
                # we need to move the items further along
                steps += 1
            else:
                # let's move things, working backwards
                while steps > 0:
                    field[row + steps * d_r][col + steps * d_c] = field[row + (steps - 1) * d_r][col + (steps - 1) * d_c]
                    steps -= 1
                field[row][col] = '.'
                row += d_r
                col += d_c
                # print_field(field)
                break
    
    return field

def execute_moves_widened(field, moves):
    (row, col) = find_robot(field)
    for (d_r, d_c) in moves:
        # print_field(field)
        moves_to_process = []
        moves_work = gather_moves(row, col, d_r, d_c, field, moves_to_process)
        if moves_work:
            # We might hit a box through multiple different boxes and we only want to move it once so keep track
            moves_taken = set()
            while len(moves_to_process) > 0:
                move_row, move_col = moves_to_process.pop()
                if not (move_row, move_col) in moves_taken:
                    field[move_row + d_r][move_col + d_c] = field[move_row][move_col]
                    field[move_row][move_col] = '.'
                    moves_taken.add((move_row, move_col))
            field[row][col] = '.'
            row += d_r
            col += d_c
    
    return field

def gather_moves(row, col, d_r, d_c, field, moves):
    if field[row][col] == '.':
        return True
    if field[row][col] == '#':
        return False

    moves.append((row, col))
    move_works = gather_moves(row + d_r, col + d_c, d_r, d_c, field, moves)
    if d_r != 0 and field[row][col] == '[':
        moves.append((row, col+1))
        return move_works and gather_moves(row + d_r, col + 1 + d_c, d_r, d_c, field, moves)
    if d_r != 0 and field[row][col] == ']':
        moves.append((row, col-1))
        return move_works and gather_moves(row + d_r, col - 1 + d_c, d_r, d_c, field, moves)
    
    return move_works
        



def find_robot(field):
    for row, row_list in enumerate(field):
        for col, value in enumerate(row_list):
            if value == '@':
                return (row, col)

def print_field(field):
    for row, row_list in enumerate(field):
        for col, value in enumerate(row_list):
            print(value, end='')
        print('')
            
def box_sum(field):
    # The GPS coordinate of a box is equal to 100 times its distance from the top edge of the 
    # map plus its distance from the left edge of the map. (This process does not stop at wall 
    # tiles; measure all the way to the edges of the map.)

    # what is the sum of all boxes' GPS coordinates?
    sum = 0
    for row, row_list in enumerate(field):
        for col, value in enumerate(row_list):
            if value == 'O':
                sum += 100 * row + col
    return sum

def box_sum_widened(field):
    sum = 0
    for row, row_list in enumerate(field):
        for col, value in enumerate(row_list):
            if value == '[':
                sum += 100 * row + col
    return sum

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    split = text.split("\n\n")
    field = [list(line) for line in split[0].splitlines()]

    mapping = {
        '^': (-1, 0),
        'v': (1, 0),
        '>': (0, 1),
        '<': (0, -1),
        '\n': None
    }
    moves = [x for x in map(lambda c: mapping[c], split[1]) if x is not None]

    return field, moves

def parse_and_widen_input(text):
    # If the tile is #, the new map contains ## instead.
    # If the tile is O, the new map contains [] instead.
    # If the tile is ., the new map contains .. instead.
    # If the tile is @, the new map contains @. instead.
    split = text.split("\n\n")
    field = [list(line.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')) for line in split[0].splitlines()]

    mapping = {
        '^': (-1, 0),
        'v': (1, 0),
        '>': (0, 1),
        '<': (0, -1),
        '\n': None
    }
    moves = [x for x in map(lambda c: mapping[c], split[1]) if x is not None]

    return field, moves


text = read_file('day15.txt')
field, moves = parse_input(text)

field = execute_moves(field, moves)
sum = box_sum(field)
print(sum)

field, moves = parse_and_widen_input(text)
print_field(field)
field = execute_moves_widened(field, moves)
sum = box_sum_widened(field)
print(sum)
