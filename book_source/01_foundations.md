# Part I - Engineering the project
## 1. Project vision and how to use this book
Build the robot in layers. First make a model observable. Then move a joint under feedback, recover known geometric relationships, measure behavior, and build software boundaries that reject bad commands. Only after those skills are repeatable should money and force enter the project. The physical outcome depends on verified parts, fabrication, and commissioning evidence.

The simulation target is the Menlo Research Asimov 1. The initial physical target is a guarded, supported module that can sense an object and execute a small, repeatable gesture. A complete walking humanoid is a later research objective with separate feasibility and safety gates. Success means you can explain a failure using measurements, reproduce a result from a pinned configuration, and decide when the evidence is insufficient to proceed.

This book is written for an experienced software engineer beginning robotics. You already understand interfaces and distributed systems. The new challenges are physical units, geometric frames, forces, contact, uncertainty, deadlines, and faults that can release stored energy. A software rollback cannot restore a stripped gearbox.

Each lesson follows A-O: purpose, concepts, physical relevance, architecture, prerequisites, implementation, complete code, walkthrough, expected result, validation, troubleshooting, exercise, hardware connection, completion checklist, and preview. Read one lesson, run its tests, and record the result before continuing. All original teaching code is printed in the book and also saved beside it under humanoid_lab/. External CAD and meshes remain in the upstream checkout because copying them into code listings would not make them reproducible or useful.

### What has and has not been demonstrated
The included lab is an educational simulation stack. Headless physics, model contracts, small IK, synthetic perception, command-gate tests, and the supported demonstration were exercised during preparation. Exact results appear in the validation appendix. ROS 2 package files are provided but require a Jazzy installation for integration testing. A short PPO run validates the training plumbing; it does not demonstrate learned standing or walking. No physical actuator was connected, no harness was load tested, and no completed robot is claimed.

Verified means supported by a named primary source or directly inspected asset. Engineering assumption means a proposed design value that must be tested. Unverified means a claim not independently established here. Missing means unavailable in the inspected public release, not proof that the manufacturer does not possess it. Every acceptance threshold proposed by this book is an engineering exercise, not a manufacturer rating.

### Your workstation and budget
You reported an Intel Core i7 and NVIDIA GeForce RTX, with an optional EUR 2,000-3,000 laptop purchase. The exact CPU generation, RAM, GPU, VRAM, operating system, and driver remain unknown. Start with CPU MuJoCo. Do not buy a laptop based on the RTX label alone: mobile GPUs differ in memory, power limits, cooling, and sustained throughput. Treat the possible laptop allowance separately from the EUR 6,000 robot budget until you decide otherwise.

Run the following inventory commands on Linux; they read information without changing drivers. On Windows, record the same facts from System Information and nvidia-smi. Save output in your experiment log, including OS version and free SSD space.
```bash
lscpu
free -h
cat /etc/os-release
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
df -h .
```
For the early single-model lessons, 16 GB RAM and a modern CPU are a practical planning target, not a measured minimum. Rendering needs a functioning graphics stack; physics can run headlessly. Measure simulated seconds per wall second before planning a large training job. A new laptop is unnecessary for learning coordinates, controllers, ROS messages, or small PPO tasks.

## 2. Feasibility assessment and official-source audit
The official README describes a roughly 1.2 m, 35 kg machine with 25 powered joints and advertises a USD 20,000 unassembled kit. That public asking price is not an EU landed quotation. It is enough to reject the claim that buying the published kit fits EUR 6,000. It does not determine the self-source cost. [S1]

The checked-out main revision is 96a6807c163e4e6cabdc124eefcc45b0ae2cb57a. The GitHub tree was inspected directly on 25 October 2026. Some search-indexed pages described an older 23-joint simulation and different paths. The actual pinned checkout contains 25-DOF and 27-DOF model variants. Use the 25-DOF version throughout this book. Its upstream simulation README names MuJoCo 3.4.0 as validated; the lab uses that version. [S2]

