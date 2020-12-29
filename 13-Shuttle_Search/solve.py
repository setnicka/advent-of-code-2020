#!/usr/bin/python3

import math

start = int(input())
buses = input().split(',')

busIntervals = []
offset = -1
for bus in buses:
    offset += 1
    if bus == 'x':
        continue
    busIntervals.append((int(bus), offset))

firstTime = math.inf
firstBus = None
for (bus, _) in busIntervals:
    t = (start // bus + 1) * bus
    if t < firstTime:
        firstTime = t
        firstBus = bus

print(f"First bus is {firstBus} at time {firstTime}")
print(f"Part 1 solution: {firstBus * (firstTime - start)}")

###########

lcm = busIntervals[0][0]
timestamp = 0
for (bus, offset) in busIntervals:
    while (timestamp + offset) % bus != 0:
        timestamp += lcm
    # Found matching bus, add bus to lcm
    print(f"Found matching ({bus}, {offset}) at timestamp {timestamp}")
    lcm = math.lcm(lcm, bus)

print("Final timestamp:", timestamp)
