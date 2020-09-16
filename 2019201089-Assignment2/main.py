import math
import sys
import time

from tqdm import tqdm

from camera import camera
from hittable import hit_record, hittable
from hittable_list import hittable_list
from sphere import sphere

from cornell_box import cornell_box
from material import *
from aarect import *


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


def ray_color(r: ray, background: glm.vec3, world: hittable, depth: int) -> glm.vec3:
    rec = hit_record()

    if depth <= 0:
        return glm.vec3(0, 0, 0)

    if world.hit(r, 0.001, math.inf, rec):
        attenuation = glm.vec3(0, 0, 0)  # Dummy
        scattered = ray(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0))
        emitted = rec.mat_ptr.emitted(rec.u, rec.v, rec.p)

        if rec.mat_ptr.scatter(r, rec, attenuation, scattered):
            return emitted + attenuation * ray_color(scattered, background, world, depth - 1)
        else:
            return emitted

    else:  # NOT HIT CASE
        return background


# Image
aspect_ratio = 16 / 9
width = 400
height = int(width / aspect_ratio)

samples_per_pixel = None

# World
background = glm.vec3(.1, .1, .1)  # background color
#
#
#
# diffuseLight = diffuse_light(color=glm.vec3(1, 1, 1))
#
# world = hittable_list(xz_rect(-5, 5, -10, 0, -.9, material_ground))
# world.add(sphere(glm.vec3(0.0, 0.0, -2.0), 0.5, material_center))
# world.add(sphere(glm.vec3(-2.0, 0.0, -2.0), 0.5, material_left))
# world.add(sphere(glm.vec3(1.0, 0.0, -1.0), 0.5, material_right))
#
# # Light
# world.add(yz_rect(-2, 2, -2, -1, .5, diffuseLight))


diffuse_material = lambertian(glm.vec3(.5, .2, .1))

world = cornell_box()
world.add(sphere(glm.vec3(-1.0, 0.0, -2.0), 0.5, diffuse_material))

# Camera
cam = camera()

output_file = sys.argv[1] if len(sys.argv) > 1 else str(time.time()) + '.ppm'
samples_per_pixel = int(sys.argv[2].strip()) if len(sys.argv) > 2 else 10
max_depth = int(sys.argv[3].strip()) if len(sys.argv) > 3 else 100

with open(output_file, 'w') as f:
    f.write('P3\n%d %d\n255\n' % (width, height))
    for j in tqdm(range(height - 1, -1, -1), desc='loading:'):
        for i in range(width):
            color = glm.vec3(0, 0, 0)

            for sample in range(samples_per_pixel):
                u, v = (i + random_double()) / (width - 1), (j + random_double()) / (height - 1)
                r = cam.get_ray(u, v)
                color += ray_color(r, background, world, max_depth)

            write_color(f, color, spp=samples_per_pixel)
