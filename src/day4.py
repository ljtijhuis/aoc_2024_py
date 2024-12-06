
def word_search_count(lines):
    return horizontal_count(lines) + vertical_count(lines) + diagonal_count(lines)

def horizontal_count(lines):
    return sum([line.count('XMAS') + line.count('SAMX') for line in lines])

def vertical_count(lines):
    sum = 0
    for i in range(len(lines)):
        vertical_line = ''.join([line[i] for line in lines])
        sum += vertical_line.count('XMAS') + vertical_line.count('SAMX')
    return sum

def diagonal_count(lines): 
    rows = len(lines)
    cols = len(lines[0])
    diagonals = []

    #top left to bottom right
    for diag in range(rows + cols -1):
        diag_str = ''
        for offset in range(rows):
            x = -rows + diag + offset + 1
            y = offset
            if x < 0 or x > cols-1 or y > rows:
                continue
            diag_str += lines[y][x]

        diagonals.append(diag_str)

    #top right to bottom left
    for diag in range(rows + cols -1):
        diag_str = ''
        for offset in range(rows):
            x = rows + cols - 2 - diag - offset
            y = offset
            if x < 0 or x > cols-1 or y > rows:
                continue
            diag_str += lines[y][x]

        diagonals.append(diag_str)

    # print(diagonals)

    return sum([line.count('XMAS') + line.count('SAMX') for line in diagonals])

def cross_count(lines):
    # Find the A's
    # Check diagonals
    sum = 0
    for i in range(len(lines)-2):
        y = i + 1
        for j in range(len(lines[0])-2):
            x = j + 1
            if (lines[y][x] == 'A' 
                and ((lines[y-1][x-1] == 'M' and lines[y+1][x+1] == 'S') 
                or (lines[y-1][x-1] == 'S' and lines[y+1][x+1] == 'M')) 
                and ((lines[y-1][x+1] == 'M' and lines[y+1][x-1] == 'S') 
                or (lines[y-1][x+1] == 'S' and lines[y+1][x-1] == 'M'))):
                sum += 1
    return sum

def read_file(f):
    with open(f) as opened_file:
        return opened_file.readlines()

def parse_input(lines):
    return lines

lines = read_file('day4.txt')
# lines = [
#     'MMMSXXMASM',
#     'MSAMXMSMSA',
#     'AMXSXMAAMM',
#     'MSAMASMSMX',
#     'XMASAMXAMM',
#     'XXAMMXXAMA',
#     'SMSMSASXSS',
#     'SAXAMASAAA',
#     'MAMMMXMMMM',
#     'MXMXAXMASX'
# ]

# print(horizontal_count(lines))
# print(vertical_count(lines))
# print(diagonal_count(lines))
count = word_search_count(lines)
cross_count = cross_count(lines)
print(count)
print(cross_count)