############### P L A Y I N G   W I T H   F I R E ###########
# elina liu 2014

# Pitch Sheet = http://i.imgur.com/6hCx0be.png?1

# Music - Subway, by Maplestory, all rights belong to Maplestory

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# Global Variables
m = 0
bomb_timer = 0
started = False
lives = 3
ended = False

instructions_center = 0
play_button_center = 0
highscore_button_center = 0

instructions_page_pressed = False
highscore_page_pressed = False

tiles_with_items = {}
indestructable_tiles = {}
unmovable_dict = {}

player_one_name = None
player_two_name = None
# Highscore dictionary - Player Name : Highscore
highscore_board = []
ranked_board = []
current_page = "home_page"

class ImageInfo:
    def __init__(self, center, size, radius = 0,  lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        
        self.animated = animated
        
    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

#################### A R T ######################
# Splash Screen
splash_screen_image = simplegui.load_image("http://i.imgur.com/brWSn0Y.png")
splash_screen_info = ImageInfo([640, 360], [1280, 720])

# Game Over Screen
game_over_info = ImageInfo([640, 360], [1280, 720])
game_over_blue_image = simplegui.load_image("http://i.imgur.com/4UD4fWn.png")
game_over_red_image = simplegui.load_image("http://i.imgur.com/7BdbksX.png")
game_over_tied_image = simplegui.load_image("http://i.imgur.com/oCEMTcX.png")

# Instructions Button
instructions = simplegui.load_image("http://i.imgur.com/FP6iDBd.png")
instructions_info = ImageInfo([459/2, 81/2], [459, 81])

# Instructions Page
instructions_page = simplegui.load_image("http://i.imgur.com/1pP2sPa.png")
instructions_page_info = ImageInfo([640,360], [1280,720])
instructions_page_two = simplegui.load_image("http://i.imgur.com/isKgdFo.png")

# Play Button
play_button = simplegui.load_image("http://i.imgur.com/aCx7UJb.png")
play_button_info = ImageInfo([176/2, 81/2], [176, 81])

# Next Button
next_button = simplegui.load_image("http://i.imgur.com/QRgrJt5.png")
next_button_info = ImageInfo([176/2, 81/2], [176, 81])

# Highscore Button
highscore_button = simplegui.load_image("http://i.imgur.com/1eebIWS.png")
highscore_button_info = ImageInfo([459/2, 81/2], [459, 81])

# Home Button
home_button = simplegui.load_image("http://i.imgur.com/irOIQIh.png")
home_button_info = ImageInfo([176/2, 81/2], [176, 81])

# Highscore Page
highscore_page = simplegui.load_image("http://i.imgur.com/XcYZIcF.png")
highscore_page_info = ImageInfo([640,360], [1280,720])

# Save Score Button
save_score_button = simplegui.load_image("http://i.imgur.com/JJj2tYX.png")
save_score_button_info = ImageInfo([459/2, 81/2], [459, 81])
# Back Ground Grid Image
grid = simplegui.load_image("http://i.imgur.com/e00hKp8.png")

# Blue Bomber Image
blue_bomber_info = ImageInfo([20,21],[41,41], 16)
blue_bomber_image = simplegui.load_image("http://i.imgur.com/IAEVtFh.png")
blue_bomber_left_image = simplegui.load_image("http://i.imgur.com/yThkDXo.png")
blue_bomber_right_image = simplegui.load_image("http://i.imgur.com/UNU3Ovb.png")
blue_bomber_up_image = simplegui.load_image("http://i.imgur.com/1GOczXT.png")
                                             
# Red Bomber Down
red_bomber_info = ImageInfo([20,21],[41,41], 16)
red_bomber_image = simplegui.load_image("http://i.imgur.com/C6i3XGs.png")
red_bomber_left_image = simplegui.load_image("http://i.imgur.com/nwUl0Ra.png")
red_bomber_right_image = simplegui.load_image("http://i.imgur.com/B2gEeFF.png")
red_bomber_up_image = simplegui.load_image("http://i.imgur.com/aYGDNYZ.png")

# Blue Bomb Image
blue_bomb_info = ImageInfo([20,20], [41,41], 15, 200)
blue_bomb_image = simplegui.load_image("http://i.imgur.com/WfUzziQ.png")

# Red Bomb Image Placeholder
red_bomb_info = ImageInfo([20,20], [41,41], 15, 200)
red_bomb_image = simplegui.load_image("http://i.imgur.com/JGeYz1M.png")

# Blue Explosion Image
blue_explosion_info = ImageInfo([20,20], [39,39], 20, 30)
blue_explosion_image = simplegui.load_image("http://i.imgur.com/YlrhT9B.png")

# Red Explosion Image
red_explosion_info = ImageInfo([20,20], [39,39], 20, 30)
red_explosion_image = simplegui.load_image("http://i.imgur.com/DF4qATh.png")

# Barrel and Tile Image
barrel_info = ImageInfo([20,20], [41,41], 20)
barrel_image = simplegui.load_image("http://i.imgur.com/wycTG05.png")
tile_info = ImageInfo([20,20], [41,41], 20)

# Add Bomb Number Powerup Image
add_bomb_info = ImageInfo([19,19], [39,39], 19)
add_bomb_image = simplegui.load_image("http://i.imgur.com/pSyAm4e.jpg")

# Add Life Powerup
add_life_info = ImageInfo([19,19], [39,39], 19)
add_life_image = simplegui.load_image("http://i.imgur.com/R1BNLTf.png")

# Add Range Powerup
add_range_info = ImageInfo([19,19], [39,39], 19)
add_range_image = simplegui.load_image("http://i.imgur.com/Mba7l6d.png")

# Add Speed Powerup
add_speed_info = ImageInfo([19,19], [39,39], 19)
add_speed_image = simplegui.load_image("http://i.imgur.com/KiAHBfJ.png")

# Add Throw Bomb Powerup
add_throw_bomb_info = ImageInfo([20,20], [41,41], 20)
add_throw_bomb_image = simplegui.load_image("http://i.imgur.com/3S4LVAm.jpg")
                                            
# Add Walk Over Powerup
add_walk_over_info = ImageInfo([19,19], [39,39], 19)
add_walk_over_image = simplegui.load_image("http://i.imgur.com/2TIt1A3.png")

# Add Coin
coin_info = ImageInfo([19,19], [39,39], 19)
coin_image = simplegui.load_image("http://i.imgur.com/1in74Hf.png")

# New Distance - Distance up down, distance left right
def dist(p,q):
    return (math.sqrt((p[0] - q[0])**2), math.sqrt((p[1] - q[1])**2))


################### S O U N D S ##################

bomb_sound = simplegui.load_sound("http://www.mediacollege.com/downloads/sound-effects/explosion/bomb-03.mp3")
bomb_sound.set_volume(0.2)
background_sound = simplegui.load_sound("https://dl-web.dropbox.com/get/Maplestory%20Music%20%28High%20Quality%29-%20%5B4.5%5D%20Subway.mp3?_subject_uid=331836650&w=AACf_ZTIUv0hQTi28QBUgXY8K03dijp-YxkObZHTCsOmGQ")
background_sound.set_volume(0.6)

powerup_sound = simplegui.load_sound("https://dl-web.dropbox.com/get/198784__cman634__jump-sound-or-power-up-sound.mp3?_subject_uid=331836650&w=AAAsnSzexD8d3LXkx67mVIuv605SAhGOWsJbWRHox3kqxA")
powerup_sound.set_volume(0.4)

coin_sound = simplegui.load_sound("https://dl-web.dropbox.com/get/coin.wav?_subject_uid=331836650&w=AAAI3sZCHYNrsedSxdqxrIUpQADl-gcrrZdQAlrFYGtFLQ")
coin_sound.set_volume(0.7)
lose_life_sound = simplegui.load_sound("https://dl-web.dropbox.com/get/138490__randomationpictures__powerdown-2.wav?_subject_uid=331836650&w=AABYKptT9lNsvkemMjeeK9SgVuTTUFsw_DJ4ZtQXM1RWWw")

speed_sound = simplegui.load_sound("https://dl-web.dropbox.com/get/speedup.wav?_subject_uid=331836650&w=AAA0KK6co1oAVkcnZXLADMXV5Mpm4_Nws6vIBDAT1fzEhQ")

################### C L A S S E S ##################


# Bomber Class
class Bomber:
    def __init__(self, pos, vel, image_down, image_left, image_right, image_up, info, name, life, number, speed, immune = False):
        self.pos = [int(pos[0]), int(pos[1])]
        self.vel = [vel[0],vel[1]]
        self.image_down = image_down
        self.image_up = image_up
        self.image_left = image_left
        self.image_right = image_right
        self.image_up = image_up
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.dim = (self.pos[0] - self.image_size[0]/2.0, self.pos[1] - self.image_size[1]/2.0, 
                    self.pos[0] + self.image_size[1]/2.0, self.pos[1] + self.image_size[0]/2.0)
        self.lives = life
        self.immune = immune
        self.immune_time = 120
        self.hit = False
        self.name = name
        self.number = number
        self.age = 0
        self.pace = 0
        self.speed = speed
        self.distance_left = 0
        self.distance_right = 0
        self.distance_up = 0
        self.distance_down = 0
        self.bomb_limit = 1
        self.bomb_range = 1
        self.throw = None
        self.walk = None
        self.score = 0
        self.direction = "DOWN"
     
    def get_speed(self):
        return self.speed
    
    def get_score(self):
        return self.score
        
    def draw(self, canvas):
        if self.vel[1] > 0:
            canvas.draw_image(self.image_down, (self.image_center[0] + self.age * self.image_size[0], self.image_center[1]), 
                          self.image_size, (self.pos[0], self.pos[1]), (41,41))
            self.direction = "DOWN"
        if self.vel[1] < 0:
            canvas.draw_image(self.image_up, (self.image_center[0] + self.age * self.image_size[0], self.image_center[1]), 
                          self.image_size, (self.pos[0], self.pos[1]), (41,41))
            self.direction = "UP"
        if self.vel[0] > 0:
            canvas.draw_image(self.image_right, (self.image_center[0] + self.age * self.image_size[0], self.image_center[1]), 
                          self.image_size, (self.pos[0], self.pos[1]), (41,41))
            self.direction = "RIGHT"
        if self.vel[0] < 0:
            canvas.draw_image(self.image_left, (self.image_center[0] + self.age * self.image_size[0], self.image_center[1]), 
                          self.image_size, (self.pos[0], self.pos[1]), (41,41))
            self.direction = "LEFT"
        if self.vel[0] == 0 and self.vel[1] == 0:
            if self.direction == "DOWN":
                canvas.draw_image(self.image_down, (self.image_center[0] + self.age * self.image_size[0], self.image_center[1]), 
                          self.image_size, (self.pos[0], self.pos[1]), (41,41))
            if self.direction == "RIGHT":
                canvas.draw_image(self.image_right, (self.image_center[0] + self.age * self.image_size[0], self.image_center[1]), 
                          self.image_size, (self.pos[0], self.pos[1]), (41,41))
            if self.direction == "LEFT":
                canvas.draw_image(self.image_left, (self.image_center[0] + self.age * self.image_size[0], self.image_center[1]), 
                          self.image_size, (self.pos[0], self.pos[1]), (41,41))
            if self.direction == "UP":
                canvas.draw_image(self.image_up, (self.image_center[0] + self.age * self.image_size[0], self.image_center[1]), 
                          self.image_size, (self.pos[0], self.pos[1]), (41,41))
                
        canvas.draw_text(str(int(self.lives)), (80, self.number * 210 + 275), 40, "Black", "sans-serif")
        canvas.draw_text(str(int(self.score)), (80, (self.number * 210 + 380)), 40, "Black", "sans-serif")
   
    def update(self):
        global ended, started
        # Movement and Collision
        if self.vel[1] > 0:
            self.tile_center_num = check_self_tile_num((self.pos[0] + 5,self.pos[1] + 22))
            if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                self.tile_center_num = check_self_tile_num((self.pos[0] - 5,self.pos[1] + 22))
                if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                    self.pos[1] += self.vel[1]
            elif unmovable_dict[(self.tile_center_num[0], self.tile_center_num[1])] == "Bomb":
                if self.walk == True:
                    self.pos[1] += self.vel[1]
                else:    
                    self.tile_center_num = check_self_tile_num((self.pos[0] + 5,self.pos[1] + 40))
                    if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                        self.tile_center_num = check_self_tile_num((self.pos[0] - 5,self.pos[1] + 40))
                        if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                            self.pos[1] += self.vel[1]

        elif self.vel[1] < 0:
            self.tile_center_num = check_self_tile_num((self.pos[0] + 5,self.pos[1] - 22))
            if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                self.tile_center_num = check_self_tile_num((self.pos[0] - 5,self.pos[1] - 22))
                if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                    self.pos[1] += self.vel[1]
            elif unmovable_dict[(self.tile_center_num[0], self.tile_center_num[1])] == "Bomb":
                if self.walk == True:
                    self.pos[1] += self.vel[1]
                else:    
                    self.tile_center_num = check_self_tile_num((self.pos[0] + 5,self.pos[1] - 40))
                    if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                        self.tile_center_num = check_self_tile_num((self.pos[0] - 5,self.pos[1] - 40))
                        if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                            self.pos[1] += self.vel[1]
        else:
            if self.vel[0] > 0:
                self.tile_center_num = check_self_tile_num((self.pos[0] + 22, self.pos[1] + 15))
                if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                    self.tile_center_num = check_self_tile_num((self.pos[0] + 22, self.pos[1] - 8))
                    if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                        self.pos[0] += self.vel[0]
                elif unmovable_dict[(self.tile_center_num[0], self.tile_center_num[1])] == "Bomb":
                    if self.walk == True:
                        self.pos[0] += self.vel[0]
                    else:    
                        self.tile_center_num = check_self_tile_num((self.pos[0] + 40 ,self.pos[1] + 15))
                        if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                            self.tile_center_num = check_self_tile_num((self.pos[0] + 40,self.pos[1] - 8))
                            if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                                self.pos[0] += self.vel[0]
            if self.vel[0] < 0:
                self.tile_center_num = check_self_tile_num((self.pos[0] - 22, self.pos[1] + 15))
                if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                    self.tile_center_num = check_self_tile_num((self.pos[0] - 22, self.pos[1] - 8))
                    if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                        self.pos[0] += self.vel[0]
                elif unmovable_dict[(self.tile_center_num[0], self.tile_center_num[1])] == "Bomb":
                    if self.walk == True:
                        self.pos[0] += self.vel[0]
                    else:    
                        self.tile_center_num = check_self_tile_num((self.pos[0] - 40 ,self.pos[1] + 15))
                        if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                            self.tile_center_num = check_self_tile_num((self.pos[0] - 40,self.pos[1] - 8))
                            if unmovable_dict.has_key((self.tile_center_num[0], self.tile_center_num[1])) == False:
                                self.pos[0] += self.vel[0]
                    
        # Touch Explosion
        if group_collide(blue_explosions, self) == True and self.immune == False:
            self.lives -= 1
            lose_life_sound.rewind()
            lose_life_sound.play()
            self.immune = True
            self.hit = True
            if self.number == 0:
                self.score -= 100
            elif self.number == 1:
                blue_bomber.score += 500
        elif group_collide(red_explosions, self) == True and self.immune == False:
            self.lives -= 1
            lose_life_sound.rewind()
            lose_life_sound.play()
            self.immune = True
            self.hit = True
            if self.number == 0:
                red_bomber.score += 500
            elif self.number == 1:
                self.score -= 100

        if self.hit == True:
            self.immune_time -= 1
            if self.immune_time == 0:
                self.immune = False
                self.immune_time = 180
            
        # Touch Powerups
        for powerup in all_powerups:
            if collide(powerup, self) == True:
                all_powerups.remove(powerup)
                if powerup.get_coin() == 100:
                    coin_sound.rewind()
                    coin_sound.play()
                elif powerup.get_speed() == 1:
                    speed_sound.rewind()
                    speed_sound.play()
                else:
                    powerup_sound.rewind()
                    powerup_sound.play()
                self.lives += powerup.get_life()
                self.bomb_limit += powerup.get_bombs()
                self.bomb_range += powerup.get_range()
                if self.speed < 5:
                    self.speed += powerup.get_speed()
                if self.throw == None:
                    self.throw = powerup.get_throw()
                if self.walk == None:
                    self.walk = powerup.get_walk()
                self.score += powerup.get_coin()
        
        # Pace    
        if self.vel[0] != 0 or self.vel[1] != 0:
            self.pace += 1
            if self.speed == 1:
                if (int(self.pace) % int(10/self.speed) == 0):
                    self.age = (self.age + 1) % 2
            if self.speed < 3 and self.speed > 1:
                if (int(self.pace) % int(15/self.speed) == 0):
                    self.age = (self.age + 1) % 2
            if self.speed >= 3:
                if (int(self.pace) % int(20/self.speed) == 0):
                    self.age = (self.age + 1) % 2
        
        # Lives Lost
        if self.lives == 0:		
            ended = True
            started = False
            
    def drop(self):
        if self.bomb_limit > 0:
            tile_center_pos = check_self_tile_pos(self.pos)
            if tile_center_pos == None:
                pass
            else:
                if tiles_with_items.has_key(tile_center_pos):
                    if tiles_with_items[tile_center_pos] == True:
                        pass
                    else:
                        if self.number == 0:
                            a_blue_bomb = Bomb(tile_center_pos, blue_bomb_image, blue_bomb_info, self.number, self.bomb_range)
                            blue_bomb_group.add(a_blue_bomb)
                            self.bomb_limit -= 1
                        if self.number == 1:
                            a_red_bomb = Bomb(tile_center_pos, red_bomb_image, red_bomb_info, self.number, self.bomb_range)
                            red_bomb_group.add(a_red_bomb)
                            self.bomb_limit -= 1
                
                        # Update Dictionary Tiles-Item Status
                        tiles_with_items[tile_center_pos] = True
                        unmovable_dict[check_self_tile_num(self.pos)] = "Bomb"
    
                else:
                    if self.number == 0:
                        a_blue_bomb = Bomb(tile_center_pos, blue_bomb_image, blue_bomb_info, self.number, self.bomb_range)
                        blue_bomb_group.add(a_blue_bomb)
                        self.bomb_limit -= 1
                    if self.number == 1:
                        a_red_bomb = Bomb(tile_center_pos, red_bomb_image, red_bomb_info, self.number, self.bomb_range)
                        red_bomb_group.add(a_red_bomb)
                        self.bomb_limit -= 1

                    # Update Dictionary Tiles-Item Status
                    tiles_with_items[tile_center_pos] = True
                    unmovable_dict[check_self_tile_num(self.pos)] = "Bomb"
    
    def add_bomb(self):
        self.bomb_limit += 1
                
class Bomb:
    def __init__(self, pos, image, info, number, power, sound = None, timer = 0, age = None):
        self.pos = [pos[0], pos[1]]
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.number = number
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.timer = timer
        self.age = age
        if self.age == None:
            self.age = 0
        self.power = power
                  
    def draw(self,canvas):
        self.update()
        canvas.draw_image(self.image, (self.image_center[0] + 
                                       self.age * self.image_size[0], 
                                       self.image_center[1]), self.image_size, 
                                       self.pos, self.image_size)    
    def update(self):
        self.timer += 1
        if self.timer >= self.lifespan + 60:
            if self.number == 0:
                blue_bomber.add_bomb()
                for X in range(0, self.power + 1):
                    explosion = Explosion((self.pos[0] + -40 * X, self.pos[1]), 
                                          blue_explosion_image, blue_explosion_info, self.power)
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0] + -40 * X, self.pos[1]))) and indestructable_tiles[check_self_tile_num((self.pos[0] + - 40 * X, self.pos[1]))] == True:
                        break
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0] + -40 * X, self.pos[1]))) and indestructable_tiles[check_self_tile_num((self.pos[0] + - 40 * X, self.pos[1]))] == False:
                        blue_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                        indestructable_tiles[check_self_tile_num((self.pos[0] + - 40 * X, self.pos[1]))] = None
                        for barrel in all_barrels:
                            if tuple(barrel.pos) == (self.pos[0] + -40 * X, self.pos[1]):
                                all_barrels.remove(barrel)
                                for barrel in all_unmovable:
                                    if tuple(barrel.pos) == (self.pos[0] + -40 * X, self.pos[1]):
                                        all_unmovable.remove(barrel)
                                        if unmovable_dict.has_key((check_self_tile_num((self.pos[0] + -40 * X, self.pos[1])))):
                                            unmovable_dict.pop((check_self_tile_num((self.pos[0] + -40 * X, self.pos[1]))))
                                            add_powerup((self.pos[0] + -40 * X, self.pos[1]))

                        break
                    else:
                        blue_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                for X in range(0, self.power + 1):
                    explosion = Explosion((self.pos[0] + 40 * X, self.pos[1]), 
                                          blue_explosion_image, blue_explosion_info, self.power)
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))) and indestructable_tiles[check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))] == True:
                        break
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))) and indestructable_tiles[check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))] == False:
                        blue_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                        indestructable_tiles[check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))] = None
                        for barrel in all_barrels:
                            if tuple(barrel.pos) == (self.pos[0] + 40 * X, self.pos[1]):
                                all_barrels.remove(barrel)
                                for barrel in all_unmovable:
                                    if tuple(barrel.pos) == (self.pos[0] + 40 * X, self.pos[1]):
                                        all_unmovable.remove(barrel)
                                        if unmovable_dict.has_key((check_self_tile_num((self.pos[0] + 40 * X, self.pos[1])))):
                                            unmovable_dict.pop((check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))))
                                            add_powerup((self.pos[0] + 40 * X, self.pos[1]))

                        break
                    else:
                        blue_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                for Y in range(0, self.power + 1):
                    explosion = Explosion((self.pos[0], self.pos[1] + Y * -40), 
                                          blue_explosion_image, blue_explosion_info, self.power)
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))) and indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))] == True:
                        break
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))) and indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))] == False:
                        blue_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                        indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))] = None
                        for barrel in all_barrels:
                            if tuple(barrel.pos) == (self.pos[0], self.pos[1] + Y * -40):
                                all_barrels.remove(barrel)
                                for barrel in all_unmovable:
                                    if tuple(barrel.pos) == (self.pos[0], self.pos[1] + Y * -40):
                                        all_unmovable.remove(barrel)
                                        if unmovable_dict.has_key((check_self_tile_num((self.pos[0], self.pos[1] + Y * -40)))):
                                            unmovable_dict.pop((check_self_tile_num((self.pos[0], self.pos[1] + Y * -40))))
                                            add_powerup((self.pos[0], self.pos[1] + Y * -40))
                        break
                    else:
                        blue_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                for Y in range(0, self.power + 1):
                    explosion = Explosion((self.pos[0], self.pos[1] + Y * 40), 
                                          blue_explosion_image, blue_explosion_info, self.power)
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))) and indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))] == True:
                        break
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))) and indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))] == False:
                        blue_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                        indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))] = None
                        for barrel in all_barrels:
                            if tuple(barrel.pos) == (self.pos[0], self.pos[1] + Y * 40):
                                all_barrels.remove(barrel)
                                for barrel in all_unmovable:
                                    if tuple(barrel.pos) == (self.pos[0], self.pos[1] + Y * 40):
                                        all_unmovable.remove(barrel)
                                        if unmovable_dict.has_key((check_self_tile_num((self.pos[0], self.pos[1] + Y * 40)))):
                                            unmovable_dict.pop((check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))))
                                            add_powerup((self.pos[0], self.pos[1] + Y * 40))
                        break
                    else:
                        blue_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                
            if self.number == 1:
                red_bomber.add_bomb()
                for X in range(0, self.power + 1):
                    explosion = Explosion((self.pos[0] + -40 * X, self.pos[1]), 
                                          red_explosion_image, red_explosion_info, self.power)
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0] + -40 * X, self.pos[1]))) and indestructable_tiles[check_self_tile_num((self.pos[0] + - 40 * X, self.pos[1]))] == True:
                        break
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0] + -40 * X, self.pos[1]))) and indestructable_tiles[check_self_tile_num((self.pos[0] + - 40 * X, self.pos[1]))] == False:
                        red_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                        indestructable_tiles[check_self_tile_num((self.pos[0] + - 40 * X, self.pos[1]))] = None
                        for barrel in all_barrels:
                            if tuple(barrel.pos) == (self.pos[0] + -40 * X, self.pos[1]):
                                all_barrels.remove(barrel)
                                for barrel in all_unmovable:
                                    if tuple(barrel.pos) == (self.pos[0] + -40 * X, self.pos[1]):
                                        all_unmovable.remove(barrel)
                                        if unmovable_dict.has_key((check_self_tile_num((self.pos[0] + -40 * X, self.pos[1])))):
                                            unmovable_dict.pop((check_self_tile_num((self.pos[0] + -40 * X, self.pos[1]))))
                                            add_powerup((self.pos[0] + -40 * X, self.pos[1]))
                        break
                    else:
                        red_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                for X in range(0, self.power + 1):
                    explosion = Explosion((self.pos[0] + 40 * X, self.pos[1]), 
                                          red_explosion_image, red_explosion_info, self.power)
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))) and indestructable_tiles[check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))] == True:
                        break
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))) and indestructable_tiles[check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))] == False:
                        indestructable_tiles[check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))] = None
                        red_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                        for barrel in all_barrels:
                            if tuple(barrel.pos) == (self.pos[0] + 40 * X, self.pos[1]):
                                all_barrels.remove(barrel)
                                for barrel in all_unmovable:
                                    if tuple(barrel.pos) == (self.pos[0] + 40 * X, self.pos[1]):
                                        all_unmovable.remove(barrel)
                                        if unmovable_dict.has_key((check_self_tile_num((self.pos[0] + 40 * X, self.pos[1])))):
                                            unmovable_dict.pop((check_self_tile_num((self.pos[0] + 40 * X, self.pos[1]))))
                                            add_powerup((self.pos[0] + 40 * X, self.pos[1]))
                        break
                    else:
                        red_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                for Y in range(0, self.power + 1):
                    explosion = Explosion((self.pos[0], self.pos[1] + Y * -40), 
                                          red_explosion_image, red_explosion_info, self.power)
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))) and indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))] == True:
                        break
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))) and indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))] == False:
                        red_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                        indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * - 40))] = None
                        for barrel in all_barrels:
                            if tuple(barrel.pos) == (self.pos[0], self.pos[1] + Y * -40):
                                all_barrels.remove(barrel)
                                for barrel in all_unmovable:
                                    if tuple(barrel.pos) == (self.pos[0], self.pos[1] + Y * -40):
                                        all_unmovable.remove(barrel)
                                        if unmovable_dict.has_key((check_self_tile_num((self.pos[0], self.pos[1] + Y * -40)))):
                                            unmovable_dict.pop((check_self_tile_num((self.pos[0], self.pos[1] + Y * -40))))
                                            add_powerup((self.pos[0], self.pos[1] + Y * -40))
                        break
                    else:
                        red_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                for Y in range(0, self.power + 1):
                    explosion = Explosion((self.pos[0], self.pos[1] + Y * 40), 
                                          red_explosion_image, red_explosion_info, self.power)
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))) and indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))] == True:
                        break
                    if indestructable_tiles.has_key(check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))) and indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))] == False:
                        red_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
                        indestructable_tiles[check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))] = None
                        for barrel in all_barrels:
                            if tuple(barrel.pos) == (self.pos[0], self.pos[1] + Y * 40):
                                all_barrels.remove(barrel)
                                for barrel in all_unmovable:
                                    if tuple(barrel.pos) == (self.pos[0], self.pos[1] + Y * 40):
                                        all_unmovable.remove(barrel)
                                        if unmovable_dict.has_key((check_self_tile_num((self.pos[0], self.pos[1] + Y * 40)))):
                                            unmovable_dict.pop((check_self_tile_num((self.pos[0], self.pos[1] + Y * 40))))
                                            add_powerup((self.pos[0], self.pos[1] + Y * 40))
                        break
                    else:
                        red_explosions.add(explosion)
                        bomb_sound.rewind()
                        bomb_sound.play()
            
            # Update Dictionary of Tiles-Item
            tile_center_pos = check_self_tile_pos(self.pos)
            tile_center_num = check_self_tile_num(self.pos)
            tiles_with_items[tile_center_pos] = False
            unmovable_dict.pop(tile_center_num)
            return True


        elif self.timer >= self.lifespan:
            self.age = 2
            
        elif (self.timer % 10 == 0):
            self.age = (self.age + 1) % 2          
            
