"""Static support geometry and a deliberately passive free-base fall test."""
import json
import numpy as np
import mujoco as mj
from model import ROOT, load

def margin_rectangle(point, xmin, xmax, ymin, ymax):
    x, y = point
    return float(min(x-xmin, xmax-x, y-ymin, ymax-y))

def passive_trial(seed):
    rng = np.random.default_rng(seed)
    m, d = load(supported=False)
    d.qvel[:3] = rng.normal(0, .01, 3)
    start = d.qpos[:3].copy()
    fallen = False
    peak_tilt = 0.
    for _ in range(1000):
        mj.mj_step(m, d)
        rot = d.xmat[m.body('pelvis_link').id].reshape(3, 3)
        tilt = np.arccos(np.clip(rot[2, 2], -1, 1))
        peak_tilt = max(peak_tilt, float(tilt))
        if d.qpos[2] < .35 or tilt > .6:
            fallen = True; break
    return dict(seed=seed, fallen=fallen, time=float(d.time),
                displacement=float(np.linalg.norm(d.qpos[:2]-start[:2])),
                peak_tilt_rad=peak_tilt)

if __name__ == '__main__':
    # An illustrative polygon, not a measured Asimov foot polygon.
    print('Illustrative COM margin:', margin_rectangle([.01, 0], -.1, .1, -.08, .08))
    trials = [passive_trial(i) for i in range(5)]
    (ROOT/'logs/passive_trials.json').write_text(json.dumps(trials, indent=2))
    print(trials)
