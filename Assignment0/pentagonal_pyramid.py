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
        self.vertices = np.array(
            [
                1.701, 0, -0.175,
                0.525, 1.61, -0.175,
                0.525, -1.61, -0.175,
                -1.376, 1, -0.175,
                -1.376, -1, -0.175,
                0, 0, 0.876
            ]
        )
