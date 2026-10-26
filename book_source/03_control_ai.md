# Part III - Middleware, balance, learning and perception
## Lesson 5 - A modular ROS 2 humanoid workspace
### A. Why this matters
A single script is useful for proving a numerical idea. Multiple reusable robot capabilities need discoverable messages, explicit lifecycles and diagnostics. Keep the controller independent from the messaging layer so communication changes do not rewrite the physics.
### B. Concepts explained simply
A node is a process participant. A topic carries a stream; a service is a request and response; an action is a long-running goal with feedback and cancellation. Parameters configure nodes. Launch files start a repeatable set of processes. QoS expresses delivery and buffering choices; reliable delivery can still deliver stale data, while best-effort delivery can lose a fresh packet.

TF2 maintains timestamped frame relationships. URDF describes the link tree consumed by robot_state_publisher and RViz2. JointState supplies scalar joint feedback but does not define frame geometry. ros2_control standardizes controller and hardware interfaces; it is not automatically integrated merely because a topic is named joint_states. Lifecycle nodes add explicit configuration and activation transitions, useful when enabling hardware only after prerequisites pass.
### C. Real-world relevance
Separate simulation bridge, state estimation, kinematics, perception, behavior, safety and diagnostics nodes. Physical drivers should export verified state/command interfaces and preserve watchdog authority locally. The sample below provides a small two-node simulation system rather than claiming an entire hardware-control framework.
### D. Architecture
wave node -> /joint_targets -> simulation bridge -> bounded PD and physics -> /joint_states -> wave initialization and telemetry. A future estimator consumes IMU/joint/contact streams, a planner produces validated paths, and a safety node gates activation. No planner bypasses the local limits.
### E. Prerequisites
Ubuntu 24.04 and ROS 2 Jazzy. The package uses Python 3.12 to match Jazzy's system bindings. A separate --system-site-packages venv allows apt-installed rclpy to be imported. Do not activate an unrelated Conda environment.
### F. Step-by-step implementation
The complete installer below follows the official apt-source bootstrap in [S7] and refuses other OS versions. It downloads the current official Noble repository-configuration package; this is a changing bootstrap dependency, so preserve its version and checksum with your environment record. Review the script before running it on your machine. It was not executed during book preparation.
!code humanoid_lab/setup_ros.sh
```bash
bash /data/Robotics_Project/humanoid_lab/setup_ros.sh
```
After installation, prepare the package environment:
```bash
sudo apt update
sudo apt install ros-jazzy-desktop ros-dev-tools python3-colcon-common-extensions
source /opt/ros/jazzy/setup.bash
/usr/bin/python3 -m venv --system-site-packages /data/Robotics_Project/.venv-ros
source /data/Robotics_Project/.venv-ros/bin/activate
python -m pip install mujoco==3.4.0 numpy==2.2.6
export HUMANOID_LAB_ROOT=/data/Robotics_Project/humanoid_lab
cd /data/Robotics_Project/humanoid_lab/ros2_ws
colcon build --symlink-install --packages-select humanoid_bridge
source install/setup.bash
ros2 launch humanoid_bridge lab.launch.py
```
In a second terminal, source ROS and the workspace, then run ros2 topic echo /joint_states and ros2 topic hz /joint_states. Stop the wave node and observe the simulation fallback. The launch defaults to a GUI; for a headless integration check run the bridge executable directly without enabling its viewer parameter.
### G. Complete code
All files below are in /data/Robotics_Project/humanoid_lab/ros2_ws/src/humanoid_bridge/. Create resource/humanoid_bridge and humanoid_bridge/__init__.py as empty files. Names here are tutorial package names, not purported upstream Asimov packages.
!code humanoid_lab/ros2_ws/src/humanoid_bridge/package.xml
!code humanoid_lab/ros2_ws/src/humanoid_bridge/setup.py
!code humanoid_lab/ros2_ws/src/humanoid_bridge/setup.cfg
!code humanoid_lab/ros2_ws/src/humanoid_bridge/humanoid_bridge/bridge.py
!code humanoid_lab/ros2_ws/src/humanoid_bridge/humanoid_bridge/wave.py
!code humanoid_lab/ros2_ws/src/humanoid_bridge/launch/lab.launch.py
### H. Code walkthrough
The bridge creates a supported model once. It requires exact joint-name ordering and a complete finite vector. Incoming header timestamps are checked against the ROS system clock; the watchdog uses a monotonic clock. This minimal example assumes same-host clocks and does not enable simulated ROS time. Do not set use_sim_time without adding a /clock publisher and revising the timestamp contract.

