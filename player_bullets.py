class PlayerBullets:
    """This class contains the player bullets, defines their position,
    their collision with the enemies and whether the bullets are active (to kill them)"""
    def __init__(self, x: int, y: int, size):
        self.x = x  # x position of the player bullets
        self.y = y  # y position of the player bullets
        self.settings = (0, 17, 0, size, size)
        self.active = True  # checks if the bullets are still active

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

    def shoot(self):
        if self.y > -10:
            self.y -= 4
        else:
            self.active = False  # to remove the bullets from the screen

    def shoot_enemies(self):  # shoot enemies depending on the position of a bullet
        if self.y > 0:
            self.y += 4

    def check_extras(self):  # checks the position of a bullet and deactivates it
        if self.y < 0:
            self.active = False  # to remove the bullets from the screen
