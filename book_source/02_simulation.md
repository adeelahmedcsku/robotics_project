# Part II - The simulation laboratory
## Lesson 0 - Establish a reproducible environment
### A. Why this matters
You need to distinguish a model bug from a package mismatch. An environment you cannot recreate makes every later result weaker. Begin with a small, explicit dependency set and a commit-addressed robot model.
### B. Concepts explained simply
A physics engine numerically advances a state. The state includes positions and velocities. A model contains geometry, mass, joints, and equations that govern those changes. Rendering only draws a state. Therefore a successful headless test proves something useful even when no window can open, but does not prove the graphics stack works.
### C. Real-world relevance
A released robot controller needs traceable software, calibration and model versions. The same habit begins here with a Python environment and a git hash.
### D. Architecture
Operating system -> Python virtual environment -> MuJoCo binding -> pinned robot model -> tests and logs. ROS is added later so the first failure has fewer possible causes.
### E. Prerequisites
Ubuntu 24.04, internet access and adequate disk space. The commands below are for the reader's machine, not instructions to change an existing host blindly. Keep the supplied files at /data/Robotics_Project/humanoid_lab. If /data is not yours to write, choose a user-owned project directory and adapt paths consistently.
### F. Step-by-step implementation
Install standard development and desktop OpenGL support, create a venv, then install CPU PyTorch before the other dependencies so pip does not select a large CUDA stack. sudo changes OS packages; understand and review those commands on your own machine.
```bash
sudo apt update
sudo apt install python3-venv python3-dev git build-essential libgl1 libglfw3
cd /data/Robotics_Project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r humanoid_lab/requirements.txt
python -m pip check
python -m pip freeze > humanoid_lab/requirements-lock.txt
```
The supplied research checkout is already present. To recreate it on another machine where the directory does not exist:
```bash
cd /data/Robotics_Project
mkdir -p research
git clone https://github.com/menloresearch/asimov-1.git research/asimov-1
git -C research/asimov-1 checkout 96a6807c163e4e6cabdc124eefcc45b0ae2cb57a
git -C research/asimov-1 rev-parse HEAD
```
Set VS Code's interpreter to .venv/bin/python. Open the project root, run tests from a terminal first, and use a breakpoint before mj_step to inspect arrays. Do not combine a Conda interpreter, a ROS system interpreter and a pip venv accidentally.
### G. Complete code
File: /data/Robotics_Project/humanoid_lab/requirements.txt
!code humanoid_lab/requirements.txt
### H. Code walkthrough
Direct dependency pins make the intended API set explicit. The resolved lock records transitive versions as well. The upstream commit fixes asset paths and model semantics. A lock captured on x86 Linux is not necessarily portable to a different operating system or architecture.
### I. Expected result
mujoco imports and prints 3.4.0. pip check reports no dependency conflicts. The checkout hash matches the printed revision. No robot hardware is involved.
### J. Validation
```bash
python -c "import mujoco, numpy, torch; print(mujoco.__version__, numpy.__version__, torch.__version__)"
cd /data/Robotics_Project/humanoid_lab
python -m pytest -q
```
The test files are printed in the validation appendix. The prepared edition used Python 3.12.14; exact transitive versions are in requirements-lock.txt.
### K. Troubleshooting
If wheels are unavailable, verify Python 3.12 and CPU architecture before compiling packages. If OpenGL fails, run headless physics first; a DISPLAY or driver error is distinct from an XML compilation failure. On macOS, passive-viewer scripts require mjpython; this book's ROS setup remains Ubuntu-specific. [S10]
### L. Practical exercise
Create an environment manifest with OS, Python, model hash, package freeze and workstation inventory. Recreate a second venv from the freeze and compare imports.
### M. Connection to the physical Asimov 1
The release-manifest habit transfers directly. These Python package pins do not select motor firmware or electrical revisions.
### N. Completion checklist
You can explain the difference between a model, state and renderer; reproduce imports; identify your active Python executable; and locate the exact upstream model. Budget consumed by these software steps: EUR 0 excluding your existing computer and internet.
### O. Next lesson preview
Load the humanoid, inspect its joint coordinates and observe a supported motion.

