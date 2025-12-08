from __future__ import annotations
import pygame as pg
import random

from utils import *


class Enclosure(Props):
    """
    represents an enclosure that can contain multiple animals
    handles animal movement boundaries and capacity limits
    """
    
    def __init__(self, x, y, width: int, height: int) -> None:
        super().__init__("enclosure", x, y, True)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animals = []
        self.is_enclosure = True
        # calculate max capacity based on enclosure size (4 tiles per animal)
        self.max_animals = (width-1) * (height-1) // 4

    def add_animal(self, animal: Animal) -> None:
        """adds an animal to the enclosure if theres space available"""
        if len(self.animals) < self.max_animals:
            self.animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        """removes an animal from the enclosure"""
        self.animals.remove(animal)

    def move_animal(self, animal: Animal, new_x: int, new_y: int) -> None:
        """moves an animal to a new position within the enclosure"""
        if animal in self.animals:
            animal.x = new_x
            animal.y = new_y
    
    def update_animals(self, delta_time: float) -> None:
        """
        updates all animals in the enclosure with proper boundaries
        also handles collision detection between animals
        
        args:
            delta_time: time elapsed since last frame in seconds
        """
        # define enclosure boundaries with small margin to keep animals inside
        boundaries = (
            self.x + 1,  # min_x
            self.y + 1,  # min_y
            self.x + self.width - 1,  # max_x
            self.y + self.height - 1   # max_y
        )
        
        # update each animal with list of other animals for colision avoidance
        for animal in self.animals:
            other_animals = [a for a in self.animals if a != animal]
            animal.update(delta_time, boundaries, other_animals)





