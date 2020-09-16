from util import *
import glm
from ray import ray


class aabb:
    def __init__(self, a: glm.vec3, b: glm.vec3):
        self.mini, self.maxi = a, b

    def min(self):
        return self.mini

    def max(self):
        return self.maxi

    def hit(self, r: ray, tmin: float, tmax: float) -> bool:
        for a in range(3):
            invD = 1. / r.direction()[a]

            t0 = glm.fmin((self.mini[a] - r.origin()[a]) * invD,
                          (self.maxi[a] - r.origin()[a]) * invD)

            t1 = glm.fmax((self.mini[a] - r.origin()[a]) * invD,
                          (self.maxi[a] - r.origin()[a]) * invD)

            tmin, tmax = glm.fmax(t0, tmin), glm.fmin(t1, tmax)

            if tmax <= tmin:
                return False

        return True


def surrounding_box(box0: aabb, box1: aabb) -> aabb:
    small = glm.vec3(
        glm.fmin(box0.min().x(), box1.min().x()),
        glm.fmin(box0.min().y(), box1.min().y()),
        glm.fmin(box0.min().z(), box1.min().z()))

    big = glm.vec3(
        glm.fmax(box0.max().x(), box1.max().x()),
        glm.fmax(box0.max().y(), box1.max().y()),
        glm.fmax(box0.max().z(), box1.max().z())
    )

    return aabb(small, big)
