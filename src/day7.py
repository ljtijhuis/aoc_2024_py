
def check_equations(equations):
    sum = 0
    for (test_value, numbers) in equations:
        if can_evaluate(test_value, numbers[1:], numbers[0]):
            sum += test_value

    return sum


def can_evaluate(test_value, numbers, partial_result):
    if partial_result > test_value:
        return False
    
    if len(numbers) == 0:
        return partial_result == test_value
    
    # multiply with next number or add
    next_number = numbers[0]
    return (can_evaluate(test_value, numbers[1:], partial_result * next_number) 
        or can_evaluate(test_value, numbers[1:], partial_result + next_number))

def check_equations2(equations):
    sum = 0
    for (test_value, numbers) in equations:
        if can_evaluate2(test_value, numbers[1:], numbers[0]):
            sum += test_value

    return sum

def can_evaluate2(test_value, numbers, partial_result):
    if partial_result > test_value:
        return False
    
    if len(numbers) == 0:
        return partial_result == test_value
    
    # multiply with next number or add OR concat
    next_number = numbers[0]
    concatenated = int(str(partial_result) + str(next_number))
    return (can_evaluate2(test_value, numbers[1:], partial_result * next_number) 
        or can_evaluate2(test_value, numbers[1:], partial_result + next_number)
        or can_evaluate2(test_value, numbers[1:], concatenated))

def read_file(f):
    with open(f) as opened_file:
        return opened_file.readlines()

def parse_input(lines):
    equations = []
    for line in lines:
        (test_value, numbers) = line.split(": ")
        equations.append((int(test_value), [int(n) for n in numbers.split(" ")]))
    return equations

lines = read_file('day7.txt')
equations = parse_input(lines)
sum = check_equations(equations)
sum2 = check_equations2(equations)

print(sum)
print(sum2)