"""Inspect, view and log a supported Asimov joint trajectory."""
import argparse
import csv
import time
import numpy as np
import mujoco as mj
from model import ROOT, load, addresses, names, command

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--headless', action='store_true')
    p.add_argument('--seconds', type=float, default=10.)
    args = p.parse_args()
    if not 0 < args.seconds <= 600:
        p.error('seconds must be in (0, 600]')
    m, d = load()
    ids, qi, vi = addresses(m)
    joint_names = names(m)
    print('nq, nv, nu:', m.nq, m.nv, m.nu)
    for name, j in zip(joint_names, ids):
        print(name, 'range=', m.jnt_range[j])
    j = joint_names.index('left_elbow_joint')
    home = d.qpos[qi].copy()
    path = ROOT/'logs/joints.csv'
    path.parent.mkdir(exist_ok=True)
    with path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['t', 'target', 'q', 'dq', 'command_Nm'])
        def tick():
            target = home.copy()
            target[j] += 0.1*np.sin(2*np.pi*0.25*d.time)
            actual = command(m, d, target)
            mj.mj_step(m, d)
            if not np.isfinite(d.qpos).all():
                raise RuntimeError('Nonfinite simulation state')
            writer.writerow([d.time, actual[j], d.qpos[qi[j]],
                             d.qvel[vi[j]], d.ctrl[j]])
            if round(d.time/m.opt.timestep) % 100 == 0:
                f.flush()
        if args.headless:
            for _ in range(round(args.seconds/m.opt.timestep)):
                tick()
        else:
            import mujoco.viewer
            with mujoco.viewer.launch_passive(m, d) as v:
                v.cam.distance = 2.2
                v.cam.lookat[:] = [0, 0, .65]
                v.cam.elevation = -15
                while v.is_running() and d.time < args.seconds:
                    start = time.monotonic()
                    tick()
                    v.sync()
                    time.sleep(max(0., m.opt.timestep-(time.monotonic()-start)))
    print('Saved', path)

if __name__ == '__main__':
    main()
