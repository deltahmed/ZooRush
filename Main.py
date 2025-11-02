from __future__ import annotations
import pygame as pg
import sys 


from Camera import Camera
from Map import *
from Player import *
RES = WIDTH, HEIGHT = 1080,720
TILE_SIZE = 64
NUMBER_OF_TILES_X, NUMBER_OF_TILES_Y = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
FPS = 60

class Game:
    """Main Game class to handle game initialization, updates, and rendering."""
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES, pg.RESIZABLE)
        self.clock = pg.time.Clock() 
        self.delta_time = 1
        self.current_res = self.screen.get_size()
        self.half_width = self.current_res[0] // 2
        self.half_height = self.current_res[1] // 2
        self.tile_size = TILE_SIZE
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self, (0, 0), 2)
        self.camera = Camera(self)

    def update(self): 
        self.player.update()
        self.camera.update()
        self.delta_time = self.clock.tick(FPS) / 1000
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self): 
        """Draw all game elements on the screen."""
        self.screen.fill('black')
        self.map.draw()
        self.player.draw()

    def check_event(self):
        """Close the window properly when quitting."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.VIDEORESIZE:
                self.current_res = self.screen.get_size()
                self.half_width = self.current_res[0] // 2
                self.half_height = self.current_res[1] // 2
    
    def run(self):
        """Run the game loop."""
        while True:
            self.check_event()
            self.update()
            self.draw()
            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()

