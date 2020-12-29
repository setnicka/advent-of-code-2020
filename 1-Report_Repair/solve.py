#!/usr/bin/python3

import sys

data = map(int, sys.stdin.readlines())

data = sorted(data)
N = len(data)

a = 0
b = N - 1

while True:
    sum = data[a] + data[b]
    if sum < 2020:
        a += 1
    elif sum > 2020:
        b -= 1
    else:
        print(f"{data[a]}, {data[b]}: {data[a] * data[b]}")
        break

for a in range(N):
    for b in range(a, N):
        for c in range(b, N):
            sum = data[a] + data[b] + data[c]
            if sum == 2020:
                print(f"{data[a]}, {data[b]}, {data[c]}: {data[a] * data[b] * data[c]}")
