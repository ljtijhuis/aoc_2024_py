
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

def read_file(f):
    with open(f) as opened_file:
        return opened_file.read()

def parse_input(text):
    secrets = [int(line) for line in text.splitlines()]
    return secrets

text = read_file('day22.txt')
secrets = parse_input(text)

# secret = 123
# for i in range(10):
#     secret = next_secret(secret)
#     print(secret)

sum = 0
for secret in secrets:
    for i in range(2000):
        secret = next_secret(secret)
    
    sum += secret
    print(secret)
print(sum)