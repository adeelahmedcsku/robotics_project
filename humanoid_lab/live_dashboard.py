"""Read the simulation CSV while simulate.py writes it; run in another terminal."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from model import ROOT
fig, axes = plt.subplots(2, 1, sharex=True)

def update(_):
    path = ROOT/'logs/joints.csv'
    if not path.exists(): return
    try:
        data = np.genfromtxt(path, delimiter=',', names=True, invalid_raise=False)
        if data.size < 2: return
        data = data[-2500:]
        axes[0].clear(); axes[1].clear()
        axes[0].plot(data['t'], data['target'], label='target')
        axes[0].plot(data['t'], data['q'], label='feedback')
        axes[0].set_ylabel('Joint angle [rad]'); axes[0].legend()
        axes[1].plot(data['t'], data['command_Nm'])
        axes[1].set_ylabel('Command [Nm]'); axes[1].set_xlabel('Simulation time [s]')
    except (ValueError, OSError, IndexError):
        return  # Writer may be between records; try next display interval.

animation = FuncAnimation(fig, update, interval=250, cache_frame_data=False)
plt.show()
