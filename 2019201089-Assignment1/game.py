import moderngl_window
from pathlib import Path
import moderngl
import numpy as np
import glm

from Cell import *
from color import *
from util import *
import random

grid_sizes = [8, ]  # 10, 16]

direction = directions()

width = height = grid_sizes[random.randint(0, len(grid_sizes) - 1)]

time_factor, zoom_factor = 20, 20
view_change_x, view_change_y = 0, 0


class game(moderngl_window.WindowConfig):
    gl_version = (4, 3)
    window_size = (1920, 1080)
    resource_dir = Path('.').absolute()
    cell = [Cell() for i in range(width * height)]
    title = 'Maze'
    horizontal_min, horizontal_max = None, None
    vertical_min, vertical_max = None, None
    gb_finder = None

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
                x_val = (corrdinate_to_wrc(x, width)) * .1  # addition cause already its negative
                y_val = (corrdinate_to_wrc(y, height) + 1) * .1

                self.to_remove_walls += [x_val, y_val, x_val + .1, y_val]
            if dir == direction.down:
                x_val = (corrdinate_to_wrc(x, width)) * .1
                y_val = (corrdinate_to_wrc(y, height)) * .1

                self.to_remove_walls += [x_val, y_val, x_val + .1, y_val]
            if dir == direction.right:
                x_val = (corrdinate_to_wrc(x, width) + 1) * .1
                y_val = (corrdinate_to_wrc(y, height)) * .1

                self.to_remove_walls += [x_val, y_val, x_val, y_val + .1]
            if dir == direction.left:
                x_val = (corrdinate_to_wrc(x, width)) * .1
                y_val = (corrdinate_to_wrc(y, height)) * .1

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
                pass

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

        self.display()

        self.model = glm.mat4(1.)
        # self.model = glm.scale(self.model, glm.vec3(2, 2, 0))
        self.program['model'].write(self.model)

    def render(self, time: float, frame_time: float):
        self.ctx.clear(background.r, background.g, background.b)

        self.grid_vao.render(moderngl.LINES)

        if len(self.to_remove_walls):
            self.to_remove_walls_vao.render(moderngl.LINES)

    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)


background = color(.0, .0, .0)
game.run()
