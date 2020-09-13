import glm
from ray import ray


class camera:
    aspect_ratio = 16 / 9
    viewport_height = 2.
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1.

    origin = glm.vec3(0, 0, 0)

    horizontal, vertical = glm.vec3(viewport_width, .0, .0), glm.vec3(.0, viewport_height, .0)
    lower_left_corner = origin - (horizontal / 2 + vertical / 2 + glm.vec3(0, 0, focal_length))

    def __init__(self):
        pass

    def get_ray(self, u: float, v: float) -> ray:
        return ray(self.origin, self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)

