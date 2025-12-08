from __future__ import annotations
import pygame as pg
import sys 




class Camera:
    """
    camera class to handle view transformations and follow player
    manages the offset for rendering objects relative to player position
    """
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = 0, 0  # camera offset coordinates

    def update(self):
        """update camera position to keep player centered on screan"""
        player_x, player_y = self.game.player.pos
        # calculate camera offset to center player in viewport
        self.x = player_x * self.game.tile_size - self.game.half_width
        self.y = player_y * self.game.tile_size - self.game.half_height

    def apply(self, pos):
        """
        apply camera offset to world position for rendering
        rounds coordinates at render time to avoid visual gaps betwen tiles
        """
        return round(pos[0] - self.x), round(pos[1] - self.y)