A 10 ms timer advances five 2 ms physics steps and publishes feedback. The nominal wall rate is 100 Hz, not a guaranteed physical deadline. The wave node captures the first feedback pose, then publishes a smooth 50 Hz elbow target. Stopping publication causes the bridge to request its home pose after 100 ms. That is a simulation teaching fallback, not a physical emergency stop.

JointState effort here is simulated actuator force for gear-one hinge motors. A physical driver must document whether its reported value is command torque, current-derived torque, or independently measured output effort. Use SensorDataQoS for appropriate high-rate lossy telemetry only after checking compatibility; use short queues and expiration for commands even if reliable QoS is chosen.
### I. Expected result
Two nodes appear, the left elbow moves in the simulation viewer, and /joint_states updates near the nominal 100 Hz wall timer. There is no TF publisher in this minimal bridge; RViz requires robot_state_publisher with the pinned URDF and matching mesh resolution as an extension.
### J. Validation
This edition's ROS package was syntax-checked but not executed against a local Jazzy runtime. On your machine verify build, discovery, topic counts, actual viewer movement, stale-target rejection and fallback after the command node stops. Record the measured topic rate; a timer setting alone is not evidence. Then test a zero or old header stamp and a reordered name array.
### K. Troubleshooting
No rclpy import usually means the wrong Python/venv. No package discovery suggests the workspace was not built or sourced. Invisible topics across terminals may indicate ROS_DOMAIN_ID or middleware configuration differences. Mesh failures in RViz are a separate URDF path issue. An idle bridge can be correct if command timestamps are rejected.
### L. Practical exercise
Add a diagnostic topic reporting command age, rejected-message count and simulation real-time factor. Then place the bridge behind a lifecycle activation state so it refuses targets until configured.
### M. Connection to the physical Asimov 1
Node boundaries and message contracts transfer. The physical backend needs a verified hardware interface, deterministic local execution, release-specific safety state transitions and tested power isolation. Ordinary ROS Python timers do not establish real-time performance.
### N. Completion checklist
The package builds on Jazzy, two nodes exchange named data, stale targets are rejected, and stopping the publisher produces the documented simulation fallback. ROS integration remains a reader-side gate until these results are recorded.
### O. Next lesson preview
Investigate support geometry and unsupported dynamics before training a policy.

## Lesson 6 - Static balance and the limits of a supported pose
### A. Why this matters
A robot can look upright because it is fixed to the world, balanced quasi-statically, or dynamically stabilized. Those are three different engineering situations. Begin by identifying which constraints supply the forces.
### B. Concepts explained simply
Center of mass (COM) is the mass-weighted average of link centers: c=sum(m_i*c_i)/sum(m_i). Two masses, 2 kg at x=0 and 1 kg at x=.3 m, have COM x=.1 m. The support polygon is the convex hull of active contact patches. For slow, level-ground conditions, the COM's vertical projection inside that polygon is a useful static check, not a general dynamic guarantee.

Center of pressure (COP) locates the resultant normal contact force on a support plane. With two vertical loads of 100 N at x=-.1 m and 200 N at x=.1 m, COP x=.0333 m. Zero Moment Point (ZMP) is a related dynamic criterion under particular planar-contact assumptions; acceleration and angular momentum matter. COP, COM and ZMP are not interchangeable.

