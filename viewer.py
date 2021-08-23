# coding: utf-8

from math import sqrt
from tqdm import tqdm
import numpy

from scene import Scene
from multiprocessing import Pool


class Viewer:
    def __init__(self, scene: Scene, width: int, height: int, x: float, y: float, z: float):
        self.scene = scene
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.directions = [[(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)]
        self.init_directions()

    def init_directions(self):
        for x in range(self.width):
            for y in range(self.height):
                rx = x - self.x
                ry = y - self.y
                rz = - self.z
                d = sqrt(rx ** 2 + ry ** 2 + rz ** 2)
                self.directions[y][x] = (rx / d, ry / d, rz / d)

    def trace_rays(self, mod=1, val=0):
        colors = numpy.zeros((self.height, self.width, 3), numpy.uint8)
        for i in tqdm(range(self.width * self.height)):
            x = i % self.width
            y = (i - x) // self.width
            if i % mod == val:
                color = self.scene.calcul_ray_intensity(self.x, self.y, self.z, *self.directions[y][x])
                colors[y][x][0] = 255 * max(min(color[0], 1), 0)
                colors[y][x][1] = 255 * max(min(color[1], 1), 0)
                colors[y][x][2] = 255 * max(min(color[2], 1), 0)
        return colors

    def trace_rays_multiprocessing(self, num_cpu=4):
        with Pool() as pool:
            res = pool.starmap(Viewer.trace_rays, [(self, num_cpu, i) for i in range(num_cpu)])
        return sum(res)
