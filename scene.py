# coding: utf-8

from random import random
from math import sqrt, pi, cos, sin, inf, acos, exp


dist_min_vision = 0.00000001


def rotate_vetor_y(x: float, z: float, a: float):
    c = cos(a)
    s = sin(a)
    return x * c - z * s, x * s + z * c


def rotate_point_y(x: float, z: float, a: float, xc: float, zc: float):
    c = cos(a)
    s = sin(a)
    return (x - xc) * c - (z - zc) * s + xc, (x - xc) * s + (z - zc) * c + zc


class Object:
    def __init__(self, color: tuple, glossiness: float, mirror_reflection: float, roughness: float, texture: list):
        self.color = color
        self.roughness = roughness
        self.glossiness = glossiness
        self.mirror_reflection = mirror_reflection
        self.texture = texture
        # I'm not sure this is the right coef...
        self.coef_glossiness = (self.glossiness ** 2 + 1) / (self.glossiness + exp(-self.glossiness * pi / 2))

    def rotate_y(self, x: float, z: float, a: float):
        pass

    def get_texture(self, x: float, y: float, z: float):
        return self.color

    def get_intensity_coef(self, angle: float):
        return self.coef_glossiness * exp(-angle ** 2 * self.glossiness)


class Plan(Object):
    def __init__(self, u: tuple, v: tuple, point: tuple,
                 color: tuple = (1, 1, 1), glossiness: float = 0, mirror_reflection: float = 0,
                 roughness: float = 0, texture: list = None):
        self.x, self.y, self.z = point
        self.ux, self.uy, self.uz = u
        self.vx, self.vy, self.vz = v
        a = self.uy * self.vz - self.uz * self.vy
        b = self.ux * self.vz - self.uz * self.vx
        c = self.ux * self.vy - self.uy * self.vx
        dist = sqrt(a ** 2 + b ** 2 + c ** 2)
        self.a = a / dist
        self.b = b / dist
        self.c = c / dist
        self.d = -(self.a * self.x + self.b * self.y + self.c * self.z)
        Object.__init__(self, color, glossiness, mirror_reflection, roughness, texture)
        self.coef_texture = ()
        self.compute_coef_texture()

    def compute_coef_texture(self):
        if self.texture is not None:
            u_xyz_max = max(abs(self.ux), abs(self.uy), abs(self.uz))
            if u_xyz_max == abs(self.ux):
                n = 0
            elif u_xyz_max == abs(self.uy):
                n = 1
            else:
                n = 2
            self.coef_texture = (0, self.ux * self.vy - self.vx * self.uy, n)
            coef_2 = self.ux * self.vz - self.vx * self.uz
            coef_3 = self.uy * self.vz - self.vy * self.uz
            if abs(coef_2) > abs(self.coef_texture[1]):
                self.coef_texture = (1, coef_2, n)
            if abs(coef_3) > abs(self.coef_texture[1]):
                self.coef_texture = (2, coef_3, n)

    def rotate_y(self, x: float, z: float, a: float):
        old_a, old_c = self.a, self.c
        self.a, self.c = rotate_vetor_y(self.a, self.c, a)
        self.d += (old_a - self.a) * x + (old_c - self.c) * z
        self.x, self.z = rotate_point_y(self.x, self.z, a, x, z)
        self.ux, self.uz = rotate_vetor_y(self.ux, self.uz, a)
        self.vx, self.vz = rotate_vetor_y(self.vx, self.vz, a)
        self.compute_coef_texture()

    def get_texture(self, x: float, y: float, z: float):
        if self.coef_texture[0] == 0:
            y_texture = (self.ux * (y - self.y) - self.uy * (x - self.x)) / self.coef_texture[1]
        elif self.coef_texture[0] == 1:
            y_texture = (self.ux * (z - self.z) - self.uz * (x - self.x)) / self.coef_texture[1]
        else:
            y_texture = (self.uy * (z - self.z) - self.uz * (y - self.y)) / self.coef_texture[1]
        if self.coef_texture[2] == 0:
            x_texture = (x - self.x - y_texture * self.vx) / self.ux
        elif self.coef_texture[2] == 1:
            x_texture = (y - self.y - y_texture * self.vy) / self.uy
        else:
            x_texture = (z - self.z - y_texture * self.vz) / self.uz

        x_texture = int(-x_texture % len(self.texture[0]))
        y_texture = int(-y_texture % len(self.texture))
        return self.texture[y_texture][x_texture]


