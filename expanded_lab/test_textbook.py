"""Semantic numerical checks and published-module parity for the textbook."""
from pathlib import Path
import runpy
import sys
sys.path.insert(0,str(Path(__file__).parent))
import numpy as np
import pytest
from catalog import load_catalog,evaluate

SPECS={s['key']:s for s in load_catalog()}

def result(key,**changes):
    s=SPECS[key];p=dict(s['params']);p.update(changes)
    return evaluate(s,p)['metrics']

@pytest.mark.parametrize('key',list(SPECS))
def test_standalone_module_matches_catalog_in_all_six_cases(key):
    s=SPECS[key]
    path=next((Path(__file__).parent/'modules').glob('*_'+key+'.py'))
    function=runpy.run_path(str(path))['experiment']
    for v in s['values']:
        p=dict(s['params']);p[s['vary']]=v
        reference=evaluate(s,p)['metrics'];actual,_,_=function(p)
        assert actual.keys()==reference.keys()
        assert all(np.isclose(actual[k],reference[k],rtol=1e-10,atol=1e-12)
                   for k in reference)

def test_transmission_conserves_ideal_power():
    x=result('units',efficiency=1.)
    assert np.isclose(x['input_power_W'],x['output_power_W'])

def test_force_parallel_to_lever_has_zero_torque():
    assert abs(result('vectors',angle_deg=0.)['axis_torque_Nm'])<1e-12

def test_rotation_and_transform_roundtrips():
    assert result('rotations')['roundtrip_error_m']<1e-12
    assert result('transforms')['roundtrip_error_m']<1e-12

def test_quaternion_sign_equivalence():
    assert result('quaternions')['sign_equivalence_error_rad']<1e-6

def test_derivative_accuracy_reference():
    assert result('jacobian',epsilon=1e-5)['derivative_error']<1e-8

def test_implicit_decay_stays_positive_where_explicit_is_unstable():
    x=result('integration',dt=.25)
    assert x['explicit_amplification']>1 and x['implicit_final']>0

def test_payload_shifts_com_forward():
    assert result('center_mass',payload_mass=4.)['com_x_m']>result('center_mass',payload_mass=0.)['com_x_m']

def test_parallel_axis_increases_inertia():
    assert result('inertia',offset=.2)['Izz_kg_m2']>result('inertia',offset=0.)['Izz_kg_m2']

def test_unreachable_ik_is_not_reported_success():
    assert result('planar_ik',target_x=.6)['reachable']==0
    assert result('planar_ik',target_x=.35)['residual_m']<1e-10

def test_damping_trades_joint_step_for_residual():
    low=result('damped_ik',damping=.001);high=result('damped_ik',damping=.1)
    assert high['joint_step_norm_rad']<low['joint_step_norm_rad']
    assert high['predicted_residual_m']>low['predicted_residual_m']

def test_friction_impossibility_is_visible():
    assert result('friction_cone',mu=.1)['force_margin_N']<0

def test_minimum_jerk_duration_scaling():
    a=result('minimum_jerk',duration=1.);b=result('minimum_jerk',duration=2.)
    assert np.isclose(a['peak_speed_rad_s'],2*b['peak_speed_rad_s'])
    assert np.isclose(a['peak_acceleration_rad_s2'],4*b['peak_acceleration_rad_s2'])

def test_larger_speed_consumes_stopping_margin():
    assert result('rate_limits',speed=.8)['remaining_travel_margin_rad']<result('rate_limits',speed=.2)['remaining_travel_margin_rad']

def test_increased_loss_raises_temperature():
    assert result('thermal',loss_power=40.)['final_temperature_C']>result('thermal',loss_power=5.)['final_temperature_C']

def test_projection_roundtrip_and_depth_uncertainty():
    assert result('pinhole')['roundtrip_error_m']<1e-12
    assert result('stereo_depth',true_depth=2.)['depth_std_m']>result('stereo_depth',true_depth=1.)['depth_std_m']

def test_queue_freshness_under_overload():
    x=result('queue_age',consumer_period=.05)
    assert x['fifo_max_age_s']>x['latest_max_age_s']+.5

def test_synthetic_codec_detects_single_bit_faults():
    assert result('packet_codec')['rejection_fraction']==1.

def test_faults_do_not_auto_resume():
    assert result('lifecycle')['automatic_resume_count']==0
    assert result('skill_planner',amplitude=.2)['primary_request_approved']==0

def test_matching_replay_has_no_disagreement():
    assert result('replay',scale_error_factor=1.)['maximum_absolute_action_error']==0

def test_budget_counts_growth_and_contingency():
    x=result('landed_budget',motor_count=12)
    assert x['budget_margin_EUR']<0 and x['reserve_EUR']>0

def test_cable_heat_is_quadratic_in_current():
    a=result('cable_loss',current=5.);b=result('cable_loss',current=10.)
    assert np.isclose(b['conductor_heat_W'],4*a['conductor_heat_W'])

def test_stale_evidence_blocks_downstream_gate():
    assert result('commissioning_evidence',stale_gate_index=0)['walking_ready']==0

def test_manifest_order_does_not_hide_semantic_change():
    assert result('manifest_hashes',action_scale=.15)['content_identity_changed']==0
    assert result('manifest_hashes',action_scale=.2)['content_identity_changed']==1

def test_capstone_detects_dropout_but_not_uninterrupted_stream():
    assert result('capstone',dropout_start=1.)['fault_latched']==1
    assert result('capstone',dropout_start=5.)['fault_latched']==0
