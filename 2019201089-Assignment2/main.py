import glm
from tqdm import tqdm
import math
from ray import ray

from sphere import sphere
from hittable import *
from hittable_list import hittable_list


def write_color(file, color: glm.vec3):
    if file:
        file.write('%d %d %d\n' % tuple((255.999 * color).to_list()))


def ray_color(r: ray, world: hittable) -> glm.vec3:
    rec = hit_record()

    if world.hit(r, 0, math.inf, rec):
        world.hit(r, 0, math.inf, rec)
        return .5 * (rec.normal + glm.vec3(1., 1., 1.))

    unit_direction = glm.normalize(r.direction())
    t = .5 * (unit_direction.y + 1.)
    # both glms vectors are color vectors
    return (1. - t) * glm.vec3(1., 1., 1.) + t * glm.vec3(.5, .7, 1.)


aspect_ratio = 16 / 9
width = 400
height = int(width / aspect_ratio)

viewport_height = 2.
viewport_width = aspect_ratio * viewport_height
focal_length = 1.

origin = glm.vec3(.0, .0, .0)
horizontal = glm.vec3(viewport_width, 0., 0.)
vertical = glm.vec3(0., viewport_height, .0)
lower_left_corner = origin - horizontal / 2 - vertical / 2 - glm.vec3(0., 0., focal_length)

world = hittable_list(sphere(glm.vec3(0, 0, -1), .5))
world.add(sphere(glm.vec3(0, -100.5, -1), 100))

with open('sphere.ppm', 'w') as f:
    f.write('P3\n%d %d\n255\n' % (width, height))
    for j in tqdm(range(height - 1, -1, -1), desc='loading:'):
        for i in range(width):
            u, v = i / (width - 1), j / (height - 1)
            r = ray(origin, lower_left_corner + u * horizontal + v * vertical - origin)
            color = ray_color(r, world)

            write_color(f, color)
