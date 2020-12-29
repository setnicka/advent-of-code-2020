#!/usr/bin/python3

import sys

cmds = []
for line in sys.stdin:
    (cmd, arg) = line.strip().split()
    cmds.append(
        (cmd, int(arg))
    )

for x in range(len(cmds)):
    visited = [False] * len(cmds)
    i = 0
    acc = 0
    while True:
        if i == len(cmds):
            print(f"Ending program, accumulator state: {acc}")
            sys.exit(0)

        if visited[i]:
            print(f"Instruction {i} visited again, accumulator state: {acc}")
            break

        visited[i] = True
        (cmd, arg) = cmds[i]
        if cmd == 'acc':
            acc += arg
            i += 1
        elif cmd == 'jmp' and x == i:
            # Changed to nop
            i += 1
        elif cmd == 'nop' and x == i:
            # Changed to jmp
            i += arg
        elif cmd == 'jmp':
            i += arg
        elif cmd == 'nop':
            i += 1
