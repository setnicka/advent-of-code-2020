#!/usr/bin/python3

# starting_numbers = [0, 3, 6]
starting_numbers = [6, 3, 15, 13, 1, 0]
numbers = {}
spoken = 0

turn = 1
for n in starting_numbers:
    if n not in numbers:
        numbers[n] = []
    numbers[n].append(turn)
    spoken = n
    turn += 1

while turn <= 30000000:
    if len(numbers[spoken]) == 1:
        spoken = 0
    else:
        spoken = numbers[spoken][-1] - numbers[spoken][-2]
    if spoken not in numbers:
        numbers[spoken] = []
    numbers[spoken].append(turn)
    if turn % 10000 == 0:
        print(f"Spoken at turn {turn}: {spoken}")
    turn += 1
