import pygame, sys
import math
import time
from pygame.locals import *

try:
    import android
except ImportError:
    android = None

pygame.init()

#### setting up the clock
player_circle = pygame.image.load("img/final_circle.png")
# player_rect = player_circle.get_rect()
BLUE = ((0, 0, 255))
clock = pygame.time.Clock()
bullet_delay = 5


def get_angle(pos, control_center):
    center = control_center
    if pos[0] > center[0]:
        if pos[1] < center[1]:
            opposite = float(center[1] - pos[1])
            adjacent = float(pos[0] - center[0])
            rad = math.atan(opposite/adjacent)
    #### quadrant 4
        elif pos[1] > center[1]:
            opposite = float(pos[1] - center[1])
            adjacent = float(pos[0] - center[0])
            rad = 2 * math.pi - math.atan(opposite/adjacent)
        else:
            rad = 0
    elif pos[0] < center[0]:
    ### quadrant 2
        if pos[1] < center[1]:
            opposite = float(center[0] - pos[0])
            adjacent = float(center[1] - pos[1])
            rad = 0.5 * math.pi + math.atan(opposite/adjacent)
    ### quadrant 3
        elif pos[1] > center[1]:
            opposite = float(pos[1] - center[1])
            adjacent = float(center[0] - pos[0])
            rad = math.pi + math.atan(opposite/adjacent)
        else:
            rad = math.pi
    else:
        if pos[1] < center[1]:
            rad = 0.5 * math.pi
        if pos[1] > center[1]:
            rad = 1.5 * math.pi

    return(rad)

### drawing the beam
def beam(rad, player_centerx, player_centery):
    hypotenuse = 100
    center_x = player_centerx
    center_y = player_centery
    adjacent = math.cos(rad) * hypotenuse
    opposite = math.sin(rad) * hypotenuse
    x = int(center_x + adjacent)
    y = int(center_y - opposite)
    return(x, y)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, rad, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4, 4))
        self.image.fill((255, 0, 0))
        self.angle = rad
        self.center_x = center[0]
        self.center_y = center[1]
        self.rect = self.image.get_rect()
        self.hypotenuse = 1

    def update(self):
        adjacent = math.cos(self.angle) * self.hypotenuse
        opposite = math.sin(self.angle) * self.hypotenuse
        self.rect.centerx = int(self.center_x + adjacent)
        self.rect.centery = int(self.center_y - opposite)
        self.hypotenuse += 8


### variables and creating the group for bullets
bullet_group = pygame.sprite.Group()
bullet_timer = bullet_delay

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    enable = True
    android.accelerometer_enable(enable)

WHITE = ((255, 255, 255))
BLACK = ((0, 0, 0))
BLUE = ((85, 191, 223))
speed = 4
speed_2 = 6
x = 770
y = 360

windowSurface = pygame.display.set_mode((1280, 770))

player_circle = pygame.image.load("img/final_circle.png")
control_circle = pygame.draw.circle(windowSurface, WHITE, (1080, 550), 100, 4)

while True:
    if android:
        if android.check_pause():
            android.wait_for_resume()
        velocity_reading = android.accelerometer_reading()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    mouse_pos = pygame.mouse.get_pos()

        # elif event.type == MOUSEBUTTONDOWN:
        #     mouse_pos = pygame.mouse.get_pos()


### x-axis acceleration
    if velocity_reading[1] > 1 and x < 1280:
        x = x + speed
    if velocity_reading[1] > 3 and x < 1280:
        x = x + speed_2
    if velocity_reading[1] < -1 and x > 0:
        x = x - speed
    if velocity_reading[1] < -3 and x > 0:
        x = x - speed_2
### y-axis acceleration
    if velocity_reading[0] > 7 and y < 770:
        y = y + speed
    if velocity_reading[0] > 8.5 and y < 770:
        y = y + speed_2
    if velocity_reading[0] < 7 and y > 0:
        y = y - speed
    if velocity_reading[0] < 5 and y > 0:
        y = y - speed_2

    # print(velocity_reading)

    windowSurface.fill(BLACK)

    ### detects whether the control circle was pressed
    if control_circle.collidepoint(mouse_pos):
        angle = get_angle(mouse_pos, control_circle.center)
        if bullet_timer < 0:
            bullet = Bullet(angle, player_rect.center)
            bullet_group.add(bullet)
            bullet_timer = bullet_delay
        else:
            bullet_timer = bullet_timer - 1

        end_x, end_y = beam(angle, player_rect.centerx, player_rect.centery)
        pygame.draw.line(windowSurface, BLUE, (player_rect.centerx, player_rect.centery), (end_x, end_y))
        # print(angle)

    control_circle_small = pygame.draw.circle(windowSurface, BLUE, (1080, 550), 10, 2)
    control_circle = pygame.draw.circle(windowSurface, WHITE, (1080, 550), 100, 4)

    # if bullet_rect.centerx > 1290 or bullet_rect.centerx < 0:
    #     bullet_group.remove(bullet)
    #     print(bullet_group)


### drawing the bullets
    bullet_group.update()
    bullet_group.draw(windowSurface)

### blitting the player
    player_rect = player_circle.get_rect(center = (x, y))
    windowSurface.blit(player_circle, player_rect)


    clock.tick(60)
    pygame.display.update()