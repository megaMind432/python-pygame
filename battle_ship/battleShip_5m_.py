# Battle Ship improve Collision
import random
from os import path

import pygame

# Settings
WIDTH = 500
HEIGHT = 600
FPS = 60

# Colors
WHITE = (233, 233, 233)
BLACK = (0, 0, 0)
RED = (233, 0, 0)
GREEN = (0, 233, 0)
BLUE = (0, 0, 233)
YELLOW = (233, 233, 0)
CYAN = (0, 233, 233)
MAGENTA = (233, 0, 233)

# Pygame initialize and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Improve Collision")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((55, 55))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        # update the location for the sprite
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # check edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Mob(pygame.sprite.Sprite):
    # Sprite for the enemy Ship
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((34, 34))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-89, -55)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 5)

    def update(self):
        # update the position for the enemy
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH + 55 or self.rect.left < -55 or self.rect.bottom > HEIGHT + 55:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-89, -55)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(1, 5)


class Bullet(pygame.sprite.Sprite):
    # sprite for the Bullets
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((13, 21))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -13

    def update(self):
        self.rect.y += self.speedy
        # kill if it goes off the display
        if self.rect.bottom < 0:
            self.kill()


# Sprite Group
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
# Game-loop
running = True
while running:
    # keep loop running at right speed
    clock.tick(FPS)
    # Input process(events)
    for event in pygame.event.get():
        # check to see if user close the window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    all_sprites.update()

    # check to see if any of the mobs hits the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything flip the display
    pygame.display.flip()

pygame.quit()
