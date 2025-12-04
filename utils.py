from __future__ import annotations
import pygame as pg
from random import randint
from enum import Enum
from dataclasses import dataclass

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


class EnclosureType(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    TOP_LEFT = 4
    TOP_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_RIGHT = 7


@dataclass
class Tile:
    texture: int = None
    orientation: Direction = Direction.NORTH
    prop: object = None
    main_prop_tile: bool = False
    is_enclosure: bool = False
    enclosure_type: EnclosureType = None

@dataclass
class Props:
    name: str
    x: int
    y: int
    is_enclosure: bool = False



def stick_in_range(value, min_value, max_value):
    return max(min(value, max_value), min_value)