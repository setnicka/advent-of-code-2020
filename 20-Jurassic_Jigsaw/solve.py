#!/usr/bin/python3

import sys
import math

# WIDTH = 12
# HEIGHT = 12
TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


class Tile:
    id: int
    lines: list[str]
    borders: list[str]
    borderTiles: list[list]
    orientation: 0  # + (normal) and - (flipped)
    used: bool

    neighborDirections: int

    def __init__(self, id):
        self.id = id
        self.used = False

        self.lines = []
        right = []
        left = []
        for line in sys.stdin:
            line = line.strip()
            if line == "":
                break
            self.lines.append(line)
            right.append(line[-1])
            left.append(line[0])

        # Add borders
        self.borders = [
            self.lines[0],  # TOP
            "".join(right),  # RIGHT
            self.lines[-1],  # BOTTOM
            "".join(left),  # LEFT
        ]

    def __repr__(self) -> str:
        return f"Tile {self.id}"

    def getBorder(self, i, orientation):
        if orientation >= 0:
            border = self.borders[(i + orientation) % 4]
        else:
            border = self.borders[(orientation - i + 1) % 4]
            if i == TOP or i == BOTTOM:
                border = border[::-1]

        if (orientation == 1 or orientation == -4) and (i == LEFT or i == RIGHT):
            # Reverse border 1 and 3
            return border[::-1]
        elif orientation == 2 or orientation == -3:
            # Reverse everything
            return border[::-1]
        elif (orientation == 3 or orientation == -2) and (i == TOP or i == BOTTOM):
            # Revese 0 and 2
            return border[::-1]
        return border

    def getOrientedBorder(self, i):
        return self.getBorder(i, self.orientation)

    def getBorderTiles(self, i, orientation):
        if orientation >= 0:
            return self.borderTiles[(i + orientation) % 4]
        else:
            return self.borderTiles[(orientation - i + 1) % 4]

    def getOrientedBorderTiles(self, i):
        return self.getBorderTiles(i, self.orientation)

    def getMatchingOrientation(self, i, border):
        for orientation in range(-4, 4):
            if self.getBorder(i, orientation) == border:
                return orientation
        return None

    def findNeighbors(self, tiles):
        # print(f"==== Checking tile {self.id} ====")
        self.borderTiles = []
        self.neighborDirections = 0
        # Only normal (not flipped) orientations scanned (because opposite
        # tile is tested in both normal and flipped orientations)
        for orientation in range(4):
            neighbors = []
            border = self.getBorder(0, orientation)
            # print(orientation, border)
            for tile in tiles:
                if tile.id == self.id:
                    continue
                if tile.getMatchingOrientation(0, border) is not None:
                    neighbors.append(tile)
            self.borderTiles.append(neighbors)
            if len(neighbors) > 0:
                self.neighborDirections += 1
        # print(self.id, self.borderTiles)
        # for orientation in range(-4, 4):
        #     print(orientation, self.getBorder(LEFT, orientation))

    def getLines(self):
        lines = self.lines
        rotatedLines = []
        for c in range(len(self.lines[0])):
            row = []
            for r in range(len(self.lines)):
                row.append(self.lines[r][c])
            rotatedLines.append(row)

        if self.orientation == 0:
            return [line[1:-1] for line in lines[1:-1]]
        elif self.orientation == 1:
            return [line[1:-1] for line in rotatedLines[-2:0:-1]]
        elif self.orientation == 2:
            return [line[-2:0:-1] for line in lines[-2:0:-1]]
        elif self.orientation == 3:
            return [line[-2:0:-1] for line in rotatedLines[1:-1]]
        elif self.orientation == -1:
            return [line[-2:0:-1] for line in lines[1:-1]]
        elif self.orientation == -2:
            return [line[1:-1] for line in rotatedLines[1:-1]]
        elif self.orientation == -3:
            return [line[1:-1] for line in lines[-2:0:-1]]
        elif self.orientation == -4:
            return [line[-2:0:-1] for line in rotatedLines[-2:0:-1]]


tiles = []

for line in sys.stdin:
    line = line.strip()
    if line.startswith("Tile"):
        parts = line.split()
        id = int(parts[1][:-1])
        tiles.append(Tile(id))

WIDTH = int(math.sqrt(len(tiles)))
HEIGHT = WIDTH
print(WIDTH)

