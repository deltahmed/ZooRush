from __future__ import annotations
import pygame as pg
from random import randint
from dataclasses import dataclass


class Renderer:
    def __init__(self,game) -> None:
        self.game = game
        self.tiles = []
        try:
            self.tiles_spritesheet = pg.image.load('tiles.png')
        except:
            print("Erreur de chargement")

    def cut_tiles(self):
        tile_width = self.game.tile_size
        tile_height = self.game.tile_size
        for y in range(self.tiles_spritesheet.get_height() // tile_height):
            for x in range(self.tiles_spritesheet.get_width() // tile_width):
                self.tiles.append(self.tiles_spritesheet.subsurface((x * tile_width, y * tile_height, tile_width, tile_height)))

    def get_texture(self, tile_id):
        if tile_id <= 0 or tile_id > len(self.tiles):
            return None
        return self.tiles[tile_id-1]
