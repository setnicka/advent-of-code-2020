#!/usr/bin/python3

import sys

maximal = 0
used = {}
for line in sys.stdin:
    row = 0
    step = 64
    for c in line[:7]:
        if c == 'B':
            row += step
        step //= 2

    column = 0
    step = 4
    for c in line[7:]:
        if c == 'R':
            column += step
        step //= 2

    ID = row*8 + column
    maximal = max(maximal, ID)
    used[ID] = True

print(maximal)

for i in used:
    if i+2 in used and i+1 not in used:
        print(i+1)
