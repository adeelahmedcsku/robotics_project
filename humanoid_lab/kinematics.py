"""Position-only damped least-squares IK in a fixed pelvis fixture."""
import numpy as np
import mujoco as mj
from model import load, addresses, names

def planar(q, lengths=(.3, .2)):
    a, b = q; l1, l2 = lengths
    return np.array([l1*np.cos(a)+l2*np.cos(a+b),
                     l1*np.sin(a)+l2*np.sin(a+b)])

def solve(m, d, target, iterations=150, tolerance=.002):
    joint_names = names(m)
    arm = [i for i, name in enumerate(joint_names) if name.startswith('left_')
           and any(x in name for x in ('shoulder', 'elbow', 'wrist'))]
    ids, qi, vi = addresses(m)
    bid = m.body('left_wrist_yaw_link').id
    jp, jr = np.zeros((3, m.nv)), np.zeros((3, m.nv))
    for _ in range(iterations):
        mj.mj_forward(m, d)
        error = target-d.xpos[bid]
        if np.linalg.norm(error) < tolerance:
            return True, float(np.linalg.norm(error))
        mj.mj_jacBody(m, d, jp, jr, bid)
        j = jp[:, vi[arm]]
        dq = j.T @ np.linalg.solve(j@j.T+.01**2*np.eye(3), error)
        d.qpos[qi[arm]] += np.clip(dq, -.04, .04)
        d.qpos[qi[arm]] = np.clip(d.qpos[qi[arm]],
            m.jnt_range[ids[arm], 0], m.jnt_range[ids[arm], 1])
    mj.mj_forward(m, d)
    return False, float(np.linalg.norm(target-d.xpos[bid]))

if __name__ == '__main__':
    print('Two-link at zero:', planar([0., 0.]))
    m, d = load()
    target = d.xpos[m.body('left_wrist_yaw_link').id].copy()
    target += [.02, 0., .01]
    ok, error = solve(m, d, target)
    print('IK converged:', ok, 'residual [m]:', error)
    if not ok:
        raise SystemExit('Target not reached; retain last validated pose')