class Explosion:
    def __init__(self, pos, image, info, power, timer = 0, age = None):
        self.pos = pos
        self.image = image
        self.power = power
        self.timer = timer
        self.age = age

        self.image_size = info.get_size()
        self.lifespan = info.get_lifespan()

        self.dim = (self.pos[0] - self.image_size[0]/2.0, self.pos[1] - self.image_size[1]/2.0, 
                    self.pos[0] + self.image_size[1]/2.0, self.pos[1] + self.image_size[0]/2.0)
        self.image_center = info.get_center()
        self.radius = info.get_radius()        
        
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, 
                                       self.pos, self.image_size)
        self.update()
    
    def update(self):
        self.timer += 1
        if self.timer >= self.lifespan:
            return True
    def collide(self, other_object):
        two_object_distance = dist(self.pos, other_object.pos)
        two_object_radius = self.radius + other_object.radius
        return two_object_radius > two_object_distance[0] and two_object_radius > two_object_distance[1]
        
class Tile:
    def __init__(self, pos, info, image = None, destructable = False):
        self.pos = [pos[0], pos[1]]
        if image:
            self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.destructable = destructable
        # NEEDS FOUR DIMENSIONS
        self.dim = (self.pos[0] - self.image_size[0]/2.0, self.pos[1] - self.image_size[1]/2.0, 
                    self.pos[0] + self.image_size[1]/2.0, self.pos[1] + self.image_size[0]/2.0)
        
        
    def get_destructable(self):
        return self.destructable
    def get_pos(self):
        return self.pos
    
    def draw(self, canvas):
        if self.image != None:
            canvas.draw_image(self.image, self.image_center, 
                          self.image_size, self.pos, self.image_size)
    
    # Return if there is an item on the tile
    
    # Collision
    def collide(self, other_object):
        two_object_distance = dist(self.pos, other_object.pos)
        two_object_radius = self.radius + other_object.radius
        return two_object_radius > two_object_distance[0] and two_object_radius > two_object_distance[1]
    
    def collide_get_distance_X(self, other_object):
        two_object_distance = dist(self.pos, other_object.pos)
        two_object_radius = self.radius + other_object.radius
        two_object_overlap_X = two_object_radius - two_object_distance[0]
        return two_object_overlap_X

    def collide_get_distance_Y(self, other_object):
        two_object_distance = dist(self.pos, other_object.pos)
        two_object_radius = self.radius + other_object.radius
        two_object_overlap_Y = two_object_radius - two_object_distance[1]
        return two_object_overlap_Y
            
