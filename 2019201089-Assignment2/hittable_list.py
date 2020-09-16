from hittable import hittable, hit_record
from ray import ray
import glm
from aabb import aabb, surrounding_box


class hittable_list(hittable):

    def __init__(self, obj):
        self.objects = []
        self.objects.append(obj)

    def add(self, obj):
        self.objects.append(obj)

    def clear(self):
        self.objects = []

    def hit(self, r: ray, t_min, t_max, rec: hit_record):
        hit_anything, closest_so_far = False, t_max
        temp_record = hit_record()

        for obj in self.objects:
            if obj.hit(r, t_min, closest_so_far, temp_record):
                hit_anything, closest_so_far = True, temp_record.t
                rec.p, rec.t, = temp_record.p, temp_record.t
                rec.normal, rec.front_face = temp_record.normal, temp_record.front_face
                # rec.mat_ptr.scatter = temp_record.mat_ptr.scatter
                rec.mat_ptr.emit = temp_record.mat_ptr.emit

                rec.mat_ptr.albedo, rec.mat_ptr.fuzz, rec.mat_ptr.ref_ind = temp_record.mat_ptr.albedo, temp_record.mat_ptr.fuzz, temp_record.mat_ptr.ref_ind
                rec.mat_ptr.scatter = temp_record.mat_ptr.scatter
                rec.mat_ptr.emitted = temp_record.mat_ptr.emitted

        return hit_anything

    def bounding_box(self, t0: float, t1: float, output_box: aabb) -> bool:
        if len(self.objects) == 0:
            return False

        temp_box = aabb(glm.vec3(0, 0, 0), glm.vec3(0, 0, 0))
        first_box = True

        for object in self.objects:
            if not object.bounding_box(t0, t1, temp_box):
                return False

            _output_box = temp_box if first_box else surrounding_box(output_box, temp_box)
            output_box.mini, output_box.maxi = _output_box.min(), _output_box.max()
            first_box = False

        return True
