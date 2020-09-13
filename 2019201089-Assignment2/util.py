import random


def random_double() -> float:
    return random.uniform(0, 1)


def clamp(x, _min, _max) -> float:
    if _min <= x <= _max:
        return x
    return _min if x < _min else _max
