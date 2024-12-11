def hiking_score(grid):
    trailheads = get_trailheads(grid)
    score = 0
    rating = 0
    for head in trailheads:
        # BFS to find the 9s reachable
        queue = [head]
        peaks_reachable = set()

        while len(queue) > 0:
            row, col, value = queue.pop()
            if value == 9:
                peaks_reachable.add((row, col))
                rating += 1
                continue

            if get_value(row + 1, col, grid) == value + 1:
                queue.append((row + 1, col, value + 1))
            if get_value(row - 1, col, grid) == value + 1:
                queue.append((row - 1, col, value + 1))
            if get_value(row, col + 1, grid) == value + 1:
                queue.append((row, col + 1, value + 1))
            if get_value(row, col - 1, grid) == value + 1:
                queue.append((row, col - 1, value + 1))

        score += len(peaks_reachable)
    return (score, rating)

def get_value(row, col, grid):
    if (row >= 0
        and row < len(grid)
        and col >= 0
        and col < len(grid[0])):
        return grid[row][col]
    return -1

def get_trailheads(grid):
    trailheads = []
    for row, row_list in enumerate(grid):
        for col, value in enumerate(row_list):
            if value == 0:
                trailheads.append((row, col, 0))
    return trailheads

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read().splitlines()

def parse_input(lines):
    return [list(map(int, list(line))) for line in lines]

lines = read_file('day10.txt')

# lines = [
#     "0123",
#     "1234",
#     "8765",
#     "9876",
# ]

# lines = [
#     "89010123",
#     "78121874",
#     "87430965",
#     "96549874",
#     "45678903",
#     "32019012",
#     "01329801",
#     "10456732"
# ]

grid = parse_input(lines)
score, rating = hiking_score(grid)

print(score)
print(rating)