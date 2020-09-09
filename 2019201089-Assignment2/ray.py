import glm


class ray:
    orig, direc = None, None

    def __init__(self, origin: glm.vec3, direction: glm.vec3):
        self.orig, self.direc = origin, direction

    def origin(self) -> glm.vec3:
        return self.orig

    def direction(self) -> glm.vec3:
        return self.direc

    def at(self, t) -> glm.vec3:
        return self.orig + t * self.direc
