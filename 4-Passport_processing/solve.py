#!/usr/bin/python3

import sys
import re

passports = []
passport = {}
# Scan all passports
for line in sys.stdin:
    line = line.strip()
    if line == "":
        if len(passport):
            passports.append(passport)
            passport = {}
        continue

    for segment in line.split():
        (key, value) = segment.split(":")
        passport[key] = value
# Add the last one if not empty
if len(passport):
    passports.append(passport)


# Process passports
def checkHgt(value):
    m = re.match(r'^([0-9]+)(cm|in)$', value)
    if not m:
        return False
    number = int(m.groups()[0])
    unit = m.groups()[1]
    if unit == 'cm':
        return number >= 150 and number <= 193
    else:
        return number >= 59 and number <= 76


valid = 0
needed = {
    "byr": lambda value: int(value) >= 1920 and int(value) <= 2002,
    "iyr": lambda value: int(value) >= 2010 and int(value) <= 2020,
    "eyr": lambda value: int(value) >= 2020 and int(value) <= 2030,
    "hgt": checkHgt,
    "hcl": lambda value: re.match(r'^#[0-9a-f]{6}$', value),
    "ecl": lambda value: re.match(r'^(amb|blu|brn|gry|grn|hzl|oth)$', value),
    "pid": lambda value: re.match(r'^[0-9]{9}$', value),
}
optional = ["cid"]
for passport in passports:
    isValid = True
    for item in needed:
        if item not in passport:
            isValid = False
            break
        if not needed[item](passport[item]):
            isValid = False
            break
    if isValid:
        valid += 1

print(valid)
