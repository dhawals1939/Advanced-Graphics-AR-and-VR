up, down, right, left = list(range(4))


class Cell:
    def __init__(self):
        self.is_open = False
        self.road = [False] * 4