class Button:
    def __init__(self, pos, info, image, page = None, timer = 0, pressed = False):
        global started, current_page, ended
        self.pos = pos
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.page = page
        self.timer = timer
        self.pressed = pressed
        
    def draw(self, canvas):
        if self.pressed == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, (self.image_size[0]/2, self.image_size[1]/2))
        if self.pressed == True:
            canvas.draw_image(self.image, (self.image_center[0] * 3, self.image_center[1]), self.image_size, self.pos, (self.image_size[0]/2, self.image_size[1]/2))
            self.update()
        
    def update(self):
        global started, ended
        if self.timer > 10:
            self.timer = 0
        self.pressed = True
        self.timer += 1
        if self.timer > 10:
            self.pressed = False
            # save score button -> ended -> false
            if self == save_score_button_class:
                ended = False
                started = False
            # home button -> ended -> false; started -> fals
            if self == home_button_class:
                ended = False
                started = False
                
            if self == play_button_class:
                started = True
                ended = False
                restart_game()
                
            current_page_update(self.page)


def current_page_update(page):
    global current_page
    current_page = page
                             
class Powerup:
    def __init__(self, pos, info, image, add_life = 0, add_bombs = 0, add_range= 0, add_speed= 0, add_throw = None, add_walk_over = None, coin = 0):
        self.pos = pos
        self.info = info
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.add_life = add_life
        self.add_bombs = add_bombs
        self.add_range = add_range
        self.add_speed = add_speed
        self.add_throw = add_throw
        self.add_walk_over = add_walk_over
        self.coin = coin
        
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, (self.image_size[0], self.image_size[1]))
    
    def update(self):
        pass
    
    def get_life(self):
        return self.add_life
    
    def get_bombs(self):
        return self.add_bombs
    
    def get_range(self):
        return self.add_range
    
    def get_speed(self):
        return self.add_speed
    
    def get_throw(self):
        return self.add_throw
    
    def get_walk(self):
        return self.add_walk_over
    
    def get_coin(self):
        return self.coin
    
    def collide(self, other_object):
        two_object_distance = dist(self.pos, other_object.pos)
        two_object_radius = self.radius + other_object.radius
        return two_object_radius > two_object_distance[0] and two_object_radius > two_object_distance[1]

