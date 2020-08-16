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
        self.view = glm.mat4(1.0)

        self.last_frame, self.delta_time = .0, .0

        self.projection = glm.perspective(glm.radians(45.0), self.aspect_ratio, 0.1, 100.0)

        self.program['projection'].write(self.projection)

        self.camera_pos = glm.vec3(.0, .0, 3.0)
        self.camera_front = glm.vec3(0.0, 0.0, -1.0)
        self.camera_up = glm.vec3(0.0, 1.0, 0.0)

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

                # # pentagon sides
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

        self.triangle = np.array(
            [
                -.5, 0, 0,
                -.25, .5, 0,
                -.25, 0, 0,
            ]
        )

        self.triangle_color = np.array(
            [
                1., .0, .0,
                .0, 1., .0,
                .0, .0, 1.
            ]
        )
        self.box_vbo = self.ctx.buffer(self.box_vertices.astype('f4').tobytes())
        self.color_vbo = self.ctx.buffer(self.color.astype('f4').tobytes())

        self.vao_content = [
            (self.box_vbo, '3f', 'in_vert'),
            (self.color_vbo, '3f', 'in_color')
        ]

        self.vao = self.ctx.vertex_array(self.program, self.vao_content)

        # other object for reference
        self.triangle_vbo = self.ctx.buffer(self.triangle.astype('f4').tobytes())
        self.triangle_color_vbo = self.ctx.buffer(self.triangle_color.astype('f4').tobytes())

        self.program_2 = self.ctx.program(vertex_shader=open('./pentagonal_pyramid.vert.glsl').read(),
                                          fragment_shader=open('./pentagonal_pyramid.frag.glsl').read())

        self.program_2['projection'].write(self.projection)
        self.program_2['world'].write(self.world)

        self.vao_content2 = [
            (self.triangle_vbo, '3f', 'in_vert'),
            (self.triangle_color_vbo, '3f', 'in_color')
        ]
        self.vao2 = self.ctx.vertex_array(self.program_2, self.vao_content2)
        self.ctx.wireframe = True

    def render(self, time: float, frame_time: float):
        self.ctx.clear(.0, .0, .0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.delta_time = time - self.last_frame
        self.last_frame = time

        # angle = 0.02 * time
        # self.world = glm.rotate(self.world, glm.radians(angle), glm.vec3(1., .3, .5))
        self.program['world'].write(self.world)

        self.view = glm.lookAt(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)
        self.program['view'].write(self.view)
        self.program_2['view'].write(self.view)

        self.vao.render()
        self.vao2.render()

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        camera_speed = 2.5 * self.delta_time

        if action == keys.ACTION_PRESS:
            if key == keys.W:  # Z into the screen
                self.world = glm.translate(self.world,
                                           glm.vec3(self.world[0][3], self.world[1][3], self.world[2][3] - .1))
            if key == keys.S:
                self.world = glm.translate(self.world,
                                           glm.vec3(self.world[0][3], self.world[1][3], self.world[2][3] + .1))
            if key == keys.A:  # X right of screen
                self.world = glm.translate(self.world,
                                           glm.vec3(self.world[0][3] - .1, self.world[1][3], self.world[2][3]))
            if key == keys.D:
                self.world = glm.translate(self.world,
                                           glm.vec3(self.world[0][3] + .1, self.world[1][3], self.world[2][3]))
            if key == keys.R:
                self.world = glm.translate(self.world,
                                           glm.vec3(self.world[0][3], self.world[1][3] + .1, self.world[2][3]))
            if key == keys.F:
                self.world = glm.translate(self.world,
                                           glm.vec3(self.world[0][3], self.world[1][3] - .1, self.world[2][3]))
            # Camera Movement
            if key == keys.INSERT:
                self.camera_pos += camera_speed * self.camera_front;
            if key == keys.DELETE:
                self.camera_pos -= camera_speed * self.camera_front;
            if key == keys.HOME:
                self.camera_pos -= glm.normalize(glm.cross(self.camera_front, self.camera_up)) * camera_speed
            if key == keys.END:
                self.camera_pos += glm.normalize(glm.cross(self.camera_front, self.camera_up)) * camera_speed
            if key == keys.PAGE_UP:
                self.camera_pos += self.camera_up * camera_speed
            if key == keys.PAGE_DOWN:
                self.camera_pos -= self.camera_up * camera_speed
            if key == keys.B:
                self.camera_pos = glm.vec3(.0, .0, .0)
                self.camera_front = glm.vec3(0.0, 0.0, -1.0)
                self.camera_up = glm.vec3(0.0, 1.0, 0.0)
                self.view = glm.lookAt(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)
            if key == keys.N:
                self.camera_pos = glm.vec3(.0, .0, .5)
                self.camera_front = glm.vec3(0.0, 0.0, -1.0)
                self.camera_up = glm.vec3(0.0, 1.0, 0.0)
                self.view = glm.lookAt(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)
            if key == keys.M:
                self.camera_pos = glm.vec3(.0, .0, 3.0)
                self.camera_front = glm.vec3(0.0, 0.0, -1.0)
                self.camera_up = glm.vec3(0.0, 1.0, 0.0)
                self.view = glm.lookAt(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    @classmethod
    def run(cls):
        moderngl_window.run_window_config(cls)


pentagonal_pyramid.run()
