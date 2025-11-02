from __future__ import annotations
import pygame as pg
from Utils import * 



class Player:
    def __init__(self, game, init_pos, speed) -> None:
        """Player class"""
        self.game = game
        self.x, self.y = init_pos  # Player position
        self.speed = speed

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
        screen_x, screen_y = self.game.camera.apply((self.x * self.game.tile_size, self.y * self.game.tile_size))
        pg.draw.circle(self.game.screen, 'green', (screen_x + self.game.tile_size // 2, screen_y + self.game.tile_size // 2), self.game.tile_size // 4)

    def update(self):
        self.move()

    @property
    def pos(self):
        return self.x, self.y
    
