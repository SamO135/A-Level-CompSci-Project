# Sprite classes
import pygame as pg
import random
from data.settings import *
from data.GeneralFunctions import *
Vector2 = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.last_change = 0
        self.current_frame = 0
        self.load_img()
        self.image = self.walk_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (STARTING_PLATFORM[0]+50, STARTING_PLATFORM[1]-self.rect[3]/2)
        self.pos = Vector2(STARTING_PLATFORM[0]+50, STARTING_PLATFORM[1])
        self.vel = Vector2(STARTING_VEL_X, 0)
        self.acc = Vector2(0, 0)
        self.extra_lives = 0
        self.jumping = False
        self.dead = False
        self.num_of_bullets = STARTING_BULLETS


    def load_img(self):
        walk_img = ["alienPink_walk1.png", "alienPink_walk2.png"]
        jump_img = ["alienPink_jump.png"]
        die_img = ["hudX.png"]
        
        self.walk_frames = []
        for img in walk_img:
            frame = self.game.spritesheet.get_image(img)  # Only loads one time (when you start the game) so using spritesheet.get_image is fine here.
            frame.set_colorkey(BLACK)
            self.walk_frames.append(frame)

        self.jump_frames = []
        for img in jump_img:
            frame = self.game.spritesheet.get_image(img)
            frame.set_colorkey(BLACK)
            self.jump_frames.append(frame)
            
        self.die_frames = []
        for img in die_img:
            frame = self.game.spritesheet.get_image(img)
            frame.set_colorkey(BLACK)
            self.die_frames.append(frame)
            

    def animate(self):
        time = pg.time.get_ticks()
        #If not jumping
        if not self.jumping:
            if time - self.last_change > PLAYER_FRAME_DELAY:
                self.last_change = time
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_frame]

        #If jumping
        elif self.jumping:
            self.current_frame = 0
            self.image = self.jump_frames[self.current_frame]
        if self.dead:
            self.current_frame = 0
            self.image = self.die_frames[self.current_frame]
        
        
    def jump(self):
        # Jump only if standing on a platform
        self.rect[1] += 1 # <-- Added in update 19
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect[1] -= 1
        if hits:
            self.vel.y = JUMP_POWER
            self.jumping = True
            self.can_double_jump = True

        elif self.jumping and self.can_double_jump:
            if self.vel.y > DOUBLE_JUMP_POWER:
                self.vel.y = DOUBLE_JUMP_POWER
            else:
                self.vel.y -= DOUBLE_JUMP_POWER
            self.can_double_jump = False


    def jumpCut(self):
        """Called if player releasese the jump
            key before max height reached"""
        if self.vel.y < JUMP_CUT_POWER:
            self.vel.y = JUMP_CUT_POWER

        
    def update(self):
        self.animate()
        self.acc = Vector2(PLAYER_ACC, PLAYER_GRAV)
        
        # Equations of motion
        if self.vel.x < MAX_SPEED:
            self.vel.x += self.acc.x    # Acclerate player if vel is less than max velocity
        self.vel.y += self.acc.y
        self.pos += self.vel + 0.5 * self.acc # From s = ut + 0.5*at^2 just without t
        
        # Position the player
        self.rect.midbottom = self.pos









class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies, game.scrolling
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.last_change = 0
        self.current_frame = 0
        self.load_img()
        self.image = self.live_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.midbottom = (x, y)

    def load_img(self):
        enemy_type = random.choice(["fly", "slime", "bee", "mouse"])
        if enemy_type == "fly":
            live_img = self.game.fly_live_img
        elif enemy_type == "slime":
            live_img = self.game.slime_live_img
        elif enemy_type == "bee":
            live_img = self.game.bee_live_img
        elif enemy_type == "mouse":
            live_img = self.game.mouse_live_img
            
        self.live_frames = []
        for frame in live_img:
            frame.set_colorkey(BLACK)
            self.live_frames.append(frame)


    def animate(self):
        time = pg.time.get_ticks()
        #If not jumping
        if time - self.last_change > ENEMY_FRAME_DELAY:
            self.last_change = time
            self.current_frame = (self.current_frame + 1) % len(self.live_frames)
            self.image = self.live_frames[self.current_frame]


    def update(self):
        self.animate()
        









class Platform(pg.sprite.Sprite):
    PlatsOnScreen = []
    def __init__(self, game, x, y, surface):
        self.groups = game.all_sprites, game.platforms, game.scrolling
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.alreadyHit = False





    
        


class Background(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.background, game.scrolling
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.BG = pg.image.load(BG_IMAGE).convert()
        img_rect = self.BG.get_rect()
        self.image = pg.Surface((img_rect[2]-105, img_rect[3]))
        self.image.blit(self.BG, (0, 0), (2, 0, img_rect[2], img_rect[3]))
        self.image = pg.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        







class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y, radius, colour, vector):
        self.groups = game.all_sprites, game.bullets
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
        pg.draw.circle(self.image, colour, (radius,radius), radius)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = Vector2(vector)
        self.pos = Vector2(x, y)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos

        
        






class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.scrolling, game.collectables
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type = random.choice(["extra_life", "more_bullets", "coin"])
        self.load_img()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y                             #added coins to the poweup class as I noticed there were many similarities (15.30) -- should this stay here? it spawns a coin as if it is a power up, but maybe good                                             
        self.rect.midbottom = (x, y)                #because occasionally it can spawn 2 coins on a platform - like a rare point boost at the cost of a different power-up.
        self.image.set_colorkey(BLACK)

    def load_img(self):
        if self.type == "extra_life":
            self.image = self.game.heart
        elif self.type == "more_bullets":
            self.image = self.game.ammo_pickup
        elif self.type == "coin":
            self.image = self.game.coin
            




            


class Coins(PowerUp):
    def __init__(self, game, x, y):
        PowerUp.__init__(self, game, x, y)          #seperate class to PowerUps as it needs a different spawn chance
        self.type = "coin"

    def load_img(self):
        self.image = self.game.coin








class Spritesheet():
    def __init__(self, fileName):
        self.sprite_sheet = pg.image.load(SPRITESHEET).convert()
        #self.count = 0     #Used to check how many times the 'get_image' method is being used, if this number rises during a game, it is being used somewhere in the code and lagging/slowing down the game

    def get_image(self, img_name):
        #self.count += 1
        coords = get_image_coords(img_name)
        width = coords[2]
        height = coords[3]
        img = pg.Surface((width, height))
        img.blit(self.sprite_sheet, (0, 0), coords)
        img = pg.transform.scale(img, (width // 2, height // 2))
        #print(self.count)
        
        return img


