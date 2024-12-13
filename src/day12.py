def fence_pricing(grid):
    spots_covered = set()
    clusters = []

    # Go over each spot in the grid
    print("Finding clusters")
    for row, row_list in enumerate(grid):
        print("Row " + str(row))
        print("Length " + str(len(row_list)))
        for col, _ in enumerate(row_list):
            # Check if the spot is already in one of the clusters  
            if (row, col) in spots_covered:
                continue

            # If not, do a BFS to get another cluster
            cluster = bfs(row, col, grid)
            clusters.append(cluster)
            for coords in cluster:
                spots_covered.add(coords)

    # Calculate total cost
    print("Calculating cost")
    total_cost = 0
    total_cost_sides = 0
    # For each cluster, calculate perimeter
    for cluster in clusters:
        perimeter = calc_perimeter(cluster)
        sides = calc_fence_sides(cluster)
        area = len(cluster)
        total_cost += perimeter * area
        total_cost_sides += sides * area
    
    return (total_cost, total_cost_sides)
    

def bfs(row, col, grid):
    ch = grid[row][col]
    queue = [(row, col)]

    cluster = set()
    visited = set()
    while len(queue) > 0:
        row, col = queue.pop(0)
        cluster.add((row, col))

        if row > 0 and grid[row-1][col] == ch and (row-1, col) not in visited:
            queue.append((row-1, col))
            visited.add((row-1, col))
        if row+1 < len(grid) and grid[row+1][col] == ch and (row+1, col) not in visited:
            queue.append((row+1, col))
            visited.add((row+1, col))
        if col > 0 and grid[row][col-1] == ch and (row, col-1) not in visited:
            queue.append((row, col-1))
            visited.add((row, col-1))
        if col+1 < len(grid[row]) and grid[row][col+1] == ch and (row, col+1) not in visited:
            queue.append((row, col+1))
            visited.add((row, col+1))
    
    return cluster

def calc_perimeter(cluster):
    total_fences = 0
    for (row, col) in cluster:
        if not (row+1, col) in cluster:
            total_fences += 1
        if not (row-1, col) in cluster:
            total_fences += 1
        if not (row, col+1) in cluster:
            total_fences += 1
        if not (row, col-1) in cluster:
            total_fences += 1
    return total_fences

def calc_fence_sides(cluster):
    # find min and max row and col
    min_row = 9999999999
    max_row = 0
    min_col = 9999999999
    max_col = 0
    for row, col in cluster:
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

    # then go over each row and col in between to see how many pieces of fence are needed there

    # for rows, we check the top side
    distinct_fences = 0
    for row in range(min_row, max_row+1):
        running_fence = False
        for col in range(min_col, max_col+1):
            # every time we have a cell where there is no cell above it, there needs to be a fence
            if (row, col) in cluster and not (row-1, col) in cluster:
                # if the previous already was a fence, we do not count an extra
                if not running_fence:
                    running_fence = True
                    distinct_fences += 1
            else:
                running_fence = False
    
    # then the bottom sides
    for row in range(min_row, max_row+1):
        running_fence = False
        for col in range(min_col, max_col+1):
            if (row, col) in cluster and not (row+1, col) in cluster:
                if not running_fence:
                    running_fence = True
                    distinct_fences += 1
            else:
                running_fence = False

    # for columns, we check the left side
    for col in range(min_col, max_col+1):
        running_fence = False
        for row in range(min_row, max_row+1):
            # every time we have a cell where there is no cell left of it, there needs to be a fence
            if (row, col) in cluster and not (row, col-1) in cluster:
                # if the previous already was a fence, we do not count an extra
                if not running_fence:
                    running_fence = True
                    distinct_fences += 1
            else:
                running_fence = False
    
    # right side
    for col in range(min_col, max_col+1):
        running_fence = False
        for row in range(min_row, max_row+1):
            if (row, col) in cluster and not (row, col+1) in cluster:
                if not running_fence:
                    running_fence = True
                    distinct_fences += 1
            else:
                running_fence = False

    return distinct_fences

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read().splitlines()

def parse_input(lines):
    return [list(line) for line in lines]

lines = read_file('day12.txt')
# lines = [
#     "AAAA",
#     "BBCD",
#     "BBCC",
#     "EEEC"
# ]

# lines = [
#     "OOOOO",
#     "OXOXO",
#     "OOOOO",
#     "OXOXO",
#     "OOOOO"
# ]

# lines = [
#     "RRRRIICCFF",
#     "RRRRIICCCF",
#     "VVRRRCCFFF",
#     "VVRCCCJFFF",
#     "VVVVCJJCFE",
#     "VVIVCCJJEE",
#     "VVIIICJJEE",
#     "MIIIIIJJEE",
#     "MIIISIJEEE",
#     "MMMISSJEEE"
# ]

# lines = [
#     "EEEEE",
#     "EXXXX",
#     "EEEEE",
#     "EXXXX",
#     "EEEEE"
# ]

# lines = [
#     "AAAAAA",
#     "AAABBA",
#     "AAABBA",
#     "ABBAAA",
#     "ABBAAA",
#     "AAAAAA"
# ]
grid = parse_input(lines)

print(grid)

price, discounted = fence_pricing(grid)

print(price)
print(discounted)