| Subject | Evidence in this edition | Status and consequence |
|---|---|---|
| Mechanical source | mechanical/ASV1 contains 168 STEP files and 25 PDFs in the inspected tree | Verified file inventory; not assembly quantities |
| Electrical source | electrical/ contains board sources and wiring CSVs | Verified design assets; release reconciliation required |
| Simulation | sim-model/asimov_1_25dof/xml/asimov_1_25dof.xml and matching URDF | Verified files; loaded in the lab |
| 27-DOF variant | Separate model with gripper structure | Verified variant; excluded from this curriculum |
| Actuation in 25-DOF MJCF | No actuator definitions in inspected XML | Adapter explicitly adds teaching torque motors |
| Firmware and SDK | Public manual describes operation while SDK is in development | Availability must be confirmed for purchased release |
| ROS 2 compatibility | No tested upstream ROS 2 package established in this checkout | Book supplies an educational bridge |
| Complete procurement BOM | Manual requests email for BOM; referenced fabrication manifest absent here | No complete priced BOM established |
| Structural hardware revision | Commit identifies assets, not an approved physical serial-number release | Match fabrication, electronics and firmware before ordering |
| Licenses | HARDWARE-LICENSE.txt and SOFTWARE-LICENSE.txt | Preserve notices and review applicable redistribution terms |

The repository's hardware/software licenses are CERN-OHL-S-2.0 and GPL-2.0 as published. Original teaching code is separate from those assets; do not assume packaging it together changes upstream obligations. This book provides engineering guidance, not a legal interpretation of redistribution terms. [S1]

### Joint topology and revision mismatches
The documented powered layout is two six-axis legs, two five-axis arms, waist yaw, and two neck axes. Shoulder pitch/roll/yaw, elbow, and wrist yaw make five per arm. Hip pitch/roll/yaw, knee, ankle pitch, and ankle roll make six per leg. The hardware ankle is a parallel linkage: two motor coordinates map to pitch and roll. Simulator joints are not automatically motor shaft coordinates. [S3]

A concrete mismatch matters more than the label 'digital twin': the inspected XML gives the left elbow an upper range near 2.09443 rad, whereas the mechanical-tour table gives a different bound. Tutorial code reads its bounds from its pinned XML. Physical bounds must come from the accepted hardware release and measured mechanism. Never copy either table blindly into the motor driver.

The mechanical-tour page itself flags some illustrations as outdated. Documentation also describes a 23-DOF locomotion configuration with locked neck axes. These statements can coexist with a 25-axis physical robot. Model size, controlled action count, and physical motor count are different quantities. Record all three in a deployment manifest. [S3, S4]

### Development status and buildability
The public manual describes firmware modes and a supplied locomotion policy, while the repository roadmap lists software work still pending. Treat these as release-specific claims until the matching image, API schema, policy, checksums, calibration workflow, and support procedure are obtained. A manual's claim of zero-shot transfer is not evidence for your assembled unit. [S1, S4]

The platform is useful for simulation and inspecting real design tradeoffs. A full self-source build is not a beginner turnkey exercise: it combines machined parts, process-specific polymers, high-energy power, parallel ankle calibration, custom boards, and release-dependent software. Advance with one guarded module and engineering review of the support and power design.

The branch listing included main and several electrical, mechanical, gripper and simulation branches at inspection. Feature branches indicate work streams, not compatibility guarantees. Do not mix a board from one branch, an ankle from another, and firmware from a third without a documented integration decision.

## 3. Complete system architecture
Think of the system as a company with explicit authority. The planner proposes a job. A skills library translates it into a known procedure. A supervisor authorizes bounded execution. A controller makes small repeated corrections. Drivers deliver power and report measurements. No higher layer gets to bypass the lower layer's limits.

!diagram architecture

| Subsystem | Analogy | Engineering function and interface |
|---|---|---|
| Structure and transmissions | Skeleton and tendons | Carry loads and define axis geometry, stiffness, backlash and travel |
| Actuators and drivers | Muscles and local reflexes | Produce limited torque; report encoder, current and thermal state |
| Encoders, IMU and camera | Senses | Measure different quantities in named frames with timestamps |
| Power and protection | Energy supply and circuit breakers | Distribute energy, limit faults and isolate hazardous motion |
| Embedded controller | Local reflex coordinator | Enforce deadlines, watchdogs and release-specific bus rules |
| Motion controller | Skilled operator | Track joint or whole-body targets within feasible constraints |
| State estimator | Shared situational picture | Fuse delayed, noisy observations with a model |
| ROS 2 | Typed internal messaging | Connect modular components; transport alone guarantees no control deadline |
| Simulator | Rehearsal space | Approximate dynamics, contacts, sensors and failure cases |
| Policy inference | Learned reflex | Map a defined observation to a bounded action at a defined rate |
| Perception and task planner | Eyes and foreman | Locate objects and select validated skills |
| Safety supervisor | Independent authority | Veto unsafe transitions, detect stale data and trigger a tested stop |
| Logging and deployment | Flight recorder and release management | Preserve evidence, hashes, configurations and rollback artifacts |

