#!/usr/bin/python3

import sys
import re

validOld = 0
validNew = 0
for line in sys.stdin:
    (a, b, letter, passwd) = re.match(r'(\d+)-(\d+) ([a-z]): (.*)', line).groups()
    (a, b) = map(int, (a, b))
    # Old password policy, just count
    count = passwd.count(letter)
    if count >= a and count <= b:
        validOld += 1
    # New password policy, check positions
    count = 0
    if passwd[a-1] == letter:
        count += 1
    if passwd[b-1] == letter:
        count += 1
    if count == 1:
        validNew += 1

print(f"Valid old: {validOld}\tValid new: {validNew}")
