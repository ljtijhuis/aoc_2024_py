import csv
import itertools
import math

def calc_safety_factor(robots, width, height, seconds):
    quadrants = [[0, 0], [0, 0]]
    for r in robots:
        x, y, v_x, v_y = r
        new_x = (x + seconds * v_x) % width
        new_y = (y + seconds * v_y) % height
        if (new_x == ((width - 1) / 2)
            or new_y == ((height - 1) / 2)):
            continue
        
        qx = 0
        qy = 0
        if new_x > ((width - 1) / 2) - 1:
            qx = 1
        if new_y > ((height - 1) / 2) -1:
            qy = 1
        
        quadrants[qx][qy] += 1

    return quadrants[0][0] * quadrants[0][1] * quadrants[1][0] * quadrants[1][1]

def generate_csv(robots, width, height, seconds):

    filename = f"position_insights.csv"
    fieldnames = ['seconds', 'q0', 'q1', 'q2', 'q3', 'score', 'middle_x', 'middle_y', 'relative_distance', 'longest_row_sequence']

    # We keep the file open for the lifespan of the object
    log_file = open(filename, mode='w', newline='')
    writer = csv.DictWriter(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
    writer.writeheader()

    # Let's gather some insights to plot and see if we can detect a rendering that stands out
    for i in range(seconds):
        positions = {} # (x, y) => count
        quadrants = [[0, 0], [0, 0]]
        middle_x = 0
        middle_y = 0
        for r in robots:
            x, y, v_x, v_y = r
            new_x = (x + i * v_x) % width
            new_y = (y + i * v_y) % height

            positions[(new_x, new_y)] = positions.get((new_x, new_y), 0) + 1

            if new_x == ((width - 1) / 2) or new_y == ((height - 1) / 2):
                if new_x == ((width - 1) / 2):
                    middle_x += 1
                if new_y == ((height - 1) / 2):
                    middle_y += 1
            else:
                qx = 0
                qy = 0
                if new_x > ((width - 1) / 2) - 1:
                    qx = 1
                if new_y > ((height - 1) / 2) -1:
                    qy = 1        
                quadrants[qx][qy] += 1

        relative_distance = calc_relative_distance(positions)
        longest_row_sequence = calc_longest_row_sequence(positions, width, height)
        
        writer.writerow({
            'seconds': i,
            'q0': quadrants[0][0],
            'q1': quadrants[0][1],
            'q2': quadrants[1][0],
            'q3': quadrants[1][1],
            'score': quadrants[0][0] * quadrants[0][1] * quadrants[1][0] * quadrants[1][1],
            'middle_x': middle_x,
            'middle_y': middle_y,
            'relative_distance': relative_distance,
            'longest_row_sequence': longest_row_sequence            
        })
    log_file.close()

def calc_relative_distance(positions):
    total_distance = 0

    # calc distance from every point to every other point
    for a, b in itertools.combinations(positions.items(), 2):
        p1, c1 = a
        p2, c2 = b
        dx = abs(p1[0] - p2[0])
        dy = abs(p1[1] - p2[1])
        total_distance += math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)) * c1 * c2

    return total_distance

def calc_longest_row_sequence(positions, width, height):
    longest = 0
    for row in range(height):
        current = 0
        for col in range(width):
            num = positions.get((col, row))
            if not num == None:
                current += 1
                longest = max(longest, current)
            else:
                current = 0
    return longest

        
def draw(robots, width, height, seconds):
    positions = {} # (x, y) => count
    for r in robots:
        x, y, v_x, v_y = r
        new_x = (x + seconds * v_x) % width
        new_y = (y + seconds * v_y) % height
        positions[(new_x, new_y)] = positions.get((new_x, new_y), 0) + 1

    print('Seconds: ' + str(seconds))
    for row in range(height):
        for col in range(width):
            num = positions.get((col, row))
            if num == None:
                print(' ', end='')
            else:
                print(num, end='')
            
        print('')



def read_file(f):
    with open(f) as opened_file:
        return opened_file.read().splitlines()

def parse_input(lines):
    robots = []
    for line in lines:
        pos, v = line.split(" ")
        x = int(pos.split("=")[1].split(",")[0])
        y = int(pos.split("=")[1].split(",")[1])
        v_x = int(v.split("=")[1].split(",")[0])
        v_y = int(v.split("=")[1].split(",")[1])
        robots.append((x, y, v_x, v_y))
    return robots

lines = read_file('day14.txt')
# lines = [
#     "p=0,4 v=3,-3",
#     "p=6,3 v=-1,-3",
#     "p=10,3 v=-1,2",
#     "p=2,0 v=2,-1",
#     "p=0,0 v=1,3",
#     "p=3,0 v=-2,-2",
#     "p=7,6 v=-1,-3",
#     "p=3,0 v=-1,-2",
#     "p=9,3 v=2,3",
#     "p=7,3 v=-1,2",
#     "p=2,4 v=2,-3",
#     "p=9,5 v=-3,-3"
# ]

robots = parse_input(lines)

safety_factor = calc_safety_factor(robots, 11, 7, 100)
print(safety_factor)

safety_factor = calc_safety_factor(robots, 101, 103, 100)
print(safety_factor)

# let's gather some insights on the distribution
# generate_csv(robots, 11, 7, 5000)
# generate_csv(robots, 101, 103, 10000)

# Data crunching / CSV dump here: 
# https://docs.google.com/spreadsheets/d/1aWnrYg5zElkGwowCjALlRV7lTQM7JAvf0hMnqWwsMdA/edit?gid=1039272152#gid=1039272152

# draw some special values
values = [
    7569
]
for seconds in values:
    draw(robots, 101, 103, seconds)