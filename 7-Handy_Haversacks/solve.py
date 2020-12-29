#!/usr/bin/python3

import sys
import re

# Read input
graph = {}
for line in sys.stdin:
    line = line.strip()
    (color, contains) = line.split(" bags contain ")
    graph[color] = {
        "scanned": False,
        "containsShinyGold": False,
        "count": 0,
        "bags": [],
    }
    if contains == "no other bags.":
        continue
    bags = contains.split(", ")
    for bag in bags:
        m = re.match(r'^\s*([0-9]+) (\w+ \w+) bags?', bag)
        if m is None:
            print(f"Error on line '{line}' on '{bag}'")
        graph[color]['bags'].append(
            (int(m.groups()[0]), m.groups()[1])
        )


def scanBags(color, targetColor):
    if graph[color]['scanned']:
        return graph[color]['count']

    for (bagCount, bagColor) in graph[color]['bags']:
        graph[color]['count'] += bagCount * (scanBags(bagColor, targetColor) + 1)
        if bagColor == targetColor or graph[bagColor]['containsShinyGold']:
            graph[color]['containsShinyGold'] = True

    graph[color]['scanned'] = True
    return graph[color]['count']


# Recursive scan for 'shiny gold' bag
count = 0
for color in graph:
    scanBags(color, 'shiny gold')
    if graph[color]['containsShinyGold']:
        count += 1

print("Could contain shiny gold bag:", count)
print("Bags inside shiny gold bag:", graph['shiny gold']['count'])
