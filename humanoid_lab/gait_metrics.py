# /data/Robotics_Project/humanoid_lab/gait_metrics.py
import argparse
import numpy as np

def summarize(path):
    x = np.genfromtxt(path, delimiter=',', names=True)
    if len(x) < 2 or not np.all(np.diff(x['t']) > 0):
        raise ValueError('Need increasing timestamped samples')
    distance = float(np.sum(np.hypot(np.diff(x['x']), np.diff(x['y']))))
    tracking = np.sqrt(np.mean((x['vx']-x['cmd_vx'])**2+
                               (x['vy']-x['cmd_vy'])**2))
    yaw_tracking = np.sqrt(np.mean((x['wz']-x['cmd_wz'])**2))
    energy = np.trapezoid(np.maximum(x['power_w'], 0), x['t'])
    return dict(distance_m=distance, velocity_rmse_mps=float(tracking),
                yaw_rate_rmse_radps=float(yaw_tracking),
                positive_energy_j=float(energy),
                slip_rms_mps=float(np.sqrt(np.mean(x['slip_mps']**2))),
                fell=bool(np.any(x['fallen'] > 0)))

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('csv')
    print(summarize(p.parse_args().csv))
