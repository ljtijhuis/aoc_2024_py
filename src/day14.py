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

# calc_safety_factor([(2, 4, 2, -3)], 11, 7, 1)

safety_factor = calc_safety_factor(robots, 11, 7, 100)
print(safety_factor)

safety_factor = calc_safety_factor(robots, 101, 103, 100)
print(safety_factor)