import math

def is_correct_order(rules, pages):
    seen = set()
    for page in pages:
        should_precede_list = rules[page] if page in rules else None
        if should_precede_list != None:
            for should_precede in should_precede_list:
                if should_precede in seen:
                    return False
        seen.add(page)
    return True
            
def sum_for_correct_pages(rules, lines):
    # What do you get if you add up the middle page number from those correctly-ordered updates?
    sum = 0
    for pages in lines:
        if is_correct_order(rules, pages):
            # print(pages)
            # print(pages[math.floor(len(pages) / 2)])
            if len(pages) % 2 == 0:
                sum += pages[len(pages) / 2 - 1]
                sum += pages[len(pages) / 2]    
            else:
                sum += pages[math.floor(len(pages) / 2)]

    return sum

def sum_for_incorrect_pages(rules, lines):
    sum = 0
    for pages in lines:
        if not is_correct_order(rules, pages):
            # figure out sorting
            # print(pages)
            # print(rules)
            sorted_pages = sort_pages(rules, pages)
            # print(sorted_pages)

            if len(sorted_pages) % 2 == 0:
                sum += sorted_pages[(len(sorted_pages) / 2) - 1]
                sum += sorted_pages[len(sorted_pages) / 2]    
            else:
                sum += sorted_pages[math.floor(len(sorted_pages) / 2)]

    return sum

def sort_pages(rules, pages):
    dependency_counts = {}
    # get a count of how many dependencies each page has
    for page in pages:
        dependency_counts[page] = 0
    
    for (page, dependencies) in rules.items():
        if not page in dependency_counts:
            continue

        for d in dependencies:
            if not d in dependency_counts:
                continue
            dependency_counts[d] += 1

    # now we will go over each page with zero dependencies and add them to the output
    # lowering the dependency count for each page that has a dependency on it
    queue = [page for page in pages if dependency_counts[page] == 0]
    result = []
    while len(queue) > 0:
        page = queue.pop(0)
        result.append(page)
        page_rules = rules[page] if page in rules else None
        if page_rules == None:
            continue
        for p in page_rules:
            if not p in dependency_counts:
                continue
            dependency_counts[p] -= 1
            if dependency_counts[p] == 0:
                queue.append(p)

    return result
    
def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    (rules, lines) = text.split("\n\n")
    rule_dict = {}
    rules = [tuple(map(int, rule.split("|"))) for rule in rules.split("\n")]
    for (l, r) in rules:
        if l in rule_dict:
            rule_dict[l].append(r)
        else:
            rule_dict[l] = [r]
    lines = [list(map(int, line.split(","))) for line in lines.split("\n")]

    return (rule_dict, lines)

text = read_file('day5.txt')
(rules, lines) = parse_input(text)

sum = sum_for_correct_pages(rules, lines)
sum_incorrect = sum_for_incorrect_pages(rules, lines)

# print(rules)
# print(lines)
print(sum)
print(sum_incorrect)