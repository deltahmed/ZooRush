from __future__ import annotations
import pygame as pg
from utils import *


class Player:
    """
    manages the player entity in the game world
    handles movement, position tracking, inventory management and money
    the player can move around the map and collect items in their inventory
    """
    
    def __init__(self, game, init_pos, speed) -> None:
        """
        initialize a new player instance
        
        args:
            game: reference to the main game object
            init_pos: tuple containing starting x and y coordinates
            speed: movement speed in tiles per second
        """
        self.game = game
        self.x, self.y = init_pos
        self.speed = speed
        self.money = 0
        self.load_inventory()


    def load_inventory(self):
        """creates an empty inventory with all available prop types"""
        # initialize inventory dict with zero quantity for each prop
        self.inventory = {name: 0 for name in self.game.renderer.props_sizes.keys()}

    def add_to_inventory(self, item_name: str, quantity: int =1):
        """
        adds items to the player's inventory
        
        args:
            item_name: the name of the item to add
            quantity: how many to add (default is 1)
        """
        if item_name in self.inventory:
            # item already exists, increment the count
            self.inventory[item_name] += quantity
        else:
            # new item type, create entry
            self.inventory[item_name] = quantity

    def remove_from_inventory(self, item_name: str, quantity: int = 1):
        """
        removes items from inventory if available
        
        args:
            item_name: the name of the item to remove
            quantity: how many to remove (default is 1)
            
        returns:
            bool: true if succesfully removed, false if not enough items
        """
        if item_name in self.inventory:
            if self.inventory[item_name] >= quantity:
                # enough items available, remove them
                self.inventory[item_name] -= quantity
                return True
            else:
                # not enough items in inventory
                return False
        else:
            # item doesn't exist in inventory
            return False
            
    def move(self):
        """
        handles player movement based on keyboard input and mouse edge detection
        applies delta time for smooth frame-independent movement
        enforces map boundaries to keep the visible area within map limits
        """
        dx, dy = 0, 0
        
        # check keyboard input for movement direction
        keys = pg.key.get_pressed()
        if keys[pg.K_z] or keys[pg.K_w] or keys[pg.K_UP]:
            dy -= 1  # move up
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            dy += 1  # move down
        if keys[pg.K_q] or keys[pg.K_a] or keys[pg.K_LEFT]:
            dx -= 1  # move left
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            dx += 1  # move right
        
        # check mouse position for edge scrolling
        mouse_x, mouse_y = pg.mouse.get_pos()
        edge_threshold = 30  # pixels from edge to trigger scrolling
        screen_width, screen_height = self.game.current_res
        
        # mouse near top edge
        if mouse_y < edge_threshold:
            dy -= 1
        # mouse near bottom edge
        elif mouse_y > screen_height - edge_threshold:
            dy += 1
        
        # mouse near left edge
        if mouse_x < edge_threshold:
            dx -= 1
        # mouse near right edge
        elif mouse_x > screen_width - edge_threshold:
            dx += 1
        
        # calculate new position with delta time for smooth movement
        new_x = self.x + dx * self.speed * self.game.delta_time
        new_y = self.y + dy * self.speed * self.game.delta_time
        
        # calculate how many tiles are visible on screen
        # this ensures the map edges stay within view
        half_screen_tiles_x = (self.game.current_res[0] / self.game.tile_size) / 2
        half_screen_tiles_y = (self.game.current_res[1] / self.game.tile_size) / 2
        
        # get actual map dimensions from the game map
        map_width = len(self.game.map.map[0])  # 70 tiles
        map_height = len(self.game.map.map)    # 50 tiles
        
        # define movement boundaries based on actual map size
        # player must stay within these limits to keep map edges visible
        min_x = half_screen_tiles_x
        max_x = map_width - half_screen_tiles_x
        min_y = half_screen_tiles_y
        max_y = map_height - half_screen_tiles_y
        
        # apply boundaries only if they're valid
        # if screen is larger than map, center the player
        if max_x > min_x:
            new_x = max(min_x, min(new_x, max_x))
        else:
            new_x = map_width / 2  # center of the map width
            
        if max_y > min_y:
            new_y = max(min_y, min(new_y, max_y))
        else:
            new_y = map_height / 2  # center of the map height
        
        # apply the calculated movement
        self.x = new_x
        self.y = new_y
        

    def draw(self):
        """renders the player (currently not implemented)"""
        pass
        
    def update(self):
        """called every frame to update player state"""
        # update player movement
        self.move()

    @property
    def pos(self):
        """returns the current player positoin as a tuple"""
        return self.x, self.y
    
