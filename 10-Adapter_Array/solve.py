#!/usr/bin/python3

import sys

joltages = [0]
for line in sys.stdin:
    joltages.append(int(line))

joltages = sorted(joltages)
deviceJoltage = joltages[-1] + 3
joltages.append(deviceJoltage)

print(f"Device joltage is: {joltages[-1]}")

differences = [None, 0, 0, 0]
for i in range(1, len(joltages)):
    d = joltages[i] - joltages[i-1]
    differences[d] += 1

for i in range(1, 4):
    print(f"Diff {i}: {differences[i]} times")

print("Part 1 solve:", differences[1] * differences[3])

####

ways = [0] * (deviceJoltage+1)
ways[0] = 1
for joltage in joltages:
    for j in range(joltage-3, joltage):
        if j >= 0:
            ways[joltage] += ways[j]

print(ways)
print("Ways to device joltage:", ways[deviceJoltage])
