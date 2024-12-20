import math

def execute_program(program, register_values):
    instruction_pointer = 0
    registers = register_values
    output = []

    while instruction_pointer < len(program):
        instruction = program[instruction_pointer]
        match instruction:
            case 0:
                # The adv instruction (opcode 0) performs division. The numerator is the value 
                # in the A register. The denominator is found by raising 2 to the power of the 
                # instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); 
                # an operand of 5 would divide A by 2^B.) The result of the division operation 
                # is truncated to an integer and then written to the A register.
                numerator = registers[0]
                denominator = pow(2, combo_operand(program[instruction_pointer + 1], registers))
                registers[0] = math.trunc(numerator / denominator)
                instruction_pointer += 2
            case 1:
                # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and 
                # the instruction's literal operand, then stores the result in register B.
                operand = program[instruction_pointer + 1]
                registers[1] = registers[1] ^ operand
                instruction_pointer += 2
            case 2:
                # The bst instruction (opcode 2) calculates the value of its combo operand 
                # modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to 
                # the B register.
                registers[1] = combo_operand(program[instruction_pointer + 1], registers) % 8
                instruction_pointer += 2
            case 3:
                # The jnz instruction (opcode 3) does nothing if the A register is 0. However, 
                # if the A register is not zero, it jumps by setting the instruction pointer to 
                # the value of its literal operand; if this instruction jumps, the instruction 
                # pointer is not increased by 2 after this instruction.
                if registers[0] != 0:
                    instruction_pointer = program[instruction_pointer + 1]
                else:
                    instruction_pointer += 2
            case 4:
                # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and 
                # register C, then stores the result in register B. (For legacy reasons, this 
                # instruction reads an operand but ignores it.)
                registers[1] = registers[1] ^ registers[2]
                instruction_pointer += 2
            case 5:
                # The out instruction (opcode 5) calculates the value of its combo operand 
                # modulo 8, then outputs that value. (If a program outputs multiple values, 
                # they are separated by commas.)
                output.append(combo_operand(program[instruction_pointer + 1], registers) % 8)
                instruction_pointer += 2
            case 6:
                # The bdv instruction (opcode 6) works exactly like the adv instruction except 
                # that the result is stored in the B register. (The numerator is still read 
                # from the A register.)
                numerator = registers[0]
                denominator = pow(2, combo_operand(program[instruction_pointer + 1], registers))
                registers[1] = math.trunc(numerator / denominator)
                instruction_pointer += 2
            case 7:
                # The cdv instruction (opcode 7) works exactly like the adv instruction except 
                # that the result is stored in the C register. (The numerator is still read 
                # from the A register.)
                numerator = registers[0]
                denominator = pow(2, combo_operand(program[instruction_pointer + 1], registers))
                registers[2] = math.trunc(numerator / denominator)
                instruction_pointer += 2
            case _:
                raise Exception("Invalid instruction found", instruction)
    return output
            
def combo_operand(operand, registers):
    # Combo operands 0 through 3 represent literal values 0 through 3.
    # Combo operand 4 represents the value of register A.
    # Combo operand 5 represents the value of register B.
    # Combo operand 6 represents the value of register C.
    # Combo operand 7 is reserved and will not appear in valid programs.
    match operand:
        case operand if operand < 4:
            return operand
        case 4:
            return registers[0]
        case 5:
            return registers[1]
        case 6:
            return registers[2]
        case _:
            raise Exception("Invalid combo operand value found", operand)
    

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    # Register A: 729
    # Register B: 0
    # Register C: 0

    # Program: 0,1,5,4,3,0
    inputs = text.split("\n\n")
    registers = [int(line.split(": ")[1]) for line in inputs[0].splitlines()]
    program = list(map(int, inputs[1].split(": ")[1].split(",")))
    return (program, registers)

text = read_file('day17.txt')
program, register_values = parse_input(text)

output = execute_program(program, register_values)
print(",".join(str(i) for i in output))

# # Part 2

# # Input:

# # Register A: 44374556
# # Register B: 0
# # Register C: 0

# # Combo operands 0 through 3 represent literal values 0 through 3.
# # Combo operand 4 represents the value of register A.
# # Combo operand 5 represents the value of register B.
# # Combo operand 6 represents the value of register C.
# # Combo operand 7 is reserved and will not appear in valid programs.

# # Program: 
# # 2 
# # 4
# # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

# B = A % 8 (keeping only lowest 3 bits from A)

# Options:
# B = 0..7

# # 1
# # 5
# # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

# B = B XOR 101
# B = 0 -> B = 5
# B = 1 -> B = 4
# B = 2 -> B = 7
# B = 3 -> B = 6
# B = 4 -> B = 1
# B = 5 -> B = 0
# B = 6 -> B = 3
# B = 7 -> B = 2

