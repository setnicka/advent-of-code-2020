#!/usr/bin/python3

import sys
import re

fields = {}
tickets = []
my_ticket = []


def matchRanges(value, ranges):
    for (start, end) in ranges:
        if value >= start and value <= end:
            return True
    return False


# Load rules
phase = 0
for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue

    if line == "your ticket:":
        phase = 1
        continue
    elif line == "nearby tickets:":
        phase = 2
        continue

    if phase == 0:
        m = re.match(r'^([^:]+): (\d+)-(\d+) or (\d+)-(\d+)', line)
        (name, r1s, r1e, r2s, r2e) = m.groups()
        fields[name] = {
            "name": name,
            "ranges": [
                (int(r1s), int(r1e)),
                (int(r2s), int(r2e)),
            ],
            "possible_columns": [],
            "column": None,
        }
    elif phase == 1:
        my_ticket = list(map(int, line.split(",")))
    elif phase == 2:
        values = list(map(int, line.split(",")))
        tickets.append(values)

all_ranges = []
for field in fields.values():
    for r in field["ranges"]:
        all_ranges.append(r)

all_values = [[] for _ in my_ticket]

wrong_values = []
for ticket in tickets:
    valid = True
    for value in ticket:
        if not matchRanges(value, all_ranges):
            valid = False
            wrong_values.append(value)
    if valid:
        i = 0
        for value in ticket:
            all_values[i].append(value)
            i += 1

print("Sum of all wrong values:", sum(wrong_values))

for fieldName in fields:
    for i in range(len(all_values)):
        valid = True
        for value in all_values[i]:
            if not matchRanges(value, fields[fieldName]["ranges"]):
                valid = False
                break
        if valid:
            fields[fieldName]["possible_columns"].append(i)


def matchColumns(level, fieldNames, usedColumns):
    if len(fieldNames) == 0:
        print("FOUND")
        return True

    chosenField = None
    chosenPossibleColumns = []
    otherFields = []
    for i in range(len(fieldNames)):
        field = fields[fieldNames[i]]
        possibleColumns = []
        for c in field["possible_columns"]:
            if c not in usedColumns:
                possibleColumns.append(c)
        if chosenField is None or len(possibleColumns) < len(chosenPossibleColumns):
            chosenField = field
            chosenPossibleColumns = possibleColumns
            otherFields = fieldNames[:i] + fieldNames[i+1:]

    name = chosenField["name"]
    print(f"Level {level}: Chosen '{name}' with possible columns: {chosenPossibleColumns}")
    for i in chosenPossibleColumns:
        if matchColumns(level + 1, otherFields, usedColumns + [i]):
            chosenField["column"] = i
            return True

    return False


matchColumns(0, list(fields.keys()), [])

mult = 1
for fieldName in fields:
    field = fields[fieldName]
    value = my_ticket[field['column']]
    print(f"{fieldName}:\tcolumn {field['column']}\tmy ticket value: {value}")
    if fieldName.startswith("departure"):
        mult *= value

print("Part 2 (multiplied departure values):", mult)
