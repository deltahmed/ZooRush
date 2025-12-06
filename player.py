from __future__ import annotations
import pygame as pg
from utils import *



class Player:
    def __init__(self, game, init_pos, speed) -> None:
        """Player class"""
        self.game = game
        self.x, self.y = init_pos  # Player position
        self.speed = speed
        self.money = 0
        self.load_inventory()


    def load_inventory(self):
        self.inventory = {name: 0 for name in self.game.renderer.props_sizes.keys()}

    def add_to_inventory(self, item_name: str, quantity: int =1):
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity

    def remove_from_inventory(self, item_name: str, quantity: int = 1):
        if item_name in self.inventory:
            if self.inventory[item_name] >= quantity:
                self.inventory[item_name] -= quantity
                return True
            else:
                return False
        else:
            return False
    def move(self):
        dx, dy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_z] or keys[pg.K_w] or keys[pg.K_UP]:
            dy -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            dy += 1
        if keys[pg.K_q] or keys[pg.K_a] or keys[pg.K_LEFT]:
            dx -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            dx += 1
        
        # Apply movement with speed
        self.x += dx * self.speed * self.game.delta_time
        self.y += dy * self.speed * self.game.delta_time
        

    def draw(self):
        pass
    def update(self):
        self.move()

    @property
    def pos(self):
        return self.x, self.y
    