################# H A N D L E R S #################

# Mouse Handler
def mouse_handler(position):
    global started, ended, highscore_board, player_one_name, player_two_name, current_page
    print current_page
    if started == False and ended != True:
        # There are many pages when started = False
        # Home page/splash screen -> Instructions + Highscore
        if current_page == "home_page":
            if position[0] >= (1081/2 - instructions_info.size[0]/4) and position[0] <= (1081/2 + instructions_info.size[0]/4) and position[1] >= (550 - instructions_info.size[1]/4) and position[1] <= (550 + instructions_info.size[1]/4):
                instructions_button.update()
            if position[0] >= (1081/2 - highscore_button_info.size[0]/4) and position[0] <= (1081/2 + highscore_button_info.size[0]/4) and position[1] >= (600 - highscore_button_info.size[1]/4) and position[1] <= (600 + highscore_button_info.size[1]/4):
                highscore_button_class.update()		
        # Instructions -> Next, Play, Home
        if current_page == "instructions_page":
            if position[0] >= (700 - next_button_info.size[0]/4) and position[0] <= (700 + next_button_info.size[0]/4) and position[1] >= (580 - next_button_info.size[1]/4) and position[1] <= (580 + next_button_info.size[1]/4):
                next_button_class.update()
            if position[0] >= (790 - play_button_info.size[0]/4) and position[0] <= (790 + play_button_info.size[0]/4) and position[1] >= (580 - play_button_info.size[1]/4) and position[1] <= (580 + play_button_info.size[1]/4):
                play_button_class.update()
            if position[0] >= (950 - home_button_info.size[0]/4) and position[0] <= (950 + home_button_info.size[0]/4) and position[1] >= (680 - home_button_info.size[1]/4) and position[1] <= (680 + home_button_info.size[1]/4):
                home_button_class.update()		
        # Instructions 2 -> Play, Home
        if current_page == "instructions_page_two":
            if position[0] >= (790 - play_button_info.size[0]/4) and position[0] <= (790 + play_button_info.size[0]/4) and position[1] >= (580 - play_button_info.size[1]/4) and position[1] <= (580 + play_button_info.size[1]/4):
                play_button_class.update()
            if position[0] >= (950 - home_button_info.size[0]/4) and position[0] <= (950 + home_button_info.size[0]/4) and position[1] >= (680 - home_button_info.size[1]/4) and position[1] <= (680 + home_button_info.size[1]/4):
                home_button_class.update()		
        # Highscore -> Play, Home
        if current_page == "highscore_page":
            if position[0] >= (790 - play_button_info.size[0]/4) and position[0] <= (790 + play_button_info.size[0]/4) and position[1] >= (580 - play_button_info.size[1]/4) and position[1] <= (580 + play_button_info.size[1]/4):
                play_button_class.update()
            if position[0] >= (950 - home_button_info.size[0]/4) and position[0] <= (950 + home_button_info.size[0]/4) and position[1] >= (680 - home_button_info.size[1]/4) and position[1] <= (680 + home_button_info.size[1]/4):
                home_button_class.update()
    if started == True:
        pass
        # No buttons yet
    if ended == True:
        # started (game in progess) should automatically change to -> started = False
        # First, Game over screen is displayed -> started = False
        # Only one screen shows when ended = True: Game over -> 
        # buttons: save score (highscore), Home -> I want to make it so that clicking either renders ended => False
        # if any of these buttons are pressed, ended = False, started = False (back to reset)
            if position[0] >= (950 - home_button_info.size[0]/4) and position[0] <= (950 + home_button_info.size[0]/4) and position[1] >= (680 - home_button_info.size[1]/4) and position[1] <= (680 + home_button_info.size[1]/4):
                home_button_class.update()
            if position[0] >= (1081/2 - save_score_button_info.size[0]/4) and position[0] <= (1081/2 + save_score_button_info.size[0]/4) and position[1] >= (550 - save_score_button_info.size[1]/4) and position[1] <= (550 + save_score_button_info.size[1]/4):
                save_score_button_class.update()
                if blue_bomber.get_score() > red_bomber.get_score():
                    if player_one_name != None:
                        highscore_board.append((blue_bomber.get_score(), player_one_name))
                    else: 
                        print "Enter name for Blue Bomber next time"
                        highscore_board.append((blue_bomber.get_score(), "Blue"))    
                elif red_bomber.get_score() > blue_bomber.get_score():
                    if player_two_name != None:
                        highscore_board.append((red_bomber.get_score(), player_two_name))
                    else:
                        print "Enter name for Red Bomber next time"
                        highscore_board.append((red_bomber.get_score(), "Red"))
                elif red_bomber.get_score() == blue_bomber.get_score():
                    if player_one_name != None and player_two_name != None:
                        highscore_board.append((blue_bomber.get_score(), player_one_name))
                        highscore_board.append((red_bomber.get_score(), player_two_name))
                    else: 
                        print "Enter name for Blue and Red Bombers next time"
                        highscore_board.append((blue_bomber.get_score(), "Blue"))
                        highscore_board.append((red_bomber.get_score(), "Red"))
                highscore_board.sort()
                highscore_board.reverse()
                
                
