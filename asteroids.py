# Import required modules
import pygame
pygame.init()
import constants
import circleshape
import random
import soundeffects






# Create the Asteroid class, parent is CircleShape
class Asteroid(circleshape.CircleShape):
    containers = constants.ASTEROID_CONTAINERS  # Set the container for the asteroid sprite
    def __init__(self, x, y, radius):  #initialize
        self.containers = constants.ASTEROID_CONTAINERS  # Set the container for the asteroid sprite
        super().__init__(x,y,radius)  #initialize parent CircleShape - Required to draw and update asteroids!
        self.x = x
        self.y = y
        self.radius = radius
        self.lifespan = constants.ASTEROID_LIFESPAN
        self.position = pygame.Vector2(self.x,self.y)

    def draw(self,screen,color):
        self.color = color
        pygame.draw.circle(screen,self.color,(self.position.x,self.position.y),self.radius,width=2)
        #print(f"Debug: draw asteroid")
    
    def update(self,dt):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.lifespan -= dt
        if self.lifespan <= 0:
            self.kill()

    def split(self):
        self.kill()
        soundeffects.play_soundeffect("boom.mp3",0.6,1500)
        if self.radius <= constants.ASTEROID_MIN_RADIUS:
            return
        angle = random.uniform(20,50)
        asteroid_a_angle = self.velocity.rotate(angle)
        asteroid_b_angle = self.velocity.rotate(-angle)
        new_radius = self.radius - constants.ASTEROID_MIN_RADIUS
        asteroid_a = Asteroid(self.position.x,self.position.y,new_radius)
        asteroid_b = Asteroid(self.position.x,self.position.y,new_radius)
        asteroid_a_scale = asteroid_a_angle * constants.ASTEROID_VELOCITY_MULTIPLIER
        asteroid_b_scale = asteroid_b_angle * constants.ASTEROID_VELOCITY_MULTIPLIER
        asteroid_a.velocity = pygame.Vector2(asteroid_a_scale)
        asteroid_b.velocity = pygame.Vector2(asteroid_b_scale)