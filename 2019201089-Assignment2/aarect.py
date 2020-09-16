from hittable import hittable, hit_record
from aabb import aabb
from material import material
from ray import ray
import glm


class xy_rect(hittable):
    def __init__(self, _x0: float, _x1: float, _y0: float, _y1: float, _k: float, mat: material):
        self.x0, self.y0, self.x1, self.y1, self.k = _x0, _y0, _x1, _y1, _k
        self.mp = mat

    def hit(self, r: ray, t_min, t_max, rec: hit_record) -> bool:
        t = (self.k - r.origin().z) / r.direction().z if r.direction().z != 0 else 0

        if not t_min <= t <= t_max:
            return False

        x = r.origin().x + t * r.direction().x
        y = r.origin().y + t * r.direction().y

        if (not self.x0 < x < self.x1) or (not self.y0 < y < self.y1):
            return False

        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (y - self.y0) / (self.y1 - self.y0)
        rec.t = t

        outward_normal = glm.vec3(0, 0, 1)

        rec.set_face_normal(r, outward_normal)
        rec.p = r.at(t)

        rec.mat_ptr.albedo, rec.mat_ptr.fuzz, rec.mat_ptr.ref_ind = self.mp.albedo, self.mp.fuzz, self.mp.ref_ind
        rec.mat_ptr.scatter = self.mp.scatter
        rec.mat_ptr.emitted = self.mp.emitted
        rec.mat_ptr.emit = self.mp.emit

        return True

    def bounding_box(self, t0: float, t1: float, output_box: aabb) -> bool:
        _output_box = aabb(glm.vec3(self.x0, self.y0, self.k - .0001), glm.vec3(self.x1, self.y1, self.k + .0001))
        output_box.mini, output_box.maxi = _output_box.mini, _output_box.maxi
        return True


class xz_rect(hittable):
    def __init__(self, _x0: float, _x1: float, _z0: float, _z1: float, _k: float, mat: material):
        self.x0, self.z0, self.x1, self.z1, self.k = _x0, _z0, _x1, _z1, _k
        self.mp = mat

    def hit(self, r: ray, t_min, t_max, rec: hit_record) -> bool:
        t = (self.k - r.origin().y) / r.direction().y if r.direction().y != 0 else 0

        if not t_min <= t <= t_max:
            return False

        x = r.origin().x + t * r.direction().x
        z = r.origin().z + t * r.direction().z

        if (not self.x0 < x < self.x1) or (not self.z0 < z < self.z1):
            return False

        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.t = t

        outward_normal = glm.vec3(0, 1, 0)

        rec.set_face_normal(r, outward_normal)
        rec.p = r.at(t)

        rec.mat_ptr.albedo, rec.mat_ptr.fuzz, rec.mat_ptr.ref_ind = self.mp.albedo, self.mp.fuzz, self.mp.ref_ind
        rec.mat_ptr.scatter = self.mp.scatter
        rec.mat_ptr.emitted = self.mp.emitted
        rec.mat_ptr.emit = self.mp.emit

        return True

    def bounding_box(self, t0: float, t1: float, output_box: aabb) -> bool:
        _output_box = aabb(glm.vec3(self.x0, self.k - .0001, self.z0), glm.vec3(self.x1, self.k - .0001, self.z1))
        output_box.mini, output_box.maxi = _output_box.mini, _output_box.maxi
        return True


class yz_rect(hittable):
    def __init__(self, _y0: float, _y1: float, _z0: float, _z1: float, _k: float, mat: material):
        self.y0, self.z0, self.y1, self.z1, self.k = _y0, _z0, _y1, _z1, _k
        self.mp = mat

    def hit(self, r: ray, t_min, t_max, rec: hit_record) -> bool:

        t = (self.k - r.origin().x) / r.direction().x if r.direction().x != 0 else 0

        if not t_min <= t <= t_max:
            return False

        y = r.origin().y + t * r.direction().y
        z = r.origin().z + t * r.direction().z

        if (not self.y0 < y < self.y1) or (not self.z0 < z < self.z1):
            return False

        rec.u = (y - self.y0) / (self.y1 - self.y0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.t = t

        outward_normal = glm.vec3(1, 0, 0)

        rec.set_face_normal(r, outward_normal)
        rec.p = r.at(t)

        rec.mat_ptr.albedo, rec.mat_ptr.fuzz, rec.mat_ptr.ref_ind = self.mp.albedo, self.mp.fuzz, self.mp.ref_ind
        rec.mat_ptr.scatter = self.mp.scatter
        rec.mat_ptr.emitted = self.mp.emitted
        rec.mat_ptr.emit = self.mp.emit

        return True

    def bounding_box(self, t0: float, t1: float, output_box: aabb) -> bool:
        _output_box = aabb(glm.vec3(self.k - .0001, self.y0, self.z0), glm.vec3(self.k - .0001, self.y1, self.z1))
        output_box.mini, output_box.maxi = _output_box.mini, _output_box.maxi
        return True
