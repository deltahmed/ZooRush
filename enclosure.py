from __future__ import annotations
import pygame as pg
import random

from utils import *


class Enclosure(Props):
    def __init__(self, x, y, width: int, height: int) -> None:
        super().__init__("enclosure", x, y, True)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animals = []
        self.is_enclosure = True
        self.max_animals = (width-1) * (height-1) // 4  # Limite du nombre d'animaux dans l'enclos

    def add_animal(self, animal: Animal) -> None:
        if len(self.animals) < self.max_animals:
            self.animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        self.animals.remove(animal)

    def move_animal(self, animal: Animal, new_x: int, new_y: int) -> None:
        if animal in self.animals:
            animal.x = new_x
            animal.y = new_y
    
    def update_animals(self, delta_time: float) -> None:
        """
        Met à jour tous les animaux de l'enclos avec les boundaries appropriées.
        
        Args:
            delta_time: Le temps écoulé depuis la dernière frame (en secondes)
        """
        # Définir les boundaries de l'enclos (avec une petite marge)
        boundaries = (
            self.x + 1,  # min_x
            self.y + 1,  # min_y
            self.x + self.width - 1,  # max_x
            self.y + self.height - 1   # max_y
        )
        
        # Mettre à jour chaque animal avec la liste des autres animaux
        for animal in self.animals:
            other_animals = [a for a in self.animals if a != animal]
            animal.update(delta_time, boundaries, other_animals)





