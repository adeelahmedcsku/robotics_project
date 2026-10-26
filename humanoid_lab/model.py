"""Educational Asimov model adapters; simulation only."""
from pathlib import Path
import xml.etree.ElementTree as ET
import mujoco as mj
import numpy as np

ROOT = Path(__file__).resolve().parent
ASSET = (ROOT.parent / 'research/asimov-1/sim-model/'
         'asimov_1_25dof/xml/asimov_1_25dof.xml')

def load(supported: bool = True):
    tree = ET.parse(ASSET)
    xml = tree.getroot()
    xml.find('compiler').set('meshdir', str(ASSET.parent.parent / 'meshes'))
    xml.find('option').set('timestep', '0.002')
    # Fixed pelvis in the teaching fixture. This is not balancing.
    if supported:
        base = xml.find('.//freejoint')
        xml.find('.//body[@name="pelvis_link"]').remove(base)
    for actuator in list(xml.findall('actuator')):
        xml.remove(actuator)
    actuators = ET.SubElement(xml, 'actuator')
    joints = xml.findall('.//worldbody//joint')
    for j in joints:
        # Remove passive springs so they do not hide controller behavior.
        for attr in ('stiffness', 'damping', 'springref'):
            j.set(attr, '0')
        limits = j.get('actuatorfrcrange', '-8 8')
        ET.SubElement(actuators, 'motor', name=j.get('name')+'_motor',
                      joint=j.get('name'), gear='1',
                      ctrllimited='true', ctrlrange=limits)
    model = mj.MjModel.from_xml_string(ET.tostring(xml, encoding='unicode'))
    model.opt.gravity[:] = [0, 0, -9.81]
    data = mj.MjData(model)
    mj.mj_forward(model, data)
    return model, data

def addresses(model):
    ids = model.actuator_trnid[:, 0].astype(int)
    return ids, model.jnt_qposadr[ids], model.jnt_dofadr[ids]

def names(model):
    ids, _, _ = addresses(model)
    return [mj.mj_id2name(model, mj.mjtObj.mjOBJ_JOINT, int(j)) for j in ids]

def command(model, data, target, kp=35., kd=4., fraction=0.25):
    ids, qi, vi = addresses(model)
    target = np.asarray(target, dtype=float)
    if target.shape != (model.nu,) or not np.isfinite(target).all():
        raise ValueError('Expected one finite target per actuator')
    lo, hi = model.jnt_range[ids].T
    target = np.clip(target, lo, hi)
    # qfrc_bias is ideal model feedforward, not measured motor torque.
    torque = kp*(target-data.qpos[qi])-kd*data.qvel[vi]+data.qfrc_bias[vi]
    cap = np.max(np.abs(model.actuator_ctrlrange), axis=1)*fraction
    data.ctrl[:] = np.clip(torque, -cap, cap)
    return target.copy()