class Animal:
    """
    represents an animal in the game with stats, movement and animation
    animals move randomly within enclosure boundaries and avoid colliding with each other
    """
    
    def __init__(self, species: str, x: float, y: float) -> None:
        self.species = species
        # position in tile coordinates (can be floating point for smooth movement)
        self.x = x
        self.y = y
        
        # animal stats that decrease over time
        self.hunger = 100
        self.thirst = 100
        self.happiness = 100
        self.health = 100
        
        self.direction = Direction.SOUTH
        
        # random movement variables
        self.speed = 0.8  # tiles per second
        self.move_timer = 0  # time since last direction change
        self.move_interval = random.uniform(1.5, 3.0)  # interval between direction changes
        self.target_x = x
        self.target_y = y
        
        # idle state variables
        self.is_idle = False  # true when animal is paused
        self.idle_timer = 0  # time spent idle
        self.idle_duration = 0  # duration of current idle period
        self.previous_animation = 'walk'  # track animation changes
        
        # animation variables
        self.animation_timer = 0  # elapsed time for animation
        self.walk_animation_speed = 0.12  # time between frames when walking
        self.idle_animation_speed = 0.25  # time between frames when idle (slower)
        self.current_frame = 0  # current frame index
        
        # collision radius in tiles (minimum distance between animals)
        self.collision_radius = 0.4
    
    def feed(self, food_amount: int) -> None:
        """increase hunger stat by given amount (capped at 100)"""
        self.hunger = min(100, self.hunger + food_amount)

    def give_water(self, water_amount: int) -> None:
        """increase thirst stat by given amount (capped at 100)"""
        self.thirst = min(100, self.thirst + water_amount)

    def play(self, play_time: int) -> None:
        """increase happiness stat by given amount (capped at 100)"""
        self.happiness = min(100, self.happiness + play_time)

    def heal(self, health_amount: int) -> None:
        """increase health stat by given amount (capped at 100)"""
        self.health = min(100, self.health + health_amount)
    
    def get_current_animation(self) -> str:
        """returns the name of current animation (idle or walk)"""
        return 'idle' if self.is_idle else 'walk'
    
    def check_collision_with_others(self, new_x: float, new_y: float, other_animals: list) -> bool:
        """
        checks if a position would cause collision with other animals
        uses collision radius to determine if animals are too close
        
        args:
            new_x: x position to test
            new_y: y position to test
            other_animals: list of other animals in enclosure
            
        returns:
            true if collision detected, false otherwise
        """
        for other in other_animals:
            # calculate distance between this position and other animal
            dx = new_x - other.x
            dy = new_y - other.y
            distance = (dx**2 + dy**2)**0.5
            
            # check if too close (collision detected)
            if distance < (self.collision_radius + other.collision_radius):
                return True
        
        return False

    def update(self, delta_time: float, enclosure_boundaries: tuple = None, other_animals: list = None) -> None:
        """
        updates animal stats, movement and animation each frame
        handles stat degradation and health loss when hungry or thirsty
        """
        # decrease all stats over time
        self.hunger = max(0, self.hunger - 0.1 * delta_time)
        self.thirst = max(0, self.thirst - 0.1 * delta_time)
        self.happiness = max(0, self.happiness - 0.05 * delta_time)
        
        # health decreases if animal is hungry or thirsty
        if self.hunger == 0 or self.thirst == 0:
            self.health = max(0, self.health - 0.2 * delta_time)
        
        # random movement if boundaries are provided
        if enclosure_boundaries:
            if other_animals is None:
                other_animals = []
            self.random_movement(delta_time, enclosure_boundaries, other_animals)
        
        # detect animation change and reset frame if necessary
        current_animation = self.get_current_animation()
        if current_animation != self.previous_animation:
            self.current_frame = 0
            self.animation_timer = 0
            self.previous_animation = current_animation
        
        # update animation frame based on current state
        current_speed = self.idle_animation_speed if self.is_idle else self.walk_animation_speed
        self.animation_timer += delta_time
        if self.animation_timer >= current_speed:
            self.animation_timer = 0
            self.current_frame += 1

    def random_movement(self, delta_time: float, boundaries: tuple, other_animals: list) -> None:
        """
        moves animal randomly within enclosure boundaries
        handles idle periods, target selection and collision avoidance
        
        args:
            delta_time: time elapsed since last frame in seconds
            boundaries: tuple (min_x, min_y, max_x, max_y) defining enclosure limits in tiles
            other_animals: list of other animals in enclosure to avoid collisions
        """
        min_x, min_y, max_x, max_y = boundaries
        
        # handle idle state (animal standing still)
        if self.is_idle:
            self.idle_timer += delta_time
            if self.idle_timer >= self.idle_duration:
                # end idle, resume movement and choose new target
                self.is_idle = False
                self.idle_timer = 0
                # immediately choose new target position
                self.target_x = random.uniform(min_x, max_x)
                self.target_y = random.uniform(min_y, max_y)
                self.move_timer = 0
                self.move_interval = random.uniform(1.5, 3.0)
            else:
                # stay still during idle period
                return
        
        # increment movement timer
        self.move_timer += delta_time
        
        # change direction at random intervals
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.move_interval = random.uniform(1.5, 3.0)
            
            # 30% chance to enter idle instead of moving
            if random.random() < 0.3:
                self.is_idle = True
                self.idle_duration = random.uniform(2.0, 4.0)  # idle for 2-4 seconds
                return
            
            # choose new random target position within boundaries
            self.target_x = random.uniform(min_x, max_x)
            self.target_y = random.uniform(min_y, max_y)
        
        # calculate direction towards target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx**2 + dy**2)**0.5
        
        # if close to target (less than 0.1 tile), enter idle state
        if distance < 0.1:
            if not self.is_idle:
                self.is_idle = True
                self.idle_duration = random.uniform(1.0, 2.5)  # short pause before next movement
                self.idle_timer = 0
            return
        
        # normalize direction and apply speed with delta_time
        if distance > 0:
            dx = (dx / distance) * self.speed * delta_time
            dy = (dy / distance) * self.speed * delta_time
            
            # calculate new position
            new_x = self.x + dx
            new_y = self.y + dy
            
            # ensure animal stays within boundaries
            new_x = stick_in_range(new_x, min_x, max_x)
            new_y = stick_in_range(new_y, min_y, max_y)
            
            # check collisions with other animals
            if not self.check_collision_with_others(new_x, new_y, other_animals):
                # no collision, we can move
                self.x = new_x
                self.y = new_y
            else:
                # collision detected, choose new target after short pause
                self.is_idle = True
                self.idle_duration = random.uniform(0.5, 1.5)  # short pause
                self.idle_timer = 0
                return
            
            # update visual direction based on dominant movement axis
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