The official electrical design divides media/networking and motion-control responsibilities across two compute stacks. Its documented CAN-interface specification and physical branch mapping are not fully reconciled publicly; the manual explicitly calls that out. Do not infer which baud rate belongs to a limb from the number of connectors. [S5]

### Control, policy and high-level AI
Scripted control follows a prescribed time trajectory. Classical feedback uses error and a model, for example a proportional-derivative joint controller. A learned policy selects actions based on training experience. High-level AI selects a task or skill. Each can exist without the others. A wave following a sine function is not reinforcement learning, and a language interface does not make a motor controller intelligent.

Use simulation time for physical integration and monotonic wall time for watchdog deadlines. Keep these clocks explicit in messages. A playback run may execute ten simulated seconds in one wall second; a physical watchdog must still expire in actual elapsed time. A camera frame's exposure time is not its arrival time.

!diagram sequence

The physical power-isolation path must remain effective if ROS, the policy process, the planner, or the network hangs. Cutting motor power may cause a heavy robot to collapse; the support rig is part of the stop strategy. Software DAMP mode is not an emergency stop. The official software guide makes this distinction explicit. [S4]

## 4. Dependency-aware roadmap
Effort estimates below are planning ranges for an experienced software engineer, in focused hours. They include learning and debugging but exclude supplier lead times, fabrication queues, and recovery from hardware damage. Hardware costs remain unquoted unless specifically identified.

| Phase | Deliverable and dependency | Effort | Acceptance gate |
|---|---|---|---|
| 0 | Reproducible environment; none | 8-16 h | Import versions, save lock and hardware inventory |
| 1 | Asimov view and model inspection; 0 | 6-12 h | Correct joint count and finite state |
| 2 | Bounded joint trajectory; 1 | 12-24 h | Limits, error and saturation measured |
| 3 | Telemetry and sensor semantics; 2 | 12-24 h | Units, frames and time recorded |
| 4 | Forward/inverse kinematics; 2-3 | 20-40 h | Reachable target residual under 2 mm |
| 5 | ROS 2 workspace; 2-4 | 20-40 h | Two nodes communicate and stale command rejected |
| 6 | Balance experiments; 3-5 | 24-60 h | Repeatable unsupported evaluation and honest fall report |
| 7 | PPO task and export; 2-6 | 30-80 h | Held-out evaluation beats chosen baseline |
| 8 | Locomotion research; 6-7 | 80-200+ h | Tracking, falls, energy and slip evaluated |
| 9 | Perception and bounded skills; 4-5 | 20-50 h | Detect/no-detect cases and unknown-depth behavior pass |
| 10 | Sim-to-real contracts; 3-9 | 30-80 h | Observation/action/timing replay and rollback pass |
| 11 | Procurement and fabrication; 10 plus quotes | 20-60 h | Complete release-matched landed BOM within budget |
| 12 | Single-actuator electrical bench; 11 | 30-80 h | Isolation, watchdog, feedback and limits measured |
| 13 | Incremental assembly; 12 | 40-120 h | One module at a time passes inspection |
| 14 | Supported commissioning; 13 | 40-100+ h | Signed records and repeatable stop tests |
| 15 | Physical skill deployment; 10 and 14 | 40-120+ h | Supported behavior repeatable without envelope violations |
| 16 | Integrated research demonstration; 9 and 15 | 20-60 h | Object-dependent skill, logs, faults and rollback demonstrated |

Keep these dependencies visible. Procurement discovery can run while learning simulation, but purchasing high-value actuators before a compatible release is identified is premature. Locomotion is a research milestone, not a guaranteed outcome at a fixed training step count. Hardware phases may stop at a modular platform while simulation continues to full-body locomotion.

Use a milestone record with fields: gate, date, repository hash, environment lock hash, model hash, configuration, seed, test command, observed metric, threshold, outcome, reviewer, and artifact path. A failed result is useful evidence. Do not overwrite it with a later success using the same filename.

