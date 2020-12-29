#!/usr/bin/python3

import sys
from collections import deque

deck1 = deque()
deck2 = deque()

for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue
    elif line.startswith("Player 1:"):
        deck = deck1
    elif line.startswith("Player 2:"):
        deck = deck2
    else:
        deck.append(int(line))

print(deck1)
print(deck2)

round = 0
while len(deck1) > 0 and len(deck2) > 0:
    round += 1
    card1 = deck1.popleft()
    card2 = deck2.popleft()
    if card1 > card2:
        deck1.append(card1)
        deck1.append(card2)
    else:
        deck2.append(card2)
        deck2.append(card1)

deck = deck1 if len(deck1) > 0 else deck2

score = 0
i = 1
while len(deck) > 0:
    score += deck.pop() * i
    i += 1

print(f"Game ended after {round} rounds with winning deck score {score}")
