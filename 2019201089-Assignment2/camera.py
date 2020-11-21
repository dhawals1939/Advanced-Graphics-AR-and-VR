from util import *
import glm
from ray import ray


class camera:
    def __init__(self):
        self.aspect_ratio = 16 / 9
        self.viewport_height = 2.
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.

        self.origin = glm.vec3(0, 0, 0)
        self.horizontal, self.vertical = glm.vec3(self.viewport_width, 0, 0), glm.vec3(0, self.viewport_height, 0)

        self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - glm.vec3(0, 0,
                                                                                                  self.focal_length)

    def get_ray(self, u, v) -> ray:
        return ray(self.origin, self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)
