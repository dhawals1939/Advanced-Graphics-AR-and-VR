from ray import ray
from util import *
from texture import *


class material:
    def __init__(self):
        self.albedo, self.fuzz, self.ref_ind = None, None, None

    def scatter(self, r_in: ray, rec, attenuation: glm.vec3, scattered: ray) -> bool:
        raise NotImplementedError

    def emitted(self, u: float, v: float, p: glm.vec3)-> glm.vec3:
        return glm.vec3(0, 0, 0)


class lambertian(material):
    def __init__(self, a: glm.vec3 = None, tex=None):
        if tex is not None:
            self.albedo = tex
        else:
            self.albedo = solid_color(a)

        self.fuzz, self.ref_ind = None, None
        self.emit = None

    def scatter(self, r_in: ray, rec, attenuation: glm.vec3, scattered: ray) -> bool:
        scatter_direction = rec.normal + random_unit_vector()
        _scattered = ray(rec.p, scatter_direction)
        scattered.orig = _scattered.origin()
        scattered.direc = _scattered.direction()

        _albedo_corr = self.albedo.value(rec.u, rec.v, rec.p)
        attenuation.x, attenuation.y, attenuation.z = _albedo_corr.x, _albedo_corr.y, _albedo_corr.z

        return True


class metal(material):
    def __init__(self, fuzz: float, color: glm.vec3 = None, tex=None):
        self.albedo = None
        if tex is not None:
            self.albedo = tex
        else:
            self.albedo = solid_color(color)

        self.fuzz, self.ref_ind = fuzz if fuzz < 1 else 1, None
        self.emit = None

    def scatter(self, r_in: ray, rec, attenuation: glm.vec3, scattered: ray) -> bool:
        reflected = reflect(glm.normalize(r_in.direction()), rec.normal)

        _scattered = ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())

        scattered.orig = _scattered.origin()
        scattered.direc = _scattered.direction()

        _albedo_corr = self.albedo.value(rec.u, rec.v, rec.p)
        attenuation.x, attenuation.y, attenuation.z = _albedo_corr.x, _albedo_corr.y, _albedo_corr.z

        return glm.dot(scattered.direction(), rec.normal) > 0


class dielectric(material):
    def __init__(self, ri: float):
        self.ref_ind = ri
        self.fuzz, self.albedo = None, None
        self.emit = None

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


class diffuse_light(material):
    def __init__(self, tex: texture = None, color: glm.vec3 = None):
        self.albedo, self.fuzz, self.ref_ind = None, None, None
        self.emit = None
        if tex is not None:
            self.emit = tex
        else:
            self.emit = solid_color(color)

    def scatter(self, r_in: ray, rec, attenuation: glm.vec3, scattered: ray) -> bool:
        return False

    def emitted(self, u: float, v: float, p: glm.vec3):
        return self.emit.value(u, v, p)
