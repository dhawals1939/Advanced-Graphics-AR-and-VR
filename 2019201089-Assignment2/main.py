import math
import sys
import time

from tqdm import tqdm

from camera import camera
from hittable import hit_record, hittable
from hittable_list import hittable_list
from ray import ray
from sphere import sphere
from util import *
from material import *


def write_color(file, color: glm.vec3, spp=1):
    if file:
        r, g, b = color.x, color.y, color.z

        scale = 1 / spp
        r = glm.sqrt(scale * r)
        g = glm.sqrt(scale * g)
        b = glm.sqrt(scale * b)

        file.write('%d %d %d\n' % (256 * clamp(r, 0, .999),
                                   256 * clamp(g, 0, .999),
                                   256 * clamp(b, 0, .999)))


def ray_color(r: ray, world: hittable, depth: int) -> glm.vec3:
    rec = hit_record()

    if depth <= 0:
        return glm.vec3(0, 0, 0)

    if world.hit(r, 0.001, math.inf, rec):
        attenuation, scattered = glm.vec3(0, 0, 0), ray(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0))  # Dummy

        if rec.mat_ptr.scatter(r, rec, attenuation, scattered):
            return attenuation * ray_color(scattered, world, depth - 1)
        return glm.vec3(0, 0, 0)

    unit_direction = glm.normalize(r.direction())
    t = .5 * (unit_direction.y + 1.)
    # both glms vectors are color vectors
    return (1. - t) * glm.vec3(1., 1., 1.) + t * glm.vec3(.5, .7, 1.)


# Image
aspect_ratio = 16 / 9
width = 400
height = int(width / aspect_ratio)

samples_per_pixel = None


# World

material_ground = lambertian(glm.vec3(.8, .8, .0))
material_center = lambertian(glm.vec3(.1, .2, .5))

material_left = dielectric(1.5)
material_right = metal(glm.vec3(0.8, 0.6, 0.2), .0)

world = hittable_list(sphere(glm.vec3(0.0, -100.5, -1.0), 100.0, material_ground))
world.add(sphere(glm.vec3(0.0, 0.0, -1.0), 0.5, material_center))
world.add(sphere(glm.vec3(-1.0, 0.0, -1.0), 0.5, material_left))
world.add(sphere(glm.vec3(1.0, 0.0, -1.0), 0.5, material_right))

# Camera
cam = camera()

output_file = sys.argv[1] if len(sys.argv) > 1 else str(time.time()) + '.ppm'
samples_per_pixel = int(sys.argv[2].strip()) if len(sys.argv) > 2 else 30
max_depth = int(sys.argv[3].strip()) if len(sys.argv) > 3 else 10

with open(output_file, 'w') as f:
    f.write('P3\n%d %d\n255\n' % (width, height))
    for j in tqdm(range(height - 1, -1, -1), desc='loading:'):
        for i in range(width):
            color = glm.vec3(0, 0, 0)

            for sample in range(samples_per_pixel):
                u, v = (i + random_double()) / (width - 1), (j + random_double()) / (height - 1)
                r = cam.get_ray(u, v)
                color += ray_color(r, world, max_depth)

            write_color(f, color, spp=samples_per_pixel)