A linear inverted pendulum approximation uses x_ddot=(g/h)*(x-zmp) at approximately fixed COM height. At h=.6 m and x-zmp=.01 m, acceleration is about .1635 m/s^2. Small position errors can grow; being centered once is insufficient.
### C. Real-world relevance
Feet may slip, lift or deform. A harness can unload the robot and change the experiment. Report support forces and constraints when claiming standing performance.
### D. Architecture
Model mass and contacts -> support estimate -> COM and orientation estimate -> posture correction -> limited joint torques -> contact feedback. Static geometry informs planning; feedback and contact constraints determine dynamic recovery.
### E. Prerequisites
Joint control, sensor semantics and kinematics. No physical standing tests are authorized by a simulator result.
### F. Step-by-step implementation
Run the deliberately passive free-base baseline and read the JSON report. It applies no stabilizing motor commands. Its purpose is to demonstrate the failure a standing controller must improve upon.
```bash
python balance.py
```
Next implement supported posture tracking with the existing controller and compare to that baseline, labeling the fixture clearly. For actual unsupported standing research, use the stand task in Lesson 7 and measure it; do not silently treat a training run as solved.
### G. Complete code
File: /data/Robotics_Project/humanoid_lab/balance.py
!code humanoid_lab/balance.py
### H. Code walkthrough
margin_rectangle is a signed margin to four rectangle edges for a point. Its sample rectangle is illustrative, not measured Asimov geometry. A general foot-support hull needs actual contact points and convex-polygon edge distances. passive_trial loads a floating base, introduces a small seeded initial velocity, advances up to two seconds, and labels a fall when pelvis height or tilt crosses an explicitly chosen threshold.

The world-up test uses the pelvis rotation matrix's z-axis component. Quaternion components themselves should not be thresholded as if they were tilt angles. Five seeds expose repeatability; they do not establish robust control.
### I. Expected result
The prepared passive trials all fell in roughly half a simulated second. This is a useful negative baseline. A fixed-pelvis trajectory can still look stable because the fixture supplies missing support.
### J. Validation
Check positive static margin inside a rectangle and negative margin outside. Evaluate any standing controller over at least 20 held-out seeds and varied initial state before widening disturbances. Proposed research gate: 60 s per run, no falls in the declared test set, bounded tracking error and no unexplained sustained torque saturation. This is a simulation gate, not a physical safety certification.
### K. Troubleshooting
A zero fall rate from a fixed root is invalid evidence. Rising energy or large contact impulses may indicate poor initialization or gains. Torque saturation can make an otherwise good geometry infeasible. More friction can hide foot-slip failures instead of solving them.
### L. Practical exercise
Add a small known horizontal force for a short interval in simulation. Record force magnitude, duration, impulse and exact application point, then compare recovery with an unperturbed run.
### M. Connection to the physical Asimov 1
Support estimates need measured mass, contact properties and sensor calibration. A physical rig must handle the robot and a stopped or failed joint without relying on software torque.
### N. Completion checklist
You can separate supported motion from static and dynamic balance, compute a simple COM/COP example, and report both successes and falls under declared conditions.
### O. Next lesson preview
Train a small supported task, then extend the same environment contract to standing research.

## Lesson 7 - Reinforcement learning without hidden assumptions
### A. Why this matters
Learning can discover feedback strategies, but a reward is only a surrogate objective. You need enough control knowledge to recognize an unrealistic policy before deploying it.
### B. Concepts explained simply
The environment advances the simulated world. The agent chooses an action from an observation. An episode begins with reset and ends with a task failure or time limit. A policy maps observations to actions; a value function estimates future reward. Training changes policy parameters; evaluation freezes them.

PPO, Proximal Policy Optimization, constrains policy updates using a clipped probability-ratio objective so updates do not move too far from the data-generating policy at once. It still needs good observations, action scales, rewards and evaluation. Stable-Baselines3 implements PPO using PyTorch; the environment implements Gymnasium's reset/step contract. [S11, S12]

