import sys

def traverse_maze(maze):
    ((s_row, s_col), (e_row, e_col)) = find_start_and_end(maze)

    # The Reindeer start on the Start Tile (marked S) facing East and need 
    # to reach the End Tile (marked E). They can move forward one tile at a 
    # time (increasing their score by 1 point), but never into a wall (#). 
    # They can also rotate clockwise or counterclockwise 90 degrees at a time 
    # (increasing their score by 1000 points).

    # We need to keep track of current position, direction and cost so far
    # part 2: added set of places visited
    queue = [(s_row, s_col, 0, 1, 0, set((s_row, s_col)))]
    min_cost = sys.maxsize
    min_visited = set()
    visited = {(s_row, s_col): 0}

    while len(queue) > 0:
        row, col, dr, dc, cost, path = queue.pop(0)
        # print(min_cost)
        # print_field(maze, row, col)

        if cost > min_cost:
            continue
        
        # try straight
        if cell_accessible(row + dr, col + dc, maze, cost + 1, visited):
            if row + dr == e_row and col + dc == e_col:
                if cost + 1 < min_cost:
                    min_cost = cost + 1
                    min_visited = path
                elif cost + 1 == min_cost:
                    min_visited = min_visited.union(path)
            else:
                p = path.copy()
                p.add((row + dr, col + dc))
                queue.append((row + dr, col + dc, dr, dc, cost + 1, p))
                visited[(row + dr, col + dc)] = cost + 1


        # try turning left
        turn_dr, turn_dc = turn_left(dr, dc)
        if cell_accessible(row + turn_dr, col + turn_dc, maze, cost + 1001, visited):
            if row + turn_dr == e_row and col + turn_dc == e_col:
                if cost + 1001 < min_cost:
                    min_cost = cost + 1001
                    min_visited = path
                elif cost + 1001 == min_cost:
                    min_visited = min_visited.union(path)
            else:
                p = path.copy()
                p.add((row + turn_dr, col + turn_dc))
                queue.append((row + turn_dr, col + turn_dc, turn_dr, turn_dc, cost + 1001, p))
                visited[(row + turn_dr, col + turn_dc)] = cost + 1001

        # try turning right
        turn_dr, turn_dc = turn_right(dr, dc)
        if cell_accessible(row + turn_dr, col + turn_dc, maze, cost + 1001, visited):
            if row + turn_dr == e_row and col + turn_dc == e_col:
                if cost + 1001 < min_cost:
                    min_cost = cost + 1001
                    min_visited = path
                elif cost + 1001 == min_cost:
                    min_visited = min_visited.union(path)
            else:
                p = path.copy()
                p.add((row + turn_dr, col + turn_dc))
                queue.append((row + turn_dr, col + turn_dc, turn_dr, turn_dc, cost + 1001, p))
                visited[(row + turn_dr, col + turn_dc)] = cost + 1001
    
    return min_cost, min_visited



def cell_accessible(row, col, field, cost, visited):
    return (row >= 0
            and row < len(field)
            and col >= 0
            and col < len(field[0])
            and field[row][col] != '#'
            # we will only consider spots we have not visited
            # OR visited but with a higher score (and some buffer..)
            and (not (row, col) in visited or visited[row, col] + 2000 > cost))

def turn_right(dr, dc):
    return (dc, -dr)

def turn_left(dr, dc):
    return (-dc, dr)

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

text = read_file('day16.txt')
maze = parse_input(text)

cost, min_visited = traverse_maze(maze)
print(cost)
print(len(min_visited))