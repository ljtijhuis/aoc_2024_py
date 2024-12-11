def decode(dm):
    # (ID, start_pos, repeats)
    result = []
    pos = 0
    id = 0
    for i, c in enumerate(dm):
        block_size = int(c)
        id_or_empty = id if i % 2 == 0 else -1
        result.append((id_or_empty, pos, block_size))
        if i % 2 == 0:
            id += 1
        pos += block_size
    return result

def fill_gaps(decoded):
    # keep two pointers
    # left is going through the empty spots to fill
    # right is going from right to left finding non-empty to move
    left = 0
    right = len(decoded) - 1
    no_gaps = []
    open_spots = sum([entry[2] for entry in decoded if entry[0] == -1])
    while left < right:
        lentry = list(decoded[left])
        rentry = list(decoded[right])

        # scan from left looking for empty spots
        if lentry[0] != -1:
            no_gaps.append(tuple(lentry))
            left += 1
        # scan from right looking for IDs to move
        elif rentry[0] == -1:
            right -= 1
        else:
            # we have our entries to move
            spots_open = lentry[2]
            spots_needed = rentry[2]
            if spots_open > spots_needed:
                # insert an entry in left-1
                no_gaps.append((rentry[0], lentry[1], spots_needed))
                # update left by moving the starting pos and lowering repeats
                lentry[1] += spots_needed
                lentry[2] -= spots_needed
                decoded[left] = tuple(lentry)
                # we can move to the next on right
                rentry[0] = -1
                right -= 1
            elif spots_open == spots_needed:
                # just replace the ID
                lentry[0] = rentry[0]
                no_gaps.append(tuple(lentry))
                rentry[0] = -1
                left += 1
                right -= 1
            else:
                # replace the ID, lower repeats on right
                lentry[0] = rentry[0]
                no_gaps.append(tuple(lentry))
                rentry[2] -= spots_open
                decoded[right] = tuple(rentry)
                left += 1
    
    # check if anything was left
    rentry = list(decoded[right])
    if rentry[0] != -1 and rentry[2] > 0:
        no_gaps.append(tuple(rentry))
    
    next_index = no_gaps[-1][1] + no_gaps[-1][2]
    no_gaps.append((-1, next_index, open_spots))
    return no_gaps

def compact_with_gaps(decoded):
    # we go from highest index on the right to the lowest on the left
    (current_id, highest_id_index) = get_highest_id(decoded)
    while current_id >= 0:
        left = 0
        space_needed = decoded[highest_id_index][2]
        # find a spot to put it at
        while left < highest_id_index:
            if decoded[left][0] == -1 and decoded[left][2] == space_needed:
                # we found an exact length spot to move it to, replace it
                decoded[left] = (current_id, decoded[left][1], space_needed)
                decoded[highest_id_index] = (-1, decoded[highest_id_index][1], space_needed)
                break
            elif decoded[left][0] == -1 and decoded[left][2] > space_needed:
                # there is more room than needed, insert it and lower space left
                decoded.insert(left, (current_id, decoded[left][1], space_needed))
                decoded[left+1] = (-1, decoded[left+1][1]+space_needed, decoded[left+1][2]-space_needed)
                decoded[highest_id_index+1] = (-1, decoded[highest_id_index+1][1], space_needed)
                highest_id_index += 1
                break
            else:
                left += 1
        
        # go to the next one to move
        current_id -= 1
        while highest_id_index > 0:
            if decoded[highest_id_index][0] == current_id:
                break
            else:
                highest_id_index -= 1

        # merge any gap entries that are next to each other
        i = 0
        while i < len(decoded)-1:
            if decoded[i][0] == -1 and decoded[i+1][0] == -1:
                # merge
                decoded[i] = (decoded[i][0], decoded[i][1], decoded[i][2] + decoded[i+1][2])
                del decoded[i+1]
            else:
                i += 1

    
    return decoded

def get_highest_id(decoded):
    right = len(decoded) - 1
    while right > 0:
        if decoded[right][0] != -1:
            return (decoded[right][0], right)

def checksum(decoded):
    # add up the result of multiplying each of these blocks' position 
    # with the file ID number it contains. The leftmost block is in 
    # position 0. If a block contains free space, skip it instead.
    sum = 0
    i = 0
    for entry in decoded:
        id, start_pos, repeats = entry

        if id == -1:
            i += repeats
            continue

        for j in range(repeats):
            sum += (i+j) * id

        i += repeats

    return sum
        

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

# def parse_input(lines):
#     return [list(line) for line in lines]

disk_map = read_file('day9.txt')
# grid = parse_input(lines)

# disk_map = '12345'
# disk_map = '2333133121414131402'

decoded = decode(disk_map)
no_gaps = fill_gaps(decoded)
cs = checksum(no_gaps)

decoded = decode(disk_map)
compacted = compact_with_gaps(decoded)
cs_compacted = checksum(compacted)

# print(decoded)
# print(no_gaps)
print(cs)
print(cs_compacted)