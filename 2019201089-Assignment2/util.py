import random


def random_double() -> float:
    return random.uniform(0, .9999999999)


def random_double_in_range(_min, _max) -> float:
    return random.uniform(_min, _max - .000000000001)


def clamp(x: float, _min: float, _max: float) -> float:
    if _min <= x <= _max:
        return x
    return _min if x < _min else _max
