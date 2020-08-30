import moderngl_window
import moderngl
import numpy as np
import glm
from copy import deepcopy


class triangle(moderngl_window.WindowConfig):
    gl_version = (4, 3)
    title = 'Sample 1.2-Triangle'
    resizable = True
    aspect_ratio = 16 / 9
    window_size = (1920, 1080)
    text_shader = None

    def text(self, location, scale, color, text):
        self.text_shader['textColor'].write(color)

        self

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ctx.enable(moderngl.CULL_FACE)
        self.ctx.enable(moderngl.BLEND)

        vertices = np.array([
            -.5, 0.7,
            -.25, .2,
            .0, .0,
            .0, .0,
            .5, 0.7,
            .25, .2
        ])
        self.program = self.ctx.program(
            vertex_shader=open('maze.vert.glsl').read(),
            fragment_shader=open('maze.frag.glsl').read()
        )

        self.text_shader = self.ctx.program(vertex_shader=open('./text.vert.glsl').read(),
                                            fragment_shader=open('./text.frag.glsl').read())

        color = np.array([
            1., .2, .2,
            1., .2, .2,
            1., .2, .2,
            1., .2, .2,
            1., .2, .2,
            1., .2, .2,
        ])

        # indices = np.array(
        #     [
        #         0, 1, 2,
        #     ]
        # )

        self.vbo = self.ctx.buffer(vertices.astype('float32').tobytes())
        # self.ebo = self.ctx.buffer(indices.astype('int32').tobytes())
        self.cbo = self.ctx.buffer(color.astype('f4').tobytes())

        vao_content = [
            (self.vbo, '2f', 'in_vert'),
            (self.cbo, '3f', 'in_color')
        ]
        self.vao = self.ctx.vertex_array(self.program, vao_content)  # , self.ebo)
        self.points = False  # if False else True

        model = glm.mat4(1.)
        # model  = glm.scale(model, glm.vec3(.05, .05, 1))
        self.program['model'].write(model)

        self.program_2 = self.ctx.program(
            vertex_shader=open('maze.vert.glsl').read(),
            fragment_shader=open('maze.frag.glsl').read()
        )
        self.vao_2 = self.ctx.vertex_array(self.program_2, vao_content)
        self.program_2['model'].write(glm.translate(model, glm.vec3(5, 5, 0)))

    def render(self, time: float, frame_time: float):

        word = 'rtart'
        x, y = 0, 0
        scale = 0
        color = glm.vec3(1., .0, .0)
        self.text((x, y), scale, word, color)
        self.ctx.clear(.0, .0, .0)

        if self.points:
            '''plot only points'''
            mode = moderngl.POINTS
        else:
            mode = moderngl.TRIANGLES
        self.vao.render(mode=mode)
        self.vao_2.render(mode=mode)

    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)


triangle.run()


def rand():
    return 1

def cell_index(x, y):
    return 1

width, height = 0, 0

class tess(moderngl_window.WindowConfig):

    enemy_path_finding_x, enemy_path_finding_y = None, None
    enemy_finder = None
    enemy_vert_vbo, enemy_color_vbo = None, None
    enemy_program, enemy_vao_content, enemy_vao = None, None, None

    def enemy_path_finder(self):
        if self.enemy_path_finding_x is None and self.enemy_path_finding_y is None:
            self.enemy_path_finding_x, self.enemy_path_finding_y = rand() % width, rand() % height
            while self.enemy_path_finding_x == self.start_x and self.enemy_path_finding_y == self.start_y:
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

        if (self.enemy_path_finding_x == self.goal_x) and (self.enemy_path_finding_y == self.goal_y):
            self.state += 1
            self.enemy_finder.set_getgoal()  # finished
            return

        enemy_movement_direction = rand()% 4
        if enemy_movement_direction > -1:
            if enemy_movement_direction == direction.up:
                if self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y)].road[direction.up] and (
                        self.enemy_path_finding_y < height - 1) and \
                        (not self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y + 1)].is_open):
                    self.enemy_finder.set_dest(direction.up)
                    self.enemy_path_finding_y += 1

            elif enemy_movement_direction == direction.down:
                if self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y)].road[direction.down] and (
                        self.enemy_path_finding_y > 0) and \
                        (not self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y - 1)].is_open):
                    self.enemy_finder.set_dest(direction.down)
                    self.enemy_path_finding_y -= 1

            elif enemy_movement_direction == direction.right:
                if self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y)].road[direction.right] and (
                        self.enemy_path_finding_x < width - 1) and \
                        (not self.cell[cell_index(self.enemy_path_finding_x + 1, self.enemy_path_finding_y)].is_open):
                    self.enemy_finder.set_dest(direction.right)
                    self.enemy_path_finding_x += 1

            elif enemy_movement_direction == direction.left:
                if self.cell[cell_index(self.enemy_path_finding_x, self.enemy_path_finding_y)].road[direction.left] and (
                        self.enemy_path_finding_x > 0) and \
                        (not self.cell[cell_index(self.enemy_path_finding_x - 1, self.enemy_path_finding_y)].is_open):
                    self.enemy_finder.set_dest(direction.left)
                    self.enemy_path_finding_x -= 1
            enemy_movement_direction = -1