## 5. Recommended stack and reproducibility policy
The baseline is Ubuntu 24.04 LTS, Python 3.12, MuJoCo 3.4.0, and ROS 2 Jazzy. Jazzy remains supported through May 2029 according to the ROS release table. Lyrical is newer and listed through May 2031; it is not required for this curriculum. We choose Jazzy for its established Ubuntu 24.04 package set and Gazebo Harmonic pairing. Iron is already end-of-life. Recheck the release table when updating this book's environment. [S6, S7, S8]

| Tool | Best role here | Hardware and integration tradeoff |
|---|---|---|
| MuJoCo 3.4.0 | First simulation, dynamics, IK, CPU RL | Fast headless CPU physics; Python bridge needed for ROS; native MJCF |
| Gazebo Harmonic | Optional ROS-centric sensor and systems work | ROS Jazzy pairing documented; URDF/SDF conversion and plugin work; GPU rendering varies |
| Isaac Sim | Optional rich rendering and RTX sensor workflows | Significant RTX/VRAM and driver requirements; asset import must be revalidated |
| Isaac Lab | Optional batched training framework | A framework built around compatible simulation backends, not a drop-in MJCF viewer |

No simulator is 'the most realistic' for every contact, actuator, camera, or deadline. Validate the phenomenon that matters: a soft toe, backlash, thermal derating, or latency may dominate your transfer error more than the solver brand. URDF captures a tree of links and joints; MJCF adds MuJoCo-specific world, contact, sensor and actuator settings. Conversion can lose semantics and requires regression tests.

Current Isaac Sim requirements list 32 GB RAM and 16 GB VRAM at the minimum tier, with an RTX 4080-class GPU and release-specific drivers. These are product requirements, not a promise that a similarly named laptop GPU performs like its desktop counterpart. Use the Compatibility Checker for the chosen release. Keep optional Isaac environments isolated from this book's CPU virtual environment; select an exact Isaac Lab/Sim/Python pair from their cross-product compatibility page after the hardware inventory is known. No unverified pair is installed by the tutorial. [S9]

Host installation gives direct device access and straightforward desktop rendering. A virtual environment isolates Python packages but shares the host driver and kernel. A container adds userspace reproducibility but still depends on host graphics, USB/CAN permissions and kernel timing. A virtual machine isolates the OS but may complicate graphics and device passthrough. Use native Ubuntu for the initial lab when available; a headless container is useful for CI after the baseline works.

The pinned Python packages are a tested teaching baseline rather than claims about the newest versions: MuJoCo 3.4.0, NumPy 2.2.6, Matplotlib 3.10.3, pytest 8.4.1, Gymnasium 1.2.1, Stable-Baselines3 2.7.0, OpenCV 4.12.0.88, and CPU PyTorch 2.8.0. A full resolved freeze is supplied beside the code. Save apt package versions separately because pip cannot record ROS Debian packages.

## 6. Repository layout and ownership
All tutorial commands assume the following location. If you use another location, update the shell root and HUMANOID_LAB_ROOT together. The actual book and code are saved at these paths.
```text
/data/Robotics_Project/
  AI_Humanoid_Robotics_Engineering_Book.pdf
  book_source/                 editable teaching manuscript
  research/asimov-1/           pinned upstream CAD and models
  humanoid_lab/
    requirements.txt          direct teaching dependencies
    requirements-lock.txt     resolved environment snapshot
    model.py                  simulator adapter and bounded PD
    simulate.py               joint inspection and viewer
    telemetry.py              recorded plots and sensor inventory
    kinematics.py             planar FK and Asimov position IK
    balance.py                static geometry and passive fall baseline
    learning.py               reach/stand/walk Gymnasium tasks and PPO
    perception.py             image-space color detector
    safety.py                 offline command-gate exercise
    demo.py                   supported perception-to-gesture demo
    audit.py                  procurement and commissioning records
    config/                   BOM and commissioning records
    tests/                    meaningful numerical and fault tests
    ros2_ws/src/humanoid_bridge/  ROS node package and launch file
    logs/                     experiment outputs; do not version large runs
```
The simulator adapter deliberately does not import a physical CAN library. That is an architectural boundary: the tests cannot accidentally send commands to a real actuator. Create a separate hardware transport only after the release-specific protocol is verified, with its own reviewed configuration and test fixtures.
