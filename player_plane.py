import pyxel


class PlayerPlane:
    """This class contains the player plane, defines its position, its shooting range,
    its lives, its size and its movement"""
    def __init__(self, x: int, y: int, size: int):
        self.x = x  # player plane x position
        self.y = y  # player plane y position

        self.sprint = (0, 0, 0, 16, 16)  # sprint: bank number (0), position at bank (0, 0), size (16, 16)

        self.size = size  # size of the plane
        self.shoot_range = size//2  # bigger range for the player to be hit
        self.lives = 3  # default lives

        self.update_moving_bullet = False  # update moving bullets
        self.update_moving_enemies = False  # update moving enemies

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

    def move_player_plane(self, board_size: int):  # move the player's plane depending on the input key
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btn(pyxel.KEY_RIGHT) and self.x < board_size - self.size:
            self.x += 2
        elif pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x -= 2
        elif pyxel.btn(pyxel.KEY_UP) and self.y > board_size/2:
            self.y -= 2
        elif pyxel.btn(pyxel.KEY_DOWN) and self.y < board_size - self.size:
            self.y += 2

    def draw(self):  # draws the player's plane
        pyxel.blt(self.x, self.y, *self.sprint, colkey=0)
