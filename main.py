# coding: utf-8

from scene_manager import SceneManager
from viewer import Viewer

if __name__ == "__main__":
    scene_manager = SceneManager(4)
    Viewer.store_directions_in_memory = True
    scene_manager.create_video(multiprocessing=True, num_cpu=4, num_revolutions_video=1)
    exit(0)
