from __future__ import annotations
import pygame as pg
from random import randint
from dataclasses import dataclass

@dataclass
class Tile:
    type: str = "grass"
    layer: object = None


class Map:
    def __init__(self,game) -> None:
        self.game = game
        self.generate_map()
        try:
            self.tile_image = pg.image.load('tile.jpg')
            self.tile_image = pg.transform.scale(self.tile_image, (self.game.tile_size, self.game.tile_size))
        except:
            self.tile_image = pg.Surface((self.game.tile_size, self.game.tile_size))
            self.tile_image.fill('green')

    def get_tile(self, x, y):
        return self.map[y][x][0] if 0 <= x < len(self.map[0][0]) and 0 <= y < len(self.map) else None
    

    def generate_map(self):
        self.map = [[(randint(0, 1), 0, 0) for _ in range(16)] for _ in range(6)]
        print(self.map)
        return self.map

    def draw(self):
        for j in range(len(self.map)):
            for i in range(len(self.map[0])):
                if self.get_tile(i, j) and self.get_tile(i, j) == 1:
                    # Appliquer la transformation de la caméra
                    screen_x, screen_y = self.game.camera.apply((i * self.game.tile_size, j * self.game.tile_size))
                    # Ne dessiner que si visible à l'écran
                    
                    if -self.game.tile_size <= screen_x <= self.game.current_res[0] and -self.game.tile_size <= screen_y <= self.game.current_res[1]:
                        self.game.screen.blit(self.tile_image, (screen_x, screen_y))