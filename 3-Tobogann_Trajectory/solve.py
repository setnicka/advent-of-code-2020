#!/usr/bin/python3

import sys


def countTrees(mapa, dx, dy):
    x, y = (0, 0)
    trees = 0
    while y < height:
        if mapa[y][x % width] == '#':
            trees += 1
        x += dx
        y += dy
    return trees


# Read input
mapa = sys.stdin.readlines()
mapa = [line.strip() for line in mapa]
height = len(mapa)
width = len(mapa[0])

trajectories = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
mult = 1
for (dx, dy) in trajectories:
    count = countTrees(mapa, dx, dy)
    print(f"Trajectory {dx} right {dy} down: {count}")
    mult *= count

print(mult)
