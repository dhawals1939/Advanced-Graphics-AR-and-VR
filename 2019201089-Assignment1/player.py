from color import color
from stack import stack
import math
from util import *
import numpy as np
import moderngl_window
import glm

direction = directions()


class player:
    moving = None
    eye_status = None
    rolling_status = None
    walk_status = None
    body_color = None

    __current_x, __current_y = None, None
    __old_x, __old_y = None, None

    get_goal, init_dest, dest = None, None, None

    recursion_stack = None
    top_of_stack = None
    program = None

    player_type = None

    player_body = dict()

    def __init__(self, x_pos, y_pos, maze_width, maze_height, player_type):
        self.player_type = player_type

        new_xpos, new_ypos = coordinate_to_wrc(x_pos, maze_width) * .1, coordinate_to_wrc(y_pos, maze_height) * .1
        self.__old_x = self.__current_x = new_xpos
        self.__old_y = self.__current_y = new_ypos

        self.recursion_stack = stack(maze_width * maze_height * 4)
        self.moving = False
        self.rolling_status = 0

        self.draw_hero()

        self.init_dest = direction.right
        self.dest = direction.right

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

    def draw(self, goal_reached, degree):
        self.model = glm.mat4(1.)
        self.model = glm.scale(self.model, glm.vec3(.2, .2, 1))
        # look for center
        if self.player_type == 'enemy':
            self.model = glm.translate(self.model, glm.vec3(.5, 1., 0))
        else:
            self.model = glm.translate(self.model, glm.vec3(.5, .2, 0))  # center in cell
        self.model = glm.translate(self.model, glm.vec3(self.__current_x * 10, self.__current_y * 10, .0))
        if goal_reached:
            self.model = glm.scale(self.model, glm.vec3(.5, .5, 1))
            self.model = glm.rotate(self.model, glm.radians(degree * 50), glm.vec3(0, 0, 1.))
        return self.model

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

        if self.player_type == 'hero':
            self.player_body['coors'] = np.array(
                [
                    -.5, 0.7,
                    -.25, .2,
                    .0, .0,
                    .0, .0,
                    .5, 0.7,
                    .25, .2
                ])
            self.player_body['primitive'] = 'POLYGON'
            color_array = np.array(
                [[255 / 255, 32 / 255, 32 / 255] for i in range(int(len(self.player_body['coors']) / 2))])
            self.player_body['color'] = np.array(np.concatenate(color_array).flat)
        elif self.player_type == 'enemy':
            self.player_body['coors'] = np.array(
                [
                    -.5, -0.7,
                    -.25, -.2,
                    .0, .0,
                    .0, .0,
                    .5, -0.7,
                    .25, -.2
                ])
            self.player_body['primitive'] = 'POLYGON'
            color_array = np.array(
                [[32 / 255, 32 / 255, 255 / 255] for i in range(int(len(self.player_body['coors']) / 2))])
            self.player_body['color'] = np.array(np.concatenate(color_array).flat)
