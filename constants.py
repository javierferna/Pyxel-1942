import random

DELETE_ENEMIES = 270  # 'y' position to remove enemies from the list
AFTER_HIT_ENEMIES = 260
TIME_CREATE_ENEMIES = 1000
PLANE_INITIAL_X = 120
PLANE_INITIAL_Y = 200

DELAY_COLLISION = 350
CONVERSION_SECONDS = 1000
BLUE_ENEMY_CIRCLES = 15
BLUE_ENEMY_DELAY = 150
SCORE = 10

ENEMY_INITIAL_X = random.randint(1, 255)
ENEMY_INITIAL_Y = 0

PLANE_SIZE = 16
BULLET_SIZE = 16
ENEMY_SIZE = 16

ENEMY_SHOOT_DELAY = 800

BARRIER_SPRITE = (0, 0, 48, 16, 16)
BARRIER_DELAY = 6000

WIDTH = 256
HEIGHT = 256


TITLE_SPRITE = (102, 80, 1, 8, 16, 46, 30, 12)
PRESS_SPRITE = (90, 110, "PRESS ENTER TO PLAY", 7)
