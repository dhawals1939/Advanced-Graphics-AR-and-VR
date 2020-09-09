import glm
import math

from ray import ray


def hit_sphere(center: glm.vec3, radius: float, r: ray) -> float:
    oc = r.origin() - center
    a = glm.dot(r.direction(), r.direction())
    b = 2. * glm.dot(oc, r.direction())
    c = glm.dot(oc, oc) - radius * radius
    discriminant = b ** 2 - 4 * a * c
    return -1. if discriminant < 0 else (- b - math.sqrt(discriminant) / (2. * a))
