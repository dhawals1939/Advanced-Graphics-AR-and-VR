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
    def __init__(self, a: glm.vec3, fuzz: float):
        self.albedo = a
        self.fuzz, self.ref_ind = fuzz if fuzz < 1 else 1, None

    def scatter(self, r_in: ray, rec, attenuation: glm.vec3, scattered: ray) -> bool:
        reflected = reflect(glm.normalize(r_in.direction()), rec.normal)

        _scattered = ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())

        scattered.orig = _scattered.origin()
        scattered.direc = _scattered.direction()

        attenuation.x, attenuation.y, attenuation.z = self.albedo.x, self.albedo.y, self.albedo.z

        return glm.dot(scattered.direction(), rec.normal) > 0


class dielectric(material):
    def __init__(self, ri: float):
        self.ref_ind = ri
        self.fuzz, self.albedo = None, None

    def scatter(self, r_in: ray, rec, attenuation: glm.vec3, scattered: ray) -> bool:
        _att = glm.vec3(1., 1., 1.)
        attenuation.x, attenuation.y, attenuation.z = _att.x, _att.y, _att.z

        etai_over_etat = 1 / self.ref_ind if rec.front_face else self.ref_ind

        cos_theta = glm.fmin(glm.dot(-glm.normalize(r_in.direction()), rec.normal), 1.)
        sin_theta = glm.sqrt(1. - cos_theta * cos_theta)

        refracted_or_reflected = None
        if sin_theta * etai_over_etat > 1.:
            refracted_or_reflected = reflect(glm.normalize(r_in.direction()), rec.normal)
        else:
            refracted_or_reflected = refract(glm.normalize(r_in.direction()), rec.normal, etai_over_etat)

        _scattered = ray(rec.p, refracted_or_reflected)

        scattered.orig = _scattered.origin()
        scattered.direc = _scattered.direction()

        return True
