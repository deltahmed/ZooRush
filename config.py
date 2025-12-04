"""
Configuration des spritesheets des animaux.
Format:
{
    'nom_animal': {
        'walk': {
            Direction.SOUTH: (ligne, nombre_frames),
            Direction.NORTH: (ligne, nombre_frames),
            Direction.EAST: (ligne, nombre_frames),
            Direction.WEST: (ligne, nombre_frames)
        },
        'idle': {
            Direction.SOUTH: (ligne, nombre_frames),
            Direction.NORTH: (ligne, nombre_frames),
            Direction.EAST: (ligne, nombre_frames),
            Direction.WEST: (ligne, nombre_frames)
        }
    }
}

Note: Les numéros de ligne commencent à 1 (premier ligne = 1)
"""

from utils import Direction

ANIMAL_SPRITES_CONFIG = {
    'rooster': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 6),
            Direction.NORTH: (6, 6),
            Direction.EAST: (8, 6),
            Direction.WEST: (7, 6)
        }
    },
    'sheep': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 4),
            Direction.NORTH: (6, 4),
            Direction.EAST: (7, 4),
            Direction.WEST: (8, 4)
        }
    }
}


PROPS_SIZES = {
    "well": (1, 1),
    "test": (3, 3)
}