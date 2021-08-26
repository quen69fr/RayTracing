# coding: utf-8

from random import random, seed
from math import pi, cos, sin
import numpy
from PIL import Image
from multiprocessing import Pool
import moviepy.video.io.ImageSequenceClip as Movieclip
from tqdm import tqdm

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

        # Test scene :
        if self.id_scene == 0:
            self.num_frames = 30
            self.scene = Scene(0.03, ambient_color=(0.1, 0.1, 0.1), background_color=(1, 0.5, 0.5))
            self.viewer = Viewer(self.scene, 800, 600, 400, 300, -1000)
            self.scene.add_object(SphereObject(500, 200, 1700, 500, mirror_reflection=0.9, glossiness=0.3))
            self.scene.add_object(Rectangle((300, 0, 0), (0, 0, 300), (-1000, 1000, 2000), 9, 9,
                                            mirror_reflection=0.2, glossiness=0.15,
                                            texture=load_image("Textures/ChessBoard.png")))
            self.scene.add_object(Rectangle((300, 0, 0), (0, 0, 300), (-500, 800, 2500), 1, 1, color=(1, 0.5, 0),
                                            mirror_reflection=0.2, glossiness=0.15))
            # self.scene.add_object(Plan((1, 0, 0), (0, -1, 0), (0, 0, 3500),
            #                            color=(0.5, 0, 1), mirror_reflection=0.1, glossiness=0.25))
            self.scene.add_source(LightSource(-1000, -1000, -1000, 10 ** 7, radius_source=100))
            self.scene.add_source(LightSource(-400, -2000, -100, 10 ** 7, radius_source=100))

        # Revolving spheres scene :
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

        # Sample spheres (brightness, mirror reflection...) scene :
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

        # Light bloc scene :
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

        # Snowman scene :
        elif self.id_scene == 4:
            self.scene = Scene(0.03, ambient_color=(0.2, 0.2, 0.2), background_color=(0.5, 0.8, 1))
            self.viewer = Viewer(self.scene, 1920, 1080, 960, -300, -5000)
            self.scene.add_source(LightSource(-200000, -100000, -1000000, 5 * 10 ** 11, radius_source=100))
            self.scene.add_source(LightSource(-100000, -200000, -1000000, 5 * 10 ** 11, radius_source=100))
            self.num_frames = 3 * 6 * 60 - 40

        # Chess reflection scene :
        elif self.id_scene == 5:
            self.scene = Scene(0.03, ambient_color=(0.2, 0.2, 0.2))
            self.viewer = Viewer(self.scene, 1920, 1080, 960, 200, -1000)
            self.scene.add_object(SphereObject(-40, 680, 1300, 450, color=(1, 0, 0), mirror_reflection=0.8))
            self.scene.add_object(SphereObject(960, 680, 1300, 450, color=(0, 1, 0), mirror_reflection=0.8))
            self.scene.add_object(SphereObject(1960, 680, 1300, 450, color=(0, 0, 1), mirror_reflection=0.8))
            # self.scene.add_object(Plan((300, 0, 0), (0, 0, 300), (960, 1100, 2000), mirror_reflection=0.2,
            #                            glossiness=0.15, texture=load_image("Textures/ChessBoard.png")))
            d = 200
            a = 0.1
            self.scene.add_object(Plan((d * cos(a), 0, -d * sin(a)), (d * sin(a), 0, d * cos(a)),
                                       (960, 1100, 2000), mirror_reflection=0.15,
                                       glossiness=0.15, texture=load_image("Textures/ChessBoard2.png")))
            self.scene.add_source(LightSource(960, -5000, -3000, 10 ** 8, radius_source=100))

    def update_scene(self, t: int, jump: int = 1):
        if t == 0:
            return
        if self.id_scene == 0:
            self.scene.rotate_y(500, 1700, -2 * pi * jump / self.num_frames)

        elif self.id_scene == 1:
            for j in range(self.params[0]):
                self.scene.objects[j].rotate_y(500, 1700, 2 * jump * pi / self.num_frames)
                self.scene.objects[j].y = 200 + 200 * cos(4 * pi * (j / self.params[0] - jump * t / self.num_frames))

        elif self.id_scene == 4:
            for t2 in range(t - jump + 1, t + 1):
                self.scene.rotate_y(960, 3060, -2 * pi / 360)
                if t2 <= 1 * 60:
                    if t2 == 1:
                        # Floor : -1
                        self.scene.add_object(Rectangle((156, 0, 0), (0, 0, 156), (-600, 1500, 1500), 20, 20,
                                                        mirror_reflection=0.05, glossiness=0.15,
                                                        texture=load_image("Textures/RedChessBoard.png")))
                    self.scene.objects[-1] = Rectangle((156, 0, 0), (0, 0, 156), (-600, 1500, 1500), 20, 20 * t2 / 60,
                                                       mirror_reflection=0.05, glossiness=0.15,
                                                       texture=load_image("Textures/RedChessBoard.png"))
                    self.scene.objects[-1].rotate_y(960, 3060, -2 * pi * t2 / 360)
                elif t2 <= 2 * 60:
                    if t2 == 60 + 30:
                        c = (0.9, 0.7, 0.2)
                        # Cube = -5, -4, -3, -2, -1
                        self.scene.add_object(Rectangle((1, 0, 0), (0, 0, 1), (-200, 1100, 3500), 400, 400,
                                                        color=c))
                        self.scene.add_object(Rectangle((1, 0, 0), (0, 1, 0), (-200, 1100, 3500), 400, 400,
                                                        color=c))
                        self.scene.add_object(Rectangle((1, 0, 0), (0, 1, 0), (-200, 1100, 3500 + 400), 400, 400,
                                                        color=c))
                        self.scene.add_object(Rectangle((0, 1, 0), (0, 0, 1), (-200, 1100, 3500), 400, 400,
                                                        color=c))
                        self.scene.add_object(Rectangle((0, 1, 0), (0, 0, 1), (-200 + 400, 1100, 3500), 400, 400,
                                                        color=c))
                        for i in range(1, 6):
                            self.scene.objects[-i].rotate_y(960, 3060, -2 * pi * t2 / 360)
                elif t2 <= 3 * 60:
                    if t2 == 2 * 60 + 1:
                        # Mirror sphere : -1
                        self.scene.add_object(SphereObject(1800, 850, 2500, 0, mirror_reflection=0.9))
                        self.scene.objects[-1].rotate_y(960, 3060, -2 * pi * t2 / 360)
                    self.scene.objects[-1].r = 250 * (t2 - 2 * 60) / 60
                elif t2 <= 6 * 60 + 30:
                    if t2 == 3 * 60 + 1:
                        # Body : -6, -5
                        self.scene.add_object(SphereObject(960, 1300, 3060, 400, mirror_reflection=0.05))
                        self.scene.add_object(SphereObject(960, 800, 3060, 300, mirror_reflection=0.05))
                        # Head : -4
                        self.scene.add_object(SphereObject(960, 420, 3060, 210, mirror_reflection=0.05))

                        # Nose : -3
                        self.scene.add_object(SphereObject(960, 420, 3060 - 215, 25, color=(0.8, 0.3, 0.1),
                                                           mirror_reflection=0.2))
                        # Eyes : -2, -1
                        self.scene.add_object(SphereObject(960 + 75, 420 - sin(0.3) * 200, 3060 - cos(0.3) * 200,
                                                           20, color=(0, 0, 0), mirror_reflection=0.1,
                                                           glossiness=0.8))
                        self.scene.add_object(SphereObject(960 - 75, 420 - sin(0.3) * 200, 3060 - cos(0.3) * 200,
                                                           20, color=(0, 0, 0), mirror_reflection=0.1,
                                                           glossiness=0.8))

                        self.scene.objects[-6].y -= 1 * 1500
                        self.scene.objects[-5].y -= 2 * 1500
                        self.scene.objects[-4].y -= 3 * 1500

                    if t2 <= 4 * 60:
                        self.scene.objects[-6].y += 25
                    if t2 <= 5 * 60:
                        self.scene.objects[-5].y += 25
                    if t2 <= 6 * 60:
                        self.scene.objects[-4].y += 25

                    dz = 3 * 1500 + 750 - (t2 - 3 * 60) * 25

                    self.scene.objects[-3] = SphereObject(960, 420, 3060 - 215 - dz, 25, color=(0.8, 0.3, 0.1),
                                                          mirror_reflection=0.2)
                    self.scene.objects[-2] = SphereObject(960 - 75, 420 - sin(0.3) * 200,
                                                          3060 - cos(0.3) * 200 - dz, 20, color=(0, 0, 0),
                                                          mirror_reflection=0.1, glossiness=0.8)
                    self.scene.objects[-1] = SphereObject(960 + 75, 420 - sin(0.3) * 200,
                                                          3060 - cos(0.3) * 200 - dz, 20, color=(0, 0, 0),
                                                          mirror_reflection=0.1, glossiness=0.8)
                    for i in range(1, 4):
                        self.scene.objects[-i].rotate_y(960, 3060, -2 * pi * t2 / 360)
                elif t2 > 10 * 60:
                    num_flakes = 150
                    if t2 == 10 * 60 + 1:
                        seed(10)
                        for i in range(num_flakes):
                            self.scene.add_object(SphereObject(-600 + 3120 * random(), -random() * 1500,
                                                               1500 + 3120 * random(), 5 + 10 * random(),
                                                               mirror_reflection=0.05))
                            self.scene.objects[-1].rotate_y(960, 3060, -2 * pi * t2 / 360)

                    for i in range(1, num_flakes + 1):
                        flake = self.scene.objects[-i]
                        flake.y += 2.5 + random() * 6
                        if flake.y > 1500 + flake.r:
                            flake.x = -600 + 3120 * random()
                            flake.y -= 1500
                            flake.z = 1500 + 3120 * random()
                            flake.rotate_y(960, 3060, -2 * pi * t2 / 360)

    # ---------------------------------------------------------------------------------------------------------

    def create_image(self, t: int = 0, multiprocessing: bool = False, num_cpu: int = 1, preview_mod: int = 1,
                     images_saved_path: str = "Image.png", log: bool = True):
        if log:
            print("Saving image")
        # if need_update:
        #     self.update_scene(t, t)
        if multiprocessing:
            with Pool() as pool:
                res = pool.starmap(Viewer.trace_rays, [(self.viewer, num_cpu * preview_mod, i * preview_mod, log)
                                                       for i in range(num_cpu)])
            pixels = sum(res)
        else:
            pixels = self.viewer.trace_rays(mod=preview_mod, log=log)
        image = Image.fromarray(pixels)
        if "#" in images_saved_path:
            images_saved_path = images_saved_path.replace("#", str(t + 1))
        image.save(images_saved_path)
        if log:
            print(f"Image saved : {images_saved_path}")

    def create_images(self, t0: int = 0, mod: int = 1, val: int = 0, multiprocessing: bool = False, num_cpu: int = 1,
                      images_saved_path: str = "Frames/Image_#.png", store_directions_viewer_in_memory: bool = True,
                      log: bool = True):
        if store_directions_viewer_in_memory:
            self.viewer.init_directions()
        for t in (tqdm(range(self.num_frames)) if log else range(self.num_frames)):
            if t % mod == val:
                self.update_scene(t, min(t, mod))
                if t >= t0:
                    self.create_image(t, multiprocessing=multiprocessing, num_cpu=num_cpu,
                                      images_saved_path=images_saved_path, log=False)
        if store_directions_viewer_in_memory:
            self.viewer.clear_directions()

    def create_video(self, t0: int = 0, multiprocessing: bool = False, num_cpu: int = 1,
                     multiprocessing_images: bool = False, video_path: str = "Video.mp4",
                     num_revolutions_video: int = 1, fps: int = 30, gif_path: str = None,
                     images_saved_path: str = "Frames/Image_#.png", store_directions_viewer_in_memory: bool = True,
                     log: bool = True):
        if log:
            print("Saving images for video")
        if multiprocessing:
            with Pool() as pool:
                pool.starmap(SceneManager.create_images, [(self, t0, num_cpu, i, False, 1, images_saved_path,
                                                           store_directions_viewer_in_memory, log)
                                                          for i in range(num_cpu)])
        else:
            self.create_images(t0=t0, multiprocessing=multiprocessing_images, num_cpu=num_cpu,
                               store_directions_viewer_in_memory=store_directions_viewer_in_memory, log=log)
        if log:
            print("=> Images saved")

        if video_path is not None:
            clip = Movieclip.ImageSequenceClip([images_saved_path.replace("#", str(i + 1))
                                                for i in range(self.num_frames)] * num_revolutions_video, fps=fps)
            clip.write_videofile(video_path, audio=False)
        if gif_path is not None:
            clip = Movieclip.ImageSequenceClip([images_saved_path.replace("#", str(i + 1))
                                                for i in range(self.num_frames)], fps=fps)
            clip.write_gif(gif_path)
