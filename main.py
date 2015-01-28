import pygame, sys
import math
from pygame.locals import *

try:
    import android
except ImportError:
    android = None

pygame.init()
player_circle = pygame.image.load("img/final_circle.png")
player_rect = player_circle.get_rect()
player_rect_centerx = player_rect.centerx
player_rect_centery = player_rect.centery
BLUE = ((0, 0, 255))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, mouse_pos, player_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3, 3))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.angle = self.shoot(mouse_pos)
        self.distance = 32

    def update(self):
        self.rect.centerx = int(self.player_rect[0] + math.cos(self.angle) *self.distance)
        self.rect.centery = int(self.player_rect[1] - math.sin(self.angle) * self.distance)

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

    ### detects whether the control circle was pressed
    if control_circle.collidepoint(mouse_pos):
        #print("control circle pressed")
        angle = get_angle(mouse_pos, control_circle.center)
        end_x, end_y = beam(angle, player_rect.centerx, player_rect.centery)
        windowSurface.fill(BLACK)
        pygame.draw.line(windowSurface, BLUE, (player_rect.centerx, player_rect.centery), (end_x, end_y))
        print(angle)

    windowSurface.fill(BLACK)
    angle = get_angle(mouse_pos, control_circle.center)
    end_x, end_y = beam(angle, player_rect.centerx, player_rect.centery)
    pygame.draw.line(windowSurface, BLUE, (player_rect.centerx, player_rect.centery), (end_x, end_y))
    control_circle_small = pygame.draw.circle(windowSurface, BLUE, (1080, 550), 10, 2)
    control_circle = pygame.draw.circle(windowSurface, WHITE, (1080, 550), 100, 4)
### blitting the player
    player_rect = player_circle.get_rect(center = (x, y))
    windowSurface.blit(player_circle, player_rect)
    pygame.display.update()