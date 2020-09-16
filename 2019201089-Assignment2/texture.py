import glm


class texture:
    def __init__(self):
        pass

    def value(self, u: float, v: float, p: glm.vec3) -> glm.vec3:
        raise NotImplementedError


class solid_color(texture):
    def __init__(self, c: glm.vec3):
        self.color_value = glm.vec3(0, 0, 0)

        self.color_value.x, self.color_value.y, self.color_value.z = c.x, c.y, c.z

    def value(self, u: float, v: float, p: glm.vec3) -> glm.vec3:
        return self.color_value


class checker_texture(texture):
    def __init__(self, c1: glm.vec3 = None, c2: glm.vec3 = None, tex0: texture = None, tex1: texture = None):
        if tex0 is None and tex1 is None:
            self.even, self.odd = solid_color(c1), solid_color(c2)
        else:
            self.even = tex0
            self.odd = tex1

    def value(self, u: float, v: float, p: glm.vec3) -> glm.vec3:
        sines = glm.sin(10 * p.x) * glm.sin(10 * p.y) * glm.sin(10 * p.z)

        return self.odd.value(u, v, p) if sines < 0 else self.even.value(u, v, p)