## Lesson 1 - My first observable humanoid simulation
### A. Why this matters
Seeing the robot is the first milestone, but observation must include names, coordinate addresses, limits and time. A picture alone cannot establish that commands reach the intended joint.
### B. Concepts explained simply
A degree of freedom is an independent coordinate. A hinge joint rotates; a slide joint translates. A floating base adds three translations and a quaternion representation of orientation: its position array has seven entries while its velocity has six. Thus nq and nv can differ. Joint index, position-array address, velocity-array address and actuator index are different identifiers.
### C. Real-world relevance
A wrong mapping can send a knee target to a shoulder. Map by verified names, then check dimensions and ordering before every deployment.
### D. Architecture
Pinned MJCF -> teaching adapter -> MjModel -> MjData -> bounded controller -> mj_step -> viewer and CSV. The adapter fixes the pelvis, adds torque motors and retains the official mesh and inertial model.
### E. Prerequisites
Lesson 0, the upstream meshes, model.py and simulate.py below. Your first run uses a fixed pelvis fixture. It is intentionally incapable of demonstrating free standing.
### F. Step-by-step implementation
```bash
cd /data/Robotics_Project/humanoid_lab
python simulate.py --headless --seconds 10
python simulate.py --seconds 30
```
The first command tests physics without opening a window. The second opens a viewer with a useful camera distance. Rotate and zoom with the viewer controls and watch the left elbow. Head, torso and legs are visible even though this exercise moves one arm joint.
### G. Complete code
File: /data/Robotics_Project/humanoid_lab/model.py
!code humanoid_lab/model.py
File: /data/Robotics_Project/humanoid_lab/simulate.py
!code humanoid_lab/simulate.py
### H. Code walkthrough
load reads the verified XML rather than reconstructing a humanoid from guessed geometry. An absolute mesh directory makes the in-memory XML resolve assets correctly. Removing the floating joint attaches the pelvis to the world for this teaching fixture. The adapter replaces actuator definitions with gear-one torque motors, so ctrl is a simulated torque command in Nm. This is an educational actuator model, not an identified physical drive.

addresses obtains each actuator's joint and its qpos/qvel addresses. command checks the entire target vector, clips positions to model bounds, computes feedback plus ideal bias compensation, and clips torque to 25% of the XML actuator control envelope. The 25% value is a simulation teaching choice. mj_step integrates a 2 ms timestep; the CSV stores each step's feedback. The viewer's sync updates graphics; the sleep aims at readable wall-clock speed but provides no hard deadline.
### I. Expected result
The supported model has nq=25, nv=25 and nu=25. The terminal lists joint ranges, a small elbow motion appears in the viewer, and logs/joints.csv contains about 5,000 data rows for ten simulated seconds.
### J. Validation
Run test_asimov_contract and test_bounded_feedback_and_rejection from the appendix. Check finite state, model gravity, time increment and the printed actuator count. Manually verify that the left elbow moves while the fixed pelvis stays fixed. Share the test output before proceeding to Lesson 2 if following this as a coached course.
### K. Troubleshooting
A missing mesh often means the checkout is incomplete or paths belong to an older release. An absent actuator means the original model was opened without the adapter. A falling robot usually means you loaded the free-base model directly; that is not this fixture. If the window does not open, preserve the successful headless result and diagnose graphics separately.
### L. Practical exercise
Print joint type, qpos address and qvel address in a four-column inventory. Compare the supported and unsupported model dimensions without applying a motor command.
### M. Connection to the physical Asimov 1
Names and geometric inspection are reusable. Fixing the pelvis, ideal bias compensation, low-delay observations and gear-one torque motors are simulator conveniences that must be replaced or calibrated.
### N. Completion checklist
You can launch both modes, identify all 25 actuators, explain nq versus nv, find the CSV, and state why this demonstration proves no balance capability. No hardware expenditure is required.
### O. Next lesson preview
Measure tracking and introduce feedback gains, saturation and safe trajectory shapes.

## Lesson 2 - Joint control as a measurable feedback loop
### A. Why this matters
An angle command is a request. Physical motion depends on torque, inertia, gravity, friction, limits and time. Tracking error tells you whether the request is achieved.
### B. Concepts explained simply
Position q is an angle in radians, velocity dq is its rate in rad/s, and torque is a turning effort in Nm. One radian is about 57.3 degrees. A revolute joint changes orientation; a prismatic joint changes distance. The same controller structure can apply, but its units change.

