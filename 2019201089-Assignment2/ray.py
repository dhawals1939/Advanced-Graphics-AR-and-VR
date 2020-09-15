import glm


class ray:
    def __init__(self, origin: glm.vec3, direction: glm.vec3):
        self.orig, self.direc = origin, direction

    def origin(self) -> glm.vec3:
        return self.orig

    def direction(self) -> glm.vec3:
        return self.direc

    def __str__(self):
        return str(self.orig.to_list()) + " " + str(self.direc.to_list())

    def at(self, t) -> glm.vec3:
        return self.orig + t * self.direc
