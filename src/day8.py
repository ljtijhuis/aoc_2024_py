def count_antinodes(grid):
    # Get all antennas and their locations
    antennas = find_antennas(grid)
    for (antenna, locations) in antennas.items():
        for loc1 in locations:
            for loc2 in locations:
                if loc1 == loc2:
                    continue
                anti1 = (loc1[0] + (loc1[0]-loc2[0]), loc1[1] + (loc1[1]-loc2[1]))
                anti2 = (loc2[0] + (loc2[0]-loc1[0]), loc2[1] + (loc2[1]-loc1[1]))
                if (anti1[0] >= 0 
                    and anti1[0] < len(grid) 
                    and anti1[1] >= 0 
                    and anti1[1] < len(grid[0])):
                    grid[anti1[0]][anti1[1]] = '#'

                if (anti2[0] >= 0 
                    and anti2[0] < len(grid) 
                    and anti2[1] >= 0 
                    and anti2[1] < len(grid[0])):
                    grid[anti2[0]][anti2[1]] = '#'

    return sum([row.count('#') for row in grid])

def count_resonating_antinodes(grid):
    # Get all antennas and their locations
    antennas = find_antennas(grid)
    for (antenna, locations) in antennas.items():
        for loc1 in locations:
            # also mark the antennas themselves
            grid[loc1[0]][loc1[1]] = '#'
            for loc2 in locations:
                if loc1 == loc2:
                    continue

                delta_row = loc1[0] - loc2[0]
                delta_col = loc1[1] - loc2[1]
                i = 1

                while True:
                    anti = (loc1[0] + delta_row * i, loc1[1] + delta_col * i)
                    if (anti[0] >= 0 
                        and anti[0] < len(grid) 
                        and anti[1] >= 0 
                        and anti[1] < len(grid[0])):
                        grid[anti[0]][anti[1]] = '#'
                    else:
                        break
                    i += 1

                delta_row = loc2[0] - loc1[0]
                delta_col = loc2[1] - loc1[1]
                i = 1

                while True:
                    anti = (loc2[0] + delta_row * i, loc2[1] + delta_col * i)
                    if (anti[0] >= 0 
                        and anti[0] < len(grid) 
                        and anti[1] >= 0 
                        and anti[1] < len(grid[0])):
                        grid[anti[0]][anti[1]] = '#'
                    else:
                        break
                    i += 1

    return sum([row.count('#') for row in grid])


def find_antennas(grid):
    antennas = {}
    for row, row_list in enumerate(grid):
        for col, _ in enumerate(row_list):
            antenna = grid[row][col]
            if antenna != '.':
                positions = antennas.get(antenna, set())
                positions.add((row, col))
                antennas[antenna] = positions
    return antennas

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read().splitlines()

def parse_input(lines):
    return [list(line) for line in lines]

lines = read_file('day8.txt')
grid = parse_input(lines)

count = count_antinodes(grid)
resonating = count_resonating_antinodes(parse_input(lines))

print(count)
print(resonating)