class Animal:
    def __init__(self, species: str, x: float, y: float) -> None:
        self.species = species
        self.x = x  # Position en coordonnées de tuiles (peut être flottant)
        self.y = y
        self.hunger = 100
        self.thirst = 100
        self.happiness = 100
        self.health = 100
        self.direction = Direction.SOUTH
        
        # Variables pour le mouvement aléatoire
        self.speed = 0.8  # tuiles par seconde (vitesse en coordonnées de tuiles)
        self.move_timer = 0  # temps écoulé depuis le dernier changement de direction
        self.move_interval = random.uniform(1.5, 3.0)  # intervalle entre les changements de direction (secondes)
        self.target_x = x
        self.target_y = y
        self.is_idle = False  # True si l'animal est en pause
        self.idle_timer = 0  # temps écoulé en idle
        self.idle_duration = 0  # durée de l'idle actuel
        self.previous_animation = 'walk'  # Pour détecter les changements d'animation
        
        # Variables pour l'animation
        self.animation_timer = 0  # temps écoulé pour l'animation
        self.walk_animation_speed = 0.12  # temps entre chaque frame en marchant (secondes)
        self.idle_animation_speed = 0.25  # temps entre chaque frame en idle (secondes, plus lent)
        self.current_frame = 0  # index de la frame actuelle
        
        # Rayon de collision (en tuiles)
        self.collision_radius = 0.4  # Distance minimale entre animaux
    
    def feed(self, food_amount: int) -> None:
        self.hunger = min(100, self.hunger + food_amount)

    def give_water(self, water_amount: int) -> None:
        self.thirst = min(100, self.thirst + water_amount)

    def play(self, play_time: int) -> None:
        self.happiness = min(100, self.happiness + play_time)

    def heal(self, health_amount: int) -> None:
        self.health = min(100, self.health + health_amount)
    
    def get_current_animation(self) -> str:
        """
        Retourne le nom de l'animation actuelle ('idle' ou 'walk').
        """
        return 'idle' if self.is_idle else 'walk'
    
    def check_collision_with_others(self, new_x: float, new_y: float, other_animals: list) -> bool:
        """
        Vérifie si une position donnerait lieu à une collision avec d'autres animaux.
        
        Args:
            new_x: Position X à tester
            new_y: Position Y à tester
            other_animals: Liste des autres animaux de l'enclos
            
        Returns:
            True s'il y a collision, False sinon
        """
        for other in other_animals:
            # Calculer la distance entre cette position et l'autre animal
            dx = new_x - other.x
            dy = new_y - other.y
            distance = (dx**2 + dy**2)**0.5
            
            # Vérifier si trop proche
            if distance < (self.collision_radius + other.collision_radius):
                return True
        
        return False

    def update(self, delta_time: float, enclosure_boundaries: tuple = None, other_animals: list = None) -> None:
        """Met à jour l'animal : stats, mouvement et animation."""
        # Decrease hunger, thirst, happiness, and health over time
        self.hunger = max(0, self.hunger - 0.1 * delta_time)
        self.thirst = max(0, self.thirst - 0.1 * delta_time)
        self.happiness = max(0, self.happiness - 0.05 * delta_time)
        if self.hunger == 0 or self.thirst == 0:
            self.health = max(0, self.health - 0.2 * delta_time)
        
        # Mouvement aléatoire si les boundaries sont fournies
        if enclosure_boundaries:
            if other_animals is None:
                other_animals = []
            self.random_movement(delta_time, enclosure_boundaries, other_animals)
        
        # Détecter le changement d'animation et réinitialiser la frame si nécessaire
        current_animation = self.get_current_animation()
        if current_animation != self.previous_animation:
            self.current_frame = 0
            self.animation_timer = 0
            self.previous_animation = current_animation
        
        # Mettre à jour l'animation
        # Utiliser une vitesse différente selon l'animation
        current_speed = self.idle_animation_speed if self.is_idle else self.walk_animation_speed
        self.animation_timer += delta_time
        if self.animation_timer >= current_speed:
            self.animation_timer = 0
            self.current_frame += 1

    def random_movement(self, delta_time: float, boundaries: tuple, other_animals: list) -> None:
        """
        Déplace l'animal de manière aléatoire dans les limites de l'enclos.
        
        Args:
            delta_time: Le temps écoulé depuis la dernière frame (en secondes)
            boundaries: Tuple (min_x, min_y, max_x, max_y) définissant les limites de l'enclos en tuiles
            other_animals: Liste des autres animaux de l'enclos pour éviter les collisions
        """
        min_x, min_y, max_x, max_y = boundaries
        
        # Gérer l'état idle
        if self.is_idle:
            self.idle_timer += delta_time
            if self.idle_timer >= self.idle_duration:
                # Fin de l'idle, reprendre le mouvement et choisir une nouvelle cible
                self.is_idle = False
                self.idle_timer = 0
                # Choisir immédiatement une nouvelle cible
                self.target_x = random.uniform(min_x, max_x)
                self.target_y = random.uniform(min_y, max_y)
                self.move_timer = 0
                self.move_interval = random.uniform(1.5, 3.0)
            else:
                # Rester immobile pendant l'idle
                return
        
        # Incrémenter le timer
        self.move_timer += delta_time
        
        # Changer de direction à intervalles aléatoires
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.move_interval = random.uniform(1.5, 3.0)
            
            # 30% de chance d'entrer en idle au lieu de bouger
            if random.random() < 0.3:
                self.is_idle = True
                self.idle_duration = random.uniform(2.0, 4.0)  # Idle pendant 2-4 secondes
                return
            
            # Choisir une nouvelle position cible aléatoire dans les boundaries
            self.target_x = random.uniform(min_x, max_x)
            self.target_y = random.uniform(min_y, max_y)
        
        # Calculer la direction vers la cible
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        # Si on est proche de la cible (moins de 0.1 tuile), passer en idle
        if distance < 0.1:
            if not self.is_idle:
                self.is_idle = True
                self.idle_duration = random.uniform(1.0, 2.5)  # Courte pause avant le prochain mouvement
                self.idle_timer = 0
            return
        
        # Normaliser la direction et appliquer la vitesse avec delta_time
        if distance > 0:
            dx = (dx / distance) * self.speed * delta_time
            dy = (dy / distance) * self.speed * delta_time
            
            # Calculer la nouvelle position
            new_x = self.x + dx
            new_y = self.y + dy
            
            # S'assurer que l'animal reste dans les boundaries
            new_x = stick_in_range(new_x, min_x, max_x)
            new_y = stick_in_range(new_y, min_y, max_y)
            
            # Vérifier les collisions avec les autres animaux
            if not self.check_collision_with_others(new_x, new_y, other_animals):
                # Pas de collision, on peut bouger
                self.x = new_x
                self.y = new_y
            else:
                # Collision détectée, choisir une nouvelle cible
                self.is_idle = True
                self.idle_duration = random.uniform(0.5, 1.5)  # Courte pause
                self.idle_timer = 0
                return
            
            # Mettre à jour la direction visuelle en fonction du mouvement dominant
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.direction = Direction.EAST
                else:
                    self.direction = Direction.WEST
            else:
                if dy > 0:
                    self.direction = Direction.SOUTH
                else:
                    self.direction = Direction.NORTH
