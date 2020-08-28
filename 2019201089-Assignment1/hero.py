from color import color
from stack import stack
import math
from util import *
import numpy as np
import moderngl_window
import glm

direction = directions()


class hero:
    moving = None
    degree = None
    eye_status = None
    rolling_status = None
    walk_status = None
    goal_ceremony_status = None
    body_color = None

    __current_x, __current_y = None, None
    __old_x, __old_y = None, None

    get_goal, init_dest, dest = None, None, None

    recursion_stack = None
    top_of_stack = None
    program = None

    bat = dict()

    def __init__(self, x_pos, y_pos, maze_width, maze_height, **kwargs):
        new_xpos, new_ypos = coordinate_to_wrc(x_pos, maze_width), coordinate_to_wrc(y_pos, maze_height)
        self.__old_x = self.__current_x = new_xpos
        self.__old_y = self.__current_y = new_ypos

        self.recursion_stack = stack(maze_width * maze_height * 4)
        self.moving = False
        self.walk_status, self.eye_status, self.rolling_status, self.goal_ceremony_status = 0, 0, 0, 0

        self.degree = math.sin(7 * math.atan(-1) / 180)

        self.draw_hero()

        self.init_dest = self.dest = direction.right

        if 'color' in kwargs.keys():
            self.set_body_color(kwargs['color'][0], kwargs['color'][1], kwargs['color'][2])
        else:
            self.set_body_color(1., .2, .2)

    def is_moving(self):
        return self.moving

    def set_dest(self, dir):
        self.init_dest = self.dest
        self.dest = dir
        self.rolling_status, self.moving = 0, True

    def move(self):
        moving_factor = .1
        if self.rolling_status == roll_fact:
            if self.dest == direction.up:
                self.__current_y += moving_factor
            if self.dest == direction.down:
                self.__current_y -= moving_factor
            if self.dest == direction.left:
                self.__current_x -= moving_factor
            if self.dest == direction.right:
                self.__current_x += moving_factor

        if abs(self.__old_x - self.__current_x) >= .1:
            self.__current_x = self.__old_x + (.1 if self.dest == direction.right else -.1)
            self.__old_x = self.__current_x
            self.moving = False

        if abs(self.__old_y - self.__current_y) >= .1:
            self.__current_y = self.__old_y + (.1 if self.dest == direction.up else -.1)
            self.__old_y = self.__current_y
            self.moving = False

    def set_body_color(self, R, G, B):
        self.body_color = color(R, G, B)

    def draw(self):
        model = glm.mat4(1.)
        model = glm.scale(model, glm.vec3(.05, .05, 1))
        # look for center
        model = glm.translate(model, glm.vec3((self.__current_x + .1) / 2, (.1 + self.__current_y) / 2, .0))
        return model

    def update_status(self):
        if self.moving:
            self.move()
        if self.rolling_status < roll_fact:
            self.rolling_status += 1
            if self.init_dest == self.dest:
                self.rolling_status = roll_fact
            if self.rolling_status == roll_fact:
                self.init_dest = self.dest

    def current_x(self):
        return self.__current_x

    def current_y(self):
        return self.__current_y

    def set_getgoal(self):
        self.get_goal = True

    def draw_hero(self):
        self.bat['coors'] = np.array(
            [
                -.5, 0.7,
                -.25, .2,
                .0, .0,
                .0, .0,
                .5, 0.7,
                .25, .2
            ])
        self.bat['primitive'] = 'POLYGON'
        color_array = np.array([[5 / 255, 225 / 255, 245 / 255] for i in range(int(len(self.bat['corrs']) / 2))])
        self.bat['color'] = np.array(np.concatenate(color_array).flat)
