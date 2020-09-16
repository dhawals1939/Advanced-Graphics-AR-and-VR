from hittable import *
from hittable_list import *
import glm
from functools import cmp_to_key
import random


def box_compare(a: hittable, b: hittable, axis):
    box_a, box_b = aabb(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0)), aabb(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0))

    if (not a.bounding_box(0, 0, box_a)) or (not b.bounding_box(0, 0, box_b)):
        print('no bounding box')

    return box_a.min()[axis] - box_b.min()[axis]


def box_x_compare(a: hittable, b: hittable):
    return box_compare(a, b, 0)


def box_y_compare(a: hittable, b: hittable):
    return box_compare(a, b, 1)


def box_z_compare(a: hittable, b: hittable):
    return box_compare(a, b, 2)


class bvh_node(hittable):
    def __init__(self, objects_list: hittable_list, time0: float, time1: float, start=None, end=None):
        self.left, self.right, self.box = aabb(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0)), \
                                          aabb(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0)), \
                                          aabb(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0))

        if start is None and end is None:
            start, end = 0, len(objects_list.objects)

        axis = random.randint(0, 2)

        comparator = None
        if axis == 0:
            comparator = box_x_compare
        elif axis == 1:
            comparator = box_y_compare
        elif axis == 2:
            comparator = box_z_compare

        object_span = end - start

        if object_span == 1:
            self.left = self.right = objects_list.objects[start]
        elif object_span == 2:
            if comparator(objects_list.objects[start], objects_list.objects[start + 1]):
                self.left, self.right = objects_list.objects[start], objects_list.objects[start + 1]
            else:
                self.right, self.left = objects_list.objects[start], objects_list.objects[start + 1]
        else:
            #test need to check later obj reference
            objects_list.objects = sorted(objects_list.objects[start:end], key=cmp_to_key(comparator))
            mid = int(start + object_span / 2)
            self.left = bvh_node(objects_list, start, mid, time0, time1)
            self.right = bvh_node(objects_list, mid, end, time0, time1)

        box_left, box_right = aabb(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0)), aabb(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0))

        if (not self.left.bounding_box(time0, time1, box_left)) or (not self.right.bounding_box(time0, time1, box_right)):
            print('No boundig box vbh')

        self.box = surrounding_box(box_left, box_right)


    def hit(self, r: ray, t_min, t_max, rec: hit_record) -> bool:
        if not self.box.hit(r, t_min, t_max):
            return False

        hit_left = self.left.hit(r, t_min, t_max, rec)
        hit_right = self.right.hit(r, t_min, rec.t if hit_left else t_max, rec)

        return hit_left or hit_right

    def bounding_box(self, t0: float, t1: float, output_box: aabb) -> aabb:
        output_box.mini, output_box.maxi = self.box.mini, self.box.maxi
        return True
