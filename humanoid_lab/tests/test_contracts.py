import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pytest
from safety import Gate
from perception import detect
from learning import HumanoidTask

def test_fault_latches():
    g = Gate(np.array([-1.]), np.array([1.]))
    with pytest.raises(RuntimeError, match='stale'):
        g.validate(1., 0., 1, [0.], [0.], .01)
    with pytest.raises(RuntimeError):
        g.validate(1., 1., 2, [0.], [0.], .01)

def test_detection_does_not_invent_depth():
    im = np.zeros((100, 100, 3), np.uint8)
    assert detect(im) is None
    im[20:40, 30:60, 1] = 255
    assert detect(im)['depth_m'] is None

def test_seeded_reset_and_action_contract():
    env = HumanoidTask()
    a, _ = env.reset(seed=3); b, _ = env.reset(seed=3)
    assert np.array_equal(a, b)
    obs, reward, done, truncated, info = env.step(np.zeros(1))
    assert env.observation_space.contains(obs)
    assert np.isfinite(reward) and not done
    with pytest.raises(ValueError):
        env.step(np.array([np.nan]))
