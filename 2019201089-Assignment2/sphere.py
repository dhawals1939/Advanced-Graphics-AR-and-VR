from hittable import hittable, hit_record
import glm
from util import *
from ray import ray
from material import material
from aabb import aabb


class sphere(hittable):
    def __init__(self, cen: glm.vec3, radius: float, mat: material):
        super(sphere, self).__init__()
        self.center = cen
        self.radius = radius
        self.mat_ptr = mat

    def hit(self, r: ray, t_min, t_max, rec: hit_record) -> bool:
        oc = r.origin() - self.center
        a = glm.length2(r.direction())
        half_b = glm.dot(oc, r.direction())
        c = glm.length2(oc) - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant > 0:
            root = glm.sqrt(discriminant)

            temp = (-half_b - root) / a
            if t_min < temp < t_max:
                rec.t = temp
                rec.p = r.at(rec.t)
                outward_normal = (rec.p - self.center) / self.radius
                rec.set_face_normal(r, outward_normal)

                rec.mat_ptr.albedo, rec.mat_ptr.fuzz, rec.mat_ptr.ref_ind = self.mat_ptr.albedo, self.mat_ptr.fuzz, self.mat_ptr.ref_ind
                rec.mat_ptr.scatter = self.mat_ptr.scatter
                rec.mat_ptr.emitted = self.mat_ptr.emitted
                rec.mat_ptr.emit = self.mat_ptr.emit

                rec.u, rec.v = get_sphere_uv((rec.p - self.center) / self.radius)

                return True

            temp = (-half_b + root) / a
            if t_min < temp < t_max:
                rec.t = temp
                rec.p = r.at(rec.t)
                outward_normal = (rec.p - self.center) / self.radius
                rec.set_face_normal(r, outward_normal)

                rec.mat_ptr.albedo, rec.mat_ptr.fuzz, rec.mat_ptr.ref_ind = self.mat_ptr.albedo, self.mat_ptr.fuzz, self.mat_ptr.ref_ind
                rec.mat_ptr.scatter = self.mat_ptr.scatter
                rec.mat_ptr.emitted = self.mat_ptr.emitted
                rec.mat_ptr.emit = self.mat_ptr.emit

                rec.u, rec.v = get_sphere_uv((rec.p - self.center) / self.radius)

                return True

        return False

    def bounding_box(self, t0: float, t1: float, output_box: aabb) -> bool:
        _min = self.center - glm.vec3(self.radius, self.radius, self.radius)
        _max = self.center + glm.vec3(self.radius, self.radius, self.radius)

        output_box.mini.x, output_box.mini.y, output_box.mini.z = _min.x, _min.y, _min.z
        output_box.maxi.x, output_box.maxi.y, output_box.maxi.z = _max.x, _max.y, _max.z
        return True
