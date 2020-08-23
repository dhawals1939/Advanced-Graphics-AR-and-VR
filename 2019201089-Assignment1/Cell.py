class directions():
    up, down, right, left, not_any_direction = list(range(5))
    not_up, not_down, not_right, not_left = list(range(4, 8))


class Cell:
    def __init__(self):
        self.is_open = False
        self.road = [False] * 4
