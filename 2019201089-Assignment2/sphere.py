import glm
from ray import ray


def hit_sphere(center: glm.vec3, radius: float, r: ray) -> bool:
    oc = r.origin() - center
    a = glm.dot(r.direction(), r.direction())
    b = 2. * glm.dot(oc, r.direction())
    c = glm.dot(oc, oc) - radius * radius
    discriminant = b ** 2 - 4 * a * c

    return discriminant > 0
