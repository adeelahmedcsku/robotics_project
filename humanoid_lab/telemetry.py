"""Plot recorded feedback; no actuator network connection."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import ROOT, load

if __name__ == '__main__':
    data = np.genfromtxt(ROOT/'logs/joints.csv', delimiter=',', names=True)
    fig, axes = plt.subplots(3, 1, figsize=(8, 7), sharex=True)
    axes[0].plot(data['t'], data['target'], label='target')
    axes[0].plot(data['t'], data['q'], label='encoder truth')
    axes[0].set_ylabel('Angle [rad]'); axes[0].legend()
    axes[1].plot(data['t'], data['dq']); axes[1].set_ylabel('Speed [rad/s]')
    axes[2].plot(data['t'], data['command_Nm']); axes[2].set_ylabel('Command [Nm]')
    axes[2].set_xlabel('Simulation time [s]')
    fig.tight_layout(); fig.savefig(ROOT/'logs/telemetry.png', dpi=160)
    m, d = load()
    for i in range(m.nsensor):
        a, n = m.sensor_adr[i], m.sensor_dim[i]
        print(m.sensor(i).name, d.sensordata[a:a+n].copy())
    print('COM world [m]:', d.subtree_com[m.body('pelvis_link').id])
