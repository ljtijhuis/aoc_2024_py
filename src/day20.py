def best_cheats(maze):
    (start, end) = find_start_and_end(maze)
    fastest = fastest_path(maze, start, end)
    count = 0
    for row, row_list in enumerate(maze):
        if row == 0 or row == len(maze) - 1:
            continue
        for col, value in enumerate(row_list):
            if col == 0 or row == len(maze[0]) - 1:
                continue

            if value == '#':
                # remove wall
                maze[row][col] = '.'
                # calc fastest
                steps = fastest_path(maze, start, end)
                if fastest - steps  >= 100:
                    count += 1
                # place wall back
                maze[row][col] = '#'
    return count

def best_cheats_updated(maze, save_at_least):
    print("Find any cheats that save us at least " + str(save_at_least))
    (start, end) = find_start_and_end(maze)
    distances = distance_map(maze)
    count = 0

    # BFS from start
    queue = [(start[0], start[1], 0)]
    visited = set()
    visited.add((start[0], start[1]))

    while len(queue) > 0:
        row, col, steps = queue.pop(0)
        from_here = distances[(row, col)]

        # print("From (" + str(row) + "," + str(col) +") steps remaining: " + str(from_here))

        # For each position check all squares within 20 steps
        for d_r in range(21):
            for d_c in range(21-d_r):
                # If current steps + distance to the square + distance to end
                # saves at least 100 picoseconds, we found another cheat
                count += good_cheat(row, col, d_r, d_c, distances, from_here, save_at_least)
                
        if cell_accessible(row - 1, col, maze, visited):
            queue.append((row - 1, col, steps + 1))
            visited.add((row - 1, col))
        if cell_accessible(row + 1, col, maze, visited):
            queue.append((row + 1, col, steps + 1))
            visited.add((row + 1, col))
        if cell_accessible(row, col - 1, maze, visited):
            queue.append((row, col - 1, steps + 1))
            visited.add((row, col - 1))
        if cell_accessible(row, col + 1, maze, visited):
            queue.append((row, col + 1, steps + 1))
            visited.add((row, col + 1))

    return count

def good_cheat(row, col, d_r, d_c, distances, from_here, save_at_least):
    count = 0
    shortcut_distance = d_r + d_c
    
    # dedupe any overlap when one of the offsets is 0
    coords_to_check = set()
    coords_to_check.add((row + d_r, col + d_c))
    coords_to_check.add((row + d_r, col - d_c))
    coords_to_check.add((row - d_r, col + d_c))
    coords_to_check.add((row - d_r, col - d_c))
    for r, c in coords_to_check:
        if (r, c) in distances:
            to_end = distances[(r, c)]
            if from_here - (shortcut_distance + to_end) >= save_at_least:
                # print("Skipping ahead to ("+str(row + d_r)+","+str(col + d_c)+"), shortcut distance "+str(shortcut_distance)+", distance left: " + str(to_end))
                count += 1
    return count
   
def distance_map(maze):
    (start, end) = find_start_and_end(maze)
    distances = {}
    # BFS from end to all possible locations to calculate fastest
    # path to end from anywhere
    queue = [(end[0], end[1], 0)]
    distances[(end[0], end[1])] = 0
    while len(queue) > 0:
        row, col, steps = queue.pop(0)
        
        if cell_accessible(row - 1, col, field, distances):
            queue.append((row - 1, col, steps + 1))
            distances[(row - 1, col)] = steps + 1
        if cell_accessible(row + 1, col, field, distances):
            queue.append((row + 1, col, steps + 1))
            distances[(row + 1, col)] = steps + 1
        if cell_accessible(row, col - 1, field, distances):
            queue.append((row, col - 1, steps + 1))
            distances[(row, col - 1)] = steps + 1
        if cell_accessible(row, col + 1, field, distances):
            queue.append((row, col + 1, steps + 1))
            distances[(row, col + 1)] = steps + 1

    return distances

def fastest_path(field, start, end):
    queue = [(start[0], start[1], 0)]
    visited = set()
    visited.add((0, 0))

    while len(queue) > 0:
        row, col, steps = queue.pop(0)
        if row == end[0] and col == end[1]:
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
        
def find_start_and_end(maze):
    start = None
    end = None
    for row, row_list in enumerate(maze):
        for col, value in enumerate(row_list):
            if value == 'S':
                start = (row, col)
            if value == 'E':
                end = (row, col)
    return (start, end)

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
    field = [list(line) for line in text.splitlines()]
    return field

text = read_file('day20.txt')
field = parse_input(text)

# Part 1
n = best_cheats(field)
print(n)

# Part 2
n = best_cheats_updated(field, 100)
print(n)