class Rectangle(Plan):
    def __init__(self, u: tuple, v: tuple, point: tuple, width: float, height: float,
                 color: tuple = (1, 1, 1), glossiness: float = 0, mirror_reflection: float = 0,
                 roughness: float = 0, texture: list = None):
        Plan.__init__(self, u, v, point, color, glossiness, mirror_reflection, roughness, texture)
        self.points = [point, (point[0] + width * u[0], point[1] + width * u[1], point[2] + width * u[2]),
                              (point[0] + width * u[0] + height * v[0], point[1] + width * u[1] + height * v[1],
                               point[2] + width * u[2] + height * v[2]),
                              (point[0] + height * v[0], point[1] + height * v[1], point[2] + height * v[2])]
        self.vectors = [u, v, (-u[0], -u[1], -u[2]), (-v[0], -v[1], -v[2])]

    def rotate_y(self, x: float, z: float, a: float):
        Plan.rotate_y(self, x, z, a)
        for i, (px, py, pz) in enumerate(self.points):
            px, pz = rotate_point_y(px, pz, a, x, z)
            self.points[i] = (px, py, pz)
        for i, (vx, vy, vz) in enumerate(self.vectors):
            vx, vz = rotate_vetor_y(vx, vz, a)
            self.vectors[i] = (vx, vy, vz)


class Sphere:
    def __init__(self, x: float, y: float, z: float, r: float):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def rotate_y(self, x: float, z: float, a: float):
        self.x, self.z = rotate_point_y(self.x, self.z, a, x, z)


class SphereObject(Sphere, Object):
    def __init__(self, x: float, y: float, z: float, r: float,
                 color: tuple = (1, 1, 1), glossiness: float = 0, mirror_reflection: float = 0,
                 roughness: float = 0, texture: list = None):
        Object.__init__(self, color, glossiness, mirror_reflection, roughness, texture)
        Sphere.__init__(self, x, y, z, r)

    def get_texture(self, x: float, y: float, z: float):
        return self.color  # TODO


class LightSource(Sphere):
    def __init__(self, x: float, y: float, z: float, intensity: float,
                 color: tuple = (1, 1, 1), radius_source: float = 0):
        Sphere.__init__(self, x, y, z, radius_source)
        self.color_intensity = (color[0] * intensity, color[1] * intensity, color[2] * intensity)


