import math
from hittable import *


class sphere(hittable):
    center, radius = None, None

    def __init__(self, cen: glm.vec3, radius):
        super(sphere, self).__init__()
        self.center = cen
        self.radius = radius

    def hit(self, r: ray, t_min, t_max, rec: hit_record) -> bool:
        oc = r.origin() - self.center
        a = glm.length2(r.direction())
        half_b = glm.dot(oc, r.direction())
        c = glm.length2(oc) - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant > 0:
            root = math.sqrt(discriminant)

            temp = (-half_b - root) / a
            if t_min < temp < t_max:
                rec.t = temp
                rec.p = r.at(rec.t)
                outward_normal = (rec.p - self.center) / self.radius
                rec.set_face_normal(r, outward_normal)
                return True

            temp = (-half_b + root) / a
            if t_min < temp < t_max:
                rec.t = temp
                rec.p = r.at(rec.t)
                outward_normal = (rec.p - self.center) / self.radius
                rec.set_face_normal(r, outward_normal)
                return True

        return False


