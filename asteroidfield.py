# Import required modules
import pygame
pygame.init()
import constants
import gamestate
import random
import asteroids


class AsteroidField(pygame.sprite.Sprite):
    containers = constants.ASTEROID_FIELD_CONTAINERS # Set the container for the asteroid field sprite
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-gamestate.asteroid_max_radius, y * constants.SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                constants.SCREEN_WIDTH + gamestate.asteroid_max_radius, y * constants.SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * constants.SCREEN_WIDTH, -gamestate.asteroid_max_radius),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT + gamestate.asteroid_max_radius
            ),
        ],
    ]

    def __init__(self):
        self.containers = constants.ASTEROID_FIELD_CONTAINERS # Set the container for the asteroid field sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        #print(f"Debug: spawned asteroid at {position.x}, {position.y} with radius {radius}")
        asteroid = asteroids.Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        #print(f"Debug: asfield spawn timer {self.spawn_timer}")
        self.spawn_timer += dt
        #print(f"Debug: asfield spawn timer {self.spawn_timer}")
        if self.spawn_timer > gamestate.asteroid_spawn_rate:
            #print(f"Debug: entered spawn timer if statement")
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, gamestate.asteroid_kinds)
            self.spawn(gamestate.asteroid_min_radius * kind, position, velocity)
            #print(f"Debug: if-statement asteroid spawned at {position.x}, {position.y} with radius {gamestate.asteroid_min_radius * kind}")