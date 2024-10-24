import pyxel


class Background:
    """This class creates and draws the space background
    and both of the planets within it"""

    def __init__(self, width: int, height: int):
        self.width = width  # width of the screen
        self.height = height  # height of the screen

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        if type(width) != int:
            raise TypeError("The value must be an integer")
        elif width <= 0:
            raise ValueError("Width must be positive")
        else:
            self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        if type(height) != int:
            raise TypeError("The value must be an integer")
        elif height <= 0:
            raise ValueError("Height must be positive")
        else:
            self.__height = height

    def draw(self):
        counting = pyxel.frame_count % 256  # get the remainder of the frame count and the screen size

        for i in range(4):
            # draw the background, stars and planets
            pyxel.bltm(0, -(i * 256 - counting), 0, 0, 0, 256, 256)
            pyxel.blt(150, -(i * 256 - counting), 0, 0, 96, 48, 36, 12)
            pyxel.blt(25, -(i * 256 - counting), 0, 0, 136, 48, 48, 12)
