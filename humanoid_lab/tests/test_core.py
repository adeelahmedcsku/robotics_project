import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pytest
import mujoco as mj
from model import load, command, addresses
from kinematics import planar, solve
from balance import margin_rectangle

def test_asimov_contract():
    m, d = load()
    assert (m.nq, m.nv, m.nu) == (25, 25, 25)
    assert np.isclose(m.opt.timestep, .002)
    assert np.all(m.body_mass[1:] > 0)
    assert np.isfinite(d.qpos).all()

def test_bounded_feedback_and_rejection():
    m, d = load()
    with pytest.raises(ValueError):
        command(m, d, np.full(m.nu, np.nan))
    ids, qi, vi = addresses(m)
    for _ in range(500):
        command(m, d, m.qpos0[qi]); mj.mj_step(m, d)
    assert np.isfinite(d.qpos).all()
    assert np.max(np.abs(d.qvel)) < 50
    assert np.all(np.abs(d.ctrl) <= np.max(np.abs(m.actuator_ctrlrange), axis=1)*.25+1e-8)

def test_planar_geometry_and_ik():
    assert np.allclose(planar([0, 0]), [.5, 0])
    m, d = load()
    target = d.xpos[m.body('left_wrist_yaw_link').id].copy()+[.02, 0, .01]
    ok, error = solve(m, d, target)
    assert ok and error < .002

def test_static_margin_sign():
    assert margin_rectangle([0, 0], -.1, .1, -.1, .1) == .1
    assert margin_rectangle([.2, 0], -.1, .1, -.1, .1) < 0
