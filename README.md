# Ray tracing

By Quen69FR.

![demo screenshot](Results/ChessBoard1.png)

![demo screenshot](Results/RevolvingSpheresStep1.gif)

![demo screenshot](Results/LightBlock.png)

## Purpose

Recreate standard raytracing in python with following features :

* sphere and planes / rectangle
* multi light source
* ambient light
* reflexion (mirrors)
* colors
* specular reflexion (gloss)
* textures mapping
* scene animation and video mp4
* pure python
* multiprocessing




## Install

Clone from GitHub and Install Prerequisite
* python3
* Pillow (PIL)
* moviepy
* tqdm (progress bar)

python3 -m pip install -r requirements.txt


## Usage

1. Edit scene in scene_manager.py
2. Edit cpu/ressources in small main.py
3. Launch : python3 main.py

Don't use more CPU than the number available on your machine.

## Design notes

Multiprocessing can be either by distributing frames to each process (when making a movie)
or distributing various part of a single image.

## Evolution / TODO

if interested, don't hesitate to reuse and extend.

Ideas:
* Texture for spheres
* Other shapes/objects : triangles, polygones (convex...), disk...
* Bounding shapes (avoid testing the intersections on the other side of the scene or to avoid same complicated calcul 
shape intersections...)
* Add texture for : the shapes (delimit the edges), the glossiness and the mirror reflection (gray scale)...
* Add waves length instead of RGB colors
* Translucent surface : Diffusion, refraction... (in the calcul_ray_intensity function, the boolean inverse_normal
directly says from which to which materials the light ray goes)
* Load STL files
