# coding: utf-8

import moviepy.video.io.ImageSequenceClip as Movieclip
from PIL import Image

from scene_manager import SceneManager

if __name__ == "__main__":
    id_scene = 4
    one_frame = False
    create_video = True
    create_gif = False
    num_revolutions_video = 2
    multiprocessing = True
    num_cpu = 4
    fps = 30

    scene_manager = SceneManager(id_scene)
    for t in range(1 if one_frame else scene_manager.num_frames):
        if multiprocessing:
            pixels = scene_manager.viewer.trace_rays_multiprocessing(num_cpu)
        else:
            pixels = scene_manager.viewer.trace_rays()
        image = Image.fromarray(pixels)
        image.save(f"Frames/Image_{t + 1}.png")
        if not one_frame:
            print(f"{round(100 * (t + 1) / scene_manager.num_frames)} %")
            scene_manager.update_scene(t)

    if create_video or create_gif:
        if create_video:
            clip = Movieclip.ImageSequenceClip([f"Frames/Image_{i + 1}.png"
                                                for i in range(scene_manager.num_frames)] * num_revolutions_video,
                                               fps=fps)
            clip.write_videofile("Video.mp4", audio=False)
        if create_gif:
            clip = Movieclip.ImageSequenceClip([f"Frames/Image_{i + 1}.png"
                                                for i in range(scene_manager.num_frames)], fps=fps)
            clip.write_gif("Video.gif")

    exit(0)
