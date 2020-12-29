#!/usr/bin/python3

import sys
import re

mask_and = 0
mask_or = 0
floating_positions = []
primaryMem = {}
secondaryMem = {}


def setMask(mask):
    global mask_and, mask_or, floating_positions
    mask_and = 0
    mask_or = 0
    floating_positions = []
    i = 36
    for b in mask:
        i -= 1
        mask_and <<= 1
        mask_or <<= 1
        if b == '1':
            mask_or += 1  # set number to 1
        elif b == 'X':
            floating_positions.append(i)
            mask_and += 1  # copy value from number
        # else mask_and = 0 -> set 0


def setPrimaryMem(address, value):
    # bitmasks are applied to the value
    primaryMem[address] = (value & mask_and) | mask_or


def setSecondaryMem(address, value):
    # value is unchanged but bitmask is applied to address
    # and 'X' means "floating bit"

    address |= mask_or  # Apply or mask
    # Run through all possible addresses:
    setSecondaryMemFloating(address, floating_positions, value)


def setSecondaryMemFloating(address, floating_positions, value):
    if len(floating_positions) == 0:
        secondaryMem[address] = value
        return

    p = floating_positions[0]
    mask = 1 << p
    setSecondaryMemFloating(address & ~mask, floating_positions[1:], value)  # 0
    setSecondaryMemFloating(address | mask, floating_positions[1:], value)   # 1


for line in sys.stdin:
    m = re.match(r'^mask = ([01X]*)$', line)
    if m:
        setMask(m.groups()[0])
        continue
    m = re.match(r'^mem\[([0-9]+)\] = ([0-9]+)$', line)
    if m:
        address, value = map(int, m.groups())
        setPrimaryMem(address, value)
        setSecondaryMem(address, value)
    else:
        print("error")

print("Sum of values (primary mem):", sum(primaryMem.values()))
print("Sum of values (secondary mem):", sum(secondaryMem.values()))
