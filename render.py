from __future__ import annotations
import pygame as pg
import os
from random import randint

from utils import *
from config import *


class Renderer:
    def __init__(self,game) -> None:
        self.game = game
        self.props = {}
        self.props_sizes = PROPS_SIZES
        self.animals = {}  # Dictionnaire pour stocker les animations des animaux
        
        self.load_tiles()
        self.load_props()
        self.load_enclosures()
        self.load_animals()

    def load_image(self, image_path):
        try:
            # load with alpha support and avoid unnecessary pixel format conversions
            tile_image = pg.image.load(image_path).convert_alpha()
    
        except:
            tile_image = pg.Surface((self.game.tile_size, self.game.tile_size))
            tile_image.fill('green')
        return tile_image
    
    def load_tiles(self):
        self.tiles = []
        # Sort files to ensure correct order
        files = sorted(os.listdir('media/tiles'), key=lambda x: int(x.split('.')[0]))
        tiles_count = 1
        for file in files:
            try:
                if not (int(file.split('.')[0]) == tiles_count)  :
                    raise ValueError("Le nom du fichier doit être un entier représentant l'ID de la tuile.")
                # Load original image and then scale smoothly to the game's tile size
                img = self.load_image(os.path.join('media/tiles', file))
                tile_image = pg.transform.scale(img, (self.game.tile_size, self.game.tile_size))
                self.tiles.append((tile_image, pg.transform.rotate(tile_image, 90), pg.transform.rotate(tile_image, 180), pg.transform.rotate(tile_image, 270)))
            except Exception as e:
                print(f"Erreur de chargement de l'image {file}: {e}")
                self.game.quit()
            tiles_count += 1

    def load_props(self):
        for file in os.listdir('media/props'):
            try:
                img = self.load_image(os.path.join('media/props', file))
                target_size = (self.props_sizes[file.split('.')[0]][0] * self.game.tile_size, self.props_sizes[file.split('.')[0]][1] * self.game.tile_size)
                # Use scale for better quality when resizing
                tile_image = pg.transform.scale(img, target_size)
                self.props[file.split('.')[0]] = tile_image
            except Exception as e:
                print(f"Erreur de chargement de l'image {file}: {e}")
                self.game.quit()
    
    def get_prop_texture(self, name):
        try :
            return self.props[name]
        except KeyError:
            return None
        
    def get_prop_size(self, name):
        try :
            prop_size = self.props_sizes[name]
            return prop_size
        except KeyError:
            return (0, 0)

    def load_spritesheet(self, path, frame_width, frame_height):
        try :
            sheet = pg.image.load(path).convert_alpha()
            sheet_width, sheet_height = sheet.get_size()

            frames = []
            for y in range(0, sheet_height, frame_height):
                for x in range(0, sheet_width, frame_width):
                    frame = sheet.subsurface((x, y, frame_width, frame_height))
                    frames.append(frame)
            return frames
        except Exception as e:
            print(f"Erreur de chargement de l'image {path}: {e}")
            self.game.quit()


    def get_texture(self, tile: Tile):
        try :
            return self.tiles[tile.texture-1][tile.orientation.value]
        except IndexError:
            return 0

    def load_enclosures(self):
        self.enclosures_textures = []
        # Sort files to ensure correct order (0.png = TOP, 1.png = BOTTOM, etc.)
        files = sorted(os.listdir('media/custom_enclosures'), key=lambda x: int(x.split('.')[0]))
        enclosure_count = 0
        for file in files:
            try:
                if not (int(file.split('.')[0]) == enclosure_count)  :
                    raise ValueError("Le nom du fichier doit être un entier représentant l'ID de l'enclosure.")
                img = self.load_image(os.path.join('media/custom_enclosures', file))
                tile_image = pg.transform.scale(img, (self.game.tile_size, self.game.tile_size))
                # Store as a single image, not a tuple with rotations
                self.enclosures_textures.append(tile_image)
            except Exception as e:
                print(f"Erreur de chargement de l'image {file}: {e}")
                self.game.quit()
            enclosure_count += 1

    def load_animals(self):
        """
        Charge les spritesheets des animaux depuis media/animals/
        Utilise la configuration dans animal_config.py pour déterminer la structure
        de chaque spritesheet (nombre de frames par direction et animation).
        """
        animals_dir = 'media/animals'
        if not os.path.exists(animals_dir):
            print(f"Le dossier {animals_dir} n'existe pas")
            return
        
        for animal_name in os.listdir(animals_dir):
            animal_path = os.path.join(animals_dir, animal_name)
            if not os.path.isdir(animal_path):
                continue
            
            # Vérifier si l'animal est configuré
            if animal_name not in ANIMAL_SPRITES_CONFIG:
                print(f"⚠️ Animal '{animal_name}' non configuré dans animal_config.py - ignoré")
                continue
            
            # Chercher le fichier spritesheet dans le dossier de l'animal
            spritesheet_file = None
            for file in os.listdir(animal_path):
                if file.endswith('.png'):
                    spritesheet_file = os.path.join(animal_path, file)
                    break
            
            if not spritesheet_file:
                print(f"Aucun spritesheet trouvé pour {animal_name}")
                continue
            
            try:
                # Charger l'image complète
                sheet = pg.image.load(spritesheet_file).convert_alpha()
                sheet_width, sheet_height = sheet.get_size()
                
                # Récupérer la configuration de l'animal
                config = ANIMAL_SPRITES_CONFIG[animal_name]
                
                # Calculer la hauteur d'une ligne et la largeur d'une frame
                # On doit trouver le nombre maximum de lignes ET de frames
                max_row = 0
                max_frames = 0
                for animation in ['walk', 'idle']:
                    for direction in [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]:
                        row_num, num_frames = config[animation][direction]
                        max_row = max(max_row, row_num)
                        max_frames = max(max_frames, num_frames)
                
                frame_height = sheet_height // max_row
                frame_width = sheet_width // max_frames
                
                # Dictionnaire pour stocker les animations de cet animal
                animal_animations = {
                    'idle': {
                        Direction.NORTH: [],
                        Direction.SOUTH: [],
                        Direction.WEST: [],
                        Direction.EAST: []
                    },
                    'walk': {
                        Direction.NORTH: [],
                        Direction.SOUTH: [],
                        Direction.WEST: [],
                        Direction.EAST: []
                    }
                }
                
                # Charger les animations selon la configuration
                for animation in ['walk', 'idle']:
                    for direction in [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]:
                        row_num, num_frames = config[animation][direction]
                        
                        # Position Y de la ligne (ligne 1 = index 0)
                        y = (row_num - 1) * frame_height
                        
                        # Extraire chaque frame de la ligne
                        for frame_num in range(num_frames):
                            x = frame_num * frame_width
                            frame = sheet.subsurface((x, y, frame_width, frame_height))
                            # Redimensionner à la taille des tiles du jeu
                            scaled_frame = pg.transform.scale(frame, (self.game.tile_size, self.game.tile_size))
                            animal_animations[animation][direction].append(scaled_frame)
                
                self.animals[animal_name] = animal_animations
                
                
            except Exception as e:
                print(f"Erreur de chargement de l'animal {animal_name}: {e}")
                import traceback
                traceback.print_exc()
                continue
    
    def get_animal_frame(self, animal_name: str, animation: str, direction: Direction, frame_index: int):
        """
        Récupère une frame spécifique d'animation d'un animal.
        
        Args:
            animal_name: Nom de l'animal (ex: 'sheep', 'rooster')
            animation: Type d'animation ('idle' ou 'walk')
            direction: Direction (Direction.NORTH, SOUTH, WEST, EAST)
            frame_index: Index de la frame dans l'animation
            
        Returns:
            Surface pygame de la frame, ou None si non trouvée
        """
        try:
            frames = self.animals[animal_name][animation][direction]
            # Boucler l'index si nécessaire
            frame_index = frame_index % len(frames)
            return frames[frame_index]
        except (KeyError, IndexError):
            return None