# for orientation in range(-4, 4):
#     print("Orientation:", orientation)
#     tiles[0].orientation = orientation
#     lines = tiles[0].getLines()
#     for line in lines:
#         print("".join(line))

# Find all matching tiles for every tile
corners = []
mult = 1
for tile in tiles:
    tile.findNeighbors(tiles)
    if tile.neighborDirections <= 2:
        corners.append(tile)
        mult *= tile.id

print("Corners:", corners)
print("Mult of corners:", mult)

corner = corners[0]  # TODO: choose corner to find sea monsters in right direction

# Determine corner orientation to be the top-left corner
for orientation in range(4):
    if len(corner.getBorderTiles(TOP, orientation)) == 0 and len(corner.getBorderTiles(LEFT, orientation)) == 0:
        corner.orientation = orientation
        break

# SPECIAL: Every tile has at most one possible neighbor in each direction
image = []
for r in range(HEIGHT):
    image.append([None] * WIDTH)


def fillTile(r, c):
    if c == WIDTH:
        return fillTile(r+1, 0)
    if r == HEIGHT:
        return True

    if r == 0 and c == 0:
        image[r][c] = corner
        return fillTile(0, 1)
    # Try all possibilities according to the left/top tile
    if r == 0:
        tiles = image[0][c-1].getOrientedBorderTiles(RIGHT)
    else:
        tiles = image[r-1][c].getOrientedBorderTiles(BOTTOM)
    # print(f"Tiles for r={r}, c={c}:", tiles)
    for tile in tiles:
        if tile.used:
            print(f"ERROR: Tile {tile.id} is already used")
            continue

        if r == 0:
            border = image[0][c-1].getOrientedBorder(RIGHT)
            tile.orientation = tile.getMatchingOrientation(LEFT, border)
        elif c == 0:
            border = image[r-1][0].getOrientedBorder(BOTTOM)
            tile.orientation = tile.getMatchingOrientation(TOP, border)
        else:
            borderTop = image[r-1][c].getOrientedBorder(BOTTOM)
            borderLeft = image[r][c-1].getOrientedBorder(RIGHT)
            orientationTop = tile.getMatchingOrientation(TOP, borderTop)
            orientationLeft = tile.getMatchingOrientation(LEFT, borderLeft)
            if orientationLeft != orientationTop:
                print(
                    f"ERROR: Not matching orientations. TOP is {orientationTop} "
                    + "with border {borderTop} and LEFT is {orientationLeft} with border {borderLeft}"
                )
                print(tile.borders)
                continue
            tile.orientation = orientationTop

        image[r][c] = tile
        # print(f"Placing tile {tile.id} on r={r}, c={c} with orientation {tile.orientation}")
        # rightBorder = tile.getOrientedBorder(RIGHT)
        # bottomBorder = tile.getOrientedBorder(BOTTOM)
        # print(f"    right border: {rightBorder}, bottom border: {bottomBorder}")
        tile.used = True
        if fillTile(r, c+1) is True:
            return True
        print("ERROR: cannot tile with", tile)
        tile.used = False
    return False


if fillTile(0, 0) is not True:
    print("ERROR, cannot tile")
    sys.exit(1)

# Construct map
pixels = []
for row in image:
    lines = []
    for tile in row:
        lines.append(tile.getLines())
    for i in range(len(lines[0])):
        line = []
        for x in lines:
            line += x[i]
        pixels.append(line)

# Search for monster
monster = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]
monsterH = len(monster)
monsterW = len(monster[0])


def findMonster(pixels, r, c, draw=False):
    if r + monsterH > len(pixels) or c + monsterW > len(pixels[r]):
        return False
    # Monster could be here, check it

    for rr in range(monsterH):
        for cc in range(monsterW):
            if monster[rr][cc] != '#':
                continue
            if pixels[r+rr][c+cc] != '#':
                return False
            if draw:
                pixels[r+rr][c+cc] = 'O'
    return True


monsters = 0
for r in range(len(pixels)):
    for c in range(len(pixels[r])):
        if findMonster(pixels, r, c):
            monsters += 1
            findMonster(pixels, r, c, True)  # draw it

count = 0
for line in pixels:
    count += line.count("#")
    print("".join(line))

print("Monster:", monsters)
print("Non monster # fields:", count)
