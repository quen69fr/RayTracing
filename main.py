# coding: utf-8

from scene_manager import SceneManager


if __name__ == "__main__":
    # scene_manager = SceneManager(4)
    # scene_manager.create_video(multiprocessing=True, num_cpu=4)
    scene_manager = SceneManager(5)
    scene_manager.create_image(multiprocessing=True, num_cpu=4)
    exit(0)
