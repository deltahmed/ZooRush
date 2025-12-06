from __future__ import annotations
import pygame as pg

from utils import *
from enclosure import *



class Map:
    def __init__(self,game) -> None:
        self.game = game
        self.props = []
        self.enclosures = []
        self.generate_map()
        self.create_prop('test', 0, 0)
        
        # Premier enclos avec des moutons
        self.create_enclosure(5, 5, 5, 5)
        self.enclosures[0].add_animal(Animal('sheep', 6.5, 6.5))
        self.enclosures[0].add_animal(Animal('sheep', 7.5, 7.5))
        self.enclosures[0].add_animal(Animal('sheep', 8, 6))

        # Deuxième enclos avec des coqs
        self.create_enclosure(15, 10, 5, 6)
        self.enclosures[1].add_animal(Animal('rooster', 16.5, 12.5))
        self.enclosures[1].add_animal(Animal('rooster', 18, 13))
        self.enclosures[1].add_animal(Animal('rooster', 17, 14))

    def update_animals(self, delta_time: float) -> None:
        """Met à jour tous les animaux dans tous les enclos."""
        for enclosure in self.enclosures:
            enclosure.update_animals(delta_time)

    def get_tile(self, x, y):
        return self.map[y][x] if 0 <= x < len(self.map[0]) and 0 <= y < len(self.map) else None
    

    def generate_map(self):
        self.map = [[Tile(texture=randint(1,2), orientation=Direction(randint(0,3))) for _ in range(50)] for _ in range(50)]
        return self.map

    def draw(self):
        screen_props = []
        for j in range(len(self.map)):
            for i in range(len(self.map[0])):
                tile = self.get_tile(i, j)
                if tile.texture :
                   
                    screen_x, screen_y = self.game.camera.apply((i * self.game.tile_size, j * self.game.tile_size))
                    
                    
                    if -self.game.tile_size <= screen_x <= self.game.current_res[0] and -self.game.tile_size <= screen_y <= self.game.current_res[1]:

                        self.game.screen.blit(self.game.renderer.get_texture(tile), (screen_x, screen_y))
                
                if tile.prop and tile.prop.is_enclosure and tile.enclosure_type is not None:
                    screen_props.append((tile, i, j))
                elif tile.prop and tile.main_prop_tile and not tile.prop.is_enclosure:
                    screen_props.append((tile, i, j))
        
        for tile, i, j in screen_props:
            if tile.prop.is_enclosure:
                enclosure_texture = self.game.renderer.enclosures_textures[tile.enclosure_type.value]
                real_x, real_y = i * self.game.tile_size, j * self.game.tile_size
                screen_x, screen_y = self.game.camera.apply((real_x, real_y))
                self.game.screen.blit(enclosure_texture, (screen_x, screen_y))
            else:
                prop_texture = self.game.renderer.get_prop_texture(tile.prop.name)
                # Convertir les coordonnées de tuiles en pixels
                real_x = tile.prop.x * self.game.tile_size
                real_y = tile.prop.y * self.game.tile_size
                if prop_texture:
                    screen_x, screen_y = self.game.camera.apply((real_x, real_y))
                    self.game.screen.blit(prop_texture, (screen_x, screen_y))
        
        # Dessiner les animaux de tous les enclos
        for enclosure in self.enclosures:
            for animal in enclosure.animals:
                # Obtenir l'animation actuelle (idle ou walk)
                animation = animal.get_current_animation()
                
                # Obtenir la frame actuelle de l'animal
                animal_frame = self.game.renderer.get_animal_frame(
                    animal.species,
                    animation,
                    animal.direction,
                    animal.current_frame
                )
                
                if animal_frame:
                    # Convertir la position de l'animal en pixels
                    real_x = animal.x * self.game.tile_size
                    real_y = animal.y * self.game.tile_size
                    
                    # Appliquer la caméra
                    screen_x, screen_y = self.game.camera.apply((real_x, real_y))
                    
                    # Dessiner l'animal seulement s'il est visible à l'écran
                    if -self.game.tile_size <= screen_x <= self.game.current_res[0] and \
                       -self.game.tile_size <= screen_y <= self.game.current_res[1]:
                        self.game.screen.blit(animal_frame, (screen_x, screen_y))


    def create_prop(self, name, x, y):
        prop = Props(name, x, y)
        self.props.append(prop)
        self.get_tile(x, y).prop = prop
        
        self.get_tile(x, y).main_prop_tile = True
        for i in range(int(self.game.renderer.get_prop_size(name)[0])):
            for j in range(int(self.game.renderer.get_prop_size(name)[1])):
                if not (i == 0 and j == 0):
                    tile = self.get_tile(x + i, y + j)
                    if tile:
                        tile.prop = prop

    def remove_prop(self, prop):
        self.props.remove(prop)
        for i in range(int(self.game.renderer.get_prop_size(prop.name)[0])):
            for j in range(int(self.game.renderer.get_prop_size(prop.name)[1])):
                tile = self.get_tile(prop.x + i, prop.y + j)
                if tile:
                    tile.prop = None
                    tile.main_prop_tile = False

    def create_enclosure(self, x, y, width, height):
        enclosure = Enclosure(x, y, width, height)
        self.enclosures.append(enclosure)

        for i in range(width):
            for j in range(height):
                tile = self.get_tile(x + i, y + j)
                if tile:
                    tile.prop = enclosure
                    tile.is_enclosure = True

                    if i == 0 and j == 0:
                        tile.enclosure_type = EnclosureType.TOP_LEFT
                        tile.main_prop_tile = True
                    elif i == width - 1 and j == 0:
                        tile.enclosure_type = EnclosureType.TOP_RIGHT
                    elif i == 0 and j == height - 1:
                        tile.enclosure_type = EnclosureType.BOTTOM_LEFT
                    elif i == width - 1 and j == height - 1:
                        tile.enclosure_type = EnclosureType.BOTTOM_RIGHT
                    elif j == 0:
                        tile.enclosure_type = EnclosureType.TOP
                    elif j == height - 1:
                        tile.enclosure_type = EnclosureType.BOTTOM
                    elif i == 0:
                        tile.enclosure_type = EnclosureType.LEFT
                    elif i == width - 1:
                        tile.enclosure_type = EnclosureType.RIGHT

    def remove_enclosure(self, enclosure):
        self.enclosures.remove(enclosure)
        for i in range(enclosure.width):
            for j in range(enclosure.height):
                tile = self.get_tile(enclosure.x + i, enclosure.y + j)
                if tile:
                    tile.prop = None
                    tile.is_enclosure = False
                    tile.main_prop_tile = False
                    tile.enclosure_type = None
        
        