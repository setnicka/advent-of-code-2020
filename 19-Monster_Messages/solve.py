#!/usr/bin/python3

import sys
import re

allRules = {}
advanced = True


class Rule:
    id: str
    complete: bool
    regex: str
    choices: list[list]

    def __init__(self, id, rule):
        self.id = id
        if rule[0] == '"' and rule[-1] == '"':
            self.complete = True
            self.regex = rule[1:-1]
        else:
            self.complete = False
            self.choices = [x.split() for x in rule.split(" | ")]

    def getRegex(self):
        if not self.complete:
            choices = []
            for rules in self.choices:
                concat = []
                for rule in rules:
                    concat.append(allRules[rule].getRegex())

                if advanced and self.id == "11":
                    (a, b) = concat
                    for i in range(1, 10):
                        concat = [a]*i + [b]*i
                        choices.append("".join(concat))
                else:
                    choices.append("".join(concat))

            if len(choices) == 1:
                self.regex = choices[0]
            else:
                self.regex = "(" + "|".join(choices) + ")"

            if advanced and self.id == "8":
                self.regex = "(" + self.regex + ")+"

            self.complete = True
        return self.regex


# Parse rules

for line in sys.stdin:
    line = line.strip()
    if line == "":
        break
    (id, rule) = line.split(": ", maxsplit=1)
    allRules[id] = Rule(id, rule.strip())


r = re.compile("^" + allRules["0"].getRegex() + "$")

count = 0
for line in sys.stdin:
    if r.match(line.strip()):
        count += 1

print("Matching rules:", count)
