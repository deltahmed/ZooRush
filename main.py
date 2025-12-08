from __future__ import annotations
import pygame as pg
import sys

from render import *
from camera import *
from map import *
from player import *
from config import STARTING_MONEY, ANIMAL_PRICES, PROP_PRICES
from hud import HUD
from menu import Menu, MenuOption

RES = WIDTH, HEIGHT = 1080, 720
TILE_SIZE = 64
NUMBER_OF_TILES_X, NUMBER_OF_TILES_Y = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
FPS = 0


class Game:
    """
    main game class that handels all the game logic and rendering
    manages initialization, game loop, menu system and state transitions
    """

    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES, pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.delta_time = 0.016  
        self.current_res = self.screen.get_size()
        self.half_width = self.current_res[0] // 2
        self.half_height = self.current_res[1] // 2
        self.tile_size = TILE_SIZE
        self.paused = False
        self.in_menu = True
        self.game_initialized = False
        
        # load font for menu interface
        font_path = "media/hud/font/soupofjustice.ttf"
        self.menu_font = pg.font.Font(font_path, 36)

    def show_menu(self) -> MenuOption:
        """display the main menu and return the selected option"""
        menu = Menu(self.screen, self.menu_font)
        return menu.run()

    def new_game(self):
        """
        initialize a new game sesion
        sets up all game components like renderer, map, player, camera and hud
        """
        # update current resolution in case window was resised in menu
        self.current_res = self.screen.get_size()
        self.half_width = self.current_res[0] // 2
        self.half_height = self.current_res[1] // 2
        
        try:
            self.money = STARTING_MONEY
            self.renderer = Renderer(self)
            self.map = Map(self)
            # place player at center of map (map is 70x50 tiles)
            map_center_x = len(self.map.map[0]) // 2  # 70 // 2 = 35
            map_center_y = len(self.map.map) // 2      # 50 // 2 = 25
            self.player = Player(self, (map_center_x, map_center_y), 2)
            self.camera = Camera(self)
            self.hud = HUD(self)
            self.paused = False
            self.game_initialized = True
        except Exception as e:
            # critical error durring game initilization, log and quit
            print(f"Erreur fatale lors de l'initialisation du jeu: {e}")
            import traceback
            traceback.print_exc()
            self.quit()

    def update(self):
        """update game state every frame based on delta time"""
        self.delta_time = self.clock.tick(FPS) / 1000.0
        
        # dont do anything if game is not initalized yet
        if not self.game_initialized:
            return
        
        # dont update game if paused, only update hud for pause menu
        if self.paused:
            self.hud.update()
            return
        
        # calculate income per second based on animals and props
        self.calculate_income()
        
        self.player.update()
        self.camera.update()
        self.map.update_animals(self.delta_time)
        self.hud.update()
        
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        """render all game elements to screen"""
        self.screen.fill('black')
        
        if not self.game_initialized:
            return
            
        self.map.draw()
        self.player.draw()
        self.hud.draw()
    
    def calculate_income(self):
        """
        calculate and add income based on animals and props
        iterates through all enclosurs and their animals to sum up total income per second
        """
        total_income_per_second = 0
        
        # loop through all enclosures and thier animals
        for enclosure in self.map.enclosures:
            for animal in enclosure.animals:
                # add income from this animal
                if animal.species in ANIMAL_PRICES:
                    total_income_per_second += ANIMAL_PRICES[animal.species]["income"]
        
        # loop through all props for their income
        for prop in self.map.props:
            if prop.name in PROP_PRICES:
                total_income_per_second += PROP_PRICES[prop.name]["income"]
        
        # add money based on elapsed time
        self.money += total_income_per_second * self.delta_time
        self.income_per_second = total_income_per_second

    def check_event(self):
        """handle all pygame events like quit, keyboard input and window resize"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                # toggle pause with escape key
                self.paused = not self.paused
                self.hud.toggle_pause()
            elif event.type == pg.VIDEORESIZE:
                # update resolution when window is resized
                self.current_res = self.screen.get_size()
                self.half_width = self.current_res[0] // 2
                self.half_height = self.current_res[1] // 2
                # update button positions in hud
                self.hud.handle_resize()
            
            # pass event to hud for button handeling
            self.hud.handle_event(event)
    
    def return_to_menu(self):
        """return to main menu and reset game state"""
        self.in_menu = True
        self.game_initialized = False
        self.paused = False


    def quit(self):
        """cleanup and exit the game properly"""
        pg.quit()
        sys.exit()

    def run(self):
        """
        main game loop
        handles menu display and game execution
        """
        while True:
            # if in menu, show menu screen
            if self.in_menu:
                option = self.show_menu()
                
                if option == MenuOption.NEW_GAME:
                    self.in_menu = False
                    self.new_game()
                elif option == MenuOption.QUIT:
                    self.quit()
                # if info option, menu handels displaying it
            else:
                # normal game loop
                self.check_event()
                self.update()
                self.draw()
                pg.display.flip()


if __name__ == '__main__':
    # entry point of the application
    # creates a new game instance and starts the main loop
    try:
        # initialize the game object with all necesary components
        game = Game()
        # start the main game loop (menu + gameplay)
        game.run()
    except Exception as e:
        # catch any unhandled exception that might occur during execution
        # this prevents the game from crashing silently without feedback
        print(f"Error occurred: {e}")
        # ensure pygame is properly closed to free resources
        pg.quit()
        # exit the program with error code
        sys.exit()
