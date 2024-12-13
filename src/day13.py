def solve_equations(equations, increment):
    # it costs 3 tokens to push the A button and 1 token to push the B button.
    tokens = 0
    for eq in equations:
        (a, b) = solve(eq, increment)
        if a.is_integer() and b.is_integer():
            tokens += 3 * int(a) + int(b)
    return tokens

def solve(equation, increment):
    # a + b = x
    # a + b = y

    # a = x - b
    # b = y - a

    # (x - b) + b = y
    # -> x = y

    # Button A: X+94, Y+34
    # Button B: X+22, Y+67
    # Prize: X=8400, Y=5400

    # 8400 = 94A + 22B
    # 5400 = 34A + 67B

    # ==>
    # B = (5400 * 94 - 34 * 8400) / (94 * 67 - 34 * 22)
    #   = 40
    # A = (8400 - 22 * 40) / 94
    #   = 80

    # ==> 
    # B = (y * a_x - a_y * x) / (a_x * b_y - a_y * b_x)
    # A = (x - b_x * B) / a_x
    a_x, a_y, b_x, b_y, x, y = equation
    x += increment
    y += increment
    b = (y * a_x - a_y * x) / (a_x * b_y - a_y * b_x)
    a = (x - b_x * b) / a_x
    return (a, b)

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    configurations = text.split("\n\n");
    # Button A: X+42, Y+24
    # Button B: X+23, Y+55
    # Prize: X=18849, Y=8875
    equations = []
    for config in configurations:
        lines = config.splitlines()
        values = lines[0].split(": ")[1].split(", ")
        a_x = int(values[0].split("+")[1])
        a_y = int(values[1].split("+")[1])

        values = lines[1].split(": ")[1].split(", ")
        b_x = int(values[0].split("+")[1])
        b_y = int(values[1].split("+")[1])

        values = lines[2].split(": ")[1].split(", ")
        x = int(values[0].split("=")[1])
        y = int(values[1].split("=")[1])
        equations.append((a_x, a_y, b_x, b_y, x, y))

    return equations

text = read_file('day13.txt')

# text = """Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279"""

equations = parse_input(text)

tokens = solve_equations(equations, 0)
print(tokens)

tokens = solve_equations(equations, 10000000000000)
print(tokens)