# Draw Handler
def draw(canvas):
    canvas.draw_image(grid, (1081/2, 760/2), (1081,760), (1081/2, 380), (1081,760))
    if started == False and ended == False:
        if current_page == "home_page":
            canvas.draw_image(splash_screen_image, splash_screen_info.center, splash_screen_info.size, (1081/2, 379), (splash_screen_info.size[0]/1.06, splash_screen_info.size[1]/1.06))
            instructions_button.draw(canvas)
            highscore_button_class.draw(canvas)
        if current_page == "instructions_page":
            canvas.draw_image(instructions_page, instructions_page_info.center, instructions_page_info.size, (1081/2, 379), (instructions_page_info.size[0]/1.06, instructions_page_info.size[1]/1.06))
            next_button_class.draw(canvas)
            play_button_class.draw(canvas)
            home_button_class.draw(canvas)
        if current_page == "instructions_page_two":
            canvas.draw_image(instructions_page_two, instructions_page_info.center, instructions_page_info.size, (1081/2, 379), (instructions_page_info.size[0]/1.06, instructions_page_info.size[1]/1.06))
            play_button_class.draw(canvas)
            home_button_class.draw(canvas)
        if current_page == "highscore_page":
            canvas.draw_image(highscore_page, highscore_page_info.center, highscore_page_info.size, (1081/2, 379), (highscore_page_info.size[0]/1.06, highscore_page_info.size[1]/1.06))
            ranking = 0
            for item in highscore_board:
                ranking += 1
                points = item[0]
                name = item[1]
                if ranking <= 7:
                    canvas.draw_text(str(points), (360, 244 + ranking * 40), 30, "White", "sans-serif")
                    canvas.draw_text(str(name), (490, 244 + ranking * 40), 30, "White", "sans-serif")
            play_button_class.draw(canvas)
            home_button_class.draw(canvas)
    if ended == True and started == False:
        # Draw Game Over (Three varieties)
        if blue_bomber.get_score() > red_bomber.get_score() and save_score_button_class.page != True:
            canvas.draw_image(game_over_blue_image, game_over_info.center, game_over_info.size, (1081/2, 379), (game_over_info.size[0]/1.06, game_over_info.size[1]/1.06))
            canvas.draw_text("Score: " + str(blue_bomber.get_score()), (450, 500), 50, "Black", 'sans-serif')
            save_score_button_class.draw(canvas)
            home_button_class.draw(canvas)
        elif blue_bomber.get_score() < red_bomber.get_score() and save_score_button_class.page != True:
            canvas.draw_image(game_over_red_image, game_over_info.center, game_over_info.size, (1081/2, 379), (game_over_info.size[0]/1.06, game_over_info.size[1]/1.06))
            canvas.draw_text("Score: " + str(red_bomber.get_score()), (450, 500), 50, "Black", 'sans-serif')
            save_score_button_class.draw(canvas)
            home_button_class.draw(canvas)
        elif blue_bomber.get_score() == red_bomber.get_score() and save_score_button_class.page != True:
            canvas.draw_image(game_over_tied_image, game_over_info.center, game_over_info.size, (1081/2, 379), (game_over_info.size[0]/1.06, game_over_info.size[1]/1.06))
            save_score_button_class.draw(canvas)
            home_button_class.draw(canvas)	
                
    elif started == True:
        # Draw bombs
        process_sprite_group(blue_bomb_group, canvas) 
        process_sprite_group(red_bomb_group, canvas)
    
        # Draw Barrels
        for barrel in all_barrels:
            barrel.draw(canvas)
    
        # Draw Blue Bomberman
        blue_bomber.draw(canvas)
        blue_bomber.update()
        
        # Draw Red Bomberman
        red_bomber.draw(canvas)
        red_bomber.update()
        
    
        # Draw Explosions
        process_sprite_group(blue_explosions, canvas)
        process_sprite_group(red_explosions, canvas)
        
        # Draw Powerups
        for powerup in all_powerups:
            powerup.draw(canvas)
      
