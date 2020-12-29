#!/usr/bin/python3

card_pkey = int(input())
door_pkey = int(input())

card_loop_size = 0
v = 1
while v != card_pkey:
    v = (v * 7) % 20201227
    card_loop_size += 1
print("Card loop size is", card_loop_size)

# door_loop_size = 0
# v = 1
# while v != door_pkey:
#     v = (v * 7) % 20201227
#     door_loop_size += 1
# print("Door loop size is", door_loop_size)

v = 1
for i in range(card_loop_size):
    v = (v * door_pkey) % 20201227
print("Encryption key:", v)

# v = 1
# for i in range(door_loop_size):
#     v = (v * card_pkey) % 20201227
# print("Encryption key:", v)
