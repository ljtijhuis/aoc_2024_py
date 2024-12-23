
import math

def mix(secret, val):
    # To mix a value into the secret number, calculate the bitwise XOR 
    # of the given value and the secret number. Then, the secret number 
    # becomes the result of that operation. (If the secret number is 42 
    # and you were to mix 15 into the secret number, the secret number 
    # would become 37.)
    return val ^ secret

def prune(secret):
    # To prune the secret number, calculate the value of the secret 
    # number modulo 16777216. Then, the secret number becomes the 
    # result of that operation. (If the secret number is 100000000 and 
    # you were to prune the secret number, the secret number would 
    # become 16113920.)
    return secret % 16777216

def next_secret(secret):
    # Calculate the result of multiplying the secret number by 64. Then, 
    # mix this result into the secret number. Finally, prune the secret 
    # number.
    result = prune(mix(secret, secret * 64))
    # Calculate the result of dividing the secret number by 32. Round 
    # the result down to the nearest integer. Then, mix this result into 
    # the secret number. Finally, prune the secret number.
    result = prune(mix(result, math.floor(result / 32)))
    # Calculate the result of multiplying the secret number by 2048. Then, 
    # mix this result into the secret number. Finally, prune the secret 
    # number.
    return prune(mix(result, result * 2048))

def find_best_sequence(secrets):
    
    sequence_counts = {}

    for secret in secrets:
        secret_counts = {}
        generated_secrets = generate_secrets(secret)
        numbers = to_numbers(generated_secrets)

        for one, two, three, four, five in zip(numbers, numbers[1:], numbers[2:], numbers[3:], numbers[4:]):

            deltas = (two-one, three-two, four-three, five-four)
            if deltas not in secret_counts:
                secret_counts[deltas] = five
        
        for deltas, value in secret_counts.items():
            sequence_counts[deltas] = sequence_counts.get(deltas, 0) + value

    return max(sequence_counts.values())

def generate_secrets(secret):
    result = [secret]
    for i in range(2000):
        secret = next_secret(secret)
        result.append(secret)
    return result

def to_numbers(generated_secrets):
    return [s % 10 for s in generated_secrets]

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    secrets = [int(line) for line in text.splitlines()]
    return secrets

text = read_file('day22.txt')
secrets = parse_input(text)
# secrets = [
#     1,
#     2,
#     3,
#     2024
# ]

# secret = 123
# for i in range(10):
#     secret = next_secret(secret)
#     print(secret)

sum = 0
for secret in secrets:
    for i in range(2000):
        secret = next_secret(secret)
    
    sum += secret
print(sum)

bananas = find_best_sequence(secrets)
print(bananas)