For the first task the pelvis is fixed and the policy controls one elbow target offset. It observes joint errors, velocities, gravity direction, velocity channels, its previous action and the requested elbow goal. The reward penalizes squared goal error, action changes and effort. This teaches an environment contract before introducing difficult contacts.
### C. Real-world relevance
A deployable policy needs a documented observation order, normalization, action scaling, control period, actuator model and failure behavior. A neural network file alone does not specify a robot controller.
### D. Architecture
Reset and randomization -> observation -> PPO actor -> bounded position target -> PD inner loop -> ten physics steps -> observation, reward, termination and metrics. Training and inference live in separate processes from hardware transport.
### E. Prerequisites
Lessons 1-6, CPU PyTorch and the pinned Gymnasium/SB3 packages. Begin on CPU. A large GPU does not fix an erroneous joint order or reward.
### F. Step-by-step implementation
```bash
python learning.py check --task reach
python learning.py train --task reach --steps 100000
python learning.py evaluate --task reach
python learning.py export --task reach
```
The environment checker verifies interface compatibility; it cannot verify that the reward represents a useful physical task. Training saves checkpoints and a final policy. Evaluation uses seeds 100-119, separate from training seed 7. Export writes a traced actor and metadata that must travel together.
### G. Complete code
File: /data/Robotics_Project/humanoid_lab/learning.py
!code humanoid_lab/learning.py
### H. Code walkthrough
Observation length is 2*nu+9+action_dim+1. The gravity direction comes from the pelvis rotation. Supported reach uses zero base velocity channels. The initial elbow goal is randomized over a small range. Action [-1,1] becomes a bounded .2 rad elbow offset; stand/walk use .15 rad offsets for all 25 joints. These are teaching scales, not a tuned locomotion configuration.

reset seeds the environment generator, restores state, and applies a small common mass/inertia factor. This preserves physical inertia consistency while testing a narrow kind of mismatch. It is a first domain-randomization example, not comprehensive sim-to-real randomization. step returns terminated for falls or invalid physics and truncated at 250 control steps. Treating a time limit as a fall changes value targets incorrectly.

The loop uses 2 ms physics and 20 ms policy updates. The command function supplies an ideal PD inner loop. The network learns targets, not raw motor bus messages. Export checks the traced actor against its eager output on a sample. The preparation audit also compared eager and exported actions on 100 rollout observations. SB3 predict clips Box actions; an exported actor must receive the same external action clipping. Observation-schema hash checks and replay on hardware recordings are still required before deployment.
### I. Expected result
A valid environment, readable training metrics, checkpoints, metadata, a deterministic evaluation report and actor.pt. A 2,048-step smoke run only shows that the plumbing executes; it may not solve the reaching objective.
### J. Validation
Measure mean absolute elbow error over the final 50 steps per held-out episode. Compare against a no-motion baseline and the classical controller with direct goal access. Proposed reach gate: mean final error below .03 rad with no nonfinite states across 20 held-out seeds. Reject a policy that wins through a sensor-order bug or simulator exploit. Rerun with multiple training seeds before claiming reproducible learning.
### K. Troubleshooting
Reward improves but error does not: inspect individual reward terms and action scaling. Exploding values: verify finite observations and reward magnitude. Policy works only at reset: check whether goal information or time leaks into evaluation. Poor standing after reach success is expected; the dynamics and action dimension changed.
### L. Practical exercise
Log each reward component separately. Remove the effort penalty in a simulation experiment and observe whether the policy uses more saturation to improve error. Add observation noise on copies and quantify performance loss.
### M. Connection to the physical Asimov 1
The exported actor remains offline until hardware observation, timing, actuator and safety contracts pass. Randomize measured delays, friction, backlash, motor strength, noise and contact properties using defensible ranges from identification, not arbitrary values chosen to make a policy look robust.
### N. Completion checklist
You can explain every observation/action element, reproduce a seeded evaluation, compare baselines, separate termination from truncation and reject reward hacking. Training throughput and wall-time estimates come from your own benchmark.
### O. Next lesson preview
Extend evaluation to locomotion and learn what evidence a walking claim requires.

