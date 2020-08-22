import moderngl_window
from pathlib import Path
import moderngl
import numpy as np
import glm

from Cell import Cell
from Cell import up, down, right, left
from color import color
import random

grid_sizes = [8, ]  # 10, 16]

width = height = grid_sizes[random.randint(0, len(grid_sizes) - 1)]

time_factor, zoom_factor = 20, 20
view_change_x, view_change_y = 0, 0


class game(moderngl_window.WindowConfig):
    gl_version = (4, 3)
    window_size = (500, 500)
    resource_dir = Path('.').absolute()
    cell = [Cell() for i in range(width * height)]
    title = 'Maze'
    horizontal_min, horizontal_max = None, None
    vertical_min, vertical_max = None, None

    def maze_create(self):
        self.horizontal_min, self.horizontal_max = -int((width + 2) / 2 - 1), int((width + 2) / 2 - 1)
        self.vertical_min, self.vertical_max = -int((height + 2) / 2 - 1), int((height + 2) / 2 - 1)

        grid = [(x * .1, self.vertical_min * .1, x * 0.1, self.vertical_max * .1) for x in
                range(self.horizontal_min, self.horizontal_max + 1)] + \
               [(self.horizontal_min * .1, y * .1, self.horizontal_max * .1, y * .1) for y in
                range(self.vertical_min, self.vertical_max + 1)]

        self.maze = np.array(np.concatenate(grid).flat)

        def erase_wall(x, y, dir):
            if dir == up:
                x_val = (x + self.horizontal_min) * .1 # addition cause already its negative
                y_val = (y + 1 + self.vertical_min) * .1

                self.to_remove_walls += [x_val, y_val, x_val + .1, y_val]
            if dir == down:
                x_val = (x + self.horizontal_min) * .1
                y_val = (y + self.vertical_min) * .1

                self.to_remove_walls += [x_val, y_val, x_val + .1, y_val]
            if dir == right:
                x_val = (x + 1 + self.horizontal_min) * .1
                y_val = (y + self.vertical_min) * .1

                self.to_remove_walls += [x_val, y_val, x_val, y_val + .1]
            if dir == left:
                x_val = (x + self.horizontal_min) * .1
                y_val = (y + self.vertical_min) * .1

                self.to_remove_walls += [x_val, y_val, x_val, y_val + .1]

        for i in range(width * height):
            x = i % width
            y = int(i / width)

            if self.cell[i].road[right]:
                erase_wall(x, y, right)
            if self.cell[i].road[up]:
                erase_wall(x, y, up)
            if self.cell[i].road[down]:
                erase_wall(x, y, down)
            if self.cell[i].road[left]:
                erase_wall(x, y, left)

        self.to_remove_walls = np.array(self.to_remove_walls)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.program = self.ctx.program(vertex_shader=open('./maze.vert.glsl').read(),
                                        fragment_shader=open('./maze.frag.glsl').read())

        self.to_remove_walls = []
        self.maze = np.array([])

        self.cell[8].road[up] = True
        self.cell[20].road[left] = True

        self.maze_create()

        self.maze_vbo = self.ctx.buffer(self.maze.astype('f4').tobytes())
        self.maze_color_vbo = self.ctx.buffer(np.array([1., .0, .0] * int(len(self.maze))).astype('f4').tobytes())

        self.to_remove_walls_vbo = self.ctx.buffer(self.to_remove_walls.astype('f4').tobytes())
        self.to_remove_walls_color_vbo = self.ctx.buffer(np.array([background.r, background.b, background.g] * int(len(self.to_remove_walls))).astype('f4').tobytes())

        self.maze_vao_content = [
            (self.maze_vbo, '2f', 'in_vert'),
            (self.maze_color_vbo, '3f', 'in_color')
        ]

        self.to_remove_walls_vao_content = [
            (self.to_remove_walls_vbo, '2f', 'in_vert'),
            (self.to_remove_walls_color_vbo, '3f', 'in_color')
        ]
        print(self.to_remove_walls)

        self.maze_vao = self.ctx.vertex_array(self.program, self.maze_vao_content)
        self.to_remove_walls_vao = self.ctx.vertex_array(self.program, self.to_remove_walls_vao_content)

        self.model = glm.mat4(1.)
        self.program['model'].write(self.model)

    def render(self, time: float, frame_time: float):
        self.ctx.clear(background.r, background.g, background.b)

        self.maze_vao.render(moderngl.LINES)
        self.to_remove_walls_vao.render(moderngl.LINES)

    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)


background = color(.0, .0, .0)
game.run()
