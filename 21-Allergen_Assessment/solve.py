#!/usr/bin/python3

import sys

allAllergens = dict()
allIngredients = dict()

for line in sys.stdin:
    line = line.strip()[:-1]  # Remove trailing ')'
    (ingredientsPart, allergensPart) = line.split(" (contains ", maxsplit=2)
    allergens = allergensPart.split(", ")
    ingredients = set(ingredientsPart.split(" "))

    for ingredient in ingredients:
        if ingredient not in allIngredients:
            allIngredients[ingredient] = 0
        allIngredients[ingredient] += 1

    for allergen in allergens:
        if allergen not in allAllergens:
            allAllergens[allergen] = ingredients
        allAllergens[allergen] = allAllergens[allergen].intersection(ingredients)

print("Possibilities:", allAllergens)

# Eliminate from allergens that have only one possible ingredient
allergenIngredients = set()
determined = dict()

while len(allAllergens) > 0:
    for allergen in allAllergens:
        allAllergens[allergen] = allAllergens[allergen].difference(allergenIngredients)
        if len(allAllergens[allergen]) == 1:
            a = allAllergens.pop(allergen).pop()
            allergenIngredients.add(a)
            determined[allergen] = a
            break

print("Determined allergens:", determined)

# Count how many ingredients could not contain an allergen
count = 0
for ingredient in allIngredients:
    if ingredient not in allergenIngredients:
        # print(f"Ingredient {ingredient} could not contain any allergen")
        count += allIngredients[ingredient]

print(count, "ingredients could not contain any allergen")

print("Sorted allergen ingredients by allergen name:", ",".join([determined[x] for x in sorted(determined.keys())]))
