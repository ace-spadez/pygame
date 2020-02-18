import pygame
import random
import math
import os
import sys
from config import *
# initializing the pygame
pygame.init()

# font classes for score, player name, prommpt
font = pygame.font.Font(MESSAGE_FONT, 40)  # taking font face from config.py
font_ = pygame.font.Font(MESSAGE_FONT, 18)

# Configuration variables
WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode(
    (WIDTH, HEIGHT))
JUMP_VEL = 12
gameOver = False
STAGE_WIDTH = WIDTH/STAGES

# loading all the sprites
explosion_sound = pygame.mixer.Sound("music/explosion.ogg")
# background music to be played entire game
pygame.mixer.music.load("music/background_music.ogg")
pygame.mixer.music.play(-1)  # loopoijg indefinitely
# loading the ground where player stands
gnd = [pygame.image.load("images/gnd.png"),
       pygame.image.load("images/gnd-1.png")]
gnd_c = 0
# FIREBALL =[pygame.image.load("fireball32x32.png"),pygame.image.load("fireball132x32.png"),pygame.image.load("fireball232x32.png")]
EXPLOSION = [
    pygame.image.load("images/explosion-0.png"), pygame.image.load(
        "images/explosion-2.png"), pygame.image.load("images/explosion-3.png"),
    pygame.image.load("images/explosion-4.png"), pygame.image.load(
        "images/explosion-5.png"), pygame.image.load("images/explosion-6.png"),
]

# creating the lists/ Groups
dragon_list = []
explosions = pygame.sprite.Group() #this will store explosions
fireball = pygame.sprite.Group() #this will store fireballs
all_sprites = pygame.sprite.Group()
gems = pygame.sprite.Group() #for storing gems
enemies = pygame.sprite.Group() #for storing bombs

# generic function to check collisions


def check_collision(
        rect1,
        rect2):
    if (rect2.right > rect1.left
        and rect1.right > rect2.left
        and rect1.bottom > rect2.top
            and rect1.top < rect2.bottom):
        return True
    return False

# function to make a new window to start the game


def newGame():
    global dragon_list
    global explosions
    global fireball
    global all_sprites
    global gems
    global enemies
    dragon_list = []
    explosions = pygame.sprite.Group()
    fireball = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    gems = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    for i in range(STAGES):
        for j in range(5):
            gems.add(Gem(random.randint(40, WIDTH-200), STAGE_WIDTH*i-16,      #creating random gems
                         random.choice(["score", "score", "heart", "score"])))
    for i in range(STAGES):
        for j in range(BOMB_COUNT):  #creating random enemies
            enemies.add(Enemy(random.randint(40, WIDTH-200), STAGE_WIDTH*i-32))
    # all_sprites.add(player)
    for i in range(STAGES):
        dragon_list += [Dragon(i)] #creating dragons

# class for creating health and scoring gems


class Gem(pygame.sprite.Sprite):
    def __init__(
            self, x, y,
            name):
        super(Gem, self).__init__()
        self.x = x
        self.y = y
        self.name = name
        if name == "score":
            self.surf = pygame.image.load("images/gem-black.png")
        if name == "heart":
            self.surf = pygame.image.load("images/heart.png")
        self.rect = self.surf.get_rect(
            center=(
                x,
                y,
            )
        )

    def update(self, player):
        if check_collision(player.rect, self.rect):
            self.kill()
            if self.name == "heart":
                player.health += 10 #updating health after collectiong health gems
                if player.health > 64:
                    player.health = 64
            if self.name == "score":
                player.score += 1   #updating player scoring after collecting score gems

# class for creating enemiy bombs


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy, self).__init__()
        self.x = x
        self.y = y
        self.surf = pygame.image.load("images/death.png")
        self.rect = self.surf.get_rect(
            center=(
                x,
                y,
            )
        )

    def update(self, player):
        if check_collision(self.rect, player.rect):
            # pygame.mixer.Sound.stop(explosion_sound)
            self.kill()
            player.health -= 5 #reducing health after enemy collision
            explosions.add(Explosion(self.rect.centerx, self.rect.centery)) #explosion after collison with enemy
            # pygame.mixer.Sound.play(explosion_sound)
            # explosion_sound.play()/

        # player.score +=1

