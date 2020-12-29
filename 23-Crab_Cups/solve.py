#!/usr/bin/python3

# input = "389125467"  # test
input = "916438275"


class Item:
    value: int
    prev: object
    next: object

    def __init__(self, value):
        self.value = value


def doRounds(cups, currentIndex, rounds):
    L = len(cups)

    # Construct dequeue and pointers to items in dequeue
    items = [Item(x) for x in range(L+1)]
    last = None
    for i in range(L):
        item = items[cups[i]]
        item.prev = last
        if last is not None:
            last.next = item
        last = item
    # Make it circle
    item = items[cups[0]]
    item.prev = last
    last.next = item
    current = item

    for i in range(rounds):
        if i % 100_000 == 0:
            print(i)

        picked = []
        pickedValues = []
        for p in range(3):
            picked.append(current.next)
            pickedValues.append(current.next.value)
            current.next = current.next.next
            current.next.prev = current

        destinationValue = current.value - 1
        while True:
            if destinationValue == 0:
                destinationValue = L
            if destinationValue not in pickedValues:
                break
            destinationValue -= 1

        # Insert
        destination = items[destinationValue]
        for p in picked:
            destination.next.prev = p
            p.next = destination.next
            p.prev = destination
            destination.next = p
            destination = p  # for the next run

        current = current.next

    finalCups = []
    current = items[1]
    while True:
        finalCups.append(current.value)
        current = current.next
        if current == items[1]:
            break
    return finalCups


# Part 1
cups = list(map(int, list(input)))
print("Cups:", cups)
finalCups = doRounds(cups, 0, 100)
print("Final cups:", "".join(map(str, finalCups[1:])))

# Part 2
cups = list(map(int, list(input))) + list(range(10, 1_000_001))
finalCups = doRounds(cups, 0, 10_000_000)
print("First two cups after 1:", finalCups[1], finalCups[2])
print("Multiply of them:", finalCups[1] * finalCups[2])
