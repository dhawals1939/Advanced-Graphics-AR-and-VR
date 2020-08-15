import moderngl_window
import moderngl
import glm
import math
import numpy as np
from pathlib import Path


class pentagonal_pyramid(moderngl_window.WindowConfig):
    gl_version = (4, 3)
    window_size = (1920, 1080)
    resource_dir = Path('.').absolute()
    resizable = True
    title = 'Pentagonal Pyramid'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.program = self.ctx.program(vertex_shader=open('./pentagonal_pyramid.vert.glsl').read(),
                                        fragment_shader=open('./pentagonal_pyramid.frag.glsl').read())

        godel_ratio = (1 + math.sqrt(5)) / 2

import moderngl
import moderngl_window
from pathlib import Path
import numpy as np
import glm
import math

class camera(moderngl_window.WindowConfig):
    gl_version = (4, 3)
    resource_dir = Path('.').absolute()
    resizable = True
    window_size = (1920, 1080)
    aspect_ratio = 16 / 9
    title = "Camera"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.program = self.ctx.program(vertex_shader=open("./pentagonal_pyramid.vert.glsl").read(),
                                        fragment_shader=open("./pentagonal_pyramid.frag.glsl").read())

        # self.texture_bg = self.load_texture_2d('../imgs/wall.jpg')
        # self.texture_fg = self.load_texture_2d('../imgs/awesomeface.png')

        # self.program['out_tex_bg'] = 0
        # self.program['out_tex_fg'] = 1

        self.box_vertices = np.array(
            [
                # pentagon base
                .5, 0, -.5,
                .0, .5, -.5,
                .5, -.5, -.5,
                .5, -.5, -.5,
                -.5, -.5, -.5,
                .0, .5, -.5,
                .0, .5, -.5,
                -.5, .0, -.5,
                -.5, -.5, -.5,

                # pentagon sides
                .5, 0, -.5,
                0, .5, -.5,
                0, 0, 0,

                0, 0, 0,
                0, .5, -.5,
                -.5, 0, -.5,

                -.5, 0, -.5,
                -.5, -.5, -.5,
                0, 0, 0,

                0, 0, 0,
                .5, -.5, -.5,
                - .5, -.5, -.5
            ]
        )

        self.color = np.array(
            [
                # pentagon base
                1., 0, 0,
                .0, 1., .0,
                .0, 0., 1,
                .0, 0., 1,
                .5, .5, 0,
                .0, 1, 0,
                .0, 1, 0,
                .5, .0, .5,
                .5, .5, .0,

                # pentagon sides
                1, 0, 0,
                0, 1, 0,
                0.5, 0.5, 0.5,

                0.5, 0.5, 0.5,
                0, 1, .0,
                .5, 0, .5,

                .5, 0, .5,
                .5, .5, 0,
                0.5, 0.5, 0.5,

                0.5, 0.5, 0.5,
                .0, .0, 1.,
                .5, .5, 0
            ]
        )

        self.box_vbo = self.ctx.buffer(self.box_vertices.astype('f4').tobytes())
        self.color_vbo = self.ctx.buffer(self.color.astype('f4').tobytes())

        self.vao_content = [
            (self.box_vbo, '3f', 'in_vert'),
            (self.color_vbo, '3f', 'in_color')
        ]

        self.vao = self.ctx.vertex_array(self.program, self.vao_content)

    def render(self, time: float, frame_time: float):
        self.ctx.clear(.0, .0, .0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        model, view = glm.mat4(1.0), glm.mat4(1.0)

        # self.texture_bg.use(0)
        # self.texture_fg.use(1)

        radius = 10.0
        view = glm.lookAt(glm.vec3(math.sin(time) * radius, .0, math.cos(time) * radius),
                          glm.vec3(.0, .0, .0), glm.vec3(.0, 1., .0))

        projection = glm.perspective(glm.radians(45.0), self.aspect_ratio, 0.1, 100.)

        self.program["projection"].write(projection)

        self.program['view'].write(view)
        model = glm.translate(model, glm.vec3(0.0, 0.0, 0.0))
        angle = 20.
        model = glm.rotate(model, glm.radians(angle), glm.vec3(1., .3, .5))

        self.program['model'].write(model)
        self.vao.render()
        # for i in range(len(self.cube_positions)):


    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)


camera.run()
