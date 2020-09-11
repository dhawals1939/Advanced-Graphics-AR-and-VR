from ray import ray
import glm


class hit_record:
    p, normal, t, front_face = None, None, None, None

    def set_face_normal(self, r: ray, outward_normal: glm.vec3):
        self.front_face = glm.dot(r.direction(), outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class hittable:
    def hit(self, r: ray, t_min, t_max, rec: hit_record):
        raise NotImplementedError