class Scene:
    def __init__(self, threshold_intensity_mirror_reflection: float, ambient_color: tuple = (0, 0, 0),
                 background_color: tuple = (0, 0, 0)):
        self.ambient_color = ambient_color
        self.background_color = background_color
        self.objects = []
        self.sources = []
        self.threshold_intensity_mirror_reflection = threshold_intensity_mirror_reflection

    def add_object(self, obj: Object):
        self.objects.append(obj)

    def add_source(self, source: LightSource):
        self.sources.append(source)

    def rotate_y_objects(self, x: float, z: float, a: float):
        for obj in self.objects:
            obj.rotate_y(x, z, a)

    def rotate_y_sources(self, x: float, z: float, a: float):
        for source in self.sources:
            source.rotate_y(x, z, a)

    def rotate_y(self, x: float, z: float, a: float):
        self.rotate_y_objects(x, z, a)
        self.rotate_y_sources(x, z, a)

    def calcul_ray_intensity(self, x: float, y: float, z: float, rx: float, ry: float, rz: float,
                             object_to_avoid: Object = None, coef_intensity: float = 1.0):
        # Return the light intensity that the ray receives
        # The ray start at (x, y, z) and points in the direction (rx, ry, rz)

        # -----------------------------------------------------
        # Step 1 : Find the closest object croosed by the ray

        closest_obj = None
        best_dist = inf
        inverse_normal = False

        # Looking for all the objects
        for obj in self.objects + self.sources:
            if obj == object_to_avoid:
                continue
            if isinstance(obj, Sphere):
                if obj.r == 0:
                    continue
                dx = x - obj.x
                dy = y - obj.y
                dz = z - obj.z

                a = rx ** 2 + ry ** 2 + rz ** 2
                b = 2 * (rx * dx + ry * dy + rz * dz)
                c = dx ** 2 + dy ** 2 + dz ** 2 - obj.r ** 2

                delta = b ** 2 - 4 * a * c

                # Is the ray crossing the object
                if delta > 0:
                    # t of the closest intersection from the vievwer
                    t = - (b + sqrt(delta)) / (2 * a)
                    # Is the object on the right side of the viewer
                    if t > dist_min_vision:
                        # Is this object closer to the viewer than the previous ones
                        if best_dist > t:
                            inverse_normal = False
                            best_dist = t
                            closest_obj = obj
                    else:  # Otherwise the viewer could be inside the sphere
                        t = - (t + b / a)
                        # Is this object closer to the viewer than the previous ones and on the right side of the viewer
                        if best_dist > t > dist_min_vision:
                            inverse_normal = True
                            best_dist = t
                            closest_obj = obj
            elif isinstance(obj, Plan):
                d = obj.a * rx + obj.b * ry + obj.c * rz
                # Is the plan parallel to the ray
                if d != 0:
                    t = obj.a * x + obj.b * y + obj.c * z + obj.d
                    # Is this object on the right side of the viewer
                    if (t < 0 < d) or (d < 0 < t):
                        t /= -d
                        # Is this object closer to the viewer than the previous ones
                        if dist_min_vision < t < best_dist:
                            is_inside = True
                            if isinstance(obj, Rectangle):
                                # Intersection point with the plan
                                ix = x + rx * t
                                iy = y + ry * t
                                iz = z + rz * t
                                # Check if the point is inside the rectangle
                                for p, v in zip(obj.points, obj.vectors):
                                    if (ix - p[0]) * v[0] + (iy - p[1]) * v[1] + (iz - p[2]) * v[2] < 0:
                                        is_inside = False
                                        break
                            if is_inside:
                                inverse_normal = False
                                best_dist = t
                                closest_obj = obj

        # Is the ray crossing any object
        if closest_obj is None:
            return self.background_color

        # Intersection point with the object
        ix = x + rx * best_dist
        iy = y + ry * best_dist
        iz = z + rz * best_dist

        # -----------------------------------------------------
        # Step 2 : Find the intensity reseived on this intersection point

        # The normal direction of the surface object at the intersection location
        if isinstance(closest_obj, Sphere):
            nx = (ix - closest_obj.x) / closest_obj.r
            ny = (iy - closest_obj.y) / closest_obj.r
            nz = (iz - closest_obj.z) / closest_obj.r
            # Is the ray directly crossing a source
            dot_prod_viwer_n = nx * rx + ny * ry + nz * rz
            if isinstance(closest_obj, LightSource):
                # I'm not sure if it is accurate physically, but it looks ok ...
                # coef = -dot_prod_viwer_n / (best_dist ** 2)
                coef = -dot_prod_viwer_n
                return (coef * closest_obj.color_intensity[0],
                        coef * closest_obj.color_intensity[1],
                        coef * closest_obj.color_intensity[2])
        elif isinstance(closest_obj, Plan):
            nx = closest_obj.a
            ny = closest_obj.b
            nz = closest_obj.c
            dot_prod_viwer_n = nx * rx + ny * ry + nz * rz
            if dot_prod_viwer_n > 0:
                inverse_normal = True
        else:
            print("There is a unexpected object !")
            return 0, 0, 0

        if inverse_normal:
            nx *= -1
            ny *= -1
            nz *= -1
            dot_prod_viwer_n *= -1

        # Add randomness on this normal direction if the object is rough
        if closest_obj.roughness > 0:
            a1 = random() * 2 * pi
            a2 = random() * 2 * pi
            cos_a2 = cos(a2)
            r = random() * closest_obj.roughness
            nx += r * cos(a1) * cos_a2
            ny += r * sin(a1) * cos_a2
            nz += r * sin(a2)

        # 1) Adding the intensity received by the ambiant light
        color_intersection = self.ambient_color

        # 2) Adding the intensity received by every surronding sources
        # Looking for all the light sources
        for source in self.sources:
            # The direction from the source to the intersection point
            sx = ix - source.x
            sy = iy - source.y
            sz = iz - source.z

            dot_prod = nx * sx + ny * sy + nz * sz

            # Is ne source on the right side of the surface
            if dot_prod < 0:
                # Find if the light reaches directely the surface or if there is any object inbetween them
                is_visible = True

                # Looking for every object if it hide the light to the surface
                for obj in self.objects:
                    if obj == closest_obj or obj == object_to_avoid:
                        # Here the object can't be in front of himself
                        # This is NOT accurate : if the viewer is inside a sphere for instance
                        continue
                    if isinstance(obj, Sphere):
                        dx = obj.x - ix
                        dy = obj.y - iy
                        dz = obj.z - iz

                        a = sx ** 2 + sy ** 2 + sz ** 2
                        b = 2 * (sx * dx + sy * dy + sz * dz)
                        c = dx ** 2 + dy ** 2 + dz ** 2 - obj.r ** 2

                        delta = b ** 2 - 4 * a * c

                        # Is the object crossing the line between the light and the intersection
                        if delta > 0:
                            t = - (b + sqrt(delta)) / (2 * a)
                            # Is the object inbetween the light and the intersection
                            if t < 1 and (t > dist_min_vision or dist_min_vision < - (t + b / a) < 1):
                                is_visible = False
                                break
                    elif isinstance(obj, Plan):
                        pass  # TODO

                # Is the light reaches directely the surface of the object
                if is_visible:
                    # (Square) Distance from the object to the source
                    squared_dist_source = sx ** 2 + sy ** 2 + sz ** 2
                    dist_source = sqrt(squared_dist_source)

                    # The angle between the viewer direction and the reflect direction of the light from the source
                    angle = acos(max(0, min(1, ((2 * dot_prod * nx - sx) * rx +
                                                (2 * dot_prod * ny - sy) * ry +
                                                (2 * dot_prod * nz - sz) * rz) / dist_source)))

                    # Intensity received on the intersection coming from this light source
                    intensity = -closest_obj.get_intensity_coef(angle) * dot_prod / (squared_dist_source * dist_source)
                    # intensity = -closest_obj.get_intensity_coef(angle) * dot_prod / dist_source
                    color_intersection = (color_intersection[0] + intensity * source.color_intensity[0],
                                          color_intersection[1] + intensity * source.color_intensity[1],
                                          color_intersection[2] + intensity * source.color_intensity[2])

        # 3) Removing the intensity absorbed or refected by the object
        if closest_obj.texture is None:
            color_object = closest_obj.color
        else:
            color_object = closest_obj.get_texture(ix, iy, iz)
        #  / (best_dist ** 2)                  / (nx * rx + ny * ry + nz * rz)  (=> Use two_dot_prod just bellow...)
        color_intersection = ((1 - closest_obj.mirror_reflection) * color_object[0] * color_intersection[0],
                              (1 - closest_obj.mirror_reflection) * color_object[1] * color_intersection[1],
                              (1 - closest_obj.mirror_reflection) * color_object[2] * color_intersection[2])

        # 4) Adding the intensity directly transmitted by mirror reflection
        coef_intensity *= closest_obj.mirror_reflection
        if coef_intensity > self.threshold_intensity_mirror_reflection:
            two_dot_prod = 2 * dot_prod_viwer_n
            color_mirror = self.calcul_ray_intensity(ix, iy, iz,
                                                     rx - two_dot_prod * nx,
                                                     ry - two_dot_prod * ny,
                                                     rz - two_dot_prod * nz,
                                                     closest_obj, coef_intensity)
            color_intersection = (color_intersection[0] + closest_obj.mirror_reflection * color_mirror[0],
                                  color_intersection[1] + closest_obj.mirror_reflection * color_mirror[1],
                                  color_intersection[2] + closest_obj.mirror_reflection * color_mirror[2])

        # -----------------------------------------------------
        return color_intersection
