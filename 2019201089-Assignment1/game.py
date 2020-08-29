import moderngl_window
from pathlib import Path
import moderngl
import numpy as np
import glm
import random

from Cell import *
from color import *
from util import *
from hero import hero

grid_sizes = [16, ]  # 10, 16]

direction = directions()

width = height = grid_sizes[random.randint(0, len(grid_sizes) - 1)]

time_factor, zoom_factor = 20, 20
view_change_x, view_change_y = 0, 0


def cell_index(x, y):
    return width * y + x


def rand():
    return random.randint(0, 100000)


class game(moderngl_window.WindowConfig):
    gl_version = (4, 3)
    window_size = (1920, 1080)
    resource_dir = Path('.').absolute()
    aspect_ratio = 4 / 4
    cell = [Cell() for i in range(width * height)]
    title = 'Maze'
    horizontal_min, horizontal_max = None, None
    vertical_min, vertical_max = None, None
    gb_finder = None
    starting_x, starting_y = None, None
    state = None
    goal_x, goal_y = None, None
    chosen = []
    auto_mode = False
    user_input_direction = -1

    def gen_maze(self):
        dest, length, temp = None, None, None
        x, y = None
        if length == width * height:
            self.state = 0
            for i in range(width * height):
                self.cell[i].is_open = False
            return

        if length == 0:
            dest = rand() % 2 + 1

            if dest == direction.down:
                self.starting_x = x = rand() % width
                self.starting_y = y = height - 1
                self.cell[cell_index(x, y)].road[direction.up] = True

                self.goal_x = x = rand() % width
                self.goal_y = y = 0
                self.cell[cell_index(x, y)].road[direction.down] = True

            else:
                self.starting_x = x = width - 1
                self.starting_y = y = rand() % height
                self.cell[cell_index(x, y)].road[direction.right] = True

                self.goal_x = x = 0
                self.goal_y = y = rand() % height
                self.cell[cell_index(x, y)].road[direction.left] = True

            self.chosen = [0 for i in range(height * width)]

            x, y = rand() % width, rand() % height
            self.cell[cell_index(x, y)].is_open = True
            self.chosen[0] = width * y + x

            length = 1

        cell_open = False

        while not cell_open:
            temp = self.chosen[rand() % length]
            x, y = temp % width, temp % width

            dest = rand() % 4

            if dest == direction.up:
                if (y == height - 1) or self.cell[cell_index(x, y + 1)].is_open:
                    continue
                self.cell[cell_index(x, y + 1)].is_open = True

                self.cell[cell_index(x, y + 1)].road[direction.down] = True
                self.cell[cell_index(x, y)].road[direction.up] = True

                self.chosen[length] = width * (y + 1) + x
                length += 1
                cell_open = True

            elif dest == direction.down:
                if (y == 0) or self.cell[cell_index(x, y - 1)].is_open:
                    continue
                self.cell[cell_index(x, y - 1)].is_open = True

                self.cell[cell_index(x, y - 1)].road[direction.up] = True
                self.cell[cell_index(x, y)].road[direction.down] = True

                self.chosen[length] = width * (y - 1) + x
                length += 1
                cell_open = True

            elif dest == direction.right:
                if (x == width - 1) or self.cell[cell_index(x + 1, y)].is_open:
                    continue

                self.cell[cell_index(x + 1, y)].is_open = True

                self.cell[cell_index(x + 1, y)].road[direction.left] = True
                self.cell[cell_index(x, y)].road[direction.right] = True

                self.chosen[length] = width * y + x + 1
                length += 1
                cell_open = True

            elif dest == direction.left:
                if (x == 0) or self.cell[cell_index(x - 1, y)].is_open:
                    continue

                self.cell[cell_index(x - 1, y)].is_open = True

                self.cell[cell_index(x - 1, y)].road[direction.right] = True
                self.cell[cell_index(x, y)].road[direction.left] = True

                self.chosen[length] = width * y + x - 1
                length += 1
                cell_open = True

    def path_finder(self):
        x, y = self.starting_x, self.starting_y

        if self.gb_finder is None:
            self.gb_finder = hero(self.starting_x, self.starting_y, width, height)

        self.gb_finder.update_status()

        if self.gb_finder.is_moving():
            return

        if (x == self.goal_x) and (y == self.goal_y):
            self.state += 1
            self.gb_finder.set_getgoal()  # finished
            return

        if self.user_input_direction > -1:
            if self.user_input_direction == direction.up:
                if self.cell[cell_index(x, y)].road[direction.up] and (y < height - 1) and \
                        (not self.cell[cell_index(x, y + 1)].is_open):
                    self.gb_finder.set_dest(direction.up)
                    y += 1

            elif self.user_input_direction == direction.down:
                if self.cell[cell_index(x, y)].road[direction.down] and (y > 0) and \
                        (not self.cell[cell_index(x, y - 1)].is_open):
                    self.gb_finder.set_dest(direction.down)
                    y -= 1

            elif self.user_input_direction == direction.right:
                if self.cell[cell_index(x, y)].road[direction.right] and (x < width - 1) and \
                        (not self.cell[cell_index(x + 1, y)].is_open):
                    self.gb_finder.set_dest(direction.right)
                    x += 1

            elif self.user_input_direction == direction.left:
                if self.cell[cell_index(x, y)].road[direction.left] and (x > 0) and \
                        (not self.cell[cell_index(x - 1, y)].is_open):
                    self.gb_finder.set_dest(direction.left)
                    x -= 1
            self.user_input_direction = -1

    def grid_create(self):
        self.horizontal_min, self.horizontal_max = -int((width + 2) / 2 - 1), int((width + 2) / 2 - 1)
        self.vertical_min, self.vertical_max = -int((height + 2) / 2 - 1), int((height + 2) / 2 - 1)

        grid = [(x * .1, self.vertical_min * .1, x * 0.1, self.vertical_max * .1) for x in
                range(self.horizontal_min, self.horizontal_max + 1)] + \
               [(self.horizontal_min * .1, y * .1, self.horizontal_max * .1, y * .1) for y in
                range(self.vertical_min, self.vertical_max + 1)]

        self.grid = np.array(np.concatenate(grid).flat)

        def erase_wall(x, y, dir):
            if dir == direction.up:
                x_val = (coordinate_to_wrc(x, width)) * .1  # addition cause already its negative
                y_val = (coordinate_to_wrc(y, height) + 1) * .1

                self.to_remove_walls += [x_val, y_val, x_val + .1, y_val]
            if dir == direction.down:
                x_val = (coordinate_to_wrc(x, width)) * .1
                y_val = (coordinate_to_wrc(y, height)) * .1

                self.to_remove_walls += [x_val, y_val, x_val + .1, y_val]
            if dir == direction.right:
                x_val = (coordinate_to_wrc(x, width) + 1) * .1
                y_val = (coordinate_to_wrc(y, height)) * .1

                self.to_remove_walls += [x_val, y_val, x_val, y_val + .1]
            if dir == direction.left:
                x_val = (coordinate_to_wrc(x, width)) * .1
                y_val = (coordinate_to_wrc(y, height)) * .1

                self.to_remove_walls += [x_val, y_val, x_val, y_val + .1]

        for i in range(width * height):
            x = i % width
            y = int(i / width)

            if self.cell[i].road[direction.right]:
                erase_wall(x, y, direction.right)
            if self.cell[i].road[direction.up]:
                erase_wall(x, y, direction.up)
            if self.cell[i].road[direction.down]:
                erase_wall(x, y, direction.down)
            if self.cell[i].road[direction.left]:
                erase_wall(x, y, direction.left)

        self.to_remove_walls = np.array(self.to_remove_walls)

    def display(self):
        self.grid_create()

        self.grid_vbo = self.ctx.buffer(self.grid.astype('f4').tobytes())
        rand_float = random.uniform(.4, .8)
        self.grid_colors = np.array([rand_float for i in range(3 * int(len(self.grid) / 2))])

        self.grid_color_vbo = self.ctx.buffer(self.grid_colors.tobytes())

        self.grid_vao_content = [
            (self.grid_vbo, '2f', 'in_vert'),
            (self.grid_color_vbo, '3f', 'in_color')
        ]

        self.grid_vao = self.ctx.vertex_array(self.program, self.grid_vao_content)

        if len(self.to_remove_walls):
            self.to_remove_walls_vbo = self.ctx.buffer(self.to_remove_walls.astype('f4').tobytes())

            self.to_remove_walls_color_vbo = self.ctx.buffer(
                np.array([background.r, background.b, background.g] * int(len(self.to_remove_walls))).astype(
                    'f4').tobytes())

            self.to_remove_walls_vao_content = [
                (self.to_remove_walls_vbo, '2f', 'in_vert'),
                (self.to_remove_walls_color_vbo, '3f', 'in_color')
            ]

            self.to_remove_walls_vao = self.ctx.vertex_array(self.program, self.to_remove_walls_vao_content)

            if self.gb_finder:
                self.gb_finder.draw()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.program = self.ctx.program(vertex_shader=open('./maze.vert.glsl').read(),
                                        fragment_shader=open('./maze.frag.glsl').read())

        self.grid = np.array([])
        self.grid, self.grid_vbo, self.grid_vao = None, None, None
        self.grid_colors, self.grid_color_vbo, self.grid_vao = None, None, None
        self.grid_vao_content = None

        self.to_remove_walls = []
        self.to_remove_walls_vbo, self.to_remove_walls_vao, self.to_remove_walls_color_vbo = None, None, None
        self.to_remove_walls_vao_content = None

        self.cell[8].road[direction.up] = True
        self.display()

        self.model = glm.mat4(1.)
        self.model = glm.scale(self.model, glm.vec3(.5, .5, 0))
        self.program['model'].write(self.model)

    def render(self, time: float, frame_time: float):
        self.ctx.clear(background.r, background.g, background.b)

        self.grid_vao.render(moderngl.LINES)

        if len(self.to_remove_walls):
            self.to_remove_walls_vao.render(moderngl.LINES)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys
        if action == keys.ACTION_PRESS:
            if key == keys.W:
                self.user_input_direction = direction.up
            if key == keys.S:
                self.user_input_direction = direction.down
            if key == keys.A:
                self.user_input_direction = direction.left
            if key == keys.D:
                self.user_input_direction = direction.right
            if key == keys.PAGE_UP:
                pass
            if key == keys.PAGE_DOWNP:
                pass
            if key == keys.M:
                for i in range(width):
                    for j in range(1, height):
                        self.cell[cell_index(i, j)].road[direction.down] = True
                        self.cell[cell_index((i, j - 1))].road[direction.up] = True
                self.gen_maze()
        self.review_point()
        self.display()

    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)


background = color(.0, .0, .0)
game.run()
