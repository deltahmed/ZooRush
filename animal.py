from enum import Enum

from pygame import Surface
from pygame.sprite import Sprite


class Rarity(Enum):
    COMMON = 0
    RARE = 1


class Animal(Sprite):
    MAX_HUNGER = 20
    MAX_THIRST = 20

    def __init__(self, game, x, y, name, hunger=20, thirst=20, rarity=Rarity.COMMON):
        super().__init__()

        self.game = game
        self.x = x
        self.y = y
        self.name = name
        self.hunger = hunger
        self.thirst = thirst
        self.rarity = rarity
        self.image = Surface((40, 40))  # Un carré de 40x40 pixels
        self.image.fill((0, 0, 255))  # Rempli en bleu

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def eat(self, food: int):
        self.hunger += food
        if self.hunger > self.MAX_HUNGER:
            self.hunger = self.MAX_HUNGER

    def drink(self, water: int):
        self.thirst += water
        if self.thirst > self.MAX_THIRST:
            self.thirst = self.MAX_THIRST

    def sleep(self):
        pass

    def wake_up(self):
        pass

    def draw(self):
        screen_x, screen_y = self.game.camera.apply((self.x * self.game.tile_size, self.y * self.game.tile_size))
        self.rect.x = screen_x
        self.rect.y = screen_y
        self.game.screen.blit(self.image, self.rect)


class Sheep(Animal):
    def __init__(self, game, x, y):
        super().__init__(game=game, x=x, y=y, name="Sheep")