# class for creating players


class Player(pygame.sprite.Sprite):
    rounds = 0
    direc = 1
    alive = True
    score = 0
    time = 0
    # global gameOver
    health = 64
    jumping = False
    stage = 0
    speed = 5
    jump_vel = -JUMP_VEL
    jump_acc = 0.4

    def __init__(self, direc, name):
        super(Player, self).__init__()
        self.direc = direc
        self.name = name
        if STAGES > 8:
            self.surf = pygame.image.load("images/pikachu.png")
        else:
            self.surf = pygame.image.load("images/pikachu-2.png")
        if direc == 1:
            self.rect = self.surf.get_rect(
                center=(
                    0,
                    HEIGHT-32,
                )
            )
        else:
            self.rect = self.surf.get_rect(
                center=(
                    0,
                    STAGE_WIDTH-32
                )
            )

    def update(self, pressed_keys):
        if self.direc == 1 and self.rect.bottom < 0 and self.stage != 0:
            self.rounds += 1
            self.stage = 0
            self.rect.bottom = WIDTH
            newGame()
            return
        if self.direc == -1 and self.rect.top > HEIGHT and self.stage != 0:
            self.rounds += 1
            self.stage = 0
            newGame()
            return
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if not self.jumping and pressed_keys[pygame.K_SPACE]:
            self.stage += 1
            self.jumping = True
        if self.jumping:
            self.jump_vel += self.jump_acc
            self.rect.move_ip(0, self.jump_vel)
            if self.rect.bottom > HEIGHT-STAGE_WIDTH*self.stage and self.jump_vel > 0 and self.direc == 1:
                self.rect.bottom = HEIGHT-STAGE_WIDTH*self.stage
                self.jump_vel = -JUMP_VEL
                self.jumping = False
            elif self.rect.bottom > HEIGHT-STAGE_WIDTH*(STAGES-1-self.stage) and self.jump_vel > 0 and self.direc == -1:
                self.rect.bottom = HEIGHT-STAGE_WIDTH*(STAGES-1-self.stage)
                self.jump_vel = -JUMP_VEL
                self.jumping = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.health < 0:
            explosions.add(Explosion(self.rect.centerx, self.rect.centery))
            self.alive = False
            # self.kill()
        pygame.draw.rect(SCREEN, (0, 0, 0),
                         (self.rect.left, self.rect.top-10, 64, 10))
        pygame.draw.rect(SCREEN, (0, 200, 20), (self.rect.left,
                                                self.rect.top-10, self.health, 10))
        text = font.render(
            f":{self.score} Round:{self.rounds+1}", True, (2, 25, 0))
        SCREEN.blit(pygame.image.load("images/gem-black.png"),(0,0))
        SCREEN.blit(text, (32, 0))
        string = font_.render(f"{self.name}", True, (0, 200, 100))
        SCREEN.blit(string, (self.rect.left, self.rect.top-25))

# class for creating the fire breathing dragons


class Dragon(pygame.sprite.Sprite):
    id = 0
    state = 0
    dir = 1
    rand = random.randint(10, 20)
    frame_rate = 20
    frame_count = 0
    # fire = False
    fire_count = 0

    def __init__(self, id):
        super(Dragon, self).__init__()
        self.surf = pygame.transform.flip(
            pygame.image.load("images/dragon.png"), 1, 0)

        self.rect = self.surf.get_rect(
            center=(
                WIDTH - 32,
                HEIGHT - STAGE_WIDTH*id - STAGE_WIDTH/2,
            )
        )
        self.id = id

    def update(self, player):
        # if self.id <= player.stage+2 and self.id> player.stage-1:
        if self.frame_count > self.frame_rate:
            self.frame_count -= self.frame_rate
            self.rect.move_ip(0, 5*self.dir)
            self.dir = -1 * self.dir
        if self.fire_count > self.rand:
            self.rand = random.randint(50, 100)
            self.fire_count -= self.rand
            fireball.add(FireBall(self.id))
        self.fire_count += 1
        if check_collision(self.rect, player.rect):
            player.health -= 0.2
        self.frame_count += 1

# class for creationg fireballs


