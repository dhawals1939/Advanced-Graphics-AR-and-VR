from ray import ray
import glm
from material import material
from aabb import aabb

class hit_record:

    def __init__(self):
        self.p, self.normal, self.t, self.front_face = None, None, None, None
        self.mat_ptr = material()

    def set_face_normal(self, r: ray, outward_normal: glm.vec3):
        self.front_face = glm.dot(r.direction(), outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class hittable:
    def hit(self, r: ray, t_min, t_max, rec: hit_record):
        raise NotImplementedError

    def bounding_box(self, t0: float, t1: float, output_box: aabb):
        raise NotImplementedError