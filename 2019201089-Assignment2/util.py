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


def random_in_hemisphere(normal: glm.vec3) -> glm.vec3:
    in_unit_sphere = random_in_unit_sphere()
    if glm.dot(in_unit_sphere, normal) > .0:
        return in_unit_sphere
    else:
        return -in_unit_sphere
