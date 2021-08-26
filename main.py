# coding: utf-8

from scene_manager import SceneManager


if __name__ == "__main__":
    # scene_manager = SceneManager(4)
    # scene_manager.create_video(multiprocessing=True, num_cpu=4, num_revolutions_video=1)
    scene_manager = SceneManager(5)
    scene_manager.create_image(multiprocessing=True, num_cpu=4)
    exit(0)

# TODO : - Texture for spheres
#        - Other shapes/objects : triangles, polygones (convex...), disk...
#        - Bounding shapes (to avoid to test the intersections on the other side of the scene or to avoid same
#                           complicated calcul shape intersections...)
#        - Add texture for : the shapes (delimit the edges), the glossiness and the mirror reflection (gray scale)...
#        - Add waves length instead of RGB colors
#        - Translucent surface : Diffusion, refraction... (in the calcul_ray_intensity function, the boolean
#                                                          inverse_normal directly says from which to which materials
#                                                          the light ray goes)
#        - Load STL files
