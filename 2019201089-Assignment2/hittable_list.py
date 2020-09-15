from hittable import hittable, hit_record
from ray import ray


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
                rec.mat_ptr.scatter = temp_record.mat_ptr.scatter

                rec.mat_ptr.albedo, rec.mat_ptr.fuzz, rec.mat_ptr.ref_ind = temp_record.mat_ptr.albedo, temp_record.mat_ptr.fuzz, temp_record.mat_ptr.ref_ind
                rec.mat_ptr.scatter = temp_record.mat_ptr.scatter

        return hit_anything
