#!/usr/bin/python3

import sys


def combineGroup(group):
    questions = set()
    for member in group:
        for item in member:
            questions.add(item)
    return questions


def intersectGroup(group):
    questions = set(list(group[0]))
    for member in group[1:]:
        questions = questions.intersection(set(list(member)))
    return questions


groups = []
group = []
for line in sys.stdin:
    line = line.strip()
    if line == "":
        if len(group):
            groups.append(group)
        group = []
    else:
        group.append(line)
if len(group):
    groups.append(group)

sumCombined = 0
sumIntersect = 0
for group in groups:
    sumCombined += len(combineGroup(group))
    sumIntersect += len(intersectGroup(group))

print("Combined:", sumCombined)
print("Intersect:", sumIntersect)
