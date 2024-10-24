from enemies import Enemies
import constants
import pyxel


class GreenEnemies(Enemies):
    """This class contains the green enemies, defines their movement and position
        and whether they are killed or not by the player"""

    def __init__(self, x: int, y: int, size: int):
        super().__init__(x, y, size)  # inherit the attributes, properties and setters from the mother class

    def move_green_enemies(self):  # move enemies down
        if not self.kill or not self.y > constants.DELETE_ENEMIES:  # trying with function delete extras
            if (pyxel.frame_count + self.timer_enemies) % 30 > 20:  # randomize the movement of the enemy
                self.x += 1
            else:
                self.x -= 1
            self.y += 1
        else:
            self.x = constants.AFTER_HIT_ENEMIES  # send enemy to the bottom of the screen
            self.y = constants.AFTER_HIT_ENEMIES
            self.kill = True  # make sure the enemy is killed
