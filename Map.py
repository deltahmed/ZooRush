from __future__ import annotations
import pygame as pg



_ = False
map =   [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],]


class Map:
    def __init__(self,game) -> None:
        '''initialisation de la class carte'''
        self.game = game
        self.map = map
        try:
            self.tile_image = pg.image.load('tile.jpg')
            self.tile_image = pg.transform.scale(self.tile_image, (self.game.tile_size, self.game.tile_size))
        except:
            self.tile_image = pg.Surface((self.game.tile_size, self.game.tile_size))
            self.tile_image.fill('green')

    def get_tile(self, x, y):
        return self.map[y][x] if 0 <= x < len(self.map[0]) and 0 <= y < len(self.map) else None
    

    def draw(self):
        for j in range(len(self.map)):
            for i in range(len(self.map[0])):
                if self.get_tile(i, j) is not None:
                    # Appliquer la transformation de la caméra
                    screen_x, screen_y = self.game.camera.apply((i * self.game.tile_size, j * self.game.tile_size))
                    # Ne dessiner que si visible à l'écran
                    
                    if -self.game.tile_size <= screen_x <= self.game.current_res[0] and -self.game.tile_size <= screen_y <= self.game.current_res[1]:
                        self.game.screen.blit(self.tile_image, (screen_x, screen_y))