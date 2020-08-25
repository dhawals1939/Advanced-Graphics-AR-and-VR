from color import color
from stack import stack
import math
from util import *
import numpy as np

direction = directions()


class hero:
    moving = None
    degree = None
    eye_status = None
    rolling_status = None
    walk_status = None
    goal_ceremony_status = None
    body_color = color(.3, .4, .6)

    __current_x, __current_y = None, None
    __old_x, __old_y = None, None

    get_goal, init_dest, dest = None, None, None

    recursion_stack = None
    top_of_stack = None

    bat = dict()

    def __init__(self, x_pos, y_pos, maze_width, maze_height):
        new_xpos, new_ypos = corrdinate_to_wrc(x_pos, maze_width), corrdinate_to_wrc(y_pos, maze_height)
        self.__old_x = self.__current_x = new_xpos
        self.__old_y = self.__current_y = new_ypos

        self.recursion_stack = stack(maze_width * maze_height * 4)
        self.moving = False
        self.walk_status, self.eye_status, self.rolling_status, self.goal_ceremony_status = 0, 0, 0, 0

        self.degree = math.sin(7 * math.atan(-1) / 180)

        self.draw_hero()

        self.init_dest = self.dest = direction.right

    def is_moving(self):
        return self.moving

    def set_dest(self, dir):
        self.init_dest = self.dest
        self.dest = dir
        self.rolling_status, self.moving = 0, True

    def move(self):
        moving_factor = 28.5 * math.fabs(math.sin(self.degree * self.walk_status) -
                                         math.sin(self.degree * (self.walk_status - 1)))
        if self.rolling_status == roll_fact:
            if self.dest == direction.up:
                self.__current_y += moving_factor


    def set_body_color(self, R, G, B):
        pass

    def draw(self):
        pass

    def update_status(self):
        pass

    def current_x(self):
        return self.__current_x

    def current_y(self):
        return self.__current_y

    def set_getgoal(self):
        self.get_goal = True

    def draw_hero(self):
        self.bat['corrs'] = np.array(
            [
                .0, .0,
                1, -3 / 10,
                8 / 10, -1,
                2 / 10, -9 / 10,
                0, 0,
            ]
        )
        self.bat['primitive'] = 'POLYGON'
        color_array = np.array([[5 / 255, 225 / 255, 245 / 255] for i in range(int(len(self.bat['corrs']) / 2))])
        self.bat['color'] = np.array(np.concatenate(color_array).flat)
