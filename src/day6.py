import copy

def travel_grid(grid):
    # find starting position
    (x, y) = starting_position(grid)
    direction = (0, -1)
    
    visited = set()

    # keep walking while we are in the grid, count as we go
    spaces_travelled = 1
    block_opportunities = 0
    grid[y][x] = 'X'
    while True:

        # record where we are now
        visited.add((x, y, direction))
        
        # determine next spot
        (next_x, next_y) = (x + direction[0], y + direction[1])

        #are we stepping out?
        if next_x < 0 or next_x >= len(grid[0]) or next_y < 0 or next_y >= len(grid): 
            # we are exiting the grid
            break

        # can we enter the next spot?
        if grid[next_y][next_x] == '#':
            # if not, turn
            direction = next_direction(direction)
        else:

            # first check if we can create a loop by placing an obstacle
            if loop_possible(x, y, direction, grid, visited): # copy.deepcopy(directions_grid)):
                block_opportunities += 1
            
            # Count this spot for spaces traveled if we have not been here before
            if grid[next_y][next_x] != 'X':
                spaces_travelled += 1
                grid[next_y][next_x] = 'X'
            
            # update our position
            x = next_x
            y = next_y

    return (spaces_travelled, block_opportunities)

def loop_possible(x, y, direction, grid, visited):
    # we have an opportunity to create a loop
    visited_local = set()

    # place the obstacle and turn
    temp_obstacle_location = (x + direction[0], y + direction[1])
    
    # Did we check for an obstacle or walked here before?
    all_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    if grid[temp_obstacle_location[1]][temp_obstacle_location[0]] == '*' or any((temp_obstacle_location[0], temp_obstacle_location[1], d) in visited for d in all_directions):
        return False
    
    # place temp obstacle
    grid[temp_obstacle_location[1]][temp_obstacle_location[0]] = '#'

    direction = next_direction(direction)
    result = False

    # IF by taking the alternate route we eventually end up on the same path in the same direction
    # keep traversing in our alternative direction while we are in the grid and do not hit an obstacle
    while True:
        
        # if we encounter a spot where we have walked before in this same possible direction, we can create a loop
        if (x, y, direction) in visited or (x, y, direction) in visited_local: # directions_grid[y][x]:
            result = True
            break
        visited_local.add((x, y, direction))
        
        # we are using the same navigation logic as the main traversal function
        (next_x, next_y) = (x + direction[0], y + direction[1])
        if next_x < 0 or next_x >= len(grid[0]) or next_y < 0 or next_y >= len(grid): 
            break
        
        if grid[next_y][next_x] == '#':
            # if not, turn
            direction = next_direction(direction)
        else:
            # mark that we have traveled here in this given direction
            (x, y) = (next_x, next_y)
        
        

    # remove the temp obstacle - we mark we checked an obstacle here before
    grid[temp_obstacle_location[1]][temp_obstacle_location[0]] = '*'
    return result
    


def starting_position(grid):
    for i, row in enumerate(grid):
        ind = next((j for j, x in enumerate(row) if x == "^"), -1)
        if ind != -1:
            return (ind, i)

def next_direction(direction):
    # 0, -1 => 1, 0 => 0, 1 => -1, 0
    return (-direction[1], direction[0])
        
def read_file(f):
    with open(f) as opened_file:
        return opened_file.readlines()

def parse_input(lines):
    return [list(line) for line in lines]

lines = read_file('day6.txt')
parsed_lines = parse_input(lines)
(spaces_travelled, block_opportunities) = travel_grid(parsed_lines)

print(spaces_travelled)
print(block_opportunities)