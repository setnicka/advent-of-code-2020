#!/usr/bin/python3

# Use 3D cube coordinates for hex grid (for every cell x+y+z = 0 at every time)
# https://www.redblobgames.com/grids/hexagons/

import sys

blackCount = 0
blackTiles = dict()


def movePos(pos, move):
    (r, c) = pos
    (rd, cd) = {
        'e': (0, 1),
        'se': (-1, 0),
        'sw': (-1, -1),
        'w': (0, -1),
        'nw': (1, 0),
        'ne': (1, 1)
    }[move]
    return (r + rd, c + cd)


for line in sys.stdin:
    line = line.strip()
    i = 0
    pos = (0, 0)
    while i < len(line):
        if line[i] == 'e' or line[i] == 'w':
            pos = movePos(pos, line[i])
            i += 1
        else:
            pos = movePos(pos, line[i:i+2])
            i += 2
    if pos in blackTiles:
        blackCount -= 1
        blackTiles.pop(pos)
    else:
        blackTiles[pos] = True
        blackCount += 1

print(blackCount)

for i in range(100):
    whiteCandidates = dict()
    newBlackTiles = dict()
    for blackTile in blackTiles:
        blackCount = 0
        for move in ('e', 'se', 'sw', 'w', 'nw', 'ne'):
            pos = movePos(blackTile, move)
            if pos in blackTiles:
                blackCount += 1
            else:  # is white
                if pos not in whiteCandidates:
                    whiteCandidates[pos] = 0
                whiteCandidates[pos] += 1
        (r, c) = blackTile
        if blackCount > 0 and blackCount <= 2:
            newBlackTiles[blackTile] = True

    for whiteTile in whiteCandidates:
        if whiteCandidates[whiteTile] == 2:
            newBlackTiles[whiteTile] = True

    blackTiles = newBlackTiles
    print(f"After day {i+1}: {len(blackTiles)} black tiles")
