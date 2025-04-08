# This will be where we define the Player class
# This class will be used to create the player object

#import required modules
import pygame
import circleshape
import constants
import bullets
import soundeffects
import gamestate

# This file will contain the player class, variables, and create_ship() function

#Create the Player Class - parent is CircleShape
class Player(circleshape.CircleShape):
    def __init__(self,x,y):  #initialize
        self.containers = constants.PLAYER_CONTAINERS # Set the container for the player sprite
        super().__init__(x,y,constants.PLAYER_RADIUS)  #call parent initialize - required for draw/update

        # Player Ship Direction
        self.rotation = 0
        # Player Bullet Variables
        self.shot_timer = 0
        self.shot_timer_bypass = 0
        # Player Ship Death Timer (locks controls while dead)
        self.dead_timer = 0
        # Player Ship Starting Lives
        self.lives = constants.PLAYER_STARTING_LIVES
        # Player Spinning Attack Variables
        self.is_spinning = False
        self.spin_start_angle = 0
        self.current_spin_angle = 0
        self.spin_cooldown = 0
        self.spin_cooldown_max = constants.DEATH_FLOWER_COOLDOWN
        # Player Message Defaults
        self.death_flower = "Available!"
        self.bullet_stream_msg = "Available!"
        self.tri_shot_msg = "Available!"
        # Player Bullet Stream Variables
        self.bullet_stream_cooldown = 0
        self.is_bullet_stream = False
        # Player Invincibility Timer Default
        self.invincible_timer = 0
        # Player Triple Shot Variables
        self.is_tri_shot = False
        self.tri_shot_bypass = 0
        self.tri_shot_cooldown = 0

    # Lets make a ship
    def create_ship():
        make_ship = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
        return make_ship

    # Starts the Death Blossom attack
    def start_spinning_attack(self):
        # Check if the player is not already spinning and the cooldown is over
        if self.spin_cooldown <= 0 and not self.is_spinning:
            # Begin the spinning attack
            self.is_spinning = True
            # Save the starting angle
            self.spin_start_angle = self.rotation
            # Make sure current spin angle is 0.  It should be already, but just in case...
            self.current_spin_angle = 0
            # Set the group for all the bullets to be created in
            self.dead_timer = 1.5
            self.invincible_timer = constants.PLAYER_INVINCIBILITY_TIMER - 3.0

    # Enables Triple Shot.  The Keybind checks if the cooldown is over
    def tri_shot(self):
        # Sets the timer for triple shot to make the shoot() function fire 3 shots
        self.tri_shot_bypass = constants.TRI_SHOT_DURATION
        # Marks Triple Shot as active
        self.is_tri_shot = True

    # Here is where most of the logic for firing the bullets will go
    def shoot(self):
        # Make the bullet
        bullet = bullets.Shot(self.position.x,self.position.y,constants.SHOT_RADIUS)
        # Set the bullet velocity
        bullet.velocity = pygame.Vector2(0, 1)
        # Rotate the bullet velocity to match the ship rotation
        bullet.velocity.rotate_ip(self.rotation)
        # Set the bullet speed
        bullet.velocity *= constants.PLAYER_SHOOT_SPEED
        # Check if triple shot is TRUE AND death blossom is NOT active AND bullet stream is NOT active
        # We dont want to enable triple shot if the player is using death blossom or bullet stream
        # Death Blossom and bullet stream WITH triple shot would be way too overpowered
        # And it might crash the game, cause that's alot of bullets...
        if self.is_tri_shot and self.is_spinning == False and self.is_bullet_stream == False:
            # TriShot creates 2 additional bullets
            # bullet b and c are created and rotated to the left and right of the ship
            bullet_b = bullets.Shot(self.position.x,self.position.y,constants.SHOT_RADIUS)
            bullet_b.velocity = pygame.Vector2(0, 1)
            bullet_b.velocity.rotate_ip(self.rotation - constants.TRI_SHOT_ROTATION)
            bullet_b.velocity *= constants.PLAYER_SHOOT_SPEED
            bullet_c = bullets.Shot(self.position.x,self.position.y,constants.SHOT_RADIUS)
            bullet_c.velocity = pygame.Vector2(0, 1)
            bullet_c.velocity.rotate_ip(self.rotation + constants.TRI_SHOT_ROTATION)
            bullet_c.velocity *= constants.PLAYER_SHOOT_SPEED
        # Play the sound effect for the shot
        soundeffects.play_soundeffect("laser.mp3",0.6,1500)

    def bullet_stream(self):
        self.shot_timer_bypass = constants.BULLET_STREAM_DURATION
        self.is_bullet_stream = True

    # Fires the bullets from Death Blossom and updates the rotation
    def update_spinning_attack(self):
        # Define the max sping degrees
        full_rotation = 720

        # Fire 1 bullet every 45 degrees
        degrees_per_bullet = 45
        rotation_speed = 15  # Adjust for desired speed
        
        # Calculate next angle
        prev_angle = self.current_spin_angle
        self.current_spin_angle += rotation_speed
        
        # Update ship angle
        self.rotation = (self.spin_start_angle + self.current_spin_angle) % 720

        # Check if we should fire bullets
        # This checks all 45-degree marks we passed in this frame
        for angle in range(int(prev_angle) // degrees_per_bullet * degrees_per_bullet, 
                        int(self.current_spin_angle) // degrees_per_bullet * degrees_per_bullet + 1, 
                        degrees_per_bullet):
            if angle <= full_rotation:
                self.shoot()
        
        # Check if we've completed a full rotation
        if self.current_spin_angle >= full_rotation:
            self.is_spinning = False
            self.spin_cooldown = self.spin_cooldown_max

    def move(self,dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * constants.PLAYER_SPEED * dt

    def rotate(self,dt):
        self.rotation += (constants.PLAYER_TURN_SPEED * dt)

    def draw_ship(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self,screen,color):
        self.color = color  #makes the color white - I found I can also do this by replacing color with [255,255,255]
        pygame.draw.polygon(screen,self.color,self.draw_ship(),2)

    # Resets the player ship to the center of the screen
    def reset(self):
        self.x = constants.SCREEN_WIDTH / 2
        self.y = constants.SCREEN_HEIGHT / 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.position = pygame.Vector2(self.x,self.y)

    def update(self, dt):
        # Updates everything about the player ship based on the delta time clock which is called in main()
        # There are alot of checks in here to make sure timers tick down and function correctly
        # The first section will be if statements for timers and message control
        # The second section will be keyboard input

        ############################################
        # First Section: Timers and Message Control
        ############################################

        #Basic Shooting Timer
        if self.shot_timer > 0:
            self.shot_timer -= dt
        #Sound Delay So we arent spamming sounds
        if gamestate.sound_effect_timer > 0:
            gamestate.sound_effect_timer -= dt
        #Invincibility Timer
        if self.invincible_timer > 0:   #Make the player invincibility timer tick down
            self.invincible_timer -= dt
        #Controls Lockout Timer
        if self.dead_timer > 0:   #Make the player death timer tick down
            self.dead_timer -= dt
        #Key lock timer to prevent double press
        if gamestate.key_lock > 0:
            gamestate.key_lock -= dt
        if gamestate.key_lock_1 > 0:
            gamestate.key_lock_1 -= dt
        if gamestate.key_lock_2 > 0:
            gamestate.key_lock_2 -= dt
        if gamestate.key_lock_5 > 0:
            gamestate.key_lock_5 -= dt
        if gamestate.key_lock_kp_enter > 0:
            gamestate.key_lock_kp_enter -= dt
        if gamestate.key_lock_kp_plus > 0:
            gamestate.key_lock_kp_plus -= dt
        if gamestate.key_lock_spacebar > 0:
            gamestate.key_lock_spacebar -= dt
        #Death Blossom Cooldown Timer
        if self.spin_cooldown > 0:
            if self.dead_timer > 0: # Make sure the player is not dead before we let the cooldown tick down
                pass
            else:
                self.spin_cooldown -= dt
        #Death Blossom Message Control
        if self.spin_cooldown > 0:
            self.death_flower = "Cooldown: "
        else:
            self.death_flower = "Available!"

        #Bullet Stream Message Control
        if self.bullet_stream_cooldown > 0:  
            self.bullet_stream_msg = "Cooldown: "
        elif self.shot_timer_bypass > 0:
            self.bullet_stream_msg = "-ACTIVE-: "
        else:
            self.bullet_stream_msg = "Available!"
        #TriShot Message Control
        if self.tri_shot_cooldown > 0:  
            self.tri_shot_msg = "Cooldown: "
        elif self.tri_shot_bypass > 0:
            self.tri_shot_msg = "-ACTIVE-: "
        else:
            self.tri_shot_msg = "Available!"
        #Bullet Stream Timers and Cooldown
        if self.is_bullet_stream:
            if self.shot_timer_bypass > 0:
                if self.dead_timer > 0: # Make sure the player is not dead before we let the cooldown tick down
                    pass
                else:
                    self.shot_timer_bypass -= dt
            if self.shot_timer_bypass <= 0 and self.is_bullet_stream:
                self.is_bullet_stream = False
                self.shot_timer_bypass = 0
                self.bullet_stream_cooldown = constants.BULLET_STREAM_COOLDOWN
        if self.bullet_stream_cooldown > 0:
            if self.dead_timer > 0: # Make sure the player is not dead before we let the cooldown tick down
                pass
            else:
                self.bullet_stream_cooldown -= dt
        #TriShot Timers and Cooldown
        if self.is_tri_shot:
            if self.tri_shot_bypass > 0:
                if self.dead_timer > 0: # Make sure the player is not dead before we let the cooldown tick down
                    pass
                else:
                    self.tri_shot_bypass -= dt
            if self.tri_shot_bypass <= 0 and self.is_tri_shot:
                self.is_tri_shot = False
                self.tri_shot_bypass = 0
                self.tri_shot_cooldown = constants.TRI_SHOT_COOLDOWN
        if self.tri_shot_cooldown > 0:
            if self.dead_timer > 0: # Make sure the player is not dead before we let the cooldown tick down
                pass
            else:
                self.tri_shot_cooldown -= dt
        #Death Blossom Active and In Progress in this timer
        if self.is_spinning:
            self.update_spinning_attack()

        ###############################################
        # Second Section: Keyboard Input Detection
        ###############################################

        # Get the current state of all keys
        keys = pygame.key.get_pressed()

        # If the NumberPad Enter key is pressed
        if keys[pygame.K_KP_ENTER]:
            if gamestate.key_lock_kp_enter <= 0: # Check if the key lock is active
                gamestate.key_lock_kp_enter = 1 # Set the key lock to 1 to prevent double press
                print(f"DEBUG: Current asteroid_spawn_rate = {gamestate.asteroid_spawn_rate}")
            else:
                if soundeffects.get_sound_timer(): # Check if the sound effect timer is up
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
        
        # If the NumberPad Plus key is pressed
        if keys[pygame.K_KP_PLUS]:
            if gamestate.key_lock_kp_plus <= 0: # Check if the key lock is active
                gamestate.key_lock_kp_plus = 1 # Set the key lock to 1 to prevent double press
                print(f"DEBUG: Current Player Values")
                print(f"----------------------------")
                print(f"self.position = {self.position}")
                print(f"self.radius = {self.radius}")
                print(f"self.rotation = {self.rotation}")
                print(f"self.lives = {self.lives}")
                print(f"(deathblossom)self.is_spinning = {self.is_spinning}")
                print(f"self.is_bullet_stream = {self.is_bullet_stream}")
                print(f"self.is_tri_shot = {self.is_tri_shot}")
                print(f"self.current_diff = {gamestate.difficulty}")
            else:
                if soundeffects.get_sound_timer(): # Check if the sound effect timer is up
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY


        #############################################################################################
        # Difficulty Keybinds
        # NOTE: I plan on removing these after the difficulty selection screen is implemented
        #############################################################################################

        if keys[pygame.K_1]:
            if self.dead_timer > 0 or gamestate.key_lock_1 > 0: # Check if the key lock is active or the player is dead
                    if soundeffects.get_sound_timer():
                        soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                        self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                if gamestate.difficulty != 1 and gamestate.difficulty != 5: # Check if the current difficulty is not 1 or 5
                    gamestate.difficulty = 1
                    gamestate.asteroid_spawn_rate = 0.8
                    self.sound_delay_cooldown = constants.SOUND_DELAY
                    gamestate.key_lock_1 = constants.KEY_LOCK_TIMER
                else:
                    if soundeffects.get_sound_timer():
                        soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                        self.sound_delay_cooldown = constants.SOUND_DELAY
        if keys[pygame.K_2]:
            if self.dead_timer > 0 or gamestate.key_lock_2 > 0: # Check if the key lock is active or the player is dead
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                if gamestate.difficulty != 2 and gamestate.difficulty != 5: # Check if the current difficulty is not 2 or 5
                    gamestate.key_lock_2 = constants.KEY_LOCK_TIMER # Set the key lock to 1 to prevent double press
                    gamestate.difficulty = 2
                    gamestate.asteroid_spawn_rate = 0.5
                    self.sound_delay_cooldown = constants.SOUND_DELAY
                else:
                    if soundeffects.get_sound_timer():
                        soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                        self.sound_delay_cooldown = constants.SOUND_DELAY
        if keys[pygame.K_5]:
            if self.dead_timer > 0 or gamestate.key_lock_5 > 0:
                soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                if gamestate.difficulty != 5:
                    gamestate.key_lock_5 = constants.KEY_LOCK_TIMER
                    gamestate.difficulty = 5
                    gamestate.asteroid_spawn_rate = 0.1
                    self.invincible_timer = 8
                    self.lives = 0
                    self.sound_delay_cooldown = constants.SOUND_DELAY
                    gamestate.key_lock_5 = constants.KEY_LOCK_TIMER
                    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
                    warning = constants.big_font.render("-!-WARNING-!- Incoming Asteroid Storm -!-WARNING-!-",True, constants.GAMEOVER_COLOR)
                    warning_2 = constants.big_font.render("Your Extra Ships Were Destroyed In The Storm",True, constants.GAMEOVER_COLOR)
                    screen.blit(warning,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(warning)//2, constants.SCREEN_HEIGHT//2 - 50))
                    screen.blit(warning_2,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(warning)//2 + 50, constants.SCREEN_HEIGHT//2 - 50 + constants.big_font.get_linesize()))
                    pygame.display.flip()
                    pygame.time.delay(5000)
                    
                else:
                    if soundeffects.get_sound_timer():
                        soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                        self.sound_delay_cooldown = constants.SOUND_DELAY
        
        ##############################################
        # Movement Keybinds
        ##############################################

        if keys[pygame.K_a]:
            if self.dead_timer > 0: # Check if the player is dead
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                self.rotate(-dt)
        if keys[pygame.K_d]:
            if self.dead_timer > 0: # Check if the player is dead
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                self.rotate(dt)
        if keys[pygame.K_w]:
            if self.dead_timer > 0: # Check if the player is dead
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                self.move(dt)
        if keys[pygame.K_s]:
            if self.dead_timer > 0: # Check if the player is dead
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                self.move(-dt)

        ##############################################
        # Shooting and Ablility Keybinds
        ##############################################

        if keys[pygame.K_SPACE]:  # Shoot
            if self.dead_timer > 0: # Check if the player is dead
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            elif gamestate.key_lock_spacebar > 0: # Check if the key lock is active
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            elif self.is_bullet_stream and self.shot_timer <= 0: # Check if the player is using bullet stream and the shot timer is 0
                self.shoot()
                self.shot_timer = 0.1 # Set the shot timer to 0.1 seconds to allow for rapid fire
            elif self.shot_timer <= 0: # Check if the shot timer is 0
                self.shoot() # Shoot
                self.shot_timer = constants.PLAYER_SHOOT_COOLDOWN # Set the shot timer to the player shoot cooldown
        
        # Death Blossom Keybind
        if keys[pygame.K_f]: 
            if self.dead_timer > 0 or self.spin_cooldown > 0: # Check if the player is dead or the spin cooldown is active
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                self.start_spinning_attack() # Start the Death Blossom attack
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("powerup.mp3",1,1500) # Play powerup sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY

        # Bullet Stream Keybind
        if keys[pygame.K_v]:  #Bullet Stream
            if self.dead_timer > 0 or self.bullet_stream_cooldown > 0 or self.shot_timer_bypass > 0: # Check if the player is dead, or the cooldown is active:
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                self.bullet_stream()
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("powerup.mp3",1,1500) # Play powerup sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
        
        # TriShot Keybind
        if keys[pygame.K_t]:  #TriShot
            if self.dead_timer > 0 or self.tri_shot_cooldown > 0 or self.tri_shot_bypass > 0 or self.is_bullet_stream:
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("error.mp3",1,1500) # Play error sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY
            else:
                self.tri_shot()
                if soundeffects.get_sound_timer():
                    soundeffects.play_soundeffect("powerup.mp3",1,1500) # Play powerup sound
                    self.sound_delay_cooldown = constants.SOUND_DELAY