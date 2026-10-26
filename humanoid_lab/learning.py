"""CPU Gymnasium tasks: supported reach, free-base stand, free-base walk."""
import argparse
import json
import gymnasium as gym
import mujoco as mj
import numpy as np
from gymnasium import spaces
from model import ROOT, load, addresses, names, command

class HumanoidTask(gym.Env):
    metadata = {'render_modes': []}
    def __init__(self, task='reach'):
        super().__init__()
        if task not in ('reach', 'stand', 'walk'):
            raise ValueError(task)
        self.task = task
        self.m, self.d = load(supported=task == 'reach')
        self.ids, self.qi, self.vi = addresses(self.m)
        self.home = self.m.qpos0[self.qi].copy()
        self.elbow = names(self.m).index('left_elbow_joint')
        self.n = 1 if task == 'reach' else self.m.nu
        self.action_space = spaces.Box(-1., 1., (self.n,), np.float32)
        self.observation_space = spaces.Box(-np.inf, np.inf,
            (2*self.m.nu+9+self.n+1,), np.float32)
        self.nominal_mass = self.m.body_mass.copy()
        self.nominal_inertia = self.m.body_inertia.copy()
        self.previous = np.zeros(self.n)
        self.steps = 0
        self.goal = self.home[self.elbow]+.1

    def observation(self):
        rot = self.d.xmat[self.m.body('pelvis_link').id].reshape(3, 3)
        if self.task == 'reach':
            velocity, omega = np.zeros(3), np.zeros(3)
        else:
            # Free-joint translation velocity is world-frame; rotate to body.
            velocity = rot.T @ self.d.qvel[:3]
            omega = self.d.qvel[3:6].copy()
        return np.concatenate([self.d.qpos[self.qi]-self.home,
            self.d.qvel[self.vi], rot.T @ np.array([0., 0., -1.]),
            velocity, omega, self.previous,
            [self.goal-self.home[self.elbow]]]).astype(np.float32)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        mj.mj_resetData(self.m, self.d)
        # Correlated mass/inertia scaling keeps the randomized inertias physical.
        scale = self.np_random.uniform(.95, 1.05)
        self.m.body_mass[:] = self.nominal_mass*scale
        self.m.body_inertia[:] = self.nominal_inertia*scale
        mj.mj_setConst(self.m, self.d)
        self.steps = 0; self.previous = np.zeros(self.n)
        self.goal = self.home[self.elbow]+self.np_random.uniform(.05, .15)
        mj.mj_forward(self.m, self.d)
        return self.observation(), {}

    def step(self, action):
        action = np.asarray(action, dtype=float)
        if action.shape != (self.n,) or not np.isfinite(action).all():
            raise ValueError('Invalid action')
        action = np.clip(action, -1, 1)
        target = self.home.copy()
        if self.task == 'reach':
            target[self.elbow] += .2*action[0]
        else:
            target += .15*action
        for _ in range(10):
            command(self.m, self.d, target)
            mj.mj_step(self.m, self.d)
        self.steps += 1
        rot = self.d.xmat[self.m.body('pelvis_link').id].reshape(3, 3)
        upright = float(rot[2, 2])
        error = float(self.d.qpos[self.qi[self.elbow]]-self.goal)
        smooth = float(np.sum((action-self.previous)**2))
        effort = float(np.mean(self.d.ctrl**2))
        fallen = self.task != 'reach' and (self.d.qpos[2] < .35 or upright < .8)
        bad = not np.isfinite(self.d.qpos).all()
        if self.task == 'reach':
            reward = -100*error**2-.005*smooth-.0001*effort
        else:
            vx = float(self.d.qvel[0])
            desired = .15 if self.task == 'walk' else 0.
            reward = 1.+upright-np.square(vx-desired)*3-.01*smooth-.0001*effort
            if fallen: reward -= 10.
        self.previous = action.copy()
        return self.observation(), float(reward), bool(fallen or bad), self.steps >= 250, {
            'error_rad': abs(error), 'upright': upright, 'fallen': bool(fallen)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['check', 'train', 'evaluate', 'export'])
    p.add_argument('--task', default='reach', choices=['reach', 'stand', 'walk'])
    p.add_argument('--steps', type=int, default=100000)
    args = p.parse_args()
    from stable_baselines3 import PPO
    from stable_baselines3.common.env_checker import check_env
    from stable_baselines3.common.monitor import Monitor
    from stable_baselines3.common.callbacks import CheckpointCallback
    folder = ROOT/'logs'/args.task; folder.mkdir(exist_ok=True)
    env = HumanoidTask(args.task)
    if args.mode == 'check':
        check_env(env); print('Environment contract passed'); return
    if args.mode == 'train':
        model = PPO('MlpPolicy', Monitor(env, str(folder/'monitor')), seed=7,
                    device='cpu', n_steps=512, batch_size=64, verbose=1)
        model.learn(total_timesteps=args.steps, callback=CheckpointCallback(
            save_freq=10000, save_path=str(folder), name_prefix='checkpoint'))
        model.save(folder/'policy')
        (folder/'metadata.json').write_text(json.dumps(dict(
            task=args.task, seed=7, action_dim=env.n,
            observation_dim=env.observation_space.shape[0],
            joints=names(env.m), dt_control=.02, mujoco=mj.__version__), indent=2))
    elif args.mode == 'evaluate':
        model = PPO.load(folder/'policy', device='cpu')
        results = []
        for seed in range(100, 120):
            obs, _ = env.reset(seed=seed); total = 0.; errors=[]
            for _ in range(250):
                action, _ = model.predict(obs, deterministic=True)
                obs, r, end, cutoff, info = env.step(action)
                total += r; errors.append(info['error_rad'])
                if end or cutoff: break
            results.append(dict(seed=seed, total=total,
                final_error=float(np.mean(errors[-50:])), **info))
        (folder/'evaluation.json').write_text(json.dumps(results, indent=2))
        print('Mean final error:', np.mean([x['final_error'] for x in results]))
        print('Fall fraction:', np.mean([x['fallen'] for x in results]))
    else:
        import torch
        model = PPO.load(folder/'policy', device='cpu')
        class Actor(torch.nn.Module):
            def __init__(self, policy):
                super().__init__(); self.policy = policy
            def forward(self, observation):
                return self.policy(observation, deterministic=True)[0]
        sample = torch.zeros((1, env.observation_space.shape[0]))
        actor = Actor(model.policy).eval()
        traced = torch.jit.trace(actor, sample)
        assert torch.allclose(actor(sample), traced(sample))
        traced.save(str(folder/'actor.pt'))
        print('Exported inference artifact; physical deployment remains gated')
    env.close()

if __name__ == '__main__':
    main()
