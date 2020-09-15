import glm
from tqdm import tqdm
import math
from ray import ray

from sphere import sphere
from hittable import *
from util import *
from hittable_list import hittable_list
from camera import camera


def write_color(file, color: glm.vec3, spp=1):
    if file:
        r, g, b = color.x, color.y, color.z

        scale = 1 / spp
        r = math.sqrt(scale * r)
        g = math.sqrt(scale * g)
        b = math.sqrt(scale * b)

        file.write('%d %d %d\n' % (256 * clamp(r, 0, .999),
                                   256 * clamp(g, 0, .999),
                                   256 * clamp(b, 0, .999)))


def ray_color(r: ray, world: hittable, depth: int) -> glm.vec3:
    rec = hit_record()

    if depth <= 0:
        return glm.vec3(0, 0, 0)

    if world.hit(r, 0.001, math.inf, rec):
        target = rec.p + rec.normal + random_in_hemisphere(rec.normal)
        return .5 * ray_color(ray(rec.p, target - rec.p), world, depth -1)

    unit_direction = glm.normalize(r.direction())
    t = .5 * (unit_direction.y + 1.)
    # both glms vectors are color vectors
    return (1. - t) * glm.vec3(1., 1., 1.) + t * glm.vec3(.5, .7, 1.)


# Image
aspect_ratio = 16 / 9
width = 400
height = int(width / aspect_ratio)

samples_per_pixel = 20

max_depth = 400

# World
world = hittable_list(sphere(glm.vec3(0, 0, -1), .5))
world.add(sphere(glm.vec3(0, -100.5, -1), 100))

# Camera
cam = camera()

with open('lambertian_aliased_sphere.ppm', 'w') as f:
    f.write('P3\n%d %d\n255\n' % (width, height))
    for j in tqdm(range(height - 1, -1, -1), desc='loading:'):
        for i in range(width):
            color = glm.vec3(0, 0, 0)

            for sample in range(samples_per_pixel):

                u, v = (i + random_double()) / (width - 1), (j + random_double()) / (height - 1)
                r = cam.get_ray(u, v)
                color += ray_color(r, world, max_depth)

            write_color(f, color, spp=samples_per_pixel)