# 00000101 = ... + 1 * 2 ^2 + 0 * 2 ^ 1 + 1 * 2 ^ 0 = 5
# 10000100
# 10000001

# # 7
# # 5
# # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

# C = A / 2 ^ B (truncated to an int)

# B = 0 -> B = 5 -> C = A /  32 = A / 00100000
# B = 1 -> B = 4 -> C = A /  16 = A / 00010000
# B = 2 -> B = 7 -> C = A / 128 = A / 10000000
# B = 3 -> B = 6 -> C = A /  64 = A / 01000000
# B = 4 -> B = 1 -> C = A /   2 = A / 00000010
# B = 5 -> B = 0 -> C = A /   1 = A / 00000001
# B = 6 -> B = 3 -> C = A /   8 = A / 00001000
# B = 7 -> B = 2 -> C = A /   4 = A / 00000100

# C = A >> B

# # 1
# # 6
# # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

# B = B XOR 110
# B = 0 -> B = 5 -> B = 3
# B = 1 -> B = 4 -> B = 2
# B = 2 -> B = 7 -> B = 1
# B = 3 -> B = 6 -> B = 0
# B = 4 -> B = 1 -> B = 7
# B = 5 -> B = 0 -> B = 6
# B = 6 -> B = 3 -> B = 5
# B = 7 -> B = 2 -> B = 4

# # 0
# # 3
# # The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

# A = A / pow(2, 3) = A / 8 (truncated to an int)
# This is the same as A >> 3 !! so we are just going through all 3 bit values of A

# # 4
# # 1
# # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

# B = B XOR C
# B = 0 -> B = 5 -> B = 3
# B = 1 -> B = 4 -> B = 2
# B = 2 -> B = 7 -> B = 1
# B = 3 -> B = 6 -> B = 0
# B = 4 -> B = 1 -> B = 7
# B = 5 -> B = 0 -> B = 6
# B = 6 -> B = 3 -> B = 5
# B = 7 -> B = 2 -> B = 4

# # 5
# # 5
# # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

# output.append(B % 8) (i.e. lowest 3 bits of B)

# # 3
# # 0
# # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
# if A != 0: we go back to start

# What we know:
# We only finish the program when A == 0 and on each iteration we divide by 8 (rounded down to an int)
# Our program length is 16, we only add one value to output on each loop 
# -> there are 16 loops (and reset 15 times)
# -> 35184372088832 <= A <= 246290604621824 (see below)

# Let's work backwards, because it seems A is just constantly shifted by 3 bits, used to calculate C and is the first input to B

# 2,4,1,5,7,5,1,6,0,3,4,1,5,5,3,0

# output = 2 (= 010 is lowest 3 digits of B)
# 010 = ((A % 8 XOR 101) XOR 110) XOR (A >> (A % 8 XOR 101))

# A = 0000000000 -> 101 XOR 110 = 011 XOR 000 = 011 = 3
# A = 0000000001 -> 100 XOR 110 = 010 XOR 000 = 010 = 2

# LHS = (A % 8 XOR 101) XOR 110 = (A % 8 XOR 011)
# RHS = A >> (A % 8 XOR 101)
# -> LHS = 000 -> RHS = 010
# -> LHS = 001 -> RHS = 011
# -> LHS = 010 -> RHS = 000
# -> LHS = 011 -> RHS = 001
# -> LHS = 100 -> RHS = 110
# -> LHS = 101 -> RHS = 111
# -> LHS = 110 -> RHS = 100
# -> LHS = 111 -> RHS = 101

# before we jump out A is between 1 and 7, so bounds are:
a_upper = 7
a_lower = 1
for i in range(15):
    a_upper *= 8
    a_lower *= 8

print(a_lower)
print(a_upper)

# My first thought was to check values 0 through 7 for the next num in program
# then bitshift 3 and go to the next number. But the operation `C = A >> B`
# can make a specific output number dependent on the bits to the left of it, 
# so we will recurse over all values in the 0 through 7 range that produces the
# right value before moving on.
def find_a_recursive(i, a, program):
    print("A is now " + str(a))
    val = program[len(program)-1-i]
    print("Trying to find " + str(val))
    found = False
    for next_num in range(8):
        print("Adding " + str(next_num))
        output = execute_program(program, [a + next_num, 0, 0])
        print(output)
        if output[0] == val:
            # we found the next number, move on
            found = True
            next_a = a + next_num
            if len(output) == len(program):
                return next_a
            
            next_a = next_a << 3
            result = find_a_recursive(i + 1, next_a, program)
            if result > 0:
                return result
            else:
                found = False
    if not found:
        return -1

a = find_a_recursive(0, 0, program)
print("Found A = " + str(a))
