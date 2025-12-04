from __future__ import annotations
import pygame as pg

from utils import *
from enclosure import *


class HUD_Enum(Enum):
    Escape = 0
    Inventory = 1
    Market = 2
    MOOD = 3


class HUD:
    def __init__(self,game) -> None:
        self.game = game

        self.hud = 0


    def load_hud_textures(self):
        pass


    def draw(self):
        pass