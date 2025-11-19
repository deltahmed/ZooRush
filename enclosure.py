import pygame

from animal import Animal


def scale_to_max(image: pygame.Surface, max_size: int):
    width, height = image.get_size()

    # si rien ne dépasse, on retourne tel quel
    if width <= max_size and height <= max_size:
        return image

    # déterminer le facteur d’échelle
    scale_factor = max_size / max(width, height)

    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # resize proportionnel
    return pygame.transform.smoothscale(image, (new_width, new_height))


class Enclosure:
    def __init__(self, game, x, y, animals: list[Animal] = None, size=3):
        self.game = game
        self.size = size # nombre de cases de l’enclos
        self.x = x
        self.y = y
        self.animals = animals or []

        # --- Chargement et resize des clôtures ---
        self.fence_horizontal_image = pygame.image.load("h_fence.png").convert_alpha()
        self.fence_horizontal_image = scale_to_max(self.fence_horizontal_image, game.tile_size)

        self.fence_vertical_image = pygame.image.load("v_fence.png").convert_alpha()
        self.fence_vertical_image = scale_to_max(self.fence_vertical_image, game.tile_size)

        # Taille réelle des images (pour corriger le placement)
        self.h_w, self.h_h = self.fence_horizontal_image.get_size()
        self.v_w, self.v_h = self.fence_vertical_image.get_size()

    def draw(self, debug=False):
        screen = self.game.screen
        tile = self.game.tile_size

        # Position pixel initiale (convertie via camera)
        start_px, start_py = self.game.camera.apply((self.x * tile, self.y * tile))

        # --- Top horizontal ---
        for i in range(self.size):
            px = start_px + i * self.h_w
            py = start_py
            rect = pygame.Rect(px, py, self.h_w, self.h_h)
            screen.blit(self.fence_horizontal_image, rect)
            if debug:
                pygame.draw.rect(screen, (0, 255, 0), rect, 1)

        # --- Vertical left ---
        for j in range(self.size):
            px = start_px
            py = start_py + j * self.v_h
            rect = pygame.Rect(px, py, self.v_w, self.v_h)
            screen.blit(self.fence_vertical_image, rect)
            if debug:
                pygame.draw.rect(screen, (255, 0, 0), rect, 1)

        # --- Vertical right ---
        for j in range(self.size):
            px = start_px + self.size * self.h_w - self.v_w
            py = start_py + j * self.v_h
            rect = pygame.Rect(px, py, self.v_w, self.v_h)
            screen.blit(self.fence_vertical_image, rect)
            if debug:
                pygame.draw.rect(screen, (255, 0, 0), rect, 1)

        # --- Bottom horizontal ---
        bottom_y = start_py + self.size * self.v_h - self.h_h
        for i in range(self.size):
            px = start_px + i * self.h_w
            rect = pygame.Rect(px, bottom_y, self.h_w, self.h_h)
            screen.blit(self.fence_horizontal_image, rect)
            if debug:
                pygame.draw.rect(screen, (0, 0, 255), rect, 1)

    def update_animals(self):
        for animal in self.animals:
            animal.update()

    def draw_animals(self):
        for animal in self.animals:
            animal.draw()