Our controller uses tau = Kp*(q_target-q) - Kd*dq + bias(q,dq). Kp has units Nm/rad and Kd has units Nm*s/rad. With error 0.1 rad, Kp=35 and velocity 0.2 rad/s, Kd=4, the feedback portion is 3.5-0.8=2.7 Nm. Gravity and other bias terms are additional. A torque cap may reduce the result.

PID adds Ki times the accumulated error. Integral action can remove steady offsets but can wind up when the motor saturates. Begin with PD and an identified bias before adding an integral. If using integral control, freeze or back-calculate the integral during saturation and reset it on state transitions.
### C. Real-world relevance
Actual current, temperature, voltage and tracking-error measurements constrain usable gains. A high simulated gain does not authorize the same gain on an assembled limb.
### D. Architecture
Reference trajectory -> position/velocity limits -> PD and bias -> torque saturation -> actuator and joint -> encoder feedback. Log both requested and applied values; hiding clipping prevents diagnosis.
### E. Prerequisites
Lesson 1 and basic differentiation. Keep the fixed-pelvis fixture. The code for this lesson is the complete command function and simulator from Lesson 1; no unprinted source file is required.
### F. Step-by-step implementation
Run the ten-second trajectory, then render its telemetry. Change only one simulation parameter at a time. Try Kp=20 with Kd=4, then Kp=35 with Kd=6. Preserve separate CSVs before rerunning.
```bash
python simulate.py --headless --seconds 10
cp logs/joints.csv logs/joints_baseline.csv
python telemetry.py
```
For both arms, create a second index by joint name and use a mirrored bounded elbow excursion. For a knee, read its asymmetric sign and limits first. Test a 0.03 rad knee excursion in the supported fixture, never by assuming left and right signs match. A minimum-jerk transition uses s(t)=10*r^3-15*r^4+6*r^5, r clipped to [0,1], with q(t)=q_start+s*(q_end-q_start).
### G. Complete code
The executable files are model.py and simulate.py printed in Lesson 1, plus telemetry.py in Lesson 3. The additional numerical analysis is this complete terminal program:
```bash
python - <<'PY'
import numpy as np
x = np.genfromtxt('logs/joints.csv', delimiter=',', names=True)
e = x['target']-x['q']
print('RMSE rad:', np.sqrt(np.mean(e*e)))
print('Peak speed rad/s:', np.max(np.abs(x['dq'])))
print('Peak command Nm:', np.max(np.abs(x['command_Nm'])))
assert np.isfinite(e).all()
PY
```
### H. Code walkthrough
The sine target is 0.1 rad at 0.25 Hz around the XML reference pose, with model-limit clipping. The callback executes before integration so torque is computed from the current state. qfrc_bias is ideal model information; physical software would need a trusted dynamics model or another strategy. Position and torque clipping protect different quantities. Neither ensures collision avoidance.
### I. Expected result
The elbow follows a smooth curve with nonzero error. Torque may plateau where the simulation cap is active. The supported pelvis prevents whole-body falling but other joints can still oscillate or contact.
### J. Validation
Require finite state and applied commands within their configured caps. Proposed exercise target: elbow RMSE below 0.1 rad for the baseline run; record the measured value rather than assuming success. Inject NaN and wrong-length targets and verify rejection. Compare a smooth trajectory against a step command in simulation and inspect peak speed.
### K. Troubleshooting
Oscillation suggests excessive gain, inadequate damping or an integration issue. Persistent error with a flat-topped torque trace suggests saturation or load mismatch. A joint moving opposite to expectation suggests a sign/frame problem, not a need to negate every command globally.
### L. Practical exercise
Implement minimum-jerk motion as a new simulation-only trajectory, compute peak speed, and reject duration choices that exceed a chosen speed envelope.
### M. Connection to the physical Asimov 1
The feedback structure and logging transfer. Gains, friction, current-to-torque conversion, backlash, position zeros, thermal limits and ankle mapping require measured data. Simulator limits are not physical protection settings.
### N. Completion checklist
You can distinguish angle, speed and torque; reproduce tracking metrics; explain saturation and integral windup; and reject invalid commands. Continue only after a repeatable joint experiment.
### O. Next lesson preview
Read sensors with explicit units, frames and timestamps, and turn logs into a useful diagnostic view.

