import re

def mul_sum(lines):
# mul(X,Y), where X and Y are each 1-3 digit numbers
    regex = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    sum = 0
    for line in lines:
        matches = regex.findall(line)
        for match in matches:
            d1 = int(match[0])
            d2 = int(match[1])
            sum += d1 * d2
    return sum

def read_file(f):
    with open(f) as opened_file:
        return [opened_file.read()]

def parse_input(lines):
    filtered = []
    for line in lines:
        enabled = line.split('do()')
        for l in enabled:
            filtered.append(l.split('don\'t()')[0])
    return filtered

lines = read_file('day3.txt')
filtered = parse_input(lines)
sum = mul_sum(lines)
sum_filtered = mul_sum(filtered)



print(sum)
print(sum_filtered)