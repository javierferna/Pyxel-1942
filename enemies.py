import pyxel
from time import time


class Enemies:
    """This mother class defines the position, size, shooting range and timing
    of enemies planes. It also states whether enemies are killed or not"""
    def __init__(self, x: int, y: int, size: int):
        self.x = x  # x position of the enemies
        self.y = y  # y position of the enemies
        self.size = size  # size of the enemies
        self.range_shoot = size // 2  # range of shooting for the enemies to be hit
        self.kill = False  # check if the enemies are alive

        self.timer_enemies = pyxel.rndi(0, 59)  # randomize the initial position of the enemies

        # timing
        self.old_millis_plane = round(time() * 1000)
        self.old_millis_enemies = round(time() * 1000)
        self.delta_time = 0

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if type(x) != int:
            raise TypeError("The value must be an integer")
        else:
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if type(y) != int:
            raise TypeError("The value must be an integer")
        else:
            self.__y = y

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        if type(size) != int:
            raise TypeError("The value must be an integer")
        else:
            self.__size = size
