from hittable import hittable, hit_record
from aabb import aabb
from material import material
from ray import ray
import glm
import numpy as np


class triangle(hittable):
    def __init__(self, a: glm.vec3, b: glm.vec3, c: glm.vec3, mat_ptr: material):
        self.a, self.b, self.c = a, b, c
        self.mp = mat_ptr

        self.centroid = (a + b + c) / 3

    def hit(self, r: ray, t_min, t_max, rec: hit_record) -> bool:
        diff_a_ray_orig = self.a - r.origin()
        diff_a_b = self.a - self.b
        diff_a_c = self.a - self.c
        d = r.direction()

        A = np.array([
            diff_a_b.to_list(),
            diff_a_c.to_list(),
            d.to_list()
        ])

        V = np.array(diff_a_ray_orig.to_list())

        solution = None
        try:
            solution = np.linalg.solve(A, V)
        except:
            return False

        beta, gamma, t = solution

        if not (t_min < t < t_max):
            return False

        if not (0 < gamma < 1):
            return False

        if not (0 < beta < (1 - gamma)):
            return False

        rec.u = .4
        rec.v = .4
        rec.t = t

        outward_normal = glm.cross(diff_a_c, diff_a_b)

        rec.set_face_normal(r, outward_normal)
        rec.p = r.at(t)

        rec.mat_ptr.albedo, rec.mat_ptr.fuzz, rec.mat_ptr.ref_ind = self.mp.albedo, self.mp.fuzz, self.mp.ref_ind
        rec.mat_ptr.scatter = self.mp.scatter
        rec.mat_ptr.emitted = self.mp.emitted
        rec.mat_ptr.emit = self.mp.emit

        return True

    def bounding_box(self, t0: float, t1: float, output_box: aabb) -> bool:
        min_x, min_y, min_z = min(self.a.x, self.b.x, self.c.x), min(self.a.y, self.b.y, self.c.y), \
                              min(self.a.z, self.b.z, self.c.z)

        max_x, max_y, max_z = max(self.a.x, self.b.x, self.c.x), max(self.a.y, self.b.y, self.c.y), \
                              max(self.a.z, self.b.z, self.c.z)

        _output_box = aabb(glm.vec3(min_x - .001, min_y - .001, min_z - .001),
                           glm.vec3(max_x + .001, max_y + .001, max_z + .001))

        output_box.mini, output_box.maxi = _output_box.mini, output_box.maxi
        return True
