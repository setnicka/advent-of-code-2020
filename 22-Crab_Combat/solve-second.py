#!/usr/bin/python3

import sys

deck1 = []
deck2 = []
deck = deck1

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


def getStateString(deck1, deck2):
    return ",".join(map(str, deck1)) + "|" + ",".join(map(str, deck2))


allStates = dict()


def recursiveCombat(deck1, deck2):
    startingState = getStateString(deck1, deck2)
    if startingState in allStates:
        # print("This game already played with result", allStates[startingState])
        return allStates[startingState]

    # print("Starting new game of recursive combat with decks", deck1, deck2)

    states = dict()
    while True:
        stateString = getStateString(deck1, deck2)
        if stateString in states:
            # If in same state -> player 1 wins
            allStates[startingState] = (1, deck1)
            return 1, deck1
        states[stateString] = True

        card1 = deck1[0]
        deck1 = deck1[1:]
        card2 = deck2[0]
        deck2 = deck2[1:]
        if len(deck1) >= card1 and len(deck2) >= card2:
            # Start a game of recursive combat
            (winner, _) = recursiveCombat(deck1[:card1], deck2[:card2])
        else:
            if card1 > card2:
                winner = 1
            else:
                winner = 2

        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

        if len(deck1) == 0:
            allStates[startingState] = (2, deck2)
            return 2, deck2
        elif len(deck2) == 0:
            allStates[startingState] = (1, deck1)
            return 1, deck1


(winner, deck) = recursiveCombat(deck1, deck2)

score = 0
i = 1
while len(deck) > 0:
    score += deck.pop() * i
    i += 1

print(f"Game ended winning player {winner} with deck score {score}")
