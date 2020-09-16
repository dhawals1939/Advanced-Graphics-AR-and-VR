from hittable import hittable
from hittable_list import hittable_list
from aarect import *
import glm


class box(hittable):
    def __init__(self, p0: glm.vec3, p1: glm.vec3, mat_ptr: material):
        self.box_min, self.box_max = glm.vec3(0, 0, 0), glm.vec3(0, 0, 0)

        self.box_min.x, self.box_min.y, self.box_min.z = p0.x, p0.y, p0.z
        self.box_max.x, self.box_max.y, self.box_max.z = p1.x, p1.y, p1.z

        self.sides = hittable_list(xy_rect(p0.x, p1.x, p0.y, p1.y, p1.z, mat_ptr))
        self.sides.add(xy_rect(p0.x, p1.x, p0.y, p1.y, p0.z, mat_ptr))

        self.sides.add(xz_rect(p0.x, p1.x, p0.z, p1.z, p1.y, mat_ptr))
        self.sides.add(xz_rect(p0.x, p1.x, p0.z, p1.z, p0.y, mat_ptr))

        self.sides.add(yz_rect(p0.y, p1.y, p0.z, p1.z, p1.x, mat_ptr))
        self.sides.add(yz_rect(p0.y, p1.y, p0.z, p1.z, p0.x, mat_ptr))

    def hit(self, r: ray, t_min, t_max, rec: hit_record) -> bool:
        return self.sides.hit(r, t_min, t_max, rec)

    def bounding_box(self, t0: float, t1: float, output_box: aabb) -> bool:
        _output_box = aabb(self.box_min, self.box_max)

        output_box.mini, output_box.maxi = _output_box.mini, output_box.maxi

        return True

