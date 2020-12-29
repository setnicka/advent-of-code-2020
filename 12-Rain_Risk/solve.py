#!/usr/bin/python3

import sys

(waypointX, waypointY) = (10, 1)  # relative to ship
(shipX, shipY) = (0, 0)

dirToAction = {
    90: 'E',
    180: 'S',
    270: 'W',
    0: 'N',
}


def rotateDir(dir, x, y):
    if dir == 90:
        return (y, -x)
    elif dir == 180:
        return (-x, -y)
    elif dir == 270:
        return (-y, x)
    else:
        return (x, y)


for line in sys.stdin:
    action = line[0]
    param = int(line[1:])
    if action == 'F':
        shipX += waypointX*param
        shipY += waypointY*param

    elif action == 'N':
        waypointY += param
    elif action == 'S':
        waypointY -= param
    elif action == 'E':
        waypointX += param
    elif action == 'W':
        waypointX -= param

    elif action == 'L':
        rotation = (-param) % 360
        (waypointX, waypointY) = rotateDir(rotation, waypointX, waypointY)
    elif action == 'R':
        rotation = param % 360
        (waypointX, waypointY) = rotateDir(rotation, waypointX, waypointY)

print(f"Final position: [{shipX},{shipY}]")
distance = abs(shipX) + abs(shipY)
print(f"Distance: {distance}")