########## H E L P E R   F U N C T I O N S ###########
def reset_all_buttons():
    for button in all_buttons:
        button.page = False
# Checking Self Pos in Regard to Tile Pos and Return Current Tile Center
def check_self_tile_pos(position):
    if int(position[0])%40 >= 8 and int(position[0])%40 <= 32 and int(position[1])%40 >= 8 and int(position[1])%40 <= 32:
        tile_number = (int(position[0])/40, int(position[1])/40)
        tile_center = (tile_number[0] * 40 + 20, tile_number[1] * 40 + 19)
        return tile_center
    else:
        return None    

def check_self_tile_num(position):
    tile_number = (int(position[0])/40, int(position[1])/40)
    return tile_number

# Adding Powerups
def add_powerup(pos):
#(self, pos, info, image, add_life = 0, add_bombs = 0, add_range= 0, add_speed= 0, add_throw = None, add_walk_over = None):

    powerup_num = random.randrange(0,31)
    # Add Life
    if powerup_num == 0:
        a_powerup = Powerup(pos, add_life_info, add_life_image, 1, 0, 0, 0, None, None, 25)
        all_powerups.add(a_powerup)
    # Add Bomb
    if powerup_num == 1 or powerup_num == 10 or powerup_num == 11:
        a_powerup = Powerup(pos, add_bomb_info, add_bomb_image, 0, 1, 0, 0, None, None, 25)
        all_powerups.add(a_powerup)
    # Add Range
    if powerup_num == 2 or powerup_num == 8 or powerup_num == 9:
        a_powerup = Powerup(pos, add_range_info, add_range_image, 0, 0, 1, 0, None, None, 25)
        all_powerups.add(a_powerup)
    # Add Speed
    if powerup_num == 3 or powerup_num == 4 or powerup_num == 7:
        a_powerup = Powerup(pos, add_speed_info, add_speed_image, 0, 0, 0, 1, None, None, 25)
        all_powerups.add(a_powerup)
    # Walk Over Bomb
    if powerup_num == 5:
        a_powerup = Powerup(pos, add_walk_over_info, add_walk_over_image, 0, 0, 0, 0, None, True, 25)
        all_powerups.add(a_powerup)             
    # Add Coin
    if powerup_num == 6:
        a_powerup = Powerup(pos, coin_info, coin_image, 0, 0, 0, 0, None, None, 100)
        all_powerups.add(a_powerup)
      
