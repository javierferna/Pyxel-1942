from enemies import Enemies
from time import time
import constants
import pyxel


class BlueEnemies(Enemies):
    """This class contains the blue enemies, defines their movement and position
       and whether they are killed or not by the player"""

    def __init__(self, x: int, y: int, size: int):
        super().__init__(x, y, size)  # inherit the attributes, properties and setters from the mother class
        self.states = 1

    def move_blue_enemies(self):  # move enemies in a circle of set radius
        if not self.kill or not self.y > constants.DELETE_ENEMIES:
            new_millis_enemies = round(time() * constants.CONVERSION_SECONDS)
            if (pyxel.frame_count % 256 > 0) and (
                    new_millis_enemies - self.old_millis_enemies) >= constants.BLUE_ENEMY_DELAY:
                if self.states == 1 or self.states == 2:  # check if the states is 1 or 2
                    self.x += constants.BLUE_ENEMY_CIRCLES
                    self.states += 1
                elif self.states == 3 or self.states == 4:  # check if the states is 3 or 4
                    self.y -= constants.BLUE_ENEMY_CIRCLES
                    self.states += 1
                elif self.states == 5 or self.states == 6:  # check if the states is 5 or 6
                    self.x -= constants.BLUE_ENEMY_CIRCLES
                    self.states += 1
                elif self.states == 7 or self.states == 8:  # check if the states is 7 or 8
                    self.y += constants.BLUE_ENEMY_CIRCLES
                    if self.states == 7:
                        self.states = 8
                    elif self.states == 8:
                        self.states = 1

                self.y += 2
                self.old_millis_enemies = new_millis_enemies
        else:
            self.x = constants.AFTER_HIT_ENEMIES  # send enemy to the bottom of the screen
            self.y = constants.AFTER_HIT_ENEMIES
            self.kill = True  # make sure the enemy is killed