class FireBall(pygame.sprite.Sprite):
    id = 0
    turn = 0

    def __init__(self, id):
        super(FireBall, self).__init__()
        # self.surf = pygame.image.load("fireball32x32.png")
        self.surf = pygame.transform.flip(
            pygame.image.load("images/bird.png"), 1, 0)
        if FIREBALL_SPEED == None:
            self.speed = random.random()*5+1
        else:
            self.speed = FIREBALL_SPEED

        self.rect = self.surf.get_rect(
            center=(
                WIDTH-150,
                HEIGHT - STAGE_WIDTH*id-STAGE_WIDTH/2-30,
            )
        )
        self.id = id

    def update(self, player):
        if self.rect.left < 0:
            self.kill()
        self.rect.move_ip(-self.speed-3*player.rounds, 0)
        self.turn = (self.turn+1) % 3
        # self.surf= FIREBALL[self.turn]
        # self.surf= FIREBALL[self.turn]
        if check_collision(self.rect, player.rect):
            self.kill()
            explosions.add(Explosion(self.rect.centerx, self.rect.centery))
            player.health -= 10

# class for creating explosions


class Explosion(pygame.sprite.Sprite):
    frames = 6
    frame_id = 0
    frame_count = 0
    frame_rate = 15

    def __init__(self, x, y):
        super(Explosion, self).__init__()
        # explosion_sound.play()
        pygame.mixer.music.load("images/explosion.ogg")
        pygame.mixer.music.play()
        # pygame.mixer.music.queue("background_music.ogg")
        pygame.mixer.music.load("music/background_music.ogg")
        pygame.mixer.music.play(-1)
        self.x = x
        self.y = y
        self.surf = EXPLOSION[0]
        self.rect = self.surf.get_rect(
            center=(
                x,
                y,
            )
        )

    def update(self, player1):
        self.frame_count += 1
        if self.frame_count < 20:
            return
        self.frame_count -= self.frame_rate
        self.frame_id += 1
        if self.frame_id == 6:
            self.kill()
            return
        self.surf = EXPLOSION[self.frame_id]


# creting 2 players
player1 = Player(1, "player1")
player2 = Player(-1, "player2")
player = None

# the main loop
while not gameOver:
    #checking for the quit presses
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameOver = True
        elif event.type == pygame.QUIT:
            gameOver = True

    #checking for the player
    if(player == None):
        player = player1
        newGame()
    elif not player1.alive and player == player1:
        player = player2
        newGame()
    elif not player2.alive and player == player2:
        #both the players have played
        #displaying hte necessary message
        text = ""
        if(player2.score > player1.score):
            text = f"Player2 won by {player2.score}-{player1.score}"
        elif(player1.score > player2.score):
            text = f"Player1 won by {player1.score}-{player2.score}"
        else:
            text = f"IT's a Draw"
        t = font.render(f"{text}", True, MESSAGE_COLOR)
        SCREEN.blit(t, (WIDTH/2-100, HEIGHT/2-20))
        pygame.display.update()
        pygame.time.delay(4000)
        
        #restaring the game automatically
        player = None
        player1 = Player(1, "player1")
        player2 = Player(-1, "player2")
        continue
    
    #drawing the stages,fireballs, explosions,enemies and the player
    for i in range(STAGES):
        SCREEN.blit(gnd[gnd_c], (0, HEIGHT-STAGE_WIDTH*i-80))
        dragon_list[i].update(player)
        SCREEN.blit(dragon_list[i].surf, dragon_list[i].rect)
    for fireballs in fireball:
        SCREEN.blit(fireballs.surf, fireballs.rect)
        fireballs.update(player)
    for explosion in explosions:
        SCREEN.blit(explosion.surf, explosion.rect)
        explosion.update(player)
    for gem in gems:
        SCREEN.blit(gem.surf, gem.rect)
        gem.update(player)
    for enemy in enemies:
        SCREEN.blit(enemy.surf, enemy.rect)
        enemy.update(player)
    SCREEN.blit(player.surf, player.rect)

    # checking key presses
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    pygame.display.flip()
    SCREEN.fill((255, 255, 255))


# pygame quitting
pygame.quit()