# Setting Names
def set_player_one_name(name):
    global player_one_name
    player_one_name = name
def set_player_two_name(name):
    global player_two_name
    player_one_name = name

########## C O L L I S I O N    D E T E C T I O N ############

# STILL A WORK IN PROGRESS
# Single Item vs Group
def collide(an_object, other_object):
    collided = False
    if an_object.collide(other_object):
        collided = True
    return collided
def group_collide(group, other_object):
    collided = False
    for item in set(group):
        if item.collide(other_object):
            collided = True
    return collided
def group_collide_distance_X(group, other_object):
    for item in set(group):
        if item.collide(other_object):
            overlap_X = item.collide_get_distance_X(other_object)
    return overlap_X
def group_collide_distance_Y(group, other_object):
    for item in set(group):
        if item.collide(other_object):
            overlap_Y = item.collide_get_distance_X(other_object)
    return overlap_Y   

# Processing the Groups of Bombs
def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        
        if sprite.update():
            group.remove(sprite)

# Key handler for bomber movement:
def bomber_move_handler(key):
    global blue_bomber, red_bomber, started
    blue_bomber_speed = blue_bomber.get_speed()
    red_bomber_speed = red_bomber.get_speed()
      
    # Starting the Game
    if started == False and ended == False and current_page == "home_page":
        if key != simplegui.KEY_MAP["x"]:
            started = True
            restart_game()
    elif started == True:        
    # Blue Bomber
        if key==simplegui.KEY_MAP["a"]:
            blue_bomber.vel[0] -= blue_bomber_speed
            blue_bomber.vel[1] = 0
        if key==simplegui.KEY_MAP["d"]:
            blue_bomber.vel[0] += blue_bomber_speed
            blue_bomber.vel[1] = 0
        if key==simplegui.KEY_MAP["w"]:
            blue_bomber.vel[1] -= blue_bomber_speed   
            blue_bomber.vel[0] = 0
        if key==simplegui.KEY_MAP["s"]:
            blue_bomber.vel[1] += blue_bomber_speed
            blue_bomber.vel[0] = 0
        if key==simplegui.KEY_MAP["f"]:
            blue_bomber.drop()
    # Red Bomber
        if key==simplegui.KEY_MAP["left"]:
            red_bomber.vel[0] -= red_bomber_speed
            red_bomber.vel[1] = 0
        if key==simplegui.KEY_MAP["right"]:
            red_bomber.vel[0] += red_bomber_speed
            red_bomber.vel[1] = 0
        if key==simplegui.KEY_MAP["up"]:
            red_bomber.vel[1] -= red_bomber_speed   
            red_bomber.vel[0] = 0
        if key==simplegui.KEY_MAP["down"]:
            red_bomber.vel[1] += red_bomber_speed
            red_bomber.vel[0] = 0
        if key==simplegui.KEY_MAP["m"]:
            red_bomber.drop()
    
def bomber_stop_handler(key):
    global blue_bomber, red_bomber
    
    # Blue Bomber
    if key == simplegui.KEY_MAP["a"] or key == simplegui.KEY_MAP["d"]:
        blue_bomber.vel[0] = 0
    elif key==simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        blue_bomber.vel[1] = 0
    
    # Red Bomber
    global red_bomber
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        red_bomber.vel[0] = 0
    elif key==simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        red_bomber.vel[1] = 0

############# I N I T I A L I Z I N G   S T U F F #############

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Playing With Fire!", 1081,760)

# Restart Game Function
def restart_game():
    global blue_bomber, blue_bomb_group, red_bomber, red_bomb_group, blue_explosions, red_explosions, all_powerups, all_barrels, all_unmovable, tiles_with_items, indestructable_tiles, unmovable_dict
    # Initialize Bomber
    blue_bomber = Bomber([300.0, 61.0], [0, 0], blue_bomber_image, blue_bomber_left_image, blue_bomber_right_image, blue_bomber_up_image,
                     blue_bomber_info, "Blue", lives, 0, 2.0)
    blue_bomb_group = set()

    red_bomber = Bomber([1020.0, 698.0], [0, 0], red_bomber_image, red_bomber_left_image, red_bomber_right_image, red_bomber_up_image,
                    red_bomber_info, "Red", lives, 1, 2.0)
    red_bomb_group = set()
    
    blue_explosions = set()
    red_explosions = set()
    # Initializing Dictionaries
    tiles_with_items = {}
    indestructable_tiles = {}
    unmovable_dict = {}

    # Initializing Powerups
    all_powerups = set()

    # Making a Set for Barrels
    all_barrels = set()

    for n in range(0,12):
        x = random.choice(range(9,24))
        barrel = Tile((x * 40 + 20, 40 + 19), barrel_info, barrel_image, True)
        all_barrels.add(barrel)
        indestructable_tiles[(x,1)] = False
    for n in range(0,12):
        x = random.choice(range(9,24))
        barrel = Tile((x * 40 + 20, 17 * 40 + 19), barrel_info, barrel_image, True)
        all_barrels.add(barrel)
        indestructable_tiles[(x,17)] = False
    for n in range(0,13):
        for y in range(3,17,2):
            x = random.choice(range(7,26))
            barrel = Tile((x * 40 + 20, y * 40 + 19), barrel_info, barrel_image, True)
            all_barrels.add(barrel)
            indestructable_tiles[(x,y)] = False
    for n in range(0,13):
        for x in range(9,24,2):
            y = random.choice(range(1,18))
            barrel = Tile((x * 40 + 20, y * 40 + 19), barrel_info, barrel_image, True)
            all_barrels.add(barrel)
            indestructable_tiles[(x,y)] = False
            
    # Floor and Grid Tiles
    # Making a Set of the Grid Tiles and Floor Tiles
    list_of_grid_tiles_x = [8, 10, 12, 14, 16, 18, 20, 22, 24]
    list_of_grid_tiles_y = [2, 4, 6, 8, 10, 12, 14, 16]
    
    all_tiles = set()
    
    for x in list_of_grid_tiles_x:
        for y in list_of_grid_tiles_y:
            tile = Tile([x*40 + 20, y*40 + 19], tile_info)
            all_tiles.add(tile)
            indestructable_tiles[(x,y)] = True
            
    for x in range(7, 26):
        tile = Tile([x*40 + 20, 19], tile_info)
        all_tiles.add(tile)
        tile = Tile([x*40 + 20, 18*40 + 19], tile_info)
        indestructable_tiles[(x,0)] = True
        all_tiles.add(tile)
        indestructable_tiles[(x,18)] = True
    
    for y in range(19):
        tile = Tile([6*40 + 20, y*40 + 19], tile_info)
        all_tiles.add(tile)
        indestructable_tiles[(6,y)] = True
        tile = Tile([26*40 + 20, y*40 + 19], tile_info)
        all_tiles.add(tile)
        indestructable_tiles[(26,y)] = True
    
    all_floor = set()
    
    list_of_floor_tiles_x = [7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27]
    list_of_floor_tiles_y = [1, 3, 5, 7, 9, 11, 13, 15, 17]
    for x in list_of_floor_tiles_x:
        for y in range(1, 18):
            floor = Tile([x*40 + 20, y*40 + 19], tile_info)
            all_floor.add(floor)
    
    for y in list_of_floor_tiles_y:
        for x in range(7, 26):
            floor = Tile([x*40 + 20, y*40 + 19], tile_info)
            all_floor.add(floor)

    all_unmovable = set()
    all_unmovable = all_barrels.union(all_tiles)
    unmovable_dict = dict(tiles_with_items.items() + indestructable_tiles.items())

    # Making New buttons
    all_buttons = set()
    instructions_button = Button((1081/2, 550), instructions_info, instructions, "instructions_page")
    all_buttons.add(instructions_button)
    highscore_button_class = Button((1081/2, 600), highscore_button_info, highscore_button, "highscore_page")
    all_buttons.add(highscore_button_class)
    play_button_class = Button((790, 580), play_button_info, play_button, "game_page")
    all_buttons.add(play_button_class)
    next_button_class = Button((700, 580), next_button_info, next_button, "instructions_page_two")
    all_buttons.add(next_button_class)
    save_score_button_class = Button((1081/2, 550), save_score_button_info, "save_score_button, highscore_page")
    all_buttons.add(save_score_button_class)
    home_button_class = Button((950, 680), home_button_info, home_button, "home_page")
    all_buttons.add(home_button_class)

