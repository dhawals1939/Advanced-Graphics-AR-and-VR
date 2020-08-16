import moderngl
import moderngl_window
from pathlib import Path
import numpy as np
import glm
import math

class pentagonal_pyramid(moderngl_window.WindowConfig):
    gl_version = (4, 3)
    resource_dir = Path('.').absolute()
    resizable = True
    window_size = (1920, 1080)
    aspect_ratio = 16 / 9
    title = "pentagonal_pyramid"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.program = self.ctx.program(vertex_shader=open("./pentagonal_pyramid.vert.glsl").read(),
                                        fragment_shader=open("./pentagonal_pyramid.frag.glsl").read())

        self.world = glm.mat4(1.0)

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
                0, 0, 0.5,

                0, 0, 0.5,
                0, .5, -.5,
                -.5, 0, -.5,

                -.5, 0, -.5,
                -.5, -.5, -.5,
                0, 0, 0.5,

                0, 0, 0.5,
                - .5, -.5, -.5,
                .5, -.5, -.5,

                .5, -.5, -.5,
                .5, 0, -.5,
                0, 0, 0.5


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
                .5, .5, 0,

                0, 0, 1.,
                1, 0, 0,
                .5, .5, .5
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

        self.program['world'].write(self.world)
        self.vao.render()

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys
        current_postion = glm.vec3(self.world[0][3], self.world[1][3], self.world[2][3])
        if action == keys.ACTION_PRESS:
            if key == keys.W:       #Z into the screen
                self.world = glm.translate(self.world, glm.vec3(self.world[0][3], self.world[1][3], self.world[2][3] - .1))
            if key == keys.S:
                self.world = glm.translate(self.world, glm.vec3(self.world[0][3], self.world[1][3], self.world[2][3] + .1))
            if key == keys.A:       # X right of screen
                self.world = glm.translate(self.world, glm.vec3(self.world[0][3] - .1, self.world[1][3], self.world[2][3]))
            if key == keys.D:
                self.world = glm.translate(self.world, glm.vec3(self.world[0][3] + .1, self.world[1][3], self.world[2][3]))
            if key == keys.R:
                self.world = glm.translate(self.world, glm.vec3(self.world[0][3], self.world[1][3] + .1, self.world[2][3]))
            if key == keys.F:
                self.world = glm.translate(self.world, glm.vec3(self.world[0][3], self.world[1][3] - .1, self.world[2][3]))


    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)


pentagonal_pyramid.run()
