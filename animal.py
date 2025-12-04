import random
from enum import Enum

import pygame.image
from pygame import Surface
from pygame.sprite import Sprite


def load_spritesheet(path, frame_width, frame_height):
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()

    frames = []
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            frame = sheet.subsurface((x, y, frame_width, frame_height))
            frames.append(frame)
    return frames


class Rarity(Enum):
    COMMON = 0
    RARE = 1


class Direction(Enum):
    SOUTH = 0
    NORTH = 1
    WEST = 2
    EAST = 3


class Movement(Enum):
    IDLE = 0
    WALK = 1


class Animal(Sprite):
    MAX_HUNGER = 20
    MAX_THIRST = 20

    def __init__(self, game, x, y, name, image, hunger=20, thirst=20, rarity=Rarity.COMMON, sub_image_size=32):
        super().__init__()
        # Animation
        self.enclosure = None
        self.move = Movement.IDLE
        self.move_frame = 0
        self.sub_image_size = sub_image_size  # 32x32 pixels by default in the full image .png
        self.direction = Direction.SOUTH

        self.animation_speed = 0.15
        self.frame_timer = 0

        self.behavior_timer = 0
        self.next_behavior_change = random.uniform(1, 3)

        self.game = game
        self.x = x
        self.y = y
        self.name = name
        self.hunger = hunger
        self.thirst = thirst
        self.rarity = rarity
        self.sheet = pygame.image.load(image).convert_alpha()  # image sheet with all subimages

        self.rect = pygame.Rect(x, y, sub_image_size, sub_image_size)
        self.update_image()

    def get_sub_image_position(self):
        # To determine y
        # base y = Direction Enum numero (self.direction)
        # if movement is IDLE, y += 4
        y = self.direction.value
        if self.move == Movement.IDLE:
            y += 4
            x = self.move_frame % 4
        else:
            x = self.move_frame % 6

        # how we determine x
        # for idle there are only 4 images so x = self.move_frame % 4
        # but when walking there are 6 images so x = self.move_frame % 6
        return x, y

    def update_animation(self):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.move_frame += 1

    def update_image(self):
        x, y = self.get_sub_image_position()
        sx = x * self.sub_image_size
        sy = y * self.sub_image_size

        frame_rect = pygame.Rect(sx, sy, 32, 32)

        self.image = self.sheet.subsurface(frame_rect)

    def draw(self):
        screen_x, screen_y = self.game.camera.apply((self.x * self.game.tile_size, self.y * self.game.tile_size))
        self.rect.x = screen_x
        self.rect.y = screen_y
        self.game.screen.blit(self.image, self.rect)

    def update_behavior(self, dt):
        self.behavior_timer += dt

        if self.behavior_timer >= self.next_behavior_change:

            self.behavior_timer = 0
            self.next_behavior_change = random.uniform(3, 5)

            next_move = Movement.IDLE
            if random.random() > 0.5:
                next_move = Movement.WALK  # mouvement

            if next_move != self.move:
                self.move = next_move
                self.move_frame = 0

            # choix direction
            self.direction = random.choice(list(Direction))

    def move_animal(self, dt):
        if self.move == Movement.IDLE:
            return

        speed = 0.5 * dt  # tuiles/sec

        new_x = self.x
        new_y = self.y

        # deplacement prévu
        if self.direction == Direction.NORTH:
            new_y -= speed
        elif self.direction == Direction.SOUTH:
            new_y += speed
        elif self.direction == Direction.WEST:
            new_x -= speed
        elif self.direction == Direction.EAST:
            new_x += speed

        # verif de l’enclos si y'en a un
        if self.enclosure is not None:
            e = self.enclosure

            # taille de l'animal en tuiles
            animal_size_in_tiles = self.sub_image_size / self.game.tile_size

            # taille réelle des barrières en tuiles
            v_w_tiles = e.v_w / self.game.tile_size
            h_h_tiles = e.h_h / self.game.tile_size

            # limites intérieures exactes en tuiles
            min_x = e.x + v_w_tiles
            max_x = e.x + e.size - v_w_tiles - animal_size_in_tiles
            min_y = e.y + h_h_tiles
            max_y = e.y + e.size - h_h_tiles - animal_size_in_tiles

            fixed_x = max(min_x, min(new_x, max_x))
            fixed_y = max(min_y, min(new_y, max_y))

            if fixed_x != new_x or fixed_y != new_y:
                # collision avec barrière
                self.direction = random.choice(list(Direction))
                self.move = Movement.IDLE
                self.move_frame = 0

            self.x = fixed_x
            self.y = fixed_y
            return

        # si pas d'enclos, aucune vérification
        self.x = new_x
        self.y = new_y

        # test empecher de sortir de la map
        # self.x = max(0, min(self.x, self.game.map_width - 1))
        # self.y = max(0, min(self.y, self.game.map_height - 1))

    # dt = le temps écoulé depuis la dernière frame (en sec)
    # c'est clock.get_time() / 1000
    def update(self, dt=0.016):
        # On utilise dt pour garder le meme temps peut importe les fps
        # Le behavior peut donc changer au maximum toute les 1 à 3 secondes
        self.update_behavior(dt)
        self.move_animal(dt)
        self.update_animation()
        self.update_image()

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


class Sheep(Animal):
    def __init__(self, game, x, y):
        super().__init__(game=game, x=x, y=y, name="Sheep", image="sheep.png")
