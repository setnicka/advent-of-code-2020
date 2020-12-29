#!/usr/bin/python3

import sys


def evalExpressionNormal(tokens):
    # Normal situation, + and * have the same precedence
    value = None
    op = None
    for x in tokens:
        if x == '+' or x == '*':
            op = x
        else:
            if op is None:
                value = int(x)
            elif op == '+':
                value += int(x)
            elif op == '*':
                value *= int(x)
            else:
                print("ERROR, unknown op", op)
    return value


def evalExpressionAddSuperior(tokens):
    # + evaluated before *
    toMultiply = []
    item = 0
    tokens.append('*')
    for x in tokens:
        if x == '*':
            if item is not None:
                toMultiply.append(item)
            item = 0
        elif x == '+':
            continue
        else:
            item += int(x)

    value = 1
    for x in toMultiply:
        value *= x
    return value


def evalTokens(tokens, evalExpression):
    # Prepare tokens
    preparedTokens = []
    i = 0
    while i < len(tokens):
        x = tokens[i]
        # print(x)
        if x == '(':
            x, skip = evalTokens(tokens[i+1:], evalExpression)
            i += skip + 1
        elif x == ')':
            # print("end brace", value, i)
            break

        preparedTokens.append(x)
        i += 1

    return evalExpression(preparedTokens), i


sumNormal = 0
sumAddSuperior = 0
for line in sys.stdin:
    tokens = line.strip().replace("(", "( ").replace(")", " )").split()
    resultNormal, _ = evalTokens(tokens, evalExpressionNormal)
    resultAddSuperior, _ = evalTokens(tokens, evalExpressionAddSuperior)
    sumNormal += resultNormal
    sumAddSuperior += resultAddSuperior

print("Sum of part 1 results:", sumNormal)
print("Sum of part 2 results:", sumAddSuperior)
