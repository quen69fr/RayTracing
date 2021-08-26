# coding: utf-8

from math import sqrt
from tqdm import tqdm
import numpy

from scene import Scene


class Viewer:

    def __init__(self, scene: Scene, width: int, height: int, x: float, y: float, z: float):
        self.scene = scene
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.directions = []

    def init_directions(self):
        for x in range(self.width):
            for y in range(self.height):
                self.directions[y][x] = self.calcul_direction(x, y)

    def clear_directions(self):
        del self.directions[:]

    def calcul_direction(self, x: int, y: int):
        rx = x - self.x
        ry = y - self.y
        rz = - self.z
        d = sqrt(rx ** 2 + ry ** 2 + rz ** 2)
        return rx / d, ry / d, rz / d

    def trace_rays(self, mod=1, val=0, log: bool = True):
        colors = numpy.zeros((self.height, self.width, 3), numpy.uint8)
        for i in (tqdm(range(self.width * self.height)) if log else range(self.width * self.height)):
            x = i % self.width
            y = (i - x) // self.width
            if i % mod == val:
                if len(self.directions) > 0:
                    direction = self.directions[y][x]
                else:
                    direction = self.calcul_direction(x, y)
                # color = self.scene.calcul_ray_intensity(self.x, self.y, self.z, *direction)
                color = self.scene.calcul_ray_intensity(x, y, 0, *direction)
                colors[y][x][0] = 255 * max(min(color[0], 1), 0)
                colors[y][x][1] = 255 * max(min(color[1], 1), 0)
                colors[y][x][2] = 255 * max(min(color[2], 1), 0)
        return colors
