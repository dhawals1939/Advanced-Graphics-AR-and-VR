def coordinate_to_wrc(x, directional_extreme):
    center_factor = -int((directional_extreme + 2) / 2 - 1)
    return x + center_factor


roll_fact = 10


class directions:
    up, down, right, left, not_any_direction = list(range(5))
    not_up, not_down, not_right, not_left = list(range(4, 8))
