#!/usr/bin/python3

import sys

cubes = [[]]
# Input is "flat" (2D)
for line in sys.stdin:
    cubes[0].append(list(line.strip()))

z_size = len(cubes)
y_size = len(cubes[0])
x_size = len(cubes[0][0])


def count_neighbors(x, y, z):
    count = 0
    current = '.'
    for zz in (z-1, z, z+1):
        for yy in (y-1, y, y+1):
            for xx in (x-1, x, x+1):
                if zz < 0 or yy < 0 or xx < 0 or zz >= z_size or yy >= y_size or xx >= x_size:
                    continue
                if xx == x and yy == y and zz == z:
                    current = cubes[zz][yy][xx]
                    continue
                if cubes[zz][yy][xx] == '#':
                    count += 1
    return (count, current)


# Each round it expands of
turn = 0
while turn < 6:
    turn += 1
    new_cubes = []
    total = 0
    for z in range(z_size + 2):
        flat = []
        for y in range(y_size + 2):
            row = []
            for x in range(x_size + 2):
                (count, current) = count_neighbors(x-1, y-1, z-1)
                if current == '#' and count in (2, 3):
                    total += 1
                    row.append('#')
                elif current == '.' and count == 3:
                    total += 1
                    row.append('#')
                else:
                    row.append('.')
            flat.append(row)
        new_cubes.append(flat)

    cubes = new_cubes
    z_size += 2
    y_size += 2
    x_size += 2

    print(f"After turn {turn} total count is {total}")
