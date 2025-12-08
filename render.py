from __future__ import annotations
import pygame as pg
import os
from random import randint

from utils import *
from config import *


class Renderer:
    """
    main rendering class that handles all visual assets loading and management
    this class is responsible for tiles, props, enclosures and animal animations
    """
    
    def __init__(self,game) -> None:
        """
        initialize the renderer with game instance and load all visual resources
        
        args:
            game: main game instance containing tile size and other config
        """
        self.game = game
        self.props = {}  # dictionary to store prop textures
        self.props_sizes = PROPS_SIZES  # size mapping for each prop
        self.animals = {}  # stores all animal animation frames organized by type and direction
        
        # load all visual assets during initialization
        self.load_tiles()
        self.load_props()
        self.load_enclosures()
        self.load_animals()
        

    def load_image(self, image_path):
        """
        load a single image file with alpha channel support
        returns a green placeholder surface if loading fails
        
        args:
            image_path: path to the image file
            
        returns:
            pygame surface with the loaded image or a placeholder
        """
        try:
            # load with alpha support and avoid unnecessary pixel format conversions
            tile_image = pg.image.load(image_path).convert_alpha()
    
        except:
            # fallback to a simple colored square if image cant be loaded
            tile_image = pg.Surface((self.game.tile_size, self.game.tile_size))
            tile_image.fill('green')
        return tile_image
    
    def load_tiles(self):
        """
        load all ground tiles from the media/tiles directory
        each tile is loaded with 4 rotations (0, 90, 180, 270 degrees)
        tiles must be numbered sequentially starting from 1
        """
        self.tiles = []
        # sort files to ensure correct order based on numeric names
        files = sorted(os.listdir('media/tiles'), key=lambda x: int(x.split('.')[0]))
        tiles_count = 1
        for file in files:
            try:
                if not (int(file.split('.')[0]) == tiles_count)  :
                    raise ValueError("tile file name must be an integer representing the tile ID")
                # load original image and then scale smoothly to the game's tile size
                img = self.load_image(os.path.join('media/tiles', file))
                tile_image = pg.transform.scale(img, (self.game.tile_size, self.game.tile_size))
                # store the tile with all 4 rotation variants for flexibility
                self.tiles.append((tile_image, pg.transform.rotate(tile_image, 90), pg.transform.rotate(tile_image, 180), pg.transform.rotate(tile_image, 270)))
            except Exception as e:
                raise RuntimeError(f"failed to load tile image {file}: {e}")
            tiles_count += 1

    def load_props(self):
        """
        load all decorative props from media/props directory
        each prop is scaled while preserving its aspect ratio to fit within
        its designated tile space defined in PROPS_SIZES configuration
        """
        for file in os.listdir('media/props'):
            try:
                img = self.load_image(os.path.join('media/props', file))
                # calculate target size based on number of tiles this prop occupies
                target_width = self.props_sizes[file.split('.')[0]][0] * self.game.tile_size
                target_height = self.props_sizes[file.split('.')[0]][1] * self.game.tile_size
                
                # get original image dimensions to calculate aspect ratio
                original_width, original_height = img.get_size()
                original_aspect_ratio = original_width / original_height
                target_aspect_ratio = target_width / target_height
                
                # calculate new dimensions while preserving aspect ratio
                # ensure the image fits within the target area
                if original_aspect_ratio > target_aspect_ratio:
                    # image is wider, limit by width
                    new_width = target_width
                    new_height = int(target_width / original_aspect_ratio)
                else:
                    # image is taller, limit by height
                    new_height = target_height
                    new_width = int(target_height * original_aspect_ratio)
                
                # resize while maintaining aspect ratio
                tile_image = pg.transform.scale(img, (new_width, new_height))
                self.props[file.split('.')[0]] = tile_image
            except Exception as e:
                raise RuntimeError(f"failed to load prop image {file}: {e}")
    
    def get_prop_texture(self, name):
        """
        retrieve a prop texture by its name
        
        args:
            name: string identifier of the prop
            
        returns:
            pygame surface of the prop or none if not found
        """
        try :
            return self.props[name]
        except KeyError:
            # return none if the requested prop doesn't exist
            return None
        
    def get_prop_size(self, name):
        """
        get the size in tiles of a specific prop
        
        args:
            name: string identifier of the prop
            
        returns:
            tuple (width, height) in tiles, or (0, 0) if not found
        """
        try :
            prop_size = self.props_sizes[name]
            return prop_size
        except KeyError:
            # return zero size if prop size is not configured
            return (0, 0)

    def load_spritesheet(self, path, frame_width, frame_height):
        """
        load a spritesheet and split it into individual frames
        divides the sheet into equal-sized frames based on provided dimensions
        
        args:
            path: file path to the spritesheet image
            frame_width: width of each individual frame in pixels
            frame_height: height of each individual frame in pixels
            
        returns:
            list of pygame surfaces, each containing one frame
        """
        try :
            sheet = pg.image.load(path).convert_alpha()
            sheet_width, sheet_height = sheet.get_size()

            frames = []
            # iterate through the sheet row by row, column by column
            for y in range(0, sheet_height, frame_height):
                for x in range(0, sheet_width, frame_width):
                    # extract each frame as a subsurface
                    frame = sheet.subsurface((x, y, frame_width, frame_height))
                    frames.append(frame)
            return frames
        except Exception as e:
            raise RuntimeError(f"failed to load spritesheet {path}: {e}")


    def get_texture(self, tile: Tile):
        """
        get the appropriate texture for a tile based on its type and orientation
        
        args:
            tile: tile object containing texture id and orientation
            
        returns:
            pygame surface with the correctly rotated texture, or 0 if not found
        """
        try :
            # texture id is 1-indexed, list is 0-indexed
            return self.tiles[tile.texture-1][tile.orientation.value]
        except IndexError:
            # return 0 as fallback if texture index is out of range
            return 0

    def load_enclosures(self):
        """
        load all enclosure fence textures from media/custom_enclosures
        enclosures are numbered from 0-7 representing diferent fence orientations
        (top, bottom, left, right, and corner pieces)
        """
        self.enclosures_textures = []
        # sort files to ensure correct order (0.png = TOP, 1.png = BOTTOM, etc.)
        files = sorted(os.listdir('media/custom_enclosures'), key=lambda x: int(x.split('.')[0]))
        enclosure_count = 0
        for file in files:
            try:
                if not (int(file.split('.')[0]) == enclosure_count)  :
                    raise ValueError("enclosure file name must be an integer representing the enclosure ID")
                img = self.load_image(os.path.join('media/custom_enclosures', file))
                tile_image = pg.transform.scale(img, (self.game.tile_size, self.game.tile_size))
                # store as a single image, rotations are handled by using different files
                self.enclosures_textures.append(tile_image)
            except Exception as e:
                raise RuntimeError(f"failed to load enclosure image {file}: {e}")
            enclosure_count += 1

    def load_animals(self):
        """
        load all animal spritesheets from media/animals/ directory
        uses configuration from ANIMAL_SPRITES_CONFIG to determine the structure
        of each spritesheet (number of frames per direction and animation type)
        
        each animal has idle and walk animations for all four cardinal directions
        the frames are organized in a grid where each row represents a specific
        animation state and direction combination
        """
        animals_dir = 'media/animals'
        if not os.path.exists(animals_dir):
            raise RuntimeError(f"the animals directory {animals_dir} does not exist")
        
        # iterate through each animal folder
        for animal_name in os.listdir(animals_dir):
            animal_path = os.path.join(animals_dir, animal_name)
            if not os.path.isdir(animal_path):
                continue
            
            # check if the animal is properly configured
            if animal_name not in ANIMAL_SPRITES_CONFIG:
                print(f"⚠️ animal '{animal_name}' not configured in animal_config.py - skipped")
                continue
            
            # find the spritesheet file in the animal's folder
            spritesheet_file = None
            for file in os.listdir(animal_path):
                if file.endswith('.png'):
                    spritesheet_file = os.path.join(animal_path, file)
                    break
            
            if not spritesheet_file:
                raise RuntimeError(f"no spritesheet found for {animal_name}")
            
            try:
                # load the complete spritesheet image
                sheet = pg.image.load(spritesheet_file).convert_alpha()
                sheet_width, sheet_height = sheet.get_size()
                
                # get the configuration for this specific animal
                config = ANIMAL_SPRITES_CONFIG[animal_name]
                
                # calculate the height of one row and width of one frame
                # we need to find the maximum number of rows AND frames
                max_row = 0
                max_frames = 0
                for animation in ['walk', 'idle']:
                    for direction in [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]:
                        row_num, num_frames = config[animation][direction]
                        max_row = max(max_row, row_num)
                        max_frames = max(max_frames, num_frames)
                
                # calculate individual frame dimensions
                frame_height = sheet_height // max_row
                frame_width = sheet_width // max_frames
                
                # dictionary to store animations for this animal
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
                
                # load animations according to configuration
                for animation in ['walk', 'idle']:
                    for direction in [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]:
                        row_num, num_frames = config[animation][direction]
                        
                        # calculate Y position of the row (row 1 = index 0)
                        y = (row_num - 1) * frame_height
                        
                        # extract each frame from the row
                        for frame_num in range(num_frames):
                            x = frame_num * frame_width
                            frame = sheet.subsurface((x, y, frame_width, frame_height))
                            # resize to match game's tile size
                            scaled_frame = pg.transform.scale(frame, (self.game.tile_size, self.game.tile_size))
                            animal_animations[animation][direction].append(scaled_frame)
                
                # store the complete animation set for this animal
                self.animals[animal_name] = animal_animations
                
                
            except Exception as e:
                raise RuntimeError(f"failed to load animal {animal_name}: {e}")
    
    def get_animal_frame(self, animal_name: str, animation: str, direction: Direction, frame_index: int):
        """
        retrieve a specific animation frame for an animal
        handles frame index wrapping so animations loop seamlessly
        
        args:
            animal_name: name of the animal (eg 'sheep', 'rooster', 'piglet')
            animation: type of animation ('idle' or 'walk')
            direction: cardinal direction (Direction.NORTH, SOUTH, WEST, EAST)
            frame_index: index of the frame in the animation sequence
            
        returns:
            pygame surface containing the requested frame, or none if not found
        """
        try:
            frames = self.animals[animal_name][animation][direction]
            # wrap the index if it exceeds the number of frames available
            frame_index = frame_index % len(frames)
            return frames[frame_index]
        except (KeyError, IndexError):
            # return none if animal, animation or direction doesn't exist
            return None