## Lesson 3 - Sensors, telemetry and state estimation
### A. Why this matters
A controller needs a trustworthy estimate of what the robot is doing now. Sensor messages are partial, noisy, delayed observations, not the entire physical state.
### B. Concepts explained simply
An encoder measures a shaft or output angle. A gyroscope measures angular velocity. An accelerometer measures specific force rather than simply the second derivative of world position; its stationary reading includes the support reaction against gravity. A camera measures light projected into pixels. Foot contact is an interaction between surfaces, not a boolean always available from the real hardware.

Latency is age, jitter is variation in age, and sample frequency is how often a measurement is produced. A 10 Hz telemetry feed cannot be silently substituted for a 500 Hz feedback loop. Store exposure/sample time, receive time, sequence, frame and units. Your IoT experience helps with delivery and observability, while actuator deadlines require a different timing contract.
### C. Real-world relevance
The physical robot's encoder offsets and IMU orientation affect every estimate. Gravity projected into the wrong frame can look like a sustained acceleration. Motor current is not a calibrated contact-force sensor.
### D. Architecture
!diagram telemetry
### E. Prerequisites
A successful joint log from Lesson 2, NumPy and Matplotlib. No physical IMU or camera is needed for this lesson.
### F. Step-by-step implementation
```bash
python telemetry.py
```
Open logs/telemetry.png. The terminal prints sensor names and dimensions from the actual model, then its subtree center of mass in world coordinates. MuJoCo gyro and accelerometer channels are modeled sensors; frame quaternion and linear velocity channels are privileged simulation signals unless corresponding estimators exist on hardware.
### G. Complete code
File: /data/Robotics_Project/humanoid_lab/telemetry.py
!code humanoid_lab/telemetry.py
### H. Code walkthrough
genfromtxt reads named CSV columns. Three aligned plots share time so you can relate error, velocity and saturation. Sensor addresses and dimensions select exact slices; copying samples avoids retaining mutable simulator views. subtree_com is mass-weighted model truth and is used later to check an estimator, not as a sensor you can plug into a real robot.

For a basic attitude estimator, integrate gyro orientation over small dt, then correct roll/pitch slowly toward an accelerometer-derived gravity direction only when linear acceleration is plausibly low. A complementary filter combines fast gyro changes with slow gravity reference. Accelerometers alone cannot determine yaw, and a six-axis IMU without external references drifts in yaw. A full estimator also uses kinematic contact constraints and rejects slipping-foot assumptions.
### I. Expected result
Readable angle, speed and torque-command plots. The initial supported fixture's sensor values can differ from expectations until you identify local axes and specific-force conventions. Investigate a discrepancy rather than relabeling the plotted units.
### J. Validation
Check CSV time is monotonic with approximately 0.002 s increments. Verify the encoder channel's unit by changing a joint by 0.1 rad. For an added noise model, use a fixed random seed and show both ground truth and noisy measurement. Verify quaternion ordering before comparing to ROS: MuJoCo uses w,x,y,z while ROS messages use x,y,z,w.
### K. Troubleshooting
A constant copied history often comes from storing array views. A rotated gravity vector may indicate world versus sensor-frame confusion. A slow plot may indicate every physics step is being rendered. Decimate visualization while preserving controller sampling.
### L. Practical exercise
Add synthetic gyro bias and Gaussian encoder noise to copied data only. Estimate a zero-rate gyro bias from a stationary segment, subtract it, and compare drift over a held-out segment.
### M. Connection to the physical Asimov 1
Telemetry schemas and diagnostic plots are reusable. Sensor timing, calibration, transport and noise must come from real recordings. Do not assume foot force sensing is present merely because the simulator reports contacts.
### N. Completion checklist
Every stream has known units and frame; every time variable has a clock; plotted values are copies; and ground truth is distinguished from measurements and estimates.
### O. Next lesson preview
Use geometry to predict and command limb endpoints.

## Lesson 4 - Frames, forward kinematics and inverse kinematics
### A. Why this matters
A hand target is usually expressed in space, while motors accept joint coordinates. Kinematics translates between those descriptions before dynamics determines the forces required.
### B. Concepts explained simply
A coordinate frame is an origin and three axes. A rotation changes the basis used to express a vector; a translation changes its origin. A 90-degree rotation about z maps (1,0,0) to (0,1,0). With a translation (1,2,0), that same point becomes (1,3,0). The order matters.

A homogeneous transform T has a 3x3 rotation R and translation p in its upper rows, and [0,0,0,1] below. It maps a homogeneous point using x_A=T_AB*x_B. Chaining transforms means multiplication in frame order. Inverting a rigid transform uses R transpose and -R transpose times p.