## Lesson 8 - Standing, walking and turning as research milestones
### A. Why this matters
Locomotion coordinates contact transitions while preserving feasible torques and momentum. A robot moving forward while falling is not walking, and a large reward is not a gait evaluation.
### B. Concepts explained simply
A gait alternates stance, when a foot supports load, and swing, when it moves toward a future contact. A foot trajectory needs position, velocity and clearance conditions. Velocity commands specify intent, while balance and contact controllers determine whether that intent is feasible.

Classical gait generation makes phases and constraints explicit and is easier to inspect, but model error can be costly. Whole-body optimization can coordinate tasks while enforcing constraints, but requires accurate models and careful numerical design. Learned policies can handle complex contact behavior, but can exploit simulation and require broad testing. Combine approaches only with a clear authority boundary.
### C. Real-world relevance
Foot slip, terrain compliance, ankle mapping and timing delays can destroy an otherwise good simulated gait. Turning adds yaw dynamics and changes support geometry; it is a separate test axis.
### D. Architecture
Velocity command -> gait or learned policy -> whole-body/joint targets -> constrained feedback -> contacts -> state estimator -> gait/policy feedback. A fall detector and command watchdog remain outside the reward.
### E. Prerequisites
Repeatable unsupported standing evaluation and the learned-task contract. The included stand and walk variants are a runnable research starting point, not validated locomotion solutions.
### F. Step-by-step implementation
```bash
python learning.py check --task stand
python learning.py train --task stand --steps 100000
python learning.py evaluate --task stand
```
Do not start walking deployment until standing meets your declared gate. The walk variant rewards forward velocity near .15 m/s. It intentionally does not supply a claimed solved policy. Run it as a training experiment after standing, then inspect videos, contacts and metrics. It has no turning command in the current observation; add an explicit yaw-rate command, observation and tracking term before attempting turning training.
### G. Complete code
The complete environment, training and evaluation code is learning.py in Lesson 7, with --task stand or --task walk. The following complete evaluator reads a walking trajectory CSV with columns t,x,y,yaw,vx,vy,wz,cmd_vx,cmd_vy,cmd_wz,power_w,slip_mps,fallen. Produce those channels from your simulator/controller before claiming a gait result.
```python
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
```
### H. Code walkthrough
The basic stand/walk reward is intentionally small: uprightness, velocity error, action smoothness and effort. It is insufficient by itself to exclude all unwanted gaits. Add lateral velocity, yaw-rate, foot-clearance, joint-speed, contact-slip and posture constraints only after inspecting failure cases. Reward design should follow a failure explanation, not random coefficient tuning.

The metric program integrates positive power over actual time. Mechanical power tau*dq differs from battery electrical power; report which one you logged. Slip should be measured only for a declared loaded contact, not a swinging foot. A zero slip measurement with no foot load is meaningless.
### I. Expected result
You obtain performance data and possibly failures. This book does not claim that the supplied reward and 100,000 steps produce standing, walking or turning. Those are gated research deliverables requiring iteration.
### J. Validation
For each final policy, evaluate multiple training seeds and at least 20 held-out episodes per condition. Include still commands, starts/stops, forward/backward/lateral commands, turn commands after implemented, friction variation, modest slopes and declared push impulses. Proposed simulation gate: zero falls in the published test matrix, velocity RMSE under .1 m/s at .15 m/s command, and bounded slip and torque saturation with thresholds chosen before evaluation. Report confidence limits; zero observed falls is not zero real-world risk.
### K. Troubleshooting
A policy may maximize reward by shuffling, hopping or exploiting favorable collisions. A baseline can fail because the default pose starts in penetration. Contact jitter may require a smaller timestep or better collision geometry rather than more RL steps. Do not disable self-collision solely to improve scores without documenting it.
### L. Practical exercise
Add command-conditioned yaw-rate tracking and create a held-out turn test. Preserve a no-turn policy as a baseline and compare energy and fall fraction.
### M. Connection to the physical Asimov 1
No simulated gait authorizes physical walking. Release-matched policy interfaces, calibrated ankles, measured timing and protected commissioning come first. Initial real tests remain supported and slow.
### N. Completion checklist
Your gait claim has a defined test matrix, raw traces, videos, tracking/slip/energy metrics, fall counts and an explicit statement of model assumptions. Failed gates block progression.
### O. Next lesson preview
Add perception and high-level skills without giving an AI planner unrestricted motor access.

