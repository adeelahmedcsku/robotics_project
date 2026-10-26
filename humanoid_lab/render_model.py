"""Offscreen inspection image; set MUJOCO_GL before importing MuJoCo."""
import mujoco as mj
import matplotlib.pyplot as plt
from model import ROOT, load
m, d = load()
with mj.Renderer(m, height=960, width=720) as renderer:
    camera = mj.MjvCamera()
    mj.mjv_defaultCamera(camera)
    camera.lookat[:] = [0, 0, .65]
    camera.distance = 1.9
    camera.azimuth = 145
    camera.elevation = -10
    options = mj.MjvOption()
    options.geomgroup[3] = 0
    renderer.update_scene(d, camera=camera, scene_option=options)
    plt.imsave(ROOT/'logs/asimov_model.png', renderer.render())
print(ROOT/'logs/asimov_model.png')
