from __future__ import annotations
import pygame as pg
import sys 




class Camera:
    """Camera class to handle view transformations."""
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = 0, 0

    def update(self):
        player_x, player_y = self.game.player.pos
        # Keep the player centered
        self.x = player_x * self.game.tile_size - self.game.half_width
        self.y = player_y * self.game.tile_size - self.game.half_height

    def apply(self, pos):
        # Round only at render time to avoid gaps
        return round(pos[0] - self.x), round(pos[1] - self.y)