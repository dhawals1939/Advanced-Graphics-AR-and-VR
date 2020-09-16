import random
import glm


def random_double() -> float:
    return random.uniform(0, 1)


def random_double_in_range(_min, _max):
    return random.uniform(_min, _max)


def clamp(x, _min, _max) -> float:
    if _min <= x <= _max:
        return x
    return _min if x < _min else _max


def random_vec3() -> glm.vec3:
    return glm.vec3(random_double(), random_double(), random_double())


def random_vec3_in_range(_min, _max) -> glm.vec3:
    return glm.vec3(random_double_in_range(_min, _max),
                    random_double_in_range(_min, _max),
                    random_double_in_range(_min, _max))


def random_in_unit_sphere() -> glm.vec3:
    while True:
        p = random_vec3_in_range(-1, 1)
        if glm.length2(p) >= 1:
            continue
        return p


def random_unit_vector() -> glm.vec3:
    a = random_double_in_range(0, 2 * glm.pi())
    z = random_double_in_range(-1, 1)
    r = glm.sqrt(1 - z * z)
    return glm.vec3(r * glm.cos(a), r * glm.sin(a), z)


def random_in_hemisphere(normal: glm.vec3) -> glm.vec3:
    in_unit_sphere = random_in_unit_sphere()
    if glm.dot(in_unit_sphere, normal) > .0:
        return in_unit_sphere
    else:
        return -in_unit_sphere


def reflect(v: glm.vec3, n: glm.vec3):
    return v - 2 * glm.dot(v, n) * n


def refract(uv: glm.vec3, n: glm.vec3, etai_over_etat: float) -> glm.vec3:
    cos_theta = glm.dot(-uv, n)
    r_out_perpendicular = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -glm.sqrt(glm.abs(1. - glm.length2(r_out_perpendicular))) * n
    return r_out_perpendicular + r_out_parallel


def get_sphere_uv(p: glm.vec3) -> [int, int]:
    import math
    try:
        phi = math.atan2(p.z, p.x)
        theta = math.asin(p.y)
    except ValueError:
        phi, theta = 0, 0

    return 1 - (phi + math.pi) / (2 * math.pi), (theta + math.pi / 2) / math.pi
