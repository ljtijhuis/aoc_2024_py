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

# # 1
# # 5
# # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

# B = B ^ 101

# # 7
# # 5
# # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

# C = A / 2 ^ B (truncated to an int)

# # 1
# # 6
# # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

# B = B ^ 110

# # 0
# # 3
# # The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

# A = A / pow(2, 3) = A / 8 (truncated to an int)

# # 4
# # 1
# # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

# B = B ^ C

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

# before we jump out A is between 1 and 7, so bounds are:
a_upper = 7
a_lower = 1
for i in range(15):
    a_upper *= 8
    a_lower *= 8

print(a_lower)
print(a_upper)