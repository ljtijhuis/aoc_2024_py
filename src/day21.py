class Robot():
    def __init__(self):
        super().__init__()
        self.keypad = []

    def get_moves(self, sequence):
        print("Getting moves for sequence length " + str(len(sequence)))
        current = self.position
        moves = [[]]
        for key in sequence:
            target = self.get_key_position(key)
            d_r = target[0] - current[0]
            d_c = target[1] - current[1]
            if d_r == 0 and d_c == 0:
                # Press A
                moves = [m + ['A'] for m in moves]
            elif d_r == 0:
                # We only move along column axis
                c = '<' if d_c < 0 else '>'
                keys = [c for i in range(abs(d_c))]
                moves = [m + keys + ['A'] for m in moves]
            elif d_c == 0:
                # we move only along row axis
                c = '^' if d_r < 0 else 'v'
                keys = [c for i in range(abs(d_r))]
                moves = [m + keys + ['A'] for m in moves]
            else:
                # We move across both, which multiplies possible shortest paths by two
                c = '^' if d_r < 0 else 'v'
                row_moves = [c for i in range(abs(d_r))]
                c = '<' if d_c < 0 else '>'
                col_moves = [c for i in range(abs(d_c))]
                
                row_first = [m + row_moves + col_moves + ['A'] for m in moves]
                col_first = [m + col_moves + row_moves + ['A'] for m in moves]
                
                if not self.crosses_empty(current, row_moves + col_moves) and not self.crosses_empty(current, col_moves + row_moves):
                    if d_c < 0:
                        moves = col_first
                    else:
                        moves = row_first
                elif not self.crosses_empty(current, row_moves + col_moves):
                    moves = row_first
                else:
                    moves = col_first

            current = target

        return moves

    def get_key_position(self, key):
        for row, row_value in enumerate(self.keypad):
            for col, value in enumerate(row_value):
                if value == key:
                    return (row, col)
        return None
    
    def crosses_empty(self, start, moves):
        current = start
        for m in moves:
            if m == '<':
                current = (current[0], current[1] - 1)
            elif m == '>':
                current = (current[0], current[1] + 1)
            elif m == 'v':
                current = (current[0] + 1, current[1])
            else:
                current = (current[0] - 1, current[1])
            if self.keypad[current[0]][current[1]] == ' ':
                return True
        return False

    
class NumpadRobot(Robot):
    def __init__(self):
        super().__init__()
        #     0   1   2
        #   +---+---+---+
        # 0 | 7 | 8 | 9 |
        #   +---+---+---+
        # 1 | 4 | 5 | 6 |
        #   +---+---+---+
        # 2 | 1 | 2 | 3 |
        #   +---+---+---+
        # 3     | 0 | A |
        #       +---+---+
        self.position = (3,2)
        self.keypad = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            [' ', '0', 'A']
        ]
    
class DirectionsRobot(Robot):
    def __init__(self):
        super().__init__()
        #     0   1   2
        #       +---+---+
        # 0     | ^ | A |
        #   +---+---+---+
        # 1 | < | v | > |
        #   +---+---+---+
        self.position = (0,2)
        self.keypad = [
            [' ', '^', 'A'],
            ['<', 'v', '>']
        ]

    
class RobotSequence:
    def __init__(self):
        # One directional keypad that you are using.
        # Two directional keypads that robots are using.
        # One numeric keypad (on a door) that a robot is using.
        self.robots = [
            NumpadRobot(),
            DirectionsRobot(),
            DirectionsRobot()
            # DirectionsRobot()
        ]
    
    def enter_sequence(self, sequence):
        possible_sequences = self.enter_sequence_specific_robot(sequence, 0)
        a_shortest_sequence = min(possible_sequences, key=len)
        return a_shortest_sequence
        
    
    def enter_sequence_specific_robot(self, sequence, i):
        print("Getting sequence for robot " + str(i))
        possible_sequences = []
        robot = self.robots[i]
        robot_sequences = robot.get_moves(sequence)
        print("We found " + str(len(robot_sequences)) + " possible sequences")
        
        if len(self.robots) - 1 == i:
            # last robot so nothing else to do
            return robot_sequences
        
        for s in robot_sequences:
            possible_sequences += self.enter_sequence_specific_robot(s, i + 1)

        return possible_sequences
    
class RobotSequenceExtended(RobotSequence):
    def __init__(self):
        super().__init__()
        # One directional keypad that you are using.
        # 25 directional keypads that robots are using.
        # One numeric keypad (on a door) that a robot is using.
        self.robots = [
            NumpadRobot()
        ]
        for i in range(25):
            self.robots.append(DirectionsRobot())

def depth_first_search(sequence, robot_i, max_robot, mem):
    if robot_i == max_robot:
        return len(sequence)
    
    key = "".join(sequence) + str(robot_i)
    if key in mem:
        return mem[key]

    robot = DirectionsRobot() if robot_i > 0 else NumpadRobot()
    pos = robot.position

    instructions_count = 0

    # what moves do I need to do for robot i?
    for s in sequence:
        moves, pos = get_moves(s, pos, robot_i)

        # now feed the moves one by one to the robots down the line, increasing count as we go
        # for m in moves:
        instructions_count += depth_first_search(moves, robot_i + 1, max_robot, mem)

    mem[key] = instructions_count

    # return the total count to perform all the moves
    return instructions_count

def get_moves(s, start, robot_i):
    robot = DirectionsRobot() if robot_i > 0 else NumpadRobot()
    target = robot.get_key_position(s)
    d_r = target[0] - start[0]
    d_c = target[1] - start[1]
    if d_r == 0 and d_c == 0:
        # Press A
        return ['A'], target
    elif d_r == 0:
        # We only move along column axis
        c = '<' if d_c < 0 else '>'
        return [c for i in range(abs(d_c))] + ['A'], target
    elif d_c == 0:
        # we move only along row axis
        c = '^' if d_r < 0 else 'v'
        return [c for i in range(abs(d_r))] + ['A'], target
    else:
        # We move across both, which multiplies possible shortest paths by two
        c = '^' if d_r < 0 else 'v'
        row_moves = [c for i in range(abs(d_r))]
        c = '<' if d_c < 0 else '>'
        col_moves = [c for i in range(abs(d_c))]
        
        row_first = row_moves + col_moves + ['A']
        col_first = col_moves + row_moves + ['A']
        
        if not robot.crosses_empty(start, row_moves + col_moves) and not robot.crosses_empty(start, col_moves + row_moves):
            if d_c < 0:
                return col_first, target
            else:
                return row_first, target
        elif not robot.crosses_empty(start, row_moves + col_moves):
            return row_first, target
        else:
            return col_first, target

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    codes = [list(line) for line in text.splitlines()]
    return codes

text = read_file('day21.txt')
codes = parse_input(text)
# codes = ['083A']

robot_sequence = RobotSequence() # Use for part 1
# robot_sequence = RobotSequenceExtended() # Use for part 2
sum = 0
for code in codes:
    sequence = robot_sequence.enter_sequence(code)
    print(sequence)
    sum += len(sequence) * int("".join(code[0:len(code)-1]))

print(sum)

sum = 0
for code in codes:
    count = depth_first_search(code, 0, 3, {})
    sum += count * int("".join(code[0:len(code)-1]))

print(sum)

sum = 0
for code in codes:
    count = depth_first_search(code, 0, 26, {})
    sum += count * int("".join(code[0:len(code)-1]))

print(sum)

