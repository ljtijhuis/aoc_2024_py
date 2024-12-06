
def is_safe(report):
    if len(report) == 1:
        return True

    # The levels are either all increasing or all decreasing.
    # Any two adjacent levels differ by at least one and at most three.
    if report[0] < report[1]:
        # increasing
        for previous, current in zip(report, report[1:]):
            if not previous < current:
                return False
            if abs(previous - current) > 3:
                return False
        return True

    elif report[0] > report[1]:
        # decreasing
        for previous, current in zip(report, report[1:]):
            if not previous > current:
                return False
            if abs(previous - current) > 3:
                return False
        return True
    else:
        return False

def count_safe(reports):
    count = 0
    for report in reports:
        if is_safe(report):
            count += 1
    return count

def count_safe_error_tolerant(reports):
    count = 0
    for report in reports:
        if is_safe(report):
            count += 1
        else:
            # try with removing a single element
            for i in range(len(report)):
                alt_report = [x for j, x in enumerate(report) if j != i]
                if is_safe(alt_report):
                    count += 1
                    break

    return count

def read_file(f):
    with open(f) as opened_file:
        return opened_file.readlines()

def parse_input(lines):
    reports = [list(map(int, line.split())) for line in lines]
    return reports


lines = read_file('day2.txt')
parsed = parse_input(lines)

safe_reports = count_safe(parsed)
print(safe_reports)
safe_reports = count_safe_error_tolerant(parsed)
print(safe_reports)