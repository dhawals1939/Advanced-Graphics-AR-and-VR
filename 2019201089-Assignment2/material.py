from hittable import hit_record
from ray import ray
import glm


class material:
    def scatter(self, rec: hit_record, attenuation: glm.vec3, scattered: ray):
        raise NotImplementedError
