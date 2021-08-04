"""Main file for the game"""

import pygame as pg
import random
import math
from data.settings import *
from data.sprites import *
from data.GeneralFunctions import *
import os

class Game:
    def __init__(self):
        # Initialise game window, etc.
        pg.init()
        pg.mixer.init()
        self.gameDisplay = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        #self.fontName = pg.font.match_font(FONT_NAME)
        self.spritesheet = Spritesheet(SPRITESHEET)
        self.platform_lengths = {"4":None, "6":None, "8":None, "10":None, "12":None}
        for i in PLATFORM_WIDTHS:
            self.platform_lengths[str(i)] = self.load_sprites("platforms", i)
        self.load_sprites("enemy")
        self.load_sprites("collectable")
        

            


    def newGame(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.scrolling = pg.sprite.Group()
        self.collectables = pg.sprite.Group()
        self.background = pg.sprite.Group()
        Background(self, 0,0)
        self.player = Player(self)
        first_plat = Platform(self, STARTING_PLATFORM[0], STARTING_PLATFORM[1], self.platform_lengths[STARTING_PLATFORM[2]])
        Platform.PlatsOnScreen.append(first_plat) # List for calculating the position of the next platform
        self.leaderboard = self.getLeaderboard()
        self.paralax_delay = 0





    def runGame(self):
        # Game loop
        self.playing = True
        while self.playing == True:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        self.all_sprites.update()




    def update(self):
        # Game loop - Update
        self.all_sprites.update()


        """bullet collisions"""
        for bullet in self.bullets:
            bulletEnemy_hit = pg.sprite.spritecollide(bullet, self.enemies, False)
            bulletPlat_hit = pg.sprite.spritecollide(bullet, self.platforms, False)
            if bulletEnemy_hit:
                bullet.kill()
                bulletEnemy_hit[0].kill()
                self.score += KILL_POINTS
            if bulletPlat_hit:
                bullet.kill()

        """player-platform collisions"""        
        plat_hit = pg.sprite.spritecollide(self.player, self.platforms, False) #checks if player has collided with a platform
        if plat_hit: #If collided
            self.player.rect[0] -= self.player.vel.x #move player to the left by its velocity (as it may be inside the platform by a few pixels, the velocity is the maximum distance into the platform the player rect can be.
            plat_hit_left = pg.sprite.spritecollide(self.player, self.platforms, False) #check for collision again
            if not plat_hit_left: #If not collided, it means the player came from the right (hit the left side of the platform)
                self.player.rect[0] += self.player.vel.x #move the player back (right) to where it was originally when detected as collided with a platform
                self.player.vel.x = 0 #set player x-velocity to 0
                self.player.pos.x = plat_hit[0].rect[0] - self.player.rect[2]/2 #move player position to the left side of platform (as it might be a few pixels inside at the moment)
            elif plat_hit_left: #If the player is still inside of the platform, it means the player did not come from the right (they did not hit the left side of the platform)
                self.player.rect[0] += self.player.vel.x #move the player back (right) to where it was originally when detected as collided with a platform
                self.player.rect[1] += abs(self.player.vel.y) #move player down by the absolute value of the players' velocity to check if it has come from below, if it came from below, it would be moving upwards, so the y-velocity would be negative, so using absolute value simplifies using the operators (as -- would be +, but would look like - in the code)
                plat_hit_bottom = pg.sprite.spritecollide(self.player, self.platforms, False) #check for collision again
                if not plat_hit_bottom: #If not collided, it means the player came from below (hit the bottom of the platform)
                    self.player.rect[1] -= abs(self.player.vel.y) #move the player back (up) to where it was originally when detected as collided with a platform
                    self.player.vel.y = 0 #set player y-velocity to 0
                    self.player.pos.y = plat_hit[0].rect.bottom + self.player.rect[3] #move player position so top of player is at the bottom of the platform
                else:   #If still collided with platform, it means it has come from above (hit the top of the platform) as it is impossible to hit the right side of the platform in this game.
                    self.player.rect[1] -= abs(self.player.vel.y) #move the player back (up) to where it was originally when detected as collided with a platform
                    self.player.jumping = False #Player should be able to jump here, as they are on ground
                    self.player.pos.y = plat_hit[0].rect.top #set player postion to the top of the platform
                    self.player.vel.y = 0 #set player y-velocity to 0
                    if plat_hit[0].alreadyHit == False:
                        self.score += LAND_POINTS
                        plat_hit[0].alreadyHit = True

        """player-item collisions"""
        item_hit = pg.sprite.spritecollide(self.player, self.collectables, False)
        if item_hit:
            for item in item_hit:
                if item.type == "extra_life":
                    item.kill()
                    self.player.extra_lives += 1
                elif item.type == "more_bullets":
                    item.kill()
                    self.player.num_of_bullets += MORE_BULLETS
                elif item.type == "coin":
                    item.kill()
                    self.score += COIN_POINTS

        """player-enemy collisions"""
        playerEnemy_hit = pg.sprite.spritecollide(self.player, self.enemies, False)
        if playerEnemy_hit:
            if self.player.extra_lives == 0:
                self.player.dead = True
                self.playing = False
            else:
                playerEnemy_hit[0].kill()
                self.player.extra_lives -= 1



        """If player reaches right 1/2 of screen & scroll objects & off screen checks"""
        if self.player.rect.right >= SCREEN_WIDTH * 1/2:
            self.player.pos.x -= abs(self.player.vel.x)
            for obj in self.scrolling:
                if obj in self.background:
                    if self.paralax_delay == 0:
                        for bg in self.background:
                            bg.rect.x -= BG_SPEED
                        self.paralax_delay += 1
                    elif self.paralax_delay <= MAX_PARALAX_DELAY:
                        self.paralax_delay += 1
                    else:
                        self.paralax_delay = 0
                else:
                    obj.rect.x -= abs(self.player.vel.x)
                    
                if obj.rect.right < 0:
                    obj.kill()
                    if obj in self.platforms:
                        Platform.PlatsOnScreen.pop(0) # Gets rid of platform that goes off the left side of screen
            for bullet in self.bullets:
                if (bullet.rect.x > SCREEN_WIDTH or bullet.rect.x < 0) or (bullet.rect.y > SCREEN_HEIGHT or bullet.rect.y < 0):
                    bullet.kill()


        """"Die!"""
        if self.player.rect.top > SCREEN_HEIGHT:
            self.player.dead = True
            self.playing = False


        """Spawn new background images to keep same average number"""
        while len(self.background) < NUM_OF_BG:
            Background(self, SCREEN_WIDTH, 0)

        """spawn new platforms to keep same average number"""
        while len(self.platforms) < NUM_OF_PLATFORMS:
            velDifference = max(self.player.vel.x - STARTING_VEL_X, 1)
            platWidth = random.choice(PLATFORM_WIDTHS)
            platHeight = PLATFORM_HEIGHT
            plat_X = (Platform.PlatsOnScreen[-1].rect.x + Platform.PlatsOnScreen[-1].rect.width + (BASE_PLATFORM_GAP_X * (1+(velDifference/10))))
            plat_Y = (Platform.PlatsOnScreen[-1].rect.y + random.randint(-PLATFORM_GAP_Y, +PLATFORM_GAP_Y))
            if plat_Y > BOTTOM_BOUNDARY:
                plat_Y = BOTTOM_BOUNDARY
            elif plat_Y < TOP_BOUNDARY:
                plat_Y = TOP_BOUNDARY
            new_plat = Platform(self, plat_X, plat_Y, self.platform_lengths[str(platWidth)]) # Creating the new platform
            Platform.PlatsOnScreen.append(new_plat)

            """Spawn enemies"""
            probabilityOfEnemy = random.randint(1,100)
            extra_chance = min((self.score // PTS_TO_INC_CHANCE), (MAX_CHANCE_OF_ENEMY - START_CHANCE_OF_ENEMY))   #Max chance of enemy is 80% (added in folder 13)
            if probabilityOfEnemy <= START_CHANCE_OF_ENEMY + extra_chance:
                enemy_X = random.uniform(new_plat.rect.left, new_plat.rect.right)
                enemy_Y = new_plat.rect.top
                Enemy(self, enemy_X, enemy_Y)

            """Spawn powerup/collectable"""
            chanceOfItem = random.randint(1,100)
            if chanceOfItem <= CHANCE_OF_POW:
                pow_X = random.uniform(new_plat.rect.left, new_plat.rect.right)
                pow_Y = new_plat.rect.top #- POW_DIAMETER - FLOATING_HEIGHT # CHANGE 'POW_DIAMETER' WHEN ADDING SPRITES AS SIZE OF POWERUPS MAY VARY
                PowerUp(self, pow_X, pow_Y)
            if chanceOfItem <= CHANCE_OF_COIN:
                coin_X = random.uniform(new_plat.rect.left, new_plat.rect.right)
                coin_Y = new_plat.rect.top
                Coins(self, coin_X, coin_Y)





    def events(self):
        # Game loop - Event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                jump_button = event.key == pg.K_SPACE
                if jump_button:
                    self.player.jump()
                if (event.key == pg.K_RIGHT) or (event.key == pg.K_DOWN):
                    if self.player.num_of_bullets > 0: # max bullets on screen
                        if event.key == pg.K_RIGHT:
                            bullet_vector = Vector2(BULLET_VEL, 0)
                        else:
                            bullet_vector = Vector2(0, BULLET_VEL)
                        Bullet(self, self.player.rect.center[0], self.player.rect.center[1], BULLET_RAD, BULLET_COLOUR, bullet_vector)
                        self.player.num_of_bullets -= 1
                if event.key == pg.K_ESCAPE:
                    self.drawText("PAUSED", TEXT_SIZE, TEXT_COLOUR, SCREEN_WIDTH - 20, 20, 3)
                    self.showStartScreen()

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE or event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.jumpCut()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.player.num_of_bullets > 0:
                    mousePosition = event.pos
                    mpVectorTot = mousePosition - Vector2(self.player.rect.center)                       #Total Mouse-Player Vector
                    #Hyp = pg.math.Vector2.length(mpVectorTot)                          #Length of hypotenuse made from the 2 lengths (length of the vector)
                    Hyp = math.sqrt(mpVectorTot[0]**2 + mpVectorTot[1]**2)             #Length of hypotenuse made from the 2 lengths (length of the vector)
                    scalingConst = Hyp / BULLET_VEL                                     # make sure that the velocity of every bullet is the same
                    mpVector = Vector2(mpVectorTot[0]/scalingConst, mpVectorTot[1]/scalingConst) #Vector for bullet to travel on
                    Bullet(self, self.player.rect.center[0], self.player.rect.center[1], BULLET_RAD, BULLET_COLOUR, mpVector)
                    self.player.num_of_bullets -= 1




    def draw(self):
        # Game loop - Draw
        #self.gameDisplay.fill(BG_COLOUR)
##        pg.draw.rect(self.gameDisplay, RED, self.player.rect, 2)###
##        for plat in self.platforms:
##            pg.draw.rect(self.gameDisplay, RED, plat.rect, 2)
##        for enemy in self.enemies:
##            pg.draw.rect(self.gameDisplay, RED, enemy.rect, 2)
        for bg in self.background:
            self.gameDisplay.blit(bg.image, (bg.rect.x, bg.rect.y))
        self.all_sprites.draw(self.gameDisplay)
        self.drawText(str(self.score), SCORE_FONT_SIZE, TEXT_COLOUR, SCREEN_WIDTH / 2, 20, 1)
        self.displayItemsCollected()
        pg.display.flip()




    def showStartScreen(self):
        self.drawText(TITLE, TITLE_FONT_SIZE, TITLE_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 5), 1, True, GREY2)
        self.drawText("Space = Jump/Double Jump | Mouse Click/Arrow Keys = Shoot", TEXT_SIZE, TEXT_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 5) + 100, 1)
        self.drawText("Coins = +" + str(COIN_POINTS) + " points | Number 5 = +" + str(MORE_BULLETS) + " bullets | Heart = +1 extra life", TEXT_SIZE, TEXT_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 5) + 140, 1)
        self.drawText("Kill enemy = +" + str(KILL_POINTS) + " points", TEXT_SIZE, TEXT_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 5) + 180, 1)
        self.drawText("Press SPACE to play", 40, TEXT_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 5/6), 1)
        pg.display.flip()
        self.waitForKeyPress()




    def showGameOverScreen(self):
        #if self.running == True and self.playing == False:
        self.draw()
        self.drawText("GAME OVER", TITLE_FONT_SIZE, GAME_OVER_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 1/5), 1, True, GREY2)
        self.drawText("Your Score: " + str(self.score), 32, TEXT_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 2/5), 1)
        self.drawText("Press SPACE to restart", TEXT_SIZE, TEXT_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 3/5), 1)
        self.drawText("Top Scores: ", LB_TITLE_SIZE, LB_COLOUR, LB_TOP_LEFT[0], LB_TOP_LEFT[1] - (LB_TITLE_SIZE - LB_FONT_SIZE), 2)
        for i in range(len(self.leaderboard)):
            self.drawText(self.leaderboard[i][0]+": "+str(self.leaderboard[i][1]), LB_FONT_SIZE, LB_COLOUR, LB_TOP_LEFT[0], LB_TOP_LEFT[1] + ((LB_FONT_SIZE + 10) * (i+1)), 2)
        pg.display.flip()
        self.waitForKeyPress()








    def askName(self):
        waiting = True
        current_string = []
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.playing = False
                    self.running = False
                    current_string = "???"
                if event.type == pg.KEYDOWN:
                    if event.key <= 127 and event.key != pg.K_RETURN and event.key != pg.K_BACKSPACE and len(current_string) < 10:
                       current_string.append(chr(event.key))
                    elif event.key == pg.K_BACKSPACE:
                        current_string = current_string[0:-1]
                    elif event.key == pg.K_RETURN:
                        if not all(elem == " " for elem in current_string):
                            waiting = False
            for bg in self.background:
                self.gameDisplay.blit(bg.image, (bg.rect.x, bg.rect.y))
            self.all_sprites.draw(self.gameDisplay)
            self.drawText("GAME OVER", TITLE_FONT_SIZE, GAME_OVER_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 1/5), 1, True, GREY2)
            self.drawText("Your Score: " + str(self.score), 32, TEXT_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 2/5), 1)
            self.drawText("TOP 10 SCORES!", 32, TEXT_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 3/5), 1)                            #FIX THIS CODE
            self.drawText("Enter your name: " + ''.join(current_string), 30, TEXT_COLOUR, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 4/5), 1)
            pg.display.flip()

        return (''.join(current_string).upper())





    def getLeaderboard(self):
        """Sorts leaderboard highest to lowest"""
        with open(HS_FILE, "r") as f:
            leaderboard = []
            line = f.readline().split()
            while line:
                line[1] = int(line[1])
                leaderboard.append(line)            # Reads the file line-by-line and
                line = f.readline().split()         # adds each line to the 'leaderboad' array
            mergeSort(leaderboard, 0, len(leaderboard)-1, 1)

        if len(leaderboard) < NUM_OF_TOP_SCORES:
            for i in range(0, (NUM_OF_TOP_SCORES - len(leaderboard))):
                leaderboard.append(["???", DEFAULT_TOP_SCORES])
        return leaderboard




    def setLeaderboard(self):
        if self.score > self.leaderboard[-1][1]:
            file = open(HS_FILE, "a")
            name = self.askName()
            if len(name.split()) > 1:
                tempName = ""
                for item in name.split():
                    tempName += item
                    name = tempName
            file.write((name + " " + str(self.score)) + "\n")
            file.close()

        self.leaderboard = self.getLeaderboard()

        while len(self.leaderboard) > NUM_OF_TOP_SCORES: 
            self.leaderboard.pop()


        """replaces all text in file with newly sorted 'leaderboard' list"""
        file = open(HS_FILE, "w")
        for i in range(len(self.leaderboard)):
            name = (str(self.leaderboard[i][0]))         # re-writes the entire file with items in 'leaderboard' array
            score = (str(self.leaderboard[i][1]))
            file.write(name + " " + score + "\n")
        file.close()






    def waitForKeyPress(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False




    def drawText(self, text, size, colour, x, y, reference, Title=False, dropShadow=BLACK):
        dirPath_file = os.path.dirname(__file__) # Gets the directory of the folder the program file is in
        dirPath_font = os.path.join(dirPath_file, "data", "Fonts", FONT_NAME) # From the directory stored in "dirPath_file", go into the file 'Fonts' and find FONT_NAME (This is the new directory)
        font = pg.font.Font(dirPath_font, size) # Initialises the font
        textSurface = font.render(text, True, colour) # Renders the font onto a surface
        textRect = textSurface.get_rect()
        if reference == 1:
            textRect.midtop = (x, y)
        elif reference == 2:
            textRect.topleft = (x, y)
        elif reference == 3:
            textRect.topright = (x, y)
        if Title:
            textSurface = font.render(text, True, dropShadow)
            self.gameDisplay.blit(textSurface, textRect)
            textRect[0] -= 3
            textRect[1] -= 3
            textSurface = font.render(text, True, colour)
            self.gameDisplay.blit(textSurface, textRect)
        else:
            self.gameDisplay.blit(textSurface, textRect)




    def displayItemsCollected(self):
        self.drawText(("Extra Lives: " + str(self.player.extra_lives)), TEXT_SIZE, TEXT_COLOUR, 10, 20, 2)
        self.drawText(("Ammo: " + str(self.player.num_of_bullets)), TEXT_SIZE, TEXT_COLOUR, 10, 50, 2)






    def load_sprites(self, Type, length=None):
        if Type == "platforms":
            left = self.spritesheet.get_image("grassHalf_left.png")
            mid = self.spritesheet.get_image("grassHalf_mid.png")
            right = self.spritesheet.get_image("grassHalf_right.png")
            sprite_rect = mid.get_rect()

            image = pg.Surface((length*sprite_rect[2], sprite_rect[3]))
            for count in range(0, length):
                if count == 0:
                    image.blit(left, (count*sprite_rect[2], 0))
                elif count < length-1 and count > 0:
                    image.blit(mid, (count*sprite_rect[2], 0))
                elif count == length-1:
                    image.blit(right, (count*sprite_rect[2], 0))

            image.set_colorkey(BLACK)
            return image
        
        elif Type == "enemy":
            fly = self.spritesheet.get_image("fly.png")
            fly_move = self.spritesheet.get_image("fly_move.png")
            self.fly_live_img = [fly, fly_move]
            #----------------------------------------------------------
            slime = self.spritesheet.get_image("slimePurple.png")
            slime_move = self.spritesheet.get_image("slimePurple_move.png")
            self.slime_live_img = [slime, slime_move]
            #----------------------------------------------------------
            bee = self.spritesheet.get_image("bee.png")
            bee_move = self.spritesheet.get_image("bee_move.png")
            self.bee_live_img = [bee, bee_move]
            #----------------------------------------------------------
            mouse = self.spritesheet.get_image("mouse.png")
            mouse_move = self.spritesheet.get_image("mouse_move.png")
            self.mouse_live_img = [mouse, mouse_move]

        elif Type == "collectable":
            self.heart = self.spritesheet.get_image("hudHeart_full.png")
            self.ammo_pickup = self.spritesheet.get_image("hud5.png")
            self.coin = self.spritesheet.get_image("coinGold.png")




#print(os.listdir(os.path.join(os.path.dirname(__file__), "Fonts")))
game = Game()
game.newGame()
game.draw()
game.showStartScreen()
while game.running == True:
    game.newGame()
    game.runGame()
    if game.player.dead:
        game.setLeaderboard()
        game.showGameOverScreen()

pg.quit()
