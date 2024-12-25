def resolve_z(values, gates):
    # check how many z variables exist
    num_zs = 0
    while "z{:02d}".format(num_zs) in values:
        num_zs += 1
    
    resolve_stack = ["z{:02d}".format(z) for z in range(num_zs)]

    while len(resolve_stack) > 0:
        variable = resolve_stack.pop()
        if values[variable] is None:
            dep1 = gates[variable][1]
            dep2 = gates[variable][2]
            if values[dep1] is not None and values[dep2] is not None:
                # we can evaluate a new value!
                match gates[variable][0]:
                    case 'AND':
                        values[variable] = values[dep1] & values[dep2]
                    case 'OR':
                        values[variable] = values[dep1] | values[dep2]
                    case 'XOR':
                        values[variable] = values[dep1] ^ values[dep2]
                    case _:
                        raise Exception("Unknown logic condition")
            else:
                # Add self and any dependencies to the resolve stack
                resolve_stack.append(variable)
                if values[dep1] is None:
                    resolve_stack.append(dep1)
                if values[dep2] is None:
                    resolve_stack.append(dep2)

    result = 0
    for i in range(num_zs):
        result += values["z{:02d}".format(i)] * pow(2, i)
    return result


def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    split = text.split("\n\n")
    values = {}
    gates = {}
    for line in split[1].splitlines():
        gate_split = line.split(" -> ")
        # AND, OR, XOR
        logic_split = gate_split[0].split(" ")
        gates[gate_split[1]] = (logic_split[1], logic_split[0], logic_split[2]) # Operation, dependency 1, dependency 2
        
        # add all variables to our values map
        values[gate_split[1]] = None
        values[logic_split[0]] = None
        values[logic_split[2]] = None

    for line in split[0].splitlines():
        value_split = line.split(": ")
        values[value_split[0]] = int(value_split[1])

    return values, gates

text = read_file('day24_fixed.txt')
values, gates = parse_input(text)

# Part 1
z = resolve_z(values.copy(), gates)
print(z)

# Part 2
# We have 45 bits of X and Y as inputs, meaning we have 46 bits of output Z

# To start, let's evaluate all powers of 2
def reset_inputs(values):
    for i in range(45):
        values["x{:02d}".format(i)] = 0
        values["y{:02d}".format(i)] = 0

def to_binary(n):
    result = ""
    for i in reversed(range(46)):
        if pow(2, i) <= n:
            result += "1"
            n -= pow(2, i)
        else:
            result += "0"
    return result

reset_inputs(values)
for i in range(45):
    values["x{:02d}".format(i)] = 1
    z = resolve_z(values.copy(), gates)
    expected_value = pow(2, i)
    if z != expected_value:
        print("x{:02d} = 1 (rest 0), Y = 0, Z = {:d}, Expected value: {:d}".format(i, z, expected_value))
        print(to_binary(expected_value))
        print(to_binary(z))
    values["x{:02d}".format(i)] = 0

for i in range(45):
    values["y{:02d}".format(i)] = 1
    z = resolve_z(values.copy(), gates)
    expected_value = pow(2, i)
    if z != expected_value:
        print("y{:02d} = 1 (rest 0), X = 0, Z = {:d}, Expected value: {:d}".format(i, z, expected_value))
        print(to_binary(expected_value))
        print(to_binary(z))
    values["y{:02d}".format(i)] = 0

for i in range(45):
    values["x{:02d}".format(i)] = 1
    values["y{:02d}".format(i)] = 1
    z = resolve_z(values.copy(), gates)
    expected_value = 2 * pow(2, i)
    if z != expected_value:
        print("y{:02d} = 1 (rest 0), x{:02d} = 1 (rest 0), Z = {:d}, Expected value: {:d}".format(i, i, z, expected_value))
        print(to_binary(expected_value))
        print(to_binary(z))
    values["x{:02d}".format(i)] = 0
    values["y{:02d}".format(i)] = 0

# Binary adders consist of two half-adders which both contain a XOR and an AND port
# - The result of the XOR is typically the result for the specific bit, flipped by the 
#   second XOR with the carry
# - The two ANDs determine if there needs to be a carry.
# - Carries carry through all the bits this way so the further we come, the more dependencies a bit will have
# - Looking at the input with this pattern in mind, we can immediately tell these are wrong:
# x06 AND y06 -> z06
# sqv AND frp -> z11
# bmp OR vjc -> z16
# Results of a XOR will either be assigned to a z bit or a temp var. These are wrong:
# scp XOR gbp -> vwr
# frp XOR sqv -> tqm
# vgv XOR hpt -> kfs

# others found through script below:
# hcm <> gfv

# answer: gfv,hcm,kfs,tqm,vwr,z06,z11,z16

# Let's just trace all the right gates
def gen_adders(gates):
    map = {}
    for key, value in gates.items():
        map[value] = key

    in_counter = 1
    carry = "kqn"
    for in_counter in range(1, 46):
        x = "x{:02d}".format(in_counter)
        y = "y{:02d}".format(in_counter)
        print("Checking for {} and {}".format(x, y))

        # Find the initial XOR variable name
        tmp_xor_var = ""
        if ("XOR", x, y) in map:
            tmp_xor_var = map[("XOR", x, y)]
        elif ("XOR", y, x) in map:
            tmp_xor_var = map[("XOR", y, x)]
        else:
            raise Exception("Cannot find tmp_xor_var for x/y{:02d}".format(in_counter))
        
        # Now find the XOR of tmp_xor_var with the carry -> that is the output zxx
        expected_output_var = "z{:02d}".format(in_counter)
        if ("XOR", tmp_xor_var, carry) in map:
            if not map[("XOR", tmp_xor_var, carry)] == expected_output_var:
                raise Exception("Found wrong output var for {} XOR {}".format(tmp_xor_var, carry))
        elif ("XOR", carry, tmp_xor_var) in map:
            if not map[("XOR", carry, tmp_xor_var)] == expected_output_var:
                raise Exception("Found wrong output var for {} XOR {}".format(carry, tmp_xor_var))
        else:
            raise Exception("Cannot find output value for z{:02d}, values used {} {}".format(in_counter, tmp_xor_var, carry))

        # Find the AND of tmp_xor_var and the carry -> store this in another tmp
        tmp_and_var_carry = ""
        if ("AND", tmp_xor_var, carry) in map:
            tmp_and_var_carry = map[("AND", tmp_xor_var, carry)]
        elif ("AND", carry, tmp_xor_var) in map:
            tmp_and_var_carry = map[("AND", carry, tmp_xor_var)]
        else:
            raise Exception("Cannot find tmp_and_var_carry for x/y{:02d}".format(in_counter))
        
        # Find the input values AND tmp var
        tmp_and_var = ""
        if ("AND", x, y) in map:
            tmp_and_var = map[("AND", x, y)]
        elif ("AND", y, x) in map:
            tmp_and_var = map[("AND", y, x)]
        else:
            raise Exception("Cannot find tmp_and_var for x/y{:02d}".format(in_counter))

        # Now find the OR of this result and tmp_and_var_carry -> this is our new carry
        if ("OR", tmp_and_var, tmp_and_var_carry) in map:
            carry = map[("OR", tmp_and_var, tmp_and_var_carry)]
            print("New carry found: " + carry)
        elif ("OR", tmp_and_var_carry, tmp_and_var) in map:
            carry = map[("OR", tmp_and_var_carry, tmp_and_var)]
            print("New carry found: " + carry)
        else:
            raise Exception("Could not find carry for x/y{:02d} with vars {} OR {}".format(in_counter, tmp_and_var, tmp_and_var_carry))

gen_adders(gates)