# Initializing Buttons
all_buttons = set()
instructions_button = Button((1081/2, 550), instructions_info, instructions, "instructions_page")
all_buttons.add(instructions_button)
highscore_button_class = Button((1081/2, 600), highscore_button_info, highscore_button, "highscore_page")
all_buttons.add(highscore_button_class)
play_button_class = Button((790, 580), play_button_info, play_button, "game_page")
all_buttons.add(play_button_class)
next_button_class = Button((700, 580), next_button_info, next_button, "instructions_page_two")
all_buttons.add(next_button_class)
save_score_button_class = Button((1081/2, 550), save_score_button_info, save_score_button, "highscore_page")
all_buttons.add(save_score_button_class)
home_button_class = Button((950, 680), home_button_info, home_button, "home_page")
all_buttons.add(home_button_class)

# Initializing Other Stuff

# Initialize Bomber
blue_bomber = Bomber([300.0, 61.0], [0, 0], blue_bomber_image, blue_bomber_left_image, blue_bomber_right_image, blue_bomber_up_image,
                     blue_bomber_info, "Blue", lives, 0, 2.0)
blue_bomb_group = set()
red_bomber = Bomber([1020.0, 698.0], [0, 0], red_bomber_image, red_bomber_left_image, red_bomber_right_image, red_bomber_up_image,
                    red_bomber_info, "Red", lives, 1, 2.0)
red_bomb_group = set()

# Initializing explosion set
blue_explosions = set()
red_explosions = set()

# Initializing Powerups
all_powerups = set()

# Making a Set for Barrels
all_barrels = set()

for n in range(0,12):
    x = random.choice(range(9,24)) 
    barrel = Tile((x * 40 + 20, 40 + 19), barrel_info, barrel_image, True)
    all_barrels.add(barrel)
    indestructable_tiles[(x,1)] = False
for n in range(0,12):
    x = random.choice(range(9,24))
    barrel = Tile((x * 40 + 20, 17 * 40 + 19), barrel_info, barrel_image, True)
    all_barrels.add(barrel)
    indestructable_tiles[(x,17)] = False
for n in range(0,13):
    for y in range(3,17,2):
        x = random.choice(range(7,26))
        barrel = Tile((x * 40 + 20, y * 40 + 19), barrel_info, barrel_image, True)
        all_barrels.add(barrel)
        indestructable_tiles[(x,y)] = False
for n in range(0,13):
    for x in range(9,24,2):
        y = random.choice(range(1,18))
        barrel = Tile((x * 40 + 20, y * 40 + 19), barrel_info, barrel_image, True)
        all_barrels.add(barrel)
        indestructable_tiles[(x,y)] = False
# Making a Set of the Grid Tiles and Floor Tiles
list_of_grid_tiles_x = [8, 10, 12, 14, 16, 18, 20, 22, 24]
list_of_grid_tiles_y = [2, 4, 6, 8, 10, 12, 14, 16]

all_tiles = set()

for x in list_of_grid_tiles_x:
    for y in list_of_grid_tiles_y:
        tile = Tile([x*40 + 20, y*40 + 19], tile_info)
        all_tiles.add(tile)
        indestructable_tiles[(x,y)] = True
        
for x in range(7, 26):
    tile = Tile([x*40 + 20, 19], tile_info)
    all_tiles.add(tile)
    tile = Tile([x*40 + 20, 18*40 + 19], tile_info)
    indestructable_tiles[(x,0)] = True
    all_tiles.add(tile)
    indestructable_tiles[(x,18)] = True

for y in range(19):
    tile = Tile([6*40 + 20, y*40 + 19], tile_info)
    all_tiles.add(tile)
    indestructable_tiles[(6,y)] = True
    tile = Tile([26*40 + 20, y*40 + 19], tile_info)
    all_tiles.add(tile)
    indestructable_tiles[(26,y)] = True

all_floor = set()

list_of_floor_tiles_x = [7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27]
list_of_floor_tiles_y = [1, 3, 5, 7, 9, 11, 13, 15, 17]
for x in list_of_floor_tiles_x:
    for y in range(1, 18):
        floor = Tile([x*40 + 20, y*40 + 19], tile_info)
        all_floor.add(floor)

for y in list_of_floor_tiles_y:
    for x in range(7, 26):
        floor = Tile([x*40 + 20, y*40 + 19], tile_info)
        all_floor.add(floor)


# Register Handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(bomber_move_handler)
frame.set_keyup_handler(bomber_stop_handler)
frame.set_mouseclick_handler(mouse_handler)

frame.add_input("Player One Name", set_player_one_name, 150)
frame.add_input("Player Two Name", set_player_two_name, 150)

# Start the frame animation
def music_play():
    background_sound.rewind()
    background_sound.play()

frame.start()
all_unmovable = all_barrels.union(all_tiles)

unmovable_dict = dict(tiles_with_items.items() + indestructable_tiles.items())
timer = simplegui.create_timer(196000, music_play)
background_sound.play()
timer.start()
