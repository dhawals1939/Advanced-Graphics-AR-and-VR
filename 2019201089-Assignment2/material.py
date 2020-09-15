from ray import ray
from util import *


class material:
    def __init__(self):
        self.albedo, self.fuzz, self.ref_ind = None, None, None

    def scatter(self, r_in: ray, rec, attenuation: glm.vec3, scattered: ray) -> bool:
        raise NotImplementedError


class lambertian(material):
    def __init__(self, a: glm.vec3):
        self.albedo = a
        self.fuzz, self.ref_ind = None, None

    def scatter(self, r_in: ray, rec, attenuation: glm.vec3, scattered: ray) -> bool:
        scatter_direction = rec.normal + random_unit_vector()
        _scattered = ray(rec.p, scatter_direction)
        scattered.orig = _scattered.origin()
        scattered.direc = _scattered.direction()

        attenuation.x, attenuation.y, attenuation.z = self.albedo.x, self.albedo.y, self.albedo.z
        return True


class metal(material):
    def __init__(self, a :glm.vec3):
        self.albedo = a
        self.fuzz, self.ref_ind = None, None

    def scatter(self, r_in: ray, rec, attenuation: glm.vec3, scattered: ray) -> bool:
        reflected = reflect(glm.normalize(r_in.direction()), rec.normal)

        _scattered = ray(rec.p, reflected)

        scattered.orig = _scattered.origin()
        scattered.direc = _scattered.direction()

        attenuation.x, attenuation.y, attenuation.z = self.albedo.x, self.albedo.y, self.albedo.z

        return glm.dot(scattered.direction(), rec.normal) > 0
