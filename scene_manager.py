# coding: utf-8

from math import pi, cos, sin
import numpy
from PIL import Image

from viewer import Viewer
from scene import Scene, SphereObject, Plan, LightSource, Rectangle


def load_image(path: str):
    image = numpy.asarray(Image.open(path))
    return [[(c[0] / 255, c[1] / 255, c[2] / 255) for c in col] for col in image]


class SceneManager:
    def __init__(self, id_scene: int):
        self.id_scene = id_scene
        self.scene = None
        self.viewer = None
        self.num_frames = 0
        self.params = []
        if self.id_scene == 0:
            self.scene = Scene(0.03, ambient_color=(0.1, 0.1, 0.1))
            self.viewer = Viewer(self.scene, 800, 600, 400, 300, -1000)
            self.scene.add_object(SphereObject(500, 200, 1700, 500, mirror_reflection=0.99, glossiness=0.3))
            self.scene.add_object(Rectangle((300, 0, 0), (0, 0, 300), (-1000, 1000, 2000), 9, 9,
                                            mirror_reflection=0.2, glossiness=0.15,
                                            texture=load_image("Textures/ChessBoard.png")))
            # self.scene.add_object(Plan((1, 0, 0), (0, -1, 0), (0, 0, 3500),
            #                            color=(0.5, 0, 1), mirror_reflection=0.1, glossiness=0.25))
            self.scene.add_source(LightSource(-1000, -1000, -1000, 10 ** 8, radius_source=100))
            self.scene.add_source(LightSource(-400, -2000, -100, 10 ** 8, radius_source=100))

        elif self.id_scene == 1:
            self.scene = Scene(0.03, ambient_color=(0.05, 0.05, 0.05))
            self.viewer = Viewer(self.scene, 800, 600, 400, 300, -1000)
            num_spheres = 12
            colors = [(1, 0, 0), (1, 0.5, 0), (1, 1, 0), (0.5, 1, 0), (0, 1, 0), (0, 1, 0.5),
                      (0, 1, 1), (0, 0.5, 1), (0, 0, 1), (0.5, 0, 1), (1, 0, 1), (1, 0, 0.5)]
            for i in range(num_spheres):
                sphere = SphereObject(200, 200 + 200 * cos(4 * i * pi / num_spheres), 1000, 100,
                                      color=colors[i], glossiness=0.25, mirror_reflection=0.2)
                sphere.rotate_y(500, 1700, 2 * i * pi / num_spheres)
                self.scene.add_object(sphere)
            self.scene.add_object(SphereObject(500, 250, 1700, 500,
                                               glossiness=0.3, mirror_reflection=0.9))
            # self.scene.add_object(Plan((1, 0, 0), (0, 0, -1), (0, 1000, 0), glossiness=0.2, mirror_reflection=0.2))
            self.scene.add_object(Plan((300, 0, 0), (0, 0, 300), (0, 1000, 0),
                                       mirror_reflection=0.2, glossiness=0.15))
            # texture=load_image("Textures/ChessBoard.png")))
            self.scene.add_object(Plan((1, 0, 0), (0, -1, 0), (0, 0, 3500), glossiness=0.2, mirror_reflection=0.2))
            self.scene.add_source(LightSource(1500, -400, -2000, 3 * 10 ** 6, radius_source=100))
            self.scene.add_source(LightSource(1300, -600, -2000, 3 * 10 ** 6, radius_source=100))
            self.scene.add_source(LightSource(-400, -2000, -100, 3 * 10 ** 6, radius_source=100))
            self.num_frames = 180

            self.params = [num_spheres]

        elif self.id_scene == 2:
            self.scene = Scene(0.03, ambient_color=(0.05, 0.05, 0.05))
            self.viewer = Viewer(self.scene, 800, 600, 400, 300, -1500)
            for x in range(5):
                for y in range(4):
                    self.scene.add_object(SphereObject(400 + 400 * (x - 2), 300 + 350 * (y - 1.5), 1700, 150,
                                                       glossiness=x / 4, mirror_reflection=y / 3))
            self.scene.add_source(LightSource(-10000000, -10000000, -10000000, 3 * 10 ** 14,
                                              color=(1, 1, 1), radius_source=100))
            self.scene.add_object(Plan((1, 0, 0), (0, 0, -1), (0, 1000, 0), glossiness=0.2, mirror_reflection=0.2))
            self.scene.add_object(Plan((1, 0, 0), (0, -1, 0), (0, 0, 3500), glossiness=0.2, mirror_reflection=0.2))

        elif self.id_scene == 3:
            self.scene = Scene(0.03, ambient_color=(0.2, 0.2, 0.2))
            self.viewer = Viewer(self.scene, 800, 600, 400, 300, -1000)
            self.scene.add_object(Plan((1, 0, 0), (0, 0, 1), (0, 1000, 0),
                                       mirror_reflection=0.1, glossiness=0.15))
            self.scene.add_object(Plan((1, 0, 0), (0, 0, 1), (0, -400, 0),
                                       mirror_reflection=0.1, glossiness=0.15))
            self.scene.add_object(Plan((0, 1, 0), (0, 0, 1), (-200, 0, 0),
                                       mirror_reflection=0.1, glossiness=0.15, color=(0.3, 0.3, 1)))
            self.scene.add_object(Plan((0, -1, 0), (0, 0, 1), (1000, 0, 0),
                                       mirror_reflection=0.1, glossiness=0.15, color=(1, 0.3, 0.3)))
            self.scene.add_object(Plan((1, 0, 0), (0, -1, 0), (0, 0, 3500), glossiness=0.15))
            self.scene.add_object(SphereObject(500, 600, 2200, 350, color=(0.4, 0.4, 0.4),
                                               mirror_reflection=0.15, glossiness=0.3))
            self.scene.add_object(SphereObject(220, 800, 1500, 200, color=(0.3, 0.6, 0.2),
                                               mirror_reflection=0.04, glossiness=0.2))
            self.scene.add_object(SphereObject(600, 860, 1400, 130, color=(0.2, 0.2, 0.2),
                                               mirror_reflection=0.9, glossiness=0.4))
            for x in range(20):
                for z in range(20):
                    self.scene.add_source(LightSource(400 + 20 * (x - 9.5), -395, 2300 - 20 * z,
                                                      2 * 10 ** 3, radius_source=40))

        elif self.id_scene == 4:
            self.scene = Scene(0.03, ambient_color=(0.2, 0.2, 0.2), background_color=(0.5, 0.8, 1))
            self.viewer = Viewer(self.scene, 1920, 1080, 960, -300, -5000)
            self.scene.add_object(Rectangle((156, 0, 0), (0, 0, 156), (-600, 1500, 1500), 20, 20,
                                            mirror_reflection=0.05, glossiness=0.15,
                                            texture=load_image("Textures/RedChessBoard.png")))
            self.scene.add_object(SphereObject(960, 1300, 3060, 400, mirror_reflection=0.05))
            self.scene.add_object(SphereObject(960, 800, 3060, 300, mirror_reflection=0.05))
            self.scene.add_object(SphereObject(960, 420, 3060, 210, mirror_reflection=0.05))
            self.scene.add_object(SphereObject(960, 420, 3060 - 215, 25, color=(0.8, 0.3, 0.1), mirror_reflection=0.2))
            self.scene.add_object(SphereObject(960 + 75, 420 - sin(0.3) * 200, 3060 - cos(0.3) * 200, 20,
                                               color=(0, 0, 0), mirror_reflection=0.1, glossiness=0.8))
            self.scene.add_object(SphereObject(960 - 75, 420 - sin(0.3) * 200, 3060 - cos(0.3) * 200, 20,
                                               color=(0, 0, 0), mirror_reflection=0.1, glossiness=0.8))
            self.scene.add_object(SphereObject(1800, 850, 2500, 250, mirror_reflection=0.9))
            c = (0.9, 0.7, 0.2)
            self.scene.add_object(Rectangle((1, 0, 0), (0, 0, 1), (-200, 1100, 3500), 400, 400, color=c))
            self.scene.add_object(Rectangle((1, 0, 0), (0, 1, 0), (-200, 1100, 3500), 400, 400, color=c))
            self.scene.add_object(Rectangle((1, 0, 0), (0, 1, 0), (-200, 1100, 3500 + 400), 400, 400, color=c))
            self.scene.add_object(Rectangle((0, 1, 0), (0, 0, 1), (-200, 1100, 3500), 400, 400, color=c))
            self.scene.add_object(Rectangle((0, 1, 0), (0, 0, 1), (-200 + 400, 1100, 3500), 400, 400, color=c))
            self.scene.add_source(LightSource(-200000, -100000, -1000000, 10 ** 12, radius_source=100))
            self.num_frames = 360

    def update_scene(self, t: int):
        if self.id_scene == 1:
            for j in range(self.params[0]):
                self.scene.objects[j].rotate_y(500, 1700, 2 * pi / self.num_frames)
                self.scene.objects[j].y = 200 + 200 * cos(4 * pi * (j / self.params[0] - (t + 1) / self.num_frames))
        if self.id_scene == 4:
            self.scene.rotate_y(960, 3060, -2 * pi / self.num_frames)
