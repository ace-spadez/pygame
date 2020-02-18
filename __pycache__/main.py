import pygame
pygame.init()

WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
STAGES = 6
gameOver = False
STAGE_WIDTH = WIDTH/STAGES


class Player(pygame.sprite.Sprite):
    jumping = False
    speed = 5
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("pikachu-2.png")
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        pass
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >=HEIGHT:
            self.rect.bottom = HEIGHT



player = Player()
while not gameOver:

    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == pygame.KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == pygame.K_ESCAPE:
                gameOver = True
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == pygame.QUIT:
            gameOver = True
    # pygame.time.delay(40)
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    SCREEN.blit(pygame.image.load("gnd.png"),(0,HEIGHT-80))
    SCREEN.blit(player.surf, player.rect)
    pygame.display.flip()
    SCREEN.fill((0,0,0))
    
    # if pressed_keys[QUIT]:
        # break
    
pygame.quit()


