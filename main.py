# coding: utf-8

from scene_manager import SceneManager
from viewer import Viewer

if __name__ == "__main__":
    Viewer.store_directions_in_memory = True
    scene_manager = SceneManager(4)
    scene_manager.create_video(multiprocessing=True, num_cpu=4, num_revolutions_video=1)
    exit(0)

# TODO : - Texture for spheres
#        - Other shapes/objects : triangles, polygones (convex...), disk...
#        - Bounding shapes (to avoid to test the intersections on the other side of the scene or to avoid complicated
#                           calcul shape intersections...)
#        - Add texture for : the shapes (delimit the edges), the glossiness (gray scale), the mirror reflection (gray
#                            scale)...
#        - Add waves length instead of RGB colors
#        - Translucent surface : Diffusion, refraction... (in the calcul_ray_intensity function, the boolean
#                                                          inverse_normal directly say from which to which materials
#                                                          the light ray goes)
#        - Load STL files
