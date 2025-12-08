from __future__ import annotations
import pygame as pg
from random import choice

from config import PROP_PRICES
from utils import *
from enclosure import *


class Map:
    """
    main class for managing the game map, including tiles, props, enclosures and animals
    handles rendering and updates for all map elements
    """
    
    def __init__(self,game) -> None:
        """
        initialize the map with game reference and generate initial content
        
        args:
            game: reference to the main game object
        """
        self.game = game
        self.props = []  # list of all decorative props on the map
        self.enclosures = []  # list of all animal enclosures
        self.generate_map()  # create the base tile grid
        self.generate_random_props()  # populate with random decorations
        

    def update_animals(self, delta_time: float) -> None:
        """
        update all animals in all enclosures with delta time
        
        args:
            delta_time: time elapsed since last frame in seconds
        """
        # loop through each enclosure and update its animals
        for enclosure in self.enclosures:
            enclosure.update_animals(delta_time)

    def get_tile(self, x, y):
        """
        safely retrieve a tile at given coordinates
        returns none if coordinates are out of bounds
        """
        return self.map[y][x] if 0 <= x < len(self.map[0]) and 0 <= y < len(self.map) else None
    

    def generate_map(self):
        """
        generate the base grid of tiles with random textures and orientations
        creates a 70x50 tile grid
        """
        # create 2d array with random tile textures (1 or 2) and random orientations
        self.map = [[Tile(texture=randint(1,2), orientation=Direction(randint(0,3))) for _ in range(70)] for _ in range(50)]
        

    def draw(self):
        """
        main rendering method for the entire map
        draws tiles, props, enclosures and animals in correct order for proper layering
        """
        # list to store props that need to be drawn on top of tiles
        screen_props = []
        
        # iterate through all tiles in the map grid
        for j in range(len(self.map)):
            for i in range(len(self.map[0])):
                tile = self.get_tile(i, j)
                
                # draw the base tile texture if it exists
                if tile.texture :
                    # convert tile coordinates to screen coordinates
                    screen_x, screen_y = self.game.camera.apply((i * self.game.tile_size, j * self.game.tile_size))
                    
                    # only draw if tile is visible on screen (culling for performance)
                    if -self.game.tile_size <= screen_x <= self.game.current_res[0] and -self.game.tile_size <= screen_y <= self.game.current_res[1]:
                        self.game.screen.blit(self.game.renderer.get_texture(tile), (screen_x, screen_y))
                
                # collect enclosure tiles for later rendering
                if tile.prop and tile.prop.is_enclosure and tile.enclosure_type is not None:
                    screen_props.append((tile, i, j))
                # collect main prop tiles (not enclosures) for later rendering
                elif tile.prop and tile.main_prop_tile and not tile.prop.is_enclosure:
                    screen_props.append((tile, i, j))
        
        # draw all collected props on top of tiles
        for tile, i, j in screen_props:
            if tile.prop.is_enclosure:
                # render enclosure texture based on its type (corner, edge, etc)
                enclosure_texture = self.game.renderer.enclosures_textures[tile.enclosure_type.value]
                real_x, real_y = i * self.game.tile_size, j * self.game.tile_size
                screen_x, screen_y = self.game.camera.apply((real_x, real_y))
                self.game.screen.blit(enclosure_texture, (screen_x, screen_y))
            else:
                # render regular prop texture
                prop_texture = self.game.renderer.get_prop_texture(tile.prop.name)
                # convert tile coordinates to pixel coordinates
                real_x = tile.prop.x * self.game.tile_size
                real_y = tile.prop.y * self.game.tile_size
                if prop_texture:
                    screen_x, screen_y = self.game.camera.apply((real_x, real_y))
                    self.game.screen.blit(prop_texture, (screen_x, screen_y))
        
        # draw all animals from all enclosures on top of everything
        for enclosure in self.enclosures:
            for animal in enclosure.animals:
                # get the current animation state (idle or walk)
                animation = animal.get_current_animation()
                
                # retrieve the current animation frame for the animal
                animal_frame = self.game.renderer.get_animal_frame(
                    animal.species,
                    animation,
                    animal.direction,
                    animal.current_frame
                )
                
                if animal_frame:
                    # convert animal position from tile coordinates to pixels
                    real_x = animal.x * self.game.tile_size
                    real_y = animal.y * self.game.tile_size
                    
                    # apply camera transformation
                    screen_x, screen_y = self.game.camera.apply((real_x, real_y))
                    
                    # only render if animal is visible on screen
                    if -self.game.tile_size <= screen_x <= self.game.current_res[0] and \
                       -self.game.tile_size <= screen_y <= self.game.current_res[1]:
                        self.game.screen.blit(animal_frame, (screen_x, screen_y))


    def create_prop(self, name, x, y):
        """
        create a new decorative prop at specified coordinates
        handles multi-tile props by marking all ocupied tiles
        
        args:
            name: the name/type of the prop to create
            x: x coordinate in tile grid
            y: y coordinate in tile grid
        """
        # instantiate new prop object
        prop = Props(name, x, y)
        self.props.append(prop)
        
        # verify starting position is valid
        start_tile = self.get_tile(x, y)
        if not start_tile:
            return
        
        # mark the main tile of the prop
        start_tile.prop = prop
        start_tile.main_prop_tile = True
        
        # assign the prop to all tiles it occupies based on its size
        for i in range(int(self.game.renderer.get_prop_size(name)[0])):
            for j in range(int(self.game.renderer.get_prop_size(name)[1])):
                # skip the first tile since we already set it
                if not (i == 0 and j == 0):
                    tile = self.get_tile(x + i, y + j)
                    if tile:
                        tile.prop = prop

    def remove_prop(self, prop):
        """
        remove a prop from the map and clear all its occupied tiles
        
        args:
            prop: the prop object to remove
        """
        self.props.remove(prop)
        
        # clear all tiles that this prop was occupying
        for i in range(int(self.game.renderer.get_prop_size(prop.name)[0])):
            for j in range(int(self.game.renderer.get_prop_size(prop.name)[1])):
                tile = self.get_tile(prop.x + i, prop.y + j)
                if tile:
                    tile.prop = None
                    tile.main_prop_tile = False

    def create_enclosure(self, x, y, width, height):
        """
        create a new animal enclosure at specified position with given dimensions
        assigns appropriate edge types to each tile (corners, edges, etc)
        
        args:
            x: starting x coordinate
            y: starting y coordinate
            width: width of enclosure in tiles
            height: height of enclosure in tiles
        """
        # create new enclosure instance
        enclosure = Enclosure(x, y, width, height)
        self.enclosures.append(enclosure)

        # iterate through all tiles in the enclosure area
        for i in range(width):
            for j in range(height):
                tile = self.get_tile(x + i, y + j)
                if tile:
                    # mark tile as part of enclosure
                    tile.prop = enclosure
                    tile.is_enclosure = True

                    # assign specific enclosure type based on position
                    # corners get special treatment for proper rendering
                    if i == 0 and j == 0:
                        tile.enclosure_type = EnclosureType.TOP_LEFT
                        tile.main_prop_tile = True
                    elif i == width - 1 and j == 0:
                        tile.enclosure_type = EnclosureType.TOP_RIGHT
                    elif i == 0 and j == height - 1:
                        tile.enclosure_type = EnclosureType.BOTTOM_LEFT
                    elif i == width - 1 and j == height - 1:
                        tile.enclosure_type = EnclosureType.BOTTOM_RIGHT
                    # edges between corners
                    elif j == 0:
                        tile.enclosure_type = EnclosureType.TOP
                    elif j == height - 1:
                        tile.enclosure_type = EnclosureType.BOTTOM
                    elif i == 0:
                        tile.enclosure_type = EnclosureType.LEFT
                    elif i == width - 1:
                        tile.enclosure_type = EnclosureType.RIGHT

    def remove_enclosure(self, enclosure):
        """
        remove an enclosure and clear all its tiles
        
        args:
            enclosure: the enclosure object to remove
        """
        self.enclosures.remove(enclosure)
        
        # clear all tiles in the enclosure area
        for i in range(enclosure.width):
            for j in range(enclosure.height):
                tile = self.get_tile(enclosure.x + i, enclosure.y + j)
                if tile:
                    tile.prop = None
                    tile.is_enclosure = False
                    tile.main_prop_tile = False
                    tile.enclosure_type = None
    
    def generate_random_props(self):
        """
        generate random decorative props across the map without overlapping
        only uses props with zero income (decorative only, not functional)
        implements safety margins to prevent props from touching each other
        """
        # filter props that are purely decorative (income = 0)
        available_props = [name for name, data in PROP_PRICES.items() if data["income"] == 0]

        # determine how many props to scatter across the map
        num_props = randint(400, 500)
        
        # attempt to place props with collision detection
        attempts = 0
        max_attempts = num_props * 50  # prevent infinite loops if map gets too crowded
        props_placed = 0
        
        while props_placed < num_props and attempts < max_attempts:
            attempts += 1
            
            # randomly select a prop type
            prop_name = choice(available_props)
            
            # get the dimensions of this prop
            prop_size = self.game.renderer.get_prop_size(prop_name)
            if prop_size == (0, 0):
                continue
            
            prop_width, prop_height = prop_size
            
            # generate random position with safety margins
            # keep props away from map edges
            margin = 2
            safety_margin = 1  # space between props
            
            # calculate maximum valid coordinates
            # the prop occupies tiles from (x, y) to (x + prop_width - 1, y + prop_height - 1)
            # with safety margin, we need space up to (x + prop_width + safety_margin - 1, y + prop_height + safety_margin - 1)
            # so: x + prop_width + safety_margin - 1 < len(self.map[0])
            # therefore: x <= len(self.map[0]) - prop_width - safety_margin
            max_x = len(self.map[0]) - int(prop_width) - safety_margin - 1
            max_y = len(self.map) - int(prop_height) - safety_margin - 1
            
            # skip if there's not enough space for this prop
            if max_x < margin or max_y < margin:
                continue
                
            # generate random coordinates within valid range
            x = randint(margin, max_x)
            y = randint(margin, max_y)
            
            # check if placement area is clear (no overlaps)
            can_place = True
            # check area including safety margin around prop
            for i in range(-safety_margin, int(prop_width) + safety_margin):
                for j in range(-safety_margin, int(prop_height) + safety_margin):
                    check_x = x + i
                    check_y = y + j
                    # ensure we're still within map boundries
                    if check_x < 0 or check_x >= len(self.map[0]) or check_y < 0 or check_y >= len(self.map):
                        can_place = False
                        break
                    tile = self.get_tile(check_x, check_y)
                    # tile must exist and be empty
                    if not tile or tile.prop:
                        can_place = False
                        break
                if not can_place:
                    break
            
            # if location is valid and empty, place the prop
            if can_place:
                self.create_prop(prop_name, x, y)
                props_placed += 1
        
       
        