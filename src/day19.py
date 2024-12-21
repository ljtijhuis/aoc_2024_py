def count_possible_patterns(towels, patterns):
    possible = 0
    for p in patterns:
        if is_possible(p, towels, ''):
            possible += 1
    return possible

def is_possible(pattern, towels, so_far):
    if so_far == pattern:
        return True
    
    for t in towels:
        r = so_far + t
        if pattern.startswith(r) and is_possible(pattern, towels, r):
            return True
        
    return False

def count_possible_combinations(trie, patterns):
    possible = 0
    for p in patterns:
        print("Checking pattern " + p)
        known_counts = {}
        possible += possible_combinations(p, trie, known_counts)
    return possible

def possible_combinations(pattern, trie, known_counts):
    # Let's memoize
    if pattern in known_counts:
        return known_counts[pattern]
    
    print("Pattern remaining " + pattern)
    if len(pattern) == 0:
        return 1
    
    combinations = 0

    current = trie
    for i, c in enumerate(pattern):
        # we go through our trie until we find an end
        if c in current.next:
            current = current.next[c]
            if current.is_end:
                count = possible_combinations(pattern[i+1:], trie, known_counts)
                known_counts[pattern[i+1:]] = count
                combinations += count
        else:
            break
        
    return combinations
    
    # for t in towels:
    #     print("Checking <" + t + "> in " + pattern)
    #     if pattern.startswith(t):
    #         combinations += possible_combinations(pattern[len(t):], towels)
        
    # return combinations

class TrieNode:
    def __init__(self):
        self.next = {}
        self.is_end = False

def build_trie(towels):
    root = TrieNode()
    for t in towels:
        current = root
        for c in t:
            if c not in current.next:
                next = TrieNode()
                current.next[c] = next
            next = current.next[c]
            current = next
        current.is_end = True
    return root


def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    split = text.split("\n\n")
    towels = split[0].split(", ")
    patterns = split[1].splitlines()
    return towels, patterns

text = read_file('day19.txt')
towels, patterns = parse_input(text)
count = count_possible_patterns(towels, patterns)
print(count)

trie = build_trie(towels)
count = count_possible_combinations(trie, patterns)
print(count)