## Lesson 9 - Perception and embodied behavior
### A. Why this matters
Perception should change a robot's choice of validated behavior. A detector alone is not embodied AI, while a motion script that ignores feedback is not a robust interaction.
### B. Concepts explained simply
A pinhole camera maps a 3-D point to pixels: u=fx*X/Z+cx and v=fy*Y/Z+cy. With fx=400 px, cx=160 px and X/Z=.1, u=200 px. One pixel coordinate does not determine Z. A monocular colored blob supplies an image-space direction, not a verified metric reach target.

HSV separates hue from brightness and saturation, making simple color segmentation convenient under controlled lighting. Connected components group adjacent mask pixels. This is a classical vision algorithm; a trained object detector is a different technique requiring its own model license, accuracy checks and compute budget.
### C. Real-world relevance
Camera intrinsics, lens distortion, exposure, lighting and camera-to-body calibration affect object estimates. Depth requires an actual depth source, known geometry or a calibrated inference method with uncertainty.
### D. Architecture
Camera or test image -> calibrated preprocessing -> detector -> timestamped observation -> behavior state machine -> prevalidated skill -> command gate -> controller -> feedback. A language model may select a permitted skill name and bounded parameters, never arbitrary control code.
### E. Prerequisites
Lessons 4-5, OpenCV, and a supported simulated motion. Start with synthetic images so detector failures are separable from camera transport.
### F. Step-by-step implementation
```bash
python perception.py
```
Inspect logs/object.png and logs/detection.json. The green circle should be detected near pixel (210,110). The JSON explicitly leaves depth_m null. For a real camera extension, log its calibration ID, capture timestamp, image dimensions and detector result before connecting behavior.
### G. Complete code
File: /data/Robotics_Project/humanoid_lab/perception.py
!code humanoid_lab/perception.py
### H. Code walkthrough
BGR-to-HSV conversion uses OpenCV's channel convention. inRange makes a binary green mask. connectedComponentsWithStats excludes background and selects the largest component above a minimum area. Returning None is an ordinary 'not observed' state. It must not be converted to a zero coordinate that looks like a valid target.

A skill library should expose small interfaces such as observe_object, supported_wave and return_to_fixture_home. Validate object identity, observation age, preconditions, amplitude and timeout before execution. The planner's output needs a strict schema and an allowlist. Unknown skills and out-of-range values are rejected. Speech recognition and natural-language planning can be added after the deterministic path passes.
### I. Expected result
The synthetic positive image yields a centroid and area; the empty image yields no object; no unearned depth estimate appears. No model training or external AI service is required.
### J. Validation
Test no-object, correct color, distractor color, too-small blob and multiple components. Evaluate real-image precision/recall under a declared lighting setup before enabling physical gestures. Stale detections must trigger observation refresh or no motion.
### K. Troubleshooting
Wrong colors often mean RGB/BGR confusion. Hue ranges depend on OpenCV's representation. A green wall can be a larger component than the target; object identity is not guaranteed by color. Unstable detections require temporal validation and uncertainty handling, not merely larger gestures.
### L. Practical exercise
Require three consistent detections over a short time window before selecting a skill. Add a disappearance test that cancels an unstarted action without inventing a new target.
### M. Connection to the physical Asimov 1
The documented monocular camera is useful for direction and appearance tasks. Metric reaching requires calibrated geometry and additional constraints. Use a small supported gesture as the first demonstration rather than depth-dependent approaching.
### N. Completion checklist
You can distinguish image-space detection from 3-D localization, handle missing observations, explain calibration requirements and constrain the planner to an allowlisted skill.
### O. Next lesson preview
Define the contracts and rollback required to move from simulated actions to a physical stack.
