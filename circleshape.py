# This module will house the CircleShape class
# This class will be used to create shapes for game objects

# import the required modules
import pygame
pygame.init()

# This is where we define the CircleShape class
class CircleShape(pygame.sprite.Sprite):
    # Constructor for the CircleShape class
    def __init__(self, x, y, radius):  
        
        # This initializes the Sprite containers and is required to draw and update
        if hasattr(self, "containers"):  # check if the class has containers attribute
            super().__init__(self.containers) # call the parent constructor with containers
        else:
            super().__init__() # call the parent constructor without containers

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen,color):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    #lets define a method to detect collisions
    def collision(self,other):
        distance = self.position.distance_to(other.position) #distance to the other obj
        rad = self.radius + other.radius #combined radius of the circles of both obj's
        return distance <= rad