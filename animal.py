from enum import Enum

class Rarity(Enum):
    COMMON = 0
    RARE = 1

class Animal:
    MAX_HUNGER = 20
    MAX_THIRST = 20
    def __init__(self, x, y, type, name, hunger = 20, thirst = 20, rarity = Rarity.COMMON):
        self.x = x
        self.y = y
        self.type = type
        self.name = name
        self.hunger = hunger
        self.thirst = thirst
        self.rarity = rarity

    def eat(self, food: int):
        self.hunger += food
        if self.hunger > self.MAX_HUNGER:
            self.hunger = self.MAX_HUNGER

    def drink(self, water: int):
        self.thirst += water
        if self.thirst > self.MAX_THIRST:
            self.thirst = self.MAX_THIRST