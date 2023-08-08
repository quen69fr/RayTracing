# coding: utf-8

from random import random
from math import sqrt, pi, cos, sin, inf

dist_min_vision = 0.00000001


def rotate_vector_y(x: float, z: float, a: float):
    c = cos(a)
    s = sin(a)
    return x * c - z * s, x * s + z * c


def rotate_point_y(x: float, z: float, a: float, xc: float, zc: float):
    c = cos(a)
    s = sin(a)
    return (x - xc) * c - (z - zc) * s + xc, (x - xc) * s + (z - zc) * c + zc


class Object:
    def __init__(self, color: tuple, reflection: float, glossiness: float, transmission: float,
                 refraction: float, roughness: float, texture: list):
        self.color = color
        self.roughness = roughness

        self.reflection = reflection
        self.glossiness = glossiness  # TODO : Currently useless

        self.transmission = transmission
        self.refraction = refraction

        self.coef_emission = 1 - self.reflection - self.transmission

        self.texture = texture

    def rotate_y(self, x: float, z: float, a: float):
        pass

    def get_texture(self, x: float, y: float, z: float):
        return self.color


class Plan(Object):
    def __init__(self, u: tuple, v: tuple, point: tuple,
                 color: tuple = (1, 1, 1), reflection: float = 0, glossiness: float = 0,
                 transmission: float = 0, refraction: float = 1, roughness: float = 0, texture: list = None):
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
        Object.__init__(self, color, reflection, glossiness, transmission, refraction, roughness, texture)
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
        self.a, self.c = rotate_vector_y(self.a, self.c, a)
        self.d += (old_a - self.a) * x + (old_c - self.c) * z
        self.x, self.z = rotate_point_y(self.x, self.z, a, x, z)
        self.ux, self.uz = rotate_vector_y(self.ux, self.uz, a)
        self.vx, self.vz = rotate_vector_y(self.vx, self.vz, a)
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
                 color: tuple = (1, 1, 1), reflection: float = 0, glossiness: float = 0,
                 transmission: float = 0, refraction: float = 1, roughness: float = 0, texture: list = None):
        Plan.__init__(self, u, v, point, color, reflection, glossiness, transmission, refraction, roughness,
                      texture)
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
            vx, vz = rotate_vector_y(vx, vz, a)
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
                 color: tuple = (1, 1, 1), reflection: float = 0, glossiness: float = 0,
                 transmission: float = 0, refraction: float = 1, roughness: float = 0, texture: list = None):
        Object.__init__(self, color, reflection, glossiness, transmission, refraction, roughness, texture)
        Sphere.__init__(self, x, y, z, r)

    def get_texture(self, x: float, y: float, z: float):
        return self.color  # TODO


class LightSource(Sphere):
    def __init__(self, x: float, y: float, z: float, intensity: float,
                 color: tuple = (1, 1, 1), radius_source: float = 0):
        Sphere.__init__(self, x, y, z, radius_source)
        self.color_intensity = (color[0] * intensity, color[1] * intensity, color[2] * intensity)


class Scene:
    def __init__(self, threshold_intensity_min: float, ambient_color: tuple = (0, 0, 0),
                 background_color: tuple = (0, 0, 0)):
        self.ambient_color = ambient_color
        self.background_color = background_color
        self.objects = []
        self.sources = []
        self.threshold_intensity_min = threshold_intensity_min

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

    def get_closest_object(self, x: float, y: float, z: float, rx: float, ry: float, rz: float):
        closest_obj = None
        best_dist = inf
        inverse_normal = False

        for obj in self.objects + self.sources:
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
                    # t of the closest intersection from the viewer
                    t = - (b + sqrt(delta)) / (2 * a)
                    # Is the object on the right side of the viewer
                    if t > dist_min_vision:
                        # Is this object closer to the viewer than the previous one
                        if best_dist > t:
                            inverse_normal = False
                            best_dist = t
                            closest_obj = obj
                    else:  # Otherwise, the viewer could be inside the sphere
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

        return closest_obj, best_dist, inverse_normal

    def calcul_ray_intensity(self, x: float, y: float, z: float, rx: float, ry: float, rz: float,
                             coef_intensity: float = 1.0):
        # Return the light intensity that the ray receives
        # The ray start at (x, y, z) and points in the direction (rx, ry, rz)

        # -----------------------------------------------------
        # Step 1 : Find the closest object crossed by the ray

        closest_obj, best_dist, inverse_normal = self.get_closest_object(x, y, z, rx, ry, rz)

        # Is the ray crossing any object
        if closest_obj is None:
            return self.background_color

        # Is the ray directly crossing a source
        if isinstance(closest_obj, LightSource):
            # TODO : There is a problem here :
            #         -> Is the source infinite or punctual ?
            return closest_obj.color_intensity
            # return (600 * closest_obj.color_intensity[0],
            #         600 * closest_obj.color_intensity[1],
            #         600 * closest_obj.color_intensity[2])

        # Intersection point with the object
        ix = x + rx * best_dist
        iy = y + ry * best_dist
        iz = z + rz * best_dist

        # The normal direction of the surface object at the intersection location
        if isinstance(closest_obj, Sphere):
            nx = (ix - closest_obj.x) / closest_obj.r
            ny = (iy - closest_obj.y) / closest_obj.r
            nz = (iz - closest_obj.z) / closest_obj.r
            dot_prod_viewer_n = nx * rx + ny * ry + nz * rz
        elif isinstance(closest_obj, Plan):
            nx = closest_obj.a
            ny = closest_obj.b
            nz = closest_obj.c
            dot_prod_viewer_n = nx * rx + ny * ry + nz * rz
            if dot_prod_viewer_n > 0:
                inverse_normal = True
        else:
            print("There is a unexpected object !")
            return 0, 0, 0

        if inverse_normal:
            nx *= -1
            ny *= -1
            nz *= -1
            dot_prod_viewer_n *= -1

        # Add randomness on this normal direction if the object is rough
        if closest_obj.roughness > 0:
            a1 = random() * 2 * pi
            a2 = random() * 2 * pi
            cos_a2 = cos(a2)
            r = random() * closest_obj.roughness
            nx += r * cos(a1) * cos_a2
            ny += r * sin(a1) * cos_a2
            nz += r * sin(a2)

        # -----------------------------------------------------
        # Step 2 : Find the intensity received on this intersection point

        # 1) Diffusion
        color_intersection = (0, 0, 0)
        coef_intensity_emission = coef_intensity * closest_obj.coef_emission
        if coef_intensity_emission > self.threshold_intensity_min:
            # a) Adding the intensity received by the ambient light
            color_received = self.ambient_color

            # b) Adding the intensity received by every surrounding sources
            # Looking for all the light sources
            for source in self.sources:
                # The direction from the source to the intersection point
                sx = ix - source.x
                sy = iy - source.y
                sz = iz - source.z

                dot_prod = nx * sx + ny * sy + nz * sz

                # Is the source on the right side of the surface?
                if dot_prod < 0:
                    # Find if the light reaches directly the surface or if there is any object inbetween them
                    is_visible = True

                    # Looking for every object if it hides the light to the surface
                    for obj in self.objects:
                        # if obj == closest_obj or obj == object_to_avoid:
                        #     # Here the object can't be in front of itself
                        #     # This is NOT accurate : if the viewer is inside a sphere for instance
                        #     continue
                        if isinstance(obj, Sphere):
                            if obj.r == 0:
                                continue
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
                            d = obj.a * sx + obj.b * sy + obj.c * sz
                            # Is the plan parallel to the line between the light and the intersection
                            if d != 0:
                                t = obj.a * ix + obj.b * iy + obj.c * iz + obj.d
                                # Is this object on the right side of the intersection and
                                # inbetween the light and the intersection
                                if (0 < t < d) or (d < t < 0):
                                    t /= d
                                    if dist_min_vision < t:
                                        is_inside = True
                                        if isinstance(obj, Rectangle):
                                            # Intersection point with the plan
                                            i2x = ix - sx * t
                                            i2y = iy - sy * t
                                            i2z = iz - sz * t
                                            # Check if the point is inside the rectangle
                                            for p, v in zip(obj.points, obj.vectors):
                                                if (i2x - p[0]) * v[0] + (i2y - p[1]) * v[1] + (i2z - p[2]) * v[2] < 0:
                                                    is_inside = False
                                                    break
                                        if is_inside:
                                            is_visible = False
                                            break

                    # Is the light reaches directly the surface of the object
                    if is_visible:
                        coef = - dot_prod / sqrt(sx ** 2 + sy ** 2 + sz ** 2)
                        color_received = (color_received[0] + coef * source.color_intensity[0],
                                          color_received[1] + coef * source.color_intensity[1],
                                          color_received[2] + coef * source.color_intensity[2])

            # c) Resulting emission
            if closest_obj.texture is None:
                color_object = closest_obj.color
            else:
                color_object = closest_obj.get_texture(ix, iy, iz)
            color_intersection = (closest_obj.coef_emission * color_object[0] * color_received[0],
                                  closest_obj.coef_emission * color_object[1] * color_received[1],
                                  closest_obj.coef_emission * color_object[2] * color_received[2])

        # 2) Transmission
        coef_intensity_transmission = coef_intensity * closest_obj.transmission
        pure_reflection = False
        if coef_intensity_transmission > self.threshold_intensity_min:
            inv_n = closest_obj.refraction if inverse_normal else 1 / closest_obj.refraction
            cos2_i2 = 1 - inv_n ** 2 * (1 - dot_prod_viewer_n ** 2)
            if cos2_i2 < 0:
                pure_reflection = True
            else:
                c = - inv_n * dot_prod_viewer_n - sqrt(cos2_i2)
                norm = 1 / sqrt(inv_n ** 2 + c ** 2 + 2 * inv_n * c * dot_prod_viewer_n)
                color_transmission = self.calcul_ray_intensity(ix, iy, iz,
                                                               norm * (inv_n * rx + c * nx),
                                                               norm * (inv_n * ry + c * ny),
                                                               norm * (inv_n * rz + c * nz),
                                                               coef_intensity_transmission)
                color_intersection = (color_intersection[0] + closest_obj.transmission * color_transmission[0],
                                      color_intersection[1] + closest_obj.transmission * color_transmission[1],
                                      color_intersection[2] + closest_obj.transmission * color_transmission[2])

        # 3) Reflection
        # TODO : Cast several rays, depending of the glossiness ...
        coef_reflection = closest_obj.reflection
        if pure_reflection:
            coef_reflection += closest_obj.transmission
        coef_intensity_reflection = coef_intensity * coef_reflection
        if coef_intensity_reflection > self.threshold_intensity_min:
            two_dot_prod = 2 * dot_prod_viewer_n
            color_reflection = self.calcul_ray_intensity(ix, iy, iz,
                                                         rx - two_dot_prod * nx,
                                                         ry - two_dot_prod * ny,
                                                         rz - two_dot_prod * nz,
                                                         coef_intensity_reflection)
            color_intersection = (color_intersection[0] + coef_reflection * color_reflection[0],
                                  color_intersection[1] + coef_reflection * color_reflection[1],
                                  color_intersection[2] + coef_reflection * color_reflection[2])

        # -----------------------------------------------------
        return color_intersection
