import pyxel
from time import time
from player_plane import PlayerPlane
from blue_enemies import BlueEnemies
from yellow_enemies import YellowEnemies
from green_enemies import GreenEnemies
from background import Background
from player_bullets import PlayerBullets
import constants


class Board:
    """This class contains all the information needed to represent the
    board as well as all the main functionalities of our game"""

    def __init__(self, w: int, h: int):

        # attributes to initialize the screen
        self.width = w  # width of the screen
        self.height = h  # height of the screen
        self.score = 0  # score of the game
        self.background = Background(constants.WIDTH, constants.HEIGHT)  # background object
        self.play = True  # boolean to start the game

        # timing
        self.old_millis_plane = round(time() * 1000)  # renewed timer for plane
        self.old_millis_enemies = round(time() * 1000)  # renewed timer for enemies

        # initialize screen
        pyxel.init(self.width, self.height, title="1942")  # width, height and title
        # loading the pyxres file
        pyxel.load("assets/1942_final.pyxres")

        # instance of the class PlayerPlane
        self.plane = PlayerPlane(constants.PLANE_INITIAL_X, constants.PLANE_INITIAL_Y,
                                 constants.PLANE_SIZE)  # location (160, 200) and size (16) 16x16

        # types of enemies is randomized
        self.enemy_type = pyxel.rndi(1, 3)

        # enemies bullets
        self.update_moving_bullet_enemies = True

        # barrier
        self.activate_barrier = False

        # lists of bullets and enemies
        self.player_bullet_list = []
        self.enemies_bullet_list = []
        self.enemies_list = [[], [], []]
        # running the game
        pyxel.run(self.update, self.draw)

    @property
    def w(self):
        return self.__w

    @w.setter
    def w(self, w):
        if type(w) != int:
            raise TypeError("The value must be an integer")
        elif w <= 0:
            raise ValueError("Width must be positive")
        else:
            self.__w = w

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, h):
        if type(h) != int:
            raise TypeError("The value must be an integer")
        elif h <= 0:
            raise ValueError("Height must be positive")
        else:
            self.__h = h

    def update(self):

        def create_bullets():  # creates and determines the position of the bullet as that of the player planes'
            player_bullet1 = PlayerBullets(self.plane.x, self.plane.y, constants.BULLET_SIZE)
            return player_bullet1

        def create_blue_enemies():  # creates the blue enemies in a random position on top of the display
            blue_enemies = BlueEnemies(pyxel.rndi(1, 255), constants.ENEMY_INITIAL_Y, constants.ENEMY_SIZE)
            return blue_enemies

        def create_yellow_enemies():  # creates the yellow enemies in a random position on top of the display
            yellow_enemies = YellowEnemies(pyxel.rndi(1, 255), constants.ENEMY_INITIAL_Y, constants.ENEMY_SIZE)
            return yellow_enemies

        def create_green_enemies():  # creates the green enemies in a random position on top of the display
            green_enemies = GreenEnemies(pyxel.rndi(1, 255), constants.ENEMY_INITIAL_Y, constants.ENEMY_SIZE)
            return green_enemies

        def player_shoot():  # triggers bullet unless barrier is active
            if pyxel.btnp(pyxel.KEY_SPACE) and not self.activate_barrier:
                self.player_bullet_list.append(create_bullets())
                self.plane.update_moving_bullet = True  # allows the bullet to go to the top

            if self.plane.update_moving_bullet:
                for i in range(len(self.player_bullet_list)):
                    self.player_bullet_list[i].shoot()  # activate shooting method

        def move_enemies():  # stores enemies in lists depending on their type and moves them on different intervals
            new_millis_enemies = round(time() * 1000)

            if (new_millis_enemies - self.old_millis_enemies) >= constants.TIME_CREATE_ENEMIES:
                self.enemy_type = pyxel.rndi(1, 3)  # select type of enemy
                self.old_millis_enemies = new_millis_enemies
                if self.enemy_type == 1:
                    self.enemies_list[0].append(create_blue_enemies())  # append blue enemies
                elif self.enemy_type == 2:
                    self.enemies_list[1].append(create_green_enemies())  # append green enemies
                elif self.enemy_type == 3:
                    self.enemies_list[2].append(create_yellow_enemies())  # append yellow enemies
                self.plane.update_moving_enemies = True  # enemies move continuously

            if self.plane.update_moving_enemies:
                for i in range(len(self.enemies_list)):
                    if self.enemies_list[i]:
                        for j in range(len(self.enemies_list[i])):
                            if i == 0:
                                self.enemies_list[0][j].move_blue_enemies()  # move blue enemies
                            elif i == 1:
                                self.enemies_list[1][j].move_green_enemies()  # move green enemies
                            else:
                                self.enemies_list[2][j].move_yellow_enemies()  # move yellow enemies

        def kill_enemies():  # kills the enemy planes if the bullet range reaches them
            for i in range(len(self.enemies_list)):
                for j in range(len(self.enemies_list[i])):
                    for x in range(len(self.player_bullet_list)):
                        if (
                                self.player_bullet_list[x].x in range(
                            self.enemies_list[i][j].x - self.enemies_list[i][j].range_shoot,
                            self.enemies_list[i][j].x + self.enemies_list[i][j].range_shoot)
                                and self.player_bullet_list[x].y in range(
                            self.enemies_list[i][j].y - self.enemies_list[i][j].range_shoot,
                            self.enemies_list[i][j].y + self.enemies_list[i][j].range_shoot)
                        ):  # check position of the enemies and the bullets
                            self.enemies_list[i][j].kill = True  # remove the enemy

                            self.score += constants.SCORE  # if enemy is killed, the score goes up by a defined constant

        def kill_player():  # if the enemy hits the player, the player loses a life
            # timing
            new_millis_plane = round(time() * constants.CONVERSION_SECONDS)
            for i in range(len(self.enemies_list)):
                for j in range(len(self.enemies_list[i])):
                    if (
                            self.enemies_list[i][j].x in range(self.plane.x - self.plane.shoot_range,
                                                               self.plane.x + self.plane.shoot_range)
                            and self.enemies_list[i][j].y in range(self.plane.y - self.plane.shoot_range,
                                                                   self.plane.y + self.plane.shoot_range)
                            and (new_millis_plane - self.old_millis_plane) >= constants.DELAY_COLLISION
                            and not self.activate_barrier
                    ):  # check position of the enemies and the player
                        self.old_millis_plane = new_millis_plane

                        if self.plane.lives > 1:
                            self.plane.lives -= 1  # the player loses a life
                            self.play = True
                        else:
                            pyxel.quit()  # if the lives are over, the game ends

        def enemies_shoot_collision():  # checks if a bullet's range is within an enemy plane and creates a new enemy
            new_millis_plane = round(time() * constants.CONVERSION_SECONDS)
            for x in range(len(self.enemies_bullet_list)):
                if (
                        self.enemies_bullet_list[x].x in range(self.plane.x - self.plane.shoot_range,
                                                               self.plane.x + self.plane.shoot_range)
                        and self.enemies_bullet_list[x].y in range(self.plane.y - self.plane.shoot_range,
                                                                   self.plane.y + self.plane.shoot_range)
                        and (new_millis_plane - self.old_millis_plane) >= constants.DELAY_COLLISION
                        and not self.activate_barrier
                ):  # check positions and activate barrier in the collisions
                    self.old_millis_plane = new_millis_plane

                    if self.plane.lives > 1:  # if the player has any lives left, removes one life when hit by an enemy,
                        # if not, the game ends
                        self.plane.lives -= 1
                        self.play = True
                    else:
                        pyxel.quit()

        def enemies_shoot_player():  # creates new enemy bullets
            # timing
            new_millis_plane = round(time() * constants.CONVERSION_SECONDS)

            for j in range(len(self.enemies_list[1])):
                if not self.enemies_list[1][j].kill:  # if the enemy is still alive
                    if (new_millis_plane - self.old_millis_plane) >= constants.ENEMY_SHOOT_DELAY:
                        enemies_bullet1 = PlayerBullets(self.enemies_list[1][j].x, self.enemies_list[1][j].y,
                                                        constants.BULLET_SIZE)
                        self.enemies_bullet_list.append(enemies_bullet1)
                        self.update_moving_bullet_enemies = True
                        self.old_millis_plane = new_millis_plane  # timing

            if self.update_moving_bullet_enemies:  # the enemies' bullet go all the way down
                for x in range(len(self.enemies_bullet_list)):
                    self.enemies_bullet_list[x].shoot_enemies()  # activate enemies' shooting

        def delete_extras():  # removes enemies from the list if they are killed or are off limits in the display
            if self.enemies_list:
                for i in range(len(self.enemies_list)):
                    for j in range(len(self.enemies_list[i])):
                        if self.enemies_list[i][j - 1].kill or self.enemies_list[i][j - 1].y > constants.DELETE_ENEMIES:
                            del self.enemies_list[i][j - 1]  # delete the corresponding element from the list

            if self.player_bullet_list:
                for x in range(len(self.player_bullet_list)):
                    if not self.player_bullet_list[x - 1].active:
                        del self.player_bullet_list[x - 1]  # delete the corresponding element from the list

        def barrier():  # activates the barrier when the Z key is pressed
            if pyxel.btn(pyxel.KEY_Z):
                self.activate_barrier = True  # barrier is activated
            else:
                self.activate_barrier = False  # barrier is deactivated

        def start_game():  # stars the game and runs all functions. It also
            # clears the enemies and bullets lists when the ENTER key is pressed
            if pyxel.btn(pyxel.KEY_RETURN):
                self.enemies_bullet_list.clear()
                self.enemies_list = [[], [], []]
                self.player_bullet_list.clear()
                self.play = False
            # if ENTER is pressed, every method is run and the game starts
            if not self.play:
                self.plane.move_player_plane(self.width)
                player_shoot()
                move_enemies()
                kill_enemies()
                kill_player()
                enemies_shoot_player()
                enemies_shoot_collision()
                delete_extras()
                barrier()

        start_game()

    def __draw_enemies(self):  # draws the enemies in the different lists
        for j in range(len(self.enemies_list[0])):  # blue enemies
            pyxel.blt(self.enemies_list[0][j].x + 4, self.enemies_list[0][j].y - 4, 0, 32, 0, 16, 16, colkey=0)
        for x in range(len(self.enemies_list[1])):  # green enemies
            pyxel.blt(self.enemies_list[1][x].x + 4, self.enemies_list[1][x].y - 4, 0, 48, 0, 16, 16, colkey=0)
        for t in range(len(self.enemies_list[2])):  # yellow enemies
            pyxel.blt(self.enemies_list[2][t].x + 4, self.enemies_list[2][t].y - 4, 0, 32, 16, 16, 16, colkey=0)

    def __draw_bullets(self):  # draws the player and enemies' bullets
        for i in range(len(self.player_bullet_list)):  # player bullets
            pyxel.blt(self.player_bullet_list[i].x + 4, self.player_bullet_list[i].y - 4, 0, 16, 0, 8, 8, colkey=0)
        for p in range(len(self.enemies_bullet_list)):  # enemies' bullets
            pyxel.blt(self.enemies_bullet_list[p].x + 4, self.enemies_bullet_list[p].y - 4, 0, 16, 0, 8, 8,
                      colkey=0)

    def __draw_start_screen(self):  # draws the main screen, with the title.
        pyxel.blt(*constants.TITLE_SPRITE)
        pyxel.text(*constants.PRESS_SPRITE)

    def __draw_index(self):  # types the score and the number of lives
        pyxel.text(90, 12, "LIVES:" + str(self.plane.lives), col=7)
        pyxel.text(135, 12, "SCORE:" + str(self.score), pyxel.frame_count % 16)

    def draw(self):
        pyxel.cls(0)
        # draw level
        self.background.draw()
        # draw plane
        self.plane.draw()
        # draw barrier
        if self.activate_barrier:
            pyxel.blt(self.plane.x, self.plane.y - 4, *constants.BARRIER_SPRITE, colkey=0)
        # draw bullets and enemies while play is active
        if not self.play:
            self.__draw_bullets()
            self.__draw_enemies()

        # starting screen
        else:
            self.__draw_start_screen()

        # scores and lives
        self.__draw_index()
