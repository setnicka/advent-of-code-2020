#!/usr/bin/python3

import sys

# Load preamble
numbers = []
for i in range(25):
    numbers.append(int(input()))


def valid(number, numbers):
    for a in numbers:
        for b in numbers:
            if a+b == number:
                return True
    return False


invalidNumber = None
for line in sys.stdin:
    number = int(line)
    if not valid(number, numbers[-25:]) and invalidNumber is None:
        print("Not valid number:", number)
        invalidNumber = number
        break
    numbers.append(number)

# Part 2 - find contiguous set of at least two numbers that sums to the
# invalid number

sum = numbers[0]
a = 0
b = 0
while True:
    if b-a < 1:
        # At least two numbers
        b += 1
        sum += numbers[b]
    elif sum < invalidNumber:
        # Need to add number
        b += 1
        sum += numbers[b]
    elif sum > invalidNumber:
        # Need to remove number
        sum -= numbers[a]
        a += 1
    else:
        # Found
        break

sumNumbers = numbers[a:b+1]
minN = min(sumNumbers)
maxN = max(sumNumbers)
print(f"Found set of numbers {a}-{b} whose sum is {sum}:", sumNumbers)
print(f"Min is {minN}, max is {maxN} and min+max is {minN + maxN}")
