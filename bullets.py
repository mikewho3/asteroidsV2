# Import required modules
import circleshape
import constants
import pygame


# Create the Shot Class - parent is CircleShape
class Shot(circleshape.CircleShape):
    
    def __init__(self, x, y, radius):  #initialize
        self.containers = constants.BULLET_CONTAINERS  # Set the container for the shot sprite
        super().__init__(x,y,radius)  #initialize parent CircleShape - Required to draw and update asteroids!
        self.x = x
        self.y = y
        self.position = pygame.Vector2(self.x,self.y)
        self.radius = radius
        self.lifespan = constants.SHOT_LIFESPAN


    def draw(self,screen,color):
        self.color = color
        pygame.draw.circle(screen,self.color,(self.position.x,self.position.y),self.radius,width=2)
    
    def update(self,dt):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.lifespan -= dt
        if self.lifespan <=0:
            self.kill()