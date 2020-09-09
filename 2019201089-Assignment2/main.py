import glm
from tqdm import tqdm
from ray import ray

from sphere import hit_sphere

aspect_ratio = 16 / 9
width = 800
height = int(width / aspect_ratio)

viewport_height = 2.
viewport_width = aspect_ratio * viewport_height
focal_length = 1.

origin = glm.vec3(.0, .0, .0)
horizontal = glm.vec3(viewport_width, 0., 0.)
vertical = glm.vec3(0., viewport_height, .0)
lower_left_corner = origin - horizontal / 2 - vertical / 2 - glm.vec3(0., 0., focal_length)


def write_color(file, color: glm.vec3):
    if file:
        file.write('%d %d %d\n' % tuple((255.999 * color).to_list()))


def ray_color(r: ray) -> glm.vec3:
    t = hit_sphere(glm.vec3(0., 0., -1), .5, r)
    if t > .0:
        N = glm.normalize(r.at(t) - glm.vec3(0, 0, -1))
        return 0.5 * glm.vec3(N.x+1, N.y+1, N.z+1)

    unit_direction = glm.normalize(r.direc)
    t = .5 * (unit_direction.y + 1.)
    # both glms vectors are color vectors
    return (1. - t) * glm.vec3(1., 1., 1.) + t * glm.vec3(.5, .7, 1.)


with open('sphere.ppm', 'w') as f:
    f.write('P3\n%d %d\n255\n' % (width, height))
    for j in tqdm(range(height - 1, -1, -1), desc='loading:'):
        for i in range(width - 1, -1, -1):
            u, v = i / (width - 1), j / (height - 1)
            r = ray(origin, lower_left_corner + u * horizontal + v * vertical - origin)
            color = ray_color(r)

            write_color(f, color)
