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

text = read_file('day24.txt')
values, gates = parse_input(text)

z = resolve_z(values, gates)
print(z)
