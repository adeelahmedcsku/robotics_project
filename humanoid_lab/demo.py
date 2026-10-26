"""Detect an object and execute a bounded supported elbow gesture."""
import json
import numpy as np
import mujoco as mj
from model import ROOT, load, addresses, names, command
from perception import detect
from safety import Gate

def run():
    frame = np.zeros((240, 320, 3), np.uint8)
    frame[90:130, 190:230, 1] = 255
    detection = detect(frame)
    m, d = load(); ids, qi, vi = addresses(m)
    home = d.qpos[qi].copy(); joint = names(m).index('left_elbow_joint')
    gate = Gate(m.jnt_range[ids, 0], m.jnt_range[ids, 1], max_speed=1.)
    records=[]; previous=home.copy()
    if detection is None:
        return {'state': 'NO_OBJECT', 'motion': False}
    # Prevalidated gesture only. No depth-dependent reach is attempted.
    for k in range(1500):
        t = k*m.opt.timestep
        goal = home.copy()
        goal[joint] += .05*(1-np.cos(2*np.pi*t/3.))
        approved = gate.validate(t, t, k, goal, previous, m.opt.timestep)
        command(m, d, approved); previous=approved.copy()
        mj.mj_step(m, d)
        records.append([float(d.time), float(d.qpos[qi[joint]])])
    report = {'state': 'COMPLETE_SIMULATION', 'motion': True,
              'object': detection, 'steps': len(records),
              'max_elbow_rad': max(x[1] for x in records)}
    (ROOT/'logs/demo.json').write_text(json.dumps(report, indent=2))
    np.savetxt(ROOT/'logs/demo.csv', records, delimiter=',', header='t,elbow')
    return report

if __name__ == '__main__':
    print(run())
