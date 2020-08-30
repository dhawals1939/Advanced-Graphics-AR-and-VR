import moderngl_window
from pathlib import Path
import moderngl
import numpy as np
import glm
import random

from Cell import *
from color import *
from util import *
from player import player

grid_sizes = [8, 12, 16]

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
    hero_finder = None
    starting_x, starting_y = None, None
    state = -1
    goal_x, goal_y = None, None
    chosen = []
    auto_mode = False
    user_input_direction = -1
    view_zoomfactor = .5
    length = 0
    model, projection = glm.mat4(1.), glm.mat4(1.)

    init_time, current_time, prev_time = 0, 0, 0

    grid, grid_vbo, grid_vao = None, None, None
    grid_colors, grid_color_vbo = None, None
    grid_vao_content = None

    to_remove_walls = []
    to_remove_walls_vbo, to_remove_walls_vao, to_remove_walls_color_vbo = None, None, None
    to_remove_walls_vao_content = None

    hero_path_finding_x, hero_path_finding_y = None, None
    hero_vert_vbo, hero_color_vbo, hero_vao_content, hero_vao = None, None, None, None

    power = 2
    power_up_vao = None
    powerup_x, powerup_y = None, None
    powerup_program = None

    obstacle_vao = None
    obstacle_x, obstacle_y = None, None
    obstacle_program = None

    bomb_vao = None
    bomb_x, bomb_y = None, None
    bomb_program = None

    enemy_finder = None
    enemy_path_finding_x, enemy_path_finding_y = None, None
    enemy_vert_vbo, enemy_color_vbo = None, None
    enemy_program, enemy_vao_content, enemy_vao = None, None, None

    score_board_vert_vbo, score_board_color_vbo = None, None
    score_board_program, score_board_vao_content, score_board_vao = None, None, None

    score_1 = [
        -.1, .0,
        0, .1,
        .1, .0
    ]
    score_2 = [
        -.4, .0,
        -.3, .1,
        -.2, .0
    ]
    score_3 = [
        -.7, .0,
        -.6, .1,
        -.5, .0
    ]
    score = []

    def score_board(self):
        score_board_model = glm.mat4(1.)
        score_board_model = glm.translate(score_board_model, glm.vec3(2, 2, 0))
        self.score_board_program['model'].write(score_board_model)
        self.score = []

        if self.power == 0:
            self.score_board_vao = None
            return
        if self.power == 1:
            self.score = self.score_1
        if self.power == 2:
            self.score = self.score_1 + self.score_2
        if self.power == 3:
            self.score = self.score_1 + self.score_2 + self.score_3

        score_board_vert = np.array(self.score)
        score_board_color = np.array(np.concatenate([[.9, .0, .0] for i in range(int(len(score_board_vert) / 2))]).flat)

        self.score_board_vert_vbo = self.ctx.buffer(score_board_vert.astype('f4').tobytes())
        self.score_board_color_vbo = self.ctx.buffer(score_board_color.astype('f4').tobytes())

        self.score_board_vao_content = [
            (self.score_board_vert_vbo, '2f', 'in_vert'),
            (self.score_board_color_vbo, '3f', 'in_color')
        ]

        self.score_board_vao = self.ctx.vertex_array(self.score_board_program, self.score_board_vao_content)

    def enemy_path_finder(self):
        if self.enemy_path_finding_x is None and self.enemy_path_finding_y is None:
            self.enemy_path_finding_x, self.enemy_path_finding_y = rand() % width, rand() % height
            while self.enemy_path_finding_x == self.starting_x and self.enemy_path_finding_y == self.starting_y:
                self.enemy_path_finding_x, self.enemy_path_finding_y = rand() % width, rand() % height

        if self.enemy_finder is None:
            self.enemy_finder = player(self.enemy_path_finding_x, self.enemy_path_finding_y, width, height, 'enemy')

            self.enemy_vert_vbo = self.ctx.buffer(self.enemy_finder.player_body['coors'].astype('f4').tobytes())
            self.enemy_color_vbo = self.ctx.buffer(self.enemy_finder.player_body['color'].astype('f4').tobytes())

            self.enemy_vao_content = [
                (self.enemy_vert_vbo, '2f', 'in_vert'),
                (self.enemy_color_vbo, '3f', 'in_color')
            ]

            self.enemy_vao = self.ctx.vertex_array(self.enemy_program, self.enemy_vao_content)

        self.enemy_finder.update_status()

        if self.enemy_finder.is_moving():
            return

        enemy_movement_direction = rand() % 10
        if enemy_movement_direction > -1:
            if enemy_movement_direction == direction.up:
                if self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y)].road[direction.up] and (
                        self.enemy_path_finding_y < height - 1) and \
                        (not self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y + 1)].is_open):
                    self.enemy_finder.set_dest(direction.up)
                    self.enemy_path_finding_y += 1

            elif enemy_movement_direction == direction.down:
                if self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y)].road[
                    direction.down] and (
                        self.enemy_path_finding_y > 0) and \
                        (not self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y - 1)].is_open):
                    self.enemy_finder.set_dest(direction.down)
                    self.enemy_path_finding_y -= 1

            elif enemy_movement_direction == direction.right:
                if self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y)].road[
                    direction.right] and (
                        self.enemy_path_finding_x < width - 1) and \
                        (not self.cell[cell_index(self.enemy_path_finding_x + 1, self.enemy_path_finding_y)].is_open):
                    self.enemy_finder.set_dest(direction.right)
                    self.enemy_path_finding_x += 1

            elif enemy_movement_direction == direction.left:
                if self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y)].road[
                    direction.left] and (
                        self.enemy_path_finding_x > 0) and \
                        (not self.cell[cell_index(self.enemy_path_finding_x - 1, self.enemy_path_finding_y)].is_open):
                    self.enemy_finder.set_dest(direction.left)
                    self.enemy_path_finding_x -= 1

    def obstacle(self):
        self.obstacle_x, self.obstacle_y = rand() % width, rand() % height

        while self.obstacle_x == self.powerup_x and self.obstacle_y == self.powerup_y:
            self.obstacle_x, self.obstacle_y = rand() % width, rand() % height

        obstacle_vert = np.array([
            .0, -0.2,
            -.1, 0,
            .1, 0
        ])

        obstacle_color = np.array(
            [
                .0, .0, .9,
                .0, .0, .9,
                .0, .0, .9,
            ]
        )
        obstacle_vert_vbo = self.ctx.buffer(obstacle_vert.astype('f4').tobytes())
        obstacle_color_vbo = self.ctx.buffer(obstacle_color.astype('f4').tobytes())

        obstacle_vao_content = [
            (obstacle_vert_vbo, '2f', 'in_vert'),
            (obstacle_color_vbo, '3f', 'in_color')
        ]

        self.obstacle_program = self.ctx.program(vertex_shader=open('maze.vert.glsl').read(),
                                                 fragment_shader=open('maze.frag.glsl').read())

        self.obstacle_vao = self.ctx.vertex_array(self.obstacle_program, obstacle_vao_content)

        obstacle_model = glm.mat4(1.)
        obstacle_model = glm.scale(obstacle_model, glm.vec3(.2, .2, 1))
        # look for center
        obstacle_model = glm.translate(obstacle_model, glm.vec3(.5, .5, 0))  # center in cell
        obstacle_model = glm.translate(obstacle_model, glm.vec3(coordinate_to_wrc(self.obstacle_x, width),
                                                                coordinate_to_wrc(self.obstacle_y, height), .0))
        self.obstacle_program['model'].write(obstacle_model)

    def bomb(self):
        self.bomb_x, self.bomb_y = rand() % width, rand() % height

        while self.bomb_x == self.powerup_x and self.bomb_y == self.powerup_y:
            self.bomb_x, self.bomb_y = rand() % width, rand() % height

        bomb_vert = np.array([
            .0, -0.2,
            -.1, 0,
            .1, 0,
            .0, 0.2,
            -.1, 0,
            .1, 0
        ])

        bomb_color = np.array(
            [
                .0, .9, .0,
                .0, .9, .0,
                .0, .9, .0,
                .0, .9, .0,
                .0, .9, .0,
                .0, .9, .0,
            ]
        )
        bomb_vert_vbo = self.ctx.buffer(bomb_vert.astype('f4').tobytes())
        bomb_color_vbo = self.ctx.buffer(bomb_color.astype('f4').tobytes())

        bomb_vao_content = [
            (bomb_vert_vbo, '2f', 'in_vert'),
            (bomb_color_vbo, '3f', 'in_color')
        ]

        self.bomb_program = self.ctx.program(vertex_shader=open('maze.vert.glsl').read(),
                                             fragment_shader=open('maze.frag.glsl').read())

        self.bomb_vao = self.ctx.vertex_array(self.bomb_program, bomb_vao_content)

        bomb_model = glm.mat4(1.)
        bomb_model = glm.scale(bomb_model, glm.vec3(.2, .2, 1))
        # look for center
        bomb_model = glm.translate(bomb_model, glm.vec3(.5, .5, 0))  # center in cell
        bomb_model = glm.translate(bomb_model, glm.vec3(coordinate_to_wrc(self.bomb_x, width),
                                                        coordinate_to_wrc(self.bomb_y, height), .0))
        self.bomb_program['model'].write(bomb_model)

    def power_up(self):
        self.powerup_x, self.powerup_y = rand() % width, rand() % height
        while self.powerup_x == self.starting_x and self.powerup_y == self.powerup_y:
            self.powerup_x, self.powerup_y = rand() % width, rand() % height

        powerup_vert = np.array([
            .0, 0.2,
            -.1, 0,
            .1, 0
        ])

        powerup_color = np.array(
            [
                .9, .0, .0,
                .9, .0, .0,
                .9, .0, .0,
            ]
        )
        powerup_vert_vbo = self.ctx.buffer(powerup_vert.astype('f4').tobytes())
        powerup_color_vbo = self.ctx.buffer(powerup_color.astype('f4').tobytes())

        powerup_vao_content = [
            (powerup_vert_vbo, '2f', 'in_vert'),
            (powerup_color_vbo, '3f', 'in_color')
        ]

        self.powerup_program = self.ctx.program(vertex_shader=open('maze.vert.glsl').read(),
                                                fragment_shader=open('maze.frag.glsl').read())

        self.power_up_vao = self.ctx.vertex_array(self.powerup_program, powerup_vao_content)

        powerup_model = glm.mat4(1.)
        powerup_model = glm.scale(powerup_model, glm.vec3(.2, .2, 1))
        # look for center
        powerup_model = glm.translate(powerup_model, glm.vec3(0.5, 0.5, 0))  # center in cell
        powerup_model = glm.translate(powerup_model, glm.vec3(coordinate_to_wrc(self.powerup_x, width),
                                                              coordinate_to_wrc(self.powerup_y, height), .0))
        self.powerup_program['model'].write(powerup_model)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.maze_program = self.ctx.program(vertex_shader=open('./maze.vert.glsl').read(),
                                             fragment_shader=open('./maze.frag.glsl').read())

        self.hero_program = self.ctx.program(vertex_shader=open('./hero.vert.glsl').read(),
                                             fragment_shader=open('./maze.frag.glsl').read())

        self.enemy_program = self.ctx.program(vertex_shader=open('./hero.vert.glsl').read(),
                                              fragment_shader=open('./maze.frag.glsl').read())

        self.score_board_program = self.ctx.program(vertex_shader=open('./maze.vert.glsl').read(),
                                                    fragment_shader=open('./maze.frag.glsl').read())

        self.display()

        self.model = glm.mat4(1.)
        self.model = glm.scale(self.model, glm.vec3(2, 2, 0))

    def gen_maze(self):
        dest, temp = None, None
        x, y = None, None
        if self.length == width * height:
            self.state = 1
            for i in range(width * height):
                self.cell[i].is_open = False
            return

        if self.length == 0:
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

            self.length = 1

        cell_open = False

        while not cell_open:
            temp = self.chosen[rand() % self.length]
            x, y = temp % width, int(temp / width)

            dest = rand() % 4

            if dest == direction.up:
                if (y == height - 1) or self.cell[cell_index(x, y + 1)].is_open:
                    continue
                self.cell[cell_index(x, y + 1)].is_open = True

                self.cell[cell_index(x, y + 1)].road[direction.down] = True
                self.cell[cell_index(x, y)].road[direction.up] = True

                self.chosen[self.length] = width * (y + 1) + x
                self.length += 1
                cell_open = True

            elif dest == direction.down:
                if (y == 0) or self.cell[cell_index(x, y - 1)].is_open:
                    continue
                self.cell[cell_index(x, y - 1)].is_open = True

                self.cell[cell_index(x, y - 1)].road[direction.up] = True
                self.cell[cell_index(x, y)].road[direction.down] = True

                self.chosen[self.length] = width * (y - 1) + x
                self.length += 1
                cell_open = True

            elif dest == direction.right:
                if (x == width - 1) or self.cell[cell_index(x + 1, y)].is_open:
                    continue

                self.cell[cell_index(x + 1, y)].is_open = True

                self.cell[cell_index(x + 1, y)].road[direction.left] = True
                self.cell[cell_index(x, y)].road[direction.right] = True

                self.chosen[self.length] = width * y + x + 1
                self.length += 1
                cell_open = True

            elif dest == direction.left:
                if (x == 0) or self.cell[cell_index(x - 1, y)].is_open:
                    continue

                self.cell[cell_index(x - 1, y)].is_open = True

                self.cell[cell_index(x - 1, y)].road[direction.right] = True
                self.cell[cell_index(x, y)].road[direction.left] = True

                self.chosen[self.length] = width * y + x - 1
                self.length += 1
                cell_open = True

    def hero_path_finder(self):
        if self.hero_path_finding_x is None and self.hero_path_finding_y is None:
            self.hero_path_finding_x, self.hero_path_finding_y = self.starting_x, self.starting_y

        if self.hero_path_finding_x == self.powerup_x and self.hero_path_finding_y == self.powerup_y:
            print('Power Up found')
            self.power += 1
            self.powerup_x, self.powerup_y = None, None
            self.power_up_vao = None

        if self.hero_path_finding_x == self.obstacle_x and self.hero_path_finding_y == self.obstacle_y:
            self.power -= 1
            print('Obstacle found', self.power)
            self.obstacle_x, self.obstacle_y = None, None
            self.obstacle_vao = None

        if self.hero_path_finding_x == self.enemy_path_finding_x and \
                self.hero_path_finding_y == self.enemy_path_finding_y:
            print('Enemy attacked and Hero died')
            self.power = 0
            self.hero_path_finding_x, self.hero_path_finding_y = None, None
            self.hero_vao = None

        if self.hero_path_finding_x == self.bomb_x and self.hero_path_finding_y == self.bomb_y:
            print('Found Bomb')
            self.bomb_y, self.bomb_x = None, None
            self.bomb_vao = None
            for i in range(width):
                for j in range(1, height):
                    self.cell[cell_index(i, j)].road[direction.down] = True
                    self.cell[cell_index(i, j - 1)].road[direction.up] = True
            self.gen_maze()

        if self.hero_finder is None:
            self.hero_finder = player(self.starting_x, self.starting_y, width, height, 'hero')

            self.hero_vert_vbo = self.ctx.buffer(self.hero_finder.player_body['coors'].astype('f4').tobytes())
            self.hero_color_vbo = self.ctx.buffer(self.hero_finder.player_body['color'].astype('f4').tobytes())

            self.hero_vao_content = [(self.hero_vert_vbo, '2f', 'in_vert'),
                                     (self.hero_color_vbo, '3f', 'in_color')
                                     ]

            self.hero_vao = self.ctx.vertex_array(self.hero_program, self.hero_vao_content)

        self.hero_finder.update_status()

        if self.hero_finder.is_moving():
            return

        if (self.hero_path_finding_x == self.goal_x) and (self.hero_path_finding_y == self.goal_y):
            self.state += 1
            self.hero_finder.set_getgoal()  # finished
            self.enemy_vao = None
            return

        if self.user_input_direction > -1:
            if self.user_input_direction == direction.up:
                if self.cell[cell_index(self.hero_path_finding_x, self.hero_path_finding_y)].road[direction.up] and (
                        self.hero_path_finding_y < height - 1) and \
                        (not self.cell[cell_index(self.hero_path_finding_x, self.hero_path_finding_y + 1)].is_open):
                    self.hero_finder.set_dest(direction.up)
                    self.hero_path_finding_y += 1

            elif self.user_input_direction == direction.down:
                if self.cell[cell_index(self.hero_path_finding_x, self.hero_path_finding_y)].road[direction.down] and (
                        self.hero_path_finding_y > 0) and \
                        (not self.cell[cell_index(self.hero_path_finding_x, self.hero_path_finding_y - 1)].is_open):
                    self.hero_finder.set_dest(direction.down)
                    self.hero_path_finding_y -= 1

            elif self.user_input_direction == direction.right:
                if self.cell[cell_index(self.hero_path_finding_x, self.hero_path_finding_y)].road[direction.right] and (
                        self.hero_path_finding_x < width - 1) and \
                        (not self.cell[cell_index(self.hero_path_finding_x + 1, self.hero_path_finding_y)].is_open):
                    self.hero_finder.set_dest(direction.right)
                    self.hero_path_finding_x += 1

            elif self.user_input_direction == direction.left:
                if self.cell[cell_index(self.hero_path_finding_x, self.hero_path_finding_y)].road[direction.left] and (
                        self.hero_path_finding_x > 0) and \
                        (not self.cell[cell_index(self.hero_path_finding_x - 1, self.hero_path_finding_y)].is_open):
                    self.hero_finder.set_dest(direction.left)
                    self.hero_path_finding_x -= 1
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

        self.to_remove_walls = []
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
        rand_float = 1.
        self.grid_colors = np.array([rand_float for i in range(3 * int(len(self.grid) / 2))])

        self.grid_color_vbo = self.ctx.buffer(self.grid_colors.tobytes())

        self.grid_vao_content = [
            (self.grid_vbo, '2f', 'in_vert'),
            (self.grid_color_vbo, '3f', 'in_color')
        ]

        self.grid_vao = self.ctx.vertex_array(self.maze_program, self.grid_vao_content)

        if len(self.to_remove_walls):
            self.to_remove_walls_vbo = self.ctx.buffer(self.to_remove_walls.astype('f4').tobytes())

            self.to_remove_walls_color_vbo = self.ctx.buffer(
                np.array([background.r, background.b, background.g] * int(len(self.to_remove_walls))).astype(
                    'f4').tobytes())

            self.to_remove_walls_vao_content = [
                (self.to_remove_walls_vbo, '2f', 'in_vert'),
                (self.to_remove_walls_color_vbo, '3f', 'in_color')
            ]

            self.to_remove_walls_vao = self.ctx.vertex_array(self.maze_program, self.to_remove_walls_vao_content)

            if self.hero_finder:
                self.hero_program['model'].write(
                    self.hero_finder.draw(self.state > 1, self.current_time - self.init_time))

            if self.enemy_finder:
                self.enemy_program['model'].write(
                    self.enemy_finder.draw(self.state > 1, self.current_time - self.init_time)
                )

    def render(self, time: float, frame_time: float):

        if self.init_time == 0:
            self.init_time = time
            self.prev_time = self.init_time

        self.prev_time = self.current_time
        self.current_time = time

        if self.state == 0:
            self.gen_maze()
        elif self.state == 1:
            self.score_board()
            self.hero_path_finder()
            if rand() % 5 == 3:
                self.enemy_path_finder()
            self.review_point()
        elif self.state > 1:
            # exit(0)
            pass

        self.display()
        self.maze_program['model'].write(self.model)
        self.maze_program['projection'].write(self.projection)

        self.ctx.clear(background.r, background.g, background.b)

        self.grid_vao.render(moderngl.LINES)

        if len(self.to_remove_walls):
            self.to_remove_walls_vao.render(moderngl.LINES)

        if self.bomb_vao:
            self.bomb_program['projection'].write(self.projection)
            self.bomb_vao.render()

        if self.hero_vao:
            self.hero_program['projection'].write(self.projection)
            self.hero_vao.render()

        if self.power_up_vao:
            self.powerup_program['projection'].write(self.projection)
            self.power_up_vao.render()

        if self.obstacle_vao:
            self.obstacle_program['projection'].write(self.projection)
            self.obstacle_vao.render()

        if self.enemy_vao:
            self.enemy_program['projection'].write(self.projection)
            self.enemy_vao.render()

        if self.score_board_vao:
            self.score_board_program['projection'].write(self.projection)
            self.score_board_vao.render()

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys
        if action == keys.ACTION_PRESS:
            if key == keys.UP:
                self.user_input_direction = direction.up
            if key == keys.DOWN:
                self.user_input_direction = direction.down
            if key == keys.LEFT:
                self.user_input_direction = direction.left
            if key == keys.RIGHT:
                self.user_input_direction = direction.right
            if key == keys.PAGE_UP:
                if self.view_zoomfactor - 1 > 0:
                    self.view_zoomfactor -= 1
            if key == keys.PAGE_DOWN:
                if self.view_zoomfactor < width:
                    self.view_zoomfactor += 1
            if key == keys.SPACE:  # starts Maze
                self.state = 0
                self.power_up()
                self.obstacle()
                self.bomb()
        self.review_point()
        self.display()

    def review_point(self):
        if self.hero_finder is None:
            return
        view_left = self.hero_finder.current_x() - (self.view_zoomfactor)
        view_right = self.hero_finder.current_x() + self.view_zoomfactor
        view_bottom = self.hero_finder.current_y() - (self.view_zoomfactor)
        view_up = self.hero_finder.current_y() + self.view_zoomfactor

        self.projection = glm.ortho(view_left, view_right, view_bottom, view_up)

    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)


background = color(.0, .0, .0)
game.run()
