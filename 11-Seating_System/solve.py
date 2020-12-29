#!/usr/bin/python3

import sys

input_seats = []
for line in sys.stdin:
    input_seats.append(list(line))
ysize = len(input_seats)
xsize = len(input_seats[0])


def get_neighbors(seats, x, y):
    neighbors = []
    for xx in (x-1, x, x+1):
        if xx < 0 or xx >= xsize:
            continue
        for yy in (y-1, y, y+1):
            if yy < 0 or yy >= ysize or (xx == x and yy == y):
                continue
            elif seats[yy][xx] == 'L':
                neighbors.append((xx, yy))
    return neighbors


def get_visible_neighbors(seats, x, y):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbors = []
    for (dx, dy) in directions:
        xx = x + dx
        yy = y + dy
        while True:
            if yy < 0 or yy >= ysize or xx < 0 or xx >= xsize:
                break
            elif seats[yy][xx] == 'L':
                neighbors.append((xx, yy))
                break
            elif seats[yy][xx] != '.':
                break
            xx += dx
            yy += dy
    return neighbors


# Calculate neighbors for the first and the second part
neighbors = []
neighbors_visible = []
for y in range(ysize):
    row = []
    row_visible = []
    for x in range(xsize):
        row.append(get_neighbors(input_seats, x, y))
        row_visible.append(get_visible_neighbors(input_seats, x, y))
    neighbors.append(row)
    neighbors_visible.append(row_visible)


def countOccupiedNeighbors(neighbors, seats, x, y):
    occupied = 0
    for (xx, yy) in neighbors[y][x]:
        if seats[yy][xx] == '#':
            occupied += 1
    return occupied


for (part, neighbors, free_limit, full_limit) in ((1, neighbors, 0, 4), (2, neighbors_visible, 0, 5)):
    seats = input_seats
    round = 0
    while True:
        changed = 0
        new_seats = []
        for y in range(ysize):
            new_row = []
            for x in range(xsize):
                occupied = countOccupiedNeighbors(neighbors, seats, x, y)
                if seats[y][x] == 'L' and occupied <= free_limit:
                    new_row.append('#')
                    changed += 1
                elif seats[y][x] == '#' and occupied >= full_limit:
                    new_row.append('L')
                    changed += 1
                else:
                    new_row.append(seats[y][x])
            new_seats.append(new_row)
        if changed == 0:
            break
        round += 1
        print(f"Round {round} end: {changed} changed")
        seats = new_seats

    occupied = 0
    for y in range(ysize):
        for x in range(xsize):
            if seats[y][x] == '#':
                occupied += 1

    print(f"Part {part} - occupied seats after stabilization: {occupied}")