Euler angles are three ordered rotations and have singular configurations. A unit quaternion represents rotation with four numbers and a normalization constraint; q and -q represent the same orientation. Use matrices or quaternions for composition and reserve Euler angles for labeled displays.

For a two-link planar arm, x=l1*cos(q1)+l2*cos(q1+q2), y=l1*sin(q1)+l2*sin(q1+q2). With l1=.3 m, l2=.2 m and zero angles, the endpoint is (.5,0) m. At q1=pi/2 and q2=0 it is (0,.5) m. This is forward kinematics.

The Jacobian J is the local sensitivity of endpoint position to joint changes. For example, at zero angles the second row is [.5,.2], so a small elbow motion of .01 rad changes y by about .002 m. Fully stretched arms lose some directions of instantaneous motion: this is a singularity.
### C. Real-world relevance
A camera-to-base transform and encoder zero error can dominate reaching accuracy. Kinematics must use the same joint conventions as the assembled mechanism.
### D. Architecture
Target in world frame -> FK and Jacobian -> damped least-squares update -> joint constraints -> recompute FK -> residual. This lesson solves endpoint position only; it does not plan collision-free dynamic motion.
### E. Prerequisites
Lessons 1-3, NumPy matrix multiplication and the fixed-pelvis fixture. No new kinematics library is needed for the first experiment. Pinocchio becomes useful for larger model-based dynamics and optimization workflows once your conventions are tested.
### F. Step-by-step implementation
```bash
python kinematics.py
```
The target is a small displacement from the model's current left wrist-link origin. That choice makes reachability plausible and avoids inventing a hand geometry. To visualize, call solve before launching a MuJoCo passive viewer and inspect the resulting pose without dynamics. Kinematic pose inspection must not be mistaken for a physically executed trajectory.
### G. Complete code
File: /data/Robotics_Project/humanoid_lab/kinematics.py
!code humanoid_lab/kinematics.py
The following complete numerical example verifies the frame convention:
```bash
python - <<'PY'
import numpy as np
R = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 1.]])
p = np.array([1., 2., 0.])
point = R @ np.array([1., 0., 0.])+p
print(point)
assert np.allclose(point, [1., 3., 0.])
assert np.allclose(R.T @ R, np.eye(3))
PY
```
### H. Code walkthrough
mj_forward updates poses for the current coordinates. mj_jacBody calculates the wrist body-origin Jacobian. The solver selects only left-arm columns, so leg and base coordinates cannot satisfy the hand request accidentally. It uses dq=J.T*(J*J.T+lambda^2*I)^-1*error with lambda=.01, caps each iteration at .04 rad, then clips joint coordinates. Damping reduces ill-conditioning but does not make unreachable targets reachable.

The result reports a boolean and residual, so a failed solve is not passed downstream as a completed task. This implementation mutates the candidate data even on failure; keep a separate validated state and copy it back on a physical planning failure. Add orientation residuals, collision checks and a trajectory stage before any dynamic reaching deployment.
### I. Expected result
The planar example prints [.5,0]. The Asimov candidate reaches the nearby position within a 2 mm numerical tolerance on the fixed base. Numerical tolerance is not a claim of physical accuracy.
### J. Validation
Use test_planar_geometry_and_ik. Add a finite-difference Jacobian check at a nonsingular pose: perturb one angle by epsilon, recompute the wrist position, divide its displacement by epsilon, and compare to the corresponding Jacobian column. For a target several meters away, require failure reporting rather than apparent success.
### K. Troubleshooting
Wrong Jacobian columns create unexpected body motion. A stubborn residual near a limit may be reachability, not numerical failure. A body-origin target differs from a hand-tool tip; add a named site and include its offset before calling that target a grasp point.
### L. Practical exercise
Implement a transform inversion test and a small Cartesian path of five reachable waypoints, each solved from the previous successful pose. Stop on the first failure and preserve its residual.
### M. Connection to the physical Asimov 1
FK and frame tests are reusable after calibration. Wrist tool offsets, base attitude, link dimensions and the parallel ankle mapping require physical identification.
### N. Completion checklist
You can transform a point, explain rotation order and quaternion ordering, validate a Jacobian column, distinguish reachability from convergence, and reject failed IK.
### O. Next lesson preview
Place simulation and commands behind ROS 2 interfaces without changing the numerical controller.
