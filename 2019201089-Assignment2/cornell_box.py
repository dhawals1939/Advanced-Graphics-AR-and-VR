from hittable_list import hittable_list
from material import *
from aarect import *
from sphere import *
from texture import *
import glm


def cornell_box() -> hittable_list:
    checker = checker_texture(glm.vec3(0., 0., 0.), glm.vec3(0.9, 0.9, 0.9))
    material_ground = metal(.0, tex=checker)

    red = lambertian(glm.vec3(.65, .05, .05))
    white = lambertian(glm.vec3(.74, .73, .73))
    green = lambertian(glm.vec3(.12, .45, .15))

    light = diffuse_light(color=glm.vec3(15, 15, 15))

    # world = hittable_list(yz_rect(-1, 1, -5, 0, -2, green))  # left wall
    world = hittable_list(yz_rect(-1, 1, -5, 0, 2, red))  # left wall

    world.add(yz_rect(-1, 1, -5, 0, 2, red))  # right wall

    world.add(xz_rect(-1, 1, -2.5, -1.5, .9, light))  # light

    world.add(xz_rect(-2, 2, -5, 0, -1, material_ground))  # ground

    world.add(xz_rect(-2, 2, -5, 0, 1, white))  # roof

    world.add(xy_rect(-2, 2, -1, 1, -5, white))  # facing wall

    return world
