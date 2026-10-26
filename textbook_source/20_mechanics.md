# Part VII - Mechanics, kinematics and contact

A geometric model becomes an engineering model only when its mass, inertia, load paths and contact assumptions are explicit. These laboratories move from mass aggregation through rotation and transmission effects to inverse kinematics and support feasibility. They use simple idealized bodies to isolate one phenomenon at a time. The complete humanoid model combines these phenomena; its apparent complexity is a reason to validate each component relationship first, not a reason to skip the equations.

## Laboratory 11 - Link masses, payload shifts and center of mass

### A. The engineering question

Center of mass is an average weighted by mass, not by link count.

### B. Concepts and mathematical model

A light component placed far from the body can shift the combined center substantially. Adding a payload also changes inertia and torque requirements, but COM alone describes only the first moment of mass. This experiment adds a point payload to a simple three-link assembly and calculates both the new COM and the gravity moment about an origin. All coordinates must share one frame; averaging body-local positions would produce a physically meaningless answer.

c = sum(m_i*r_i)/sum(m_i); M_gravity = sum(r_i cross m_i*g).

### C. Real-world meaning and limits

Weigh actual assemblies and measure their reference positions; CAD mass depends on assigned density and included components.

### D. Architecture and data flow

Configuration (payload_mass, payload_x) -> numerical model -> total_mass_kg, com_x_m, com_z_m -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

payload_mass is kilograms; payload_x is meters in the common origin frame. The other three masses are fixed teaching links.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| payload_mass | 1 | kilograms |
| payload_x | 0.3 | meters |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/11_center_mass.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only payload_mass changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/11_center_mass.py --case 0

.venv-book/bin/python expanded_lab/modules/11_center_mass.py --case 3

.venv-book/bin/python expanded_lab/run.py center_mass --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/11_center_mass.py

### H. Walkthrough and design decisions

Broadcast masses over vector positions, form gravity forces, and compare distributed moments with the equivalent resultant at COM. This verifies the coordinate and weighting conventions together.

### I. Expected behavior and six worked cases

The controlled variable is payload_mass. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/11_center_mass.png

Figure L11. total mass kg as payload_mass changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | payload_mass | total mass kg |
|---|---|---|
| 0 | 0 | 7 |
| 1 | 0.25 | 7.25 |
| 2 | 0.5 | 7.5 |
| 3 | 1 | 8 |
| 4 | 2 | 9 |
| 5 | 4 | 11 |

#### Worked case 0: payload_mass = 0

This case keeps the nominal configuration except for payload_mass=0. The full input is {"payload_mass": 0.0, "payload_x": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| total mass kg | 7 |
| com x m | 0.01428571 |
| com z m | 0.34285714 |
| gravity pitch moment Nm | 0.981 |
| weight N | 68.67 |

1. Total mass is 4+2+1+0 = 7.000000 kg.

2. The payload lies at x=0.3 m in the shared frame.

3. Sum mass times position, then divide by total: COM=[0.014285714285714287, 0.0, 0.3428571428571429] m.

4. Sum each gravity moment to obtain pitch moment 0.981000 Nm.

5. Applying total weight at the COM reproduces the same moment, providing an independent check.

#### Worked case 1: payload_mass = 0.25

This case keeps the nominal configuration except for payload_mass=0.25. The full input is {"payload_mass": 0.25, "payload_x": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| total mass kg | 7.25 |
| com x m | 0.02413793 |
| com z m | 0.34827586 |
| gravity pitch moment Nm | 1.71675 |
| weight N | 71.1225 |

1. Total mass is 4+2+1+0.25 = 7.250000 kg.

2. The payload lies at x=0.3 m in the shared frame.

3. Sum mass times position, then divide by total: COM=[0.02413793103448276, 0.0, 0.34827586206896555] m.

4. Sum each gravity moment to obtain pitch moment 1.716750 Nm.

5. Applying total weight at the COM reproduces the same moment, providing an independent check.

The horizontal COM displacement from the origin is 0.024138 m; compare it with a measured support margin.

#### Worked case 2: payload_mass = 0.5

This case keeps the nominal configuration except for payload_mass=0.5. The full input is {"payload_mass": 0.5, "payload_x": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| total mass kg | 7.5 |
| com x m | 0.03333333 |
| com z m | 0.35333333 |
| gravity pitch moment Nm | 2.4525 |
| weight N | 73.575 |

1. Total mass is 4+2+1+0.5 = 7.500000 kg.

2. The payload lies at x=0.3 m in the shared frame.

3. Sum mass times position, then divide by total: COM=[0.03333333333333333, 0.0, 0.3533333333333334] m.

4. Sum each gravity moment to obtain pitch moment 2.452500 Nm.

5. Applying total weight at the COM reproduces the same moment, providing an independent check.

The horizontal COM displacement from the origin is 0.033333 m; compare it with a measured support margin.

#### Worked case 3: payload_mass = 1

This case keeps the nominal configuration except for payload_mass=1. The full input is {"payload_mass": 1.0, "payload_x": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| total mass kg | 8 |
| com x m | 0.05 |
| com z m | 0.3625 |
| gravity pitch moment Nm | 3.924 |
| weight N | 78.48 |

1. Total mass is 4+2+1+1 = 8.000000 kg.

2. The payload lies at x=0.3 m in the shared frame.

3. Sum mass times position, then divide by total: COM=[0.05, 0.0, 0.36250000000000004] m.

4. Sum each gravity moment to obtain pitch moment 3.924000 Nm.

5. Applying total weight at the COM reproduces the same moment, providing an independent check.

The horizontal COM displacement from the origin is 0.050000 m; compare it with a measured support margin.

#### Worked case 4: payload_mass = 2

This case keeps the nominal configuration except for payload_mass=2. The full input is {"payload_mass": 2.0, "payload_x": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| total mass kg | 9 |
| com x m | 0.07777778 |
| com z m | 0.37777778 |
| gravity pitch moment Nm | 6.867 |
| weight N | 88.29 |

1. Total mass is 4+2+1+2 = 9.000000 kg.

2. The payload lies at x=0.3 m in the shared frame.

3. Sum mass times position, then divide by total: COM=[0.07777777777777778, 0.0, 0.3777777777777778] m.

4. Sum each gravity moment to obtain pitch moment 6.867000 Nm.

5. Applying total weight at the COM reproduces the same moment, providing an independent check.

The horizontal COM displacement from the origin is 0.077778 m; compare it with a measured support margin.

#### Worked case 5: payload_mass = 4

This case keeps the nominal configuration except for payload_mass=4. The full input is {"payload_mass": 4.0, "payload_x": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| total mass kg | 11 |
| com x m | 0.11818182 |
| com z m | 0.4 |
| gravity pitch moment Nm | 12.753 |
| weight N | 107.91 |

1. Total mass is 4+2+1+4 = 11.000000 kg.

2. The payload lies at x=0.3 m in the shared frame.

3. Sum mass times position, then divide by total: COM=[0.11818181818181818, 0.0, 0.4] m.

4. Sum each gravity moment to obtain pitch moment 12.753000 Nm.

5. Applying total weight at the COM reproduces the same moment, providing an independent check.

The horizontal COM displacement from the origin is 0.118182 m; compare it with a measured support margin.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

This static point-mass model does not represent distributed inertia or dynamic contact stability.

The horizontal COM displacement from the origin is 0.014286 m; compare it with a measured support margin.

### K. Failure modes and troubleshooting

Averaging local link coordinates; omitting batteries or cables from mass accounting; treating COM margin as a dynamic balance proof.

### L. Practical exercises and extension tasks

1. Move the payload laterally and recompute roll moment.

2. Estimate COM uncertainty for a 10 mm payload-position error.

3. Add a fifth link and verify the equivalent resultant identity.

### M. Connection to the Asimov research platform

Weigh actual assemblies and measure their reference positions; CAD mass depends on assigned density and included components.

### N. Completion record

Record your chosen case, predicted trend, measured total_mass_kg, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 12, Inertia tensors and the parallel-axis theorem. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 12 - Inertia tensors and the parallel-axis theorem

### A. The engineering question

Mass describes resistance to translation.

### B. Concepts and mathematical model

Inertia describes resistance to angular acceleration about a chosen axis and origin. Two assemblies with equal mass can require very different torque if their mass is distributed differently. The inertia tensor must be expressed in a named frame; moving the reference origin adds a parallel-axis term. Physical principal inertias are nonnegative and obey constraints that arbitrary matrix entries may violate. Here a uniform box is shifted away from an axis to make the geometric effect visible.

I_box = m/12*diag(b^2+c^2,a^2+c^2,a^2+b^2); I_origin = I_com + m*((r dot r)*I-r*r.T).

### C. Real-world meaning and limits

Validate CAD inertia units, density assignments and reference frames before policy training or gravity compensation.

### D. Architecture and data flow

Configuration (mass, offset, acceleration) -> numerical model -> Izz_kg_m2, minimum_principal_kg_m2, torque_z_Nm -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

mass is kilograms; offset is the x displacement of COM from the target origin in meters; acceleration is rad/s^2.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| mass | 2 | kilograms |
| offset | 0.1 | meters |
| acceleration | 3 | SI acceleration in the chapter equation |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/12_inertia.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only offset changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/12_inertia.py --case 0

.venv-book/bin/python expanded_lab/modules/12_inertia.py --case 3

.venv-book/bin/python expanded_lab/run.py inertia --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/12_inertia.py

### H. Walkthrough and design decisions

The outer product creates both diagonal and off-diagonal terms. Eigenvalues check positive principal inertias; the torque calculation shows how placement affects actuation demand.

### I. Expected behavior and six worked cases

The controlled variable is offset. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/12_inertia.png

Figure L12. Izz kg m2 as offset changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | offset | Izz kg m2 |
|---|---|---|
| 0 | 0 | 0.00913333 |
| 1 | 0.02 | 0.00993333 |
| 2 | 0.05 | 0.01413333 |
| 3 | 0.1 | 0.02913333 |
| 4 | 0.2 | 0.08913333 |
| 5 | 0.3 | 0.18913333 |

#### Worked case 0: offset = 0

This case keeps the nominal configuration except for offset=0. The full input is {"acceleration": 3.0, "mass": 2.0, "offset": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| Izz kg m2 | 0.00913333 |
| minimum principal kg m2 | 0.00353333 |
| torque z Nm | 0.0274 |
| offset contribution kg m2 | 0.0008 |

1. A uniform 2 kg box has COM Izz=0.00833333 kg*m^2.

2. Shift the reference by [0.0, 0.02, 0.0] m.

3. The parallel-axis contribution to Izz is 0.00080000 kg*m^2.

4. Total Izz is 0.00913333; requested z acceleration is 3 rad/s^2.

5. Ignoring other dynamics, required z torque is 0.02740000 Nm.

#### Worked case 1: offset = 0.02

This case keeps the nominal configuration except for offset=0.02. The full input is {"acceleration": 3.0, "mass": 2.0, "offset": 0.02}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| Izz kg m2 | 0.00993333 |
| minimum principal kg m2 | 0.00340845 |
| torque z Nm | 0.0298 |
| offset contribution kg m2 | 0.0016 |

1. A uniform 2 kg box has COM Izz=0.00833333 kg*m^2.

2. Shift the reference by [0.02, 0.02, 0.0] m.

3. The parallel-axis contribution to Izz is 0.00160000 kg*m^2.

4. Total Izz is 0.00993333; requested z acceleration is 3 rad/s^2.

5. Ignoring other dynamics, required z torque is 0.02980000 Nm.

#### Worked case 2: offset = 0.05

This case keeps the nominal configuration except for offset=0.05. The full input is {"acceleration": 3.0, "mass": 2.0, "offset": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| Izz kg m2 | 0.01413333 |
| minimum principal kg m2 | 0.00311736 |
| torque z Nm | 0.0424 |
| offset contribution kg m2 | 0.0058 |

1. A uniform 2 kg box has COM Izz=0.00833333 kg*m^2.

2. Shift the reference by [0.05, 0.02, 0.0] m.

3. The parallel-axis contribution to Izz is 0.00580000 kg*m^2.

4. Total Izz is 0.01413333; requested z acceleration is 3 rad/s^2.

5. Ignoring other dynamics, required z torque is 0.04240000 Nm.

#### Worked case 3: offset = 0.1

This case keeps the nominal configuration except for offset=0.1. The full input is {"acceleration": 3.0, "mass": 2.0, "offset": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| Izz kg m2 | 0.02913333 |
| minimum principal kg m2 | 0.00288932 |
| torque z Nm | 0.0874 |
| offset contribution kg m2 | 0.0208 |

1. A uniform 2 kg box has COM Izz=0.00833333 kg*m^2.

2. Shift the reference by [0.1, 0.02, 0.0] m.

3. The parallel-axis contribution to Izz is 0.02080000 kg*m^2.

4. Total Izz is 0.02913333; requested z acceleration is 3 rad/s^2.

5. Ignoring other dynamics, required z torque is 0.08740000 Nm.

#### Worked case 4: offset = 0.2

This case keeps the nominal configuration except for offset=0.2. The full input is {"acceleration": 3.0, "mass": 2.0, "offset": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| Izz kg m2 | 0.08913333 |
| minimum principal kg m2 | 0.00277998 |
| torque z Nm | 0.2674 |
| offset contribution kg m2 | 0.0808 |

1. A uniform 2 kg box has COM Izz=0.00833333 kg*m^2.

2. Shift the reference by [0.2, 0.02, 0.0] m.

3. The parallel-axis contribution to Izz is 0.08080000 kg*m^2.

4. Total Izz is 0.08913333; requested z acceleration is 3 rad/s^2.

5. Ignoring other dynamics, required z torque is 0.26740000 Nm.

#### Worked case 5: offset = 0.3

This case keeps the nominal configuration except for offset=0.3. The full input is {"acceleration": 3.0, "mass": 2.0, "offset": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| Izz kg m2 | 0.18913333 |
| minimum principal kg m2 | 0.00275486 |
| torque z Nm | 0.5674 |
| offset contribution kg m2 | 0.1808 |

1. A uniform 2 kg box has COM Izz=0.00833333 kg*m^2.

2. Shift the reference by [0.3, 0.02, 0.0] m.

3. The parallel-axis contribution to Izz is 0.18080000 kg*m^2.

4. Total Izz is 0.18913333; requested z acceleration is 3 rad/s^2.

5. Ignoring other dynamics, required z torque is 0.56740000 Nm.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

This acceleration-only torque excludes gravity, Coriolis terms, friction and transmission effects.

An inertia tensor attached to the wrong origin can make a controller consistently wrong even when total mass is correct.

### K. Failure modes and troubleshooting

Using grams as kilograms; importing inertia in mm^2 units; moving inertia without transforming its frame; diagonalizing away real coupling.

### L. Practical exercises and extension tasks

1. Rotate the tensor by R*I*R.T and compare kinetic energy in both frames.

2. Double every box dimension and derive the inertia scaling at fixed mass.

3. Compare a point mass with a distributed box.

### M. Connection to the Asimov research platform

Validate CAD inertia units, density assignments and reference frames before policy training or gravity compensation.

### N. Completion record

Record your chosen case, predicted trend, measured Izz_kg_m2, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 13, Angular momentum, kinetic energy and off-axis motion. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 13 - Angular momentum, kinetic energy and off-axis motion

### A. The engineering question

For rotation about a fixed principal axis, angular momentum and angular velocity are parallel.

### B. Concepts and mathematical model

For a general rigid body they need not be. The inertia tensor maps angular velocity to angular momentum, and rotational kinetic energy is a quadratic form. This distinction matters when arms or torso motions redistribute whole-body angular momentum. Conservation arguments require the external moment assumptions to be explicit; contact forces and a support fixture can inject moments.

L=I*omega; E_rot=0.5*omega.T*I*omega; tau=I*alpha+omega cross (I*omega).

### C. Real-world meaning and limits

Whole-body controllers must account for angular momentum and contact wrench feasibility; a torso orientation target alone is incomplete.

### D. Architecture and data flow

Configuration (speed) -> numerical model -> kinetic_energy_J, momentum_norm_kg_m2_s, misalignment_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

speed is the x angular-velocity component in rad/s; the y and z components and inertia tensor are fixed.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| speed | 1 | angular speed in the chapter equation |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/13_angular_momentum.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only speed changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/13_angular_momentum.py --case 0

.venv-book/bin/python expanded_lab/modules/13_angular_momentum.py --case 3

.venv-book/bin/python expanded_lab/run.py angular_momentum --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/13_angular_momentum.py

### H. Walkthrough and design decisions

Compute momentum before energy and gyroscopic torque so the directional coupling is visible. A spherical-inertia extension should eliminate the gyroscopic term for any omega.

### I. Expected behavior and six worked cases

The controlled variable is speed. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/13_angular_momentum.png

Figure L13. kinetic energy J as speed changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | speed | kinetic energy J |
|---|---|---|
| 0 | 0.1 | 0.0338 |
| 1 | 0.3 | 0.037 |
| 2 | 0.7 | 0.053 |
| 3 | 1 | 0.0734 |
| 4 | 2 | 0.1934 |
| 5 | 4 | 0.6734 |

#### Worked case 0: speed = 0.1

This case keeps the nominal configuration except for speed=0.1. The full input is {"speed": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| kinetic energy J | 0.0338 |
| momentum norm kg m2 s | 0.09338094 |
| misalignment rad | 0.17269333 |
| gyroscopic torque Nm | 0.01179152 |
| required torque Nm | 0.03552802 |

1. Angular velocity is [0.1, 0.7, 0.2] rad/s.

2. Multiply by diagonal inertia to obtain L=[0.008, 0.08399999999999999, 0.04000000000000001] kg*m^2/s.

3. The quadratic energy is 0.033800 J.

4. Compute omega cross L: [0.011200000000000005, -0.002400000000000001, 0.0027999999999999995] Nm.

5. Include the acceleration term to obtain torque [0.011200000000000005, 0.0336, 0.0027999999999999995] Nm.

#### Worked case 1: speed = 0.3

This case keeps the nominal configuration except for speed=0.3. The full input is {"speed": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| kinetic energy J | 0.037 |
| momentum norm kg m2 s | 0.0960833 |
| misalignment rad | 0.20961727 |
| gyroscopic torque Nm | 0.01574293 |
| required torque Nm | 0.03202249 |

1. Angular velocity is [0.3, 0.7, 0.2] rad/s.

2. Multiply by diagonal inertia to obtain L=[0.024, 0.08399999999999999, 0.04000000000000001] kg*m^2/s.

3. The quadratic energy is 0.037000 J.

4. Compute omega cross L: [0.011200000000000005, -0.0072000000000000015, 0.008399999999999998] Nm.

5. Include the acceleration term to obtain torque [0.011200000000000005, 0.028799999999999996, 0.008399999999999998] Nm.

L and omega differ in direction by 0.209617 rad in this non-spherical body.

#### Worked case 2: speed = 0.7

This case keeps the nominal configuration except for speed=0.7. The full input is {"speed": 0.7}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| kinetic energy J | 0.053 |
| momentum norm kg m2 s | 0.10859098 |
| misalignment rad | 0.25948336 |
| gyroscopic torque Nm | 0.02813965 |
| required torque Nm | 0.02963511 |

1. Angular velocity is [0.7, 0.7, 0.2] rad/s.

2. Multiply by diagonal inertia to obtain L=[0.055999999999999994, 0.08399999999999999, 0.04000000000000001] kg*m^2/s.

3. The quadratic energy is 0.053000 J.

4. Compute omega cross L: [0.011200000000000005, -0.016800000000000002, 0.0196] Nm.

5. Include the acceleration term to obtain torque [0.011200000000000005, 0.019199999999999995, 0.0196] Nm.

L and omega differ in direction by 0.259483 rad in this non-spherical body.

#### Worked case 3: speed = 1

This case keeps the nominal configuration except for speed=1. The full input is {"speed": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| kinetic energy J | 0.0734 |
| momentum norm kg m2 s | 0.12270289 |
| misalignment rad | 0.25674916 |
| gyroscopic torque Nm | 0.03854141 |
| required torque Nm | 0.03245674 |

1. Angular velocity is [1.0, 0.7, 0.2] rad/s.

2. Multiply by diagonal inertia to obtain L=[0.08, 0.08399999999999999, 0.04000000000000001] kg*m^2/s.

3. The quadratic energy is 0.073400 J.

4. Compute omega cross L: [0.011200000000000005, -0.024000000000000007, 0.027999999999999997] Nm.

5. Include the acceleration term to obtain torque [0.011200000000000005, 0.01199999999999999, 0.027999999999999997] Nm.

L and omega differ in direction by 0.256749 rad in this non-spherical body.

#### Worked case 4: speed = 2

This case keeps the nominal configuration except for speed=2. The full input is {"speed": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| kinetic energy J | 0.1934 |
| momentum norm kg m2 s | 0.18508376 |
| misalignment rad | 0.19052989 |
| gyroscopic torque Nm | 0.07460188 |
| required torque Nm | 0.05835615 |

1. Angular velocity is [2.0, 0.7, 0.2] rad/s.

2. Multiply by diagonal inertia to obtain L=[0.16, 0.08399999999999999, 0.04000000000000001] kg*m^2/s.

3. The quadratic energy is 0.193400 J.

4. Compute omega cross L: [0.011200000000000005, -0.048000000000000015, 0.055999999999999994] Nm.

5. Include the acceleration term to obtain torque [0.011200000000000005, -0.012000000000000018, 0.055999999999999994] Nm.

L and omega differ in direction by 0.190530 rad in this non-spherical body.

#### Worked case 5: speed = 4

This case keeps the nominal configuration except for speed=4. The full input is {"speed": 4.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| kinetic energy J | 0.6734 |
| momentum norm kg m2 s | 0.33325066 |
| misalignment rad | 0.10940494 |
| gyroscopic torque Nm | 0.14793728 |
| required torque Nm | 0.12755172 |

1. Angular velocity is [4.0, 0.7, 0.2] rad/s.

2. Multiply by diagonal inertia to obtain L=[0.32, 0.08399999999999999, 0.04000000000000001] kg*m^2/s.

3. The quadratic energy is 0.673400 J.

4. Compute omega cross L: [0.011200000000000005, -0.09600000000000003, 0.11199999999999999] Nm.

5. Include the acceleration term to obtain torque [0.011200000000000005, -0.06000000000000003, 0.11199999999999999] Nm.

L and omega differ in direction by 0.109405 rad in this non-spherical body.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

L and omega differ in direction by 0.172693 rad in this non-spherical body.

The calculation assumes a rigid body about its COM with a consistently expressed inertia tensor.

### K. Failure modes and troubleshooting

Treating inertia as one scalar in a three-axis problem; omitting external moments when discussing conservation.

### L. Practical exercises and extension tasks

1. Set all diagonal inertias equal and verify L is parallel to omega.

2. Reverse omega and compare momentum, energy and gyroscopic torque.

3. Evaluate kinetic energy after a frame rotation.

### M. Connection to the Asimov research platform

Whole-body controllers must account for angular momentum and contact wrench feasibility; a torso orientation target alone is incomplete.

### N. Completion record

Record your chosen case, predicted trend, measured kinetic_energy_J, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 14, Gravity, acceleration and joint-load budgeting. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 14 - Gravity, acceleration and joint-load budgeting

### A. The engineering question

A motor must support gravity and accelerate the link while overcoming friction.

### B. Concepts and mathematical model

Looking only at the static gravity torque can underestimate peaks; looking only at the peak actuator rating can overestimate continuous capability. This experiment combines a point payload and a uniform rod into an explicitly simple joint-load model. The result is useful for reasoning about sensitivity, but cannot replace a released mechanism model, bearing analysis or duty-cycle study.

tau = (m_payload*g*l + m_rod*g*l/2)*cos(q) + (m_payload*l^2+m_rod*l^2/3)*q_ddot + tau_friction.

### C. Real-world meaning and limits

Use release-specific mass/inertia, measured friction and continuous motor envelopes before choosing a physical load.

### D. Architecture and data flow

Configuration (length, payload, rod_mass, angle_deg, acceleration) -> numerical model -> gravity_Nm, inertia_kg_m2, acceleration_Nm -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

length is meters; payload and rod_mass are kilograms; acceleration is output-axis rad/s^2; angle is measured from horizontal.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| length | 0.25 | meters |
| payload | 2 | Defined by the explicit chapter model and parameter contract |
| rod_mass | 1 | Defined by the explicit chapter model and parameter contract |
| angle_deg | 20 | degrees |
| acceleration | 3 | SI acceleration in the chapter equation |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/14_joint_loading.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only acceleration changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/14_joint_loading.py --case 0

.venv-book/bin/python expanded_lab/modules/14_joint_loading.py --case 3

.venv-book/bin/python expanded_lab/run.py joint_loading --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/14_joint_loading.py

### H. Walkthrough and design decisions

The rod and payload have different lever arms and inertia formulas. Keeping gravity and acceleration terms separate makes the result auditable and supports a duty-cycle calculation later.

### I. Expected behavior and six worked cases

The controlled variable is acceleration. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/14_joint_loading.png

Figure L14. gravity Nm as acceleration changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | acceleration | gravity Nm |
|---|---|---|
| 0 | 0 | 5.76149038 |
| 1 | 1 | 5.76149038 |
| 2 | 2 | 5.76149038 |
| 3 | 3 | 5.76149038 |
| 4 | 6 | 5.76149038 |
| 5 | 12 | 5.76149038 |

#### Worked case 0: acceleration = 0

This case keeps the nominal configuration except for acceleration=0. The full input is {"acceleration": 0.0, "angle_deg": 20.0, "length": 0.25, "payload": 2.0, "rod_mass": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| gravity Nm | 5.76149038 |
| inertia kg m2 | 0.14583333 |
| acceleration Nm | 0 |
| total required Nm | 6.06149038 |
| gravity fraction | 0.95050722 |

1. Payload mass 2 kg acts at 0.25 m; rod COM acts at 0.125 m.

2. At angle 20 degrees, gravity torque is 5.761490 Nm.

3. Total modeled rotational inertia is 0.145833 kg*m^2.

4. Acceleration 0 rad/s^2 adds 0.000000 Nm.

5. Add 0.3 Nm illustrative friction: total demand is 6.061490 Nm.

#### Worked case 1: acceleration = 1

This case keeps the nominal configuration except for acceleration=1. The full input is {"acceleration": 1.0, "angle_deg": 20.0, "length": 0.25, "payload": 2.0, "rod_mass": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| gravity Nm | 5.76149038 |
| inertia kg m2 | 0.14583333 |
| acceleration Nm | 0.14583333 |
| total required Nm | 6.20732371 |
| gravity fraction | 0.92817624 |

1. Payload mass 2 kg acts at 0.25 m; rod COM acts at 0.125 m.

2. At angle 20 degrees, gravity torque is 5.761490 Nm.

3. Total modeled rotational inertia is 0.145833 kg*m^2.

4. Acceleration 1 rad/s^2 adds 0.145833 Nm.

5. Add 0.3 Nm illustrative friction: total demand is 6.207324 Nm.

#### Worked case 2: acceleration = 2

This case keeps the nominal configuration except for acceleration=2. The full input is {"acceleration": 2.0, "angle_deg": 20.0, "length": 0.25, "payload": 2.0, "rod_mass": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| gravity Nm | 5.76149038 |
| inertia kg m2 | 0.14583333 |
| acceleration Nm | 0.29166667 |
| total required Nm | 6.35315705 |
| gravity fraction | 0.90687045 |

1. Payload mass 2 kg acts at 0.25 m; rod COM acts at 0.125 m.

2. At angle 20 degrees, gravity torque is 5.761490 Nm.

3. Total modeled rotational inertia is 0.145833 kg*m^2.

4. Acceleration 2 rad/s^2 adds 0.291667 Nm.

5. Add 0.3 Nm illustrative friction: total demand is 6.353157 Nm.

#### Worked case 3: acceleration = 3

This case keeps the nominal configuration except for acceleration=3. The full input is {"acceleration": 3.0, "angle_deg": 20.0, "length": 0.25, "payload": 2.0, "rod_mass": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| gravity Nm | 5.76149038 |
| inertia kg m2 | 0.14583333 |
| acceleration Nm | 0.4375 |
| total required Nm | 6.49899038 |
| gravity fraction | 0.88652084 |

1. Payload mass 2 kg acts at 0.25 m; rod COM acts at 0.125 m.

2. At angle 20 degrees, gravity torque is 5.761490 Nm.

3. Total modeled rotational inertia is 0.145833 kg*m^2.

4. Acceleration 3 rad/s^2 adds 0.437500 Nm.

5. Add 0.3 Nm illustrative friction: total demand is 6.498990 Nm.

#### Worked case 4: acceleration = 6

This case keeps the nominal configuration except for acceleration=6. The full input is {"acceleration": 6.0, "angle_deg": 20.0, "length": 0.25, "payload": 2.0, "rod_mass": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| gravity Nm | 5.76149038 |
| inertia kg m2 | 0.14583333 |
| acceleration Nm | 0.875 |
| total required Nm | 6.93649038 |
| gravity fraction | 0.83060598 |

1. Payload mass 2 kg acts at 0.25 m; rod COM acts at 0.125 m.

2. At angle 20 degrees, gravity torque is 5.761490 Nm.

3. Total modeled rotational inertia is 0.145833 kg*m^2.

4. Acceleration 6 rad/s^2 adds 0.875000 Nm.

5. Add 0.3 Nm illustrative friction: total demand is 6.936490 Nm.

#### Worked case 5: acceleration = 12

This case keeps the nominal configuration except for acceleration=12. The full input is {"acceleration": 12.0, "angle_deg": 20.0, "length": 0.25, "payload": 2.0, "rod_mass": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| gravity Nm | 5.76149038 |
| inertia kg m2 | 0.14583333 |
| acceleration Nm | 1.75 |
| total required Nm | 7.81149038 |
| gravity fraction | 0.73756609 |

1. Payload mass 2 kg acts at 0.25 m; rod COM acts at 0.125 m.

2. At angle 20 degrees, gravity torque is 5.761490 Nm.

3. Total modeled rotational inertia is 0.145833 kg*m^2.

4. Acceleration 12 rad/s^2 adds 1.750000 Nm.

5. Add 0.3 Nm illustrative friction: total demand is 7.811490 Nm.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The load budget separates assumptions so the dominant contribution can be identified.

This one-axis model excludes impact, gear reflected inertia, cable forces and multi-link coupling.

### K. Failure modes and troubleshooting

Using motor-shaft acceleration with output-axis inertia; applying a static margin to an impact; omitting the fixture reaction load.

### L. Practical exercises and extension tasks

1. Compare the horizontal and vertical configurations.

2. Double payload mass and identify linear terms.

3. Calculate a trajectory torque trace rather than one worst-looking pose.

### M. Connection to the Asimov research platform

Use release-specific mass/inertia, measured friction and continuous motor envelopes before choosing a physical load.

### N. Completion record

Record your chosen case, predicted trend, measured gravity_Nm, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 15, Gear ratio, reflected inertia and backlash dead zones. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 15 - Gear ratio, reflected inertia and backlash dead zones

### A. The engineering question

A gearbox changes the coordinate system between a motor and an output.

### B. Concepts and mathematical model

Rotor inertia reflected to the output grows with the square of the velocity ratio, which can make a high-ratio transmission dynamically significant. Backlash is a lost-motion region during reversals, not a random measurement error. This laboratory combines an inertia calculation with a simple play operator that holds the output until the input crosses the slack boundary. It is deliberately a scalar transmission model, not an identified Asimov actuator.

I_reflected = J_motor*G^2; backlash output remains inside input +/- half_gap until a boundary forces motion.

### C. Real-world meaning and limits

Actual transmission behavior requires measured reversals and verified encoder placement; do not copy the teaching gap into a physical controller.

### D. Architecture and data flow

Configuration (ratio, rotor_inertia, backlash) -> numerical model -> reflected_inertia_kg_m2, tracking_rmse_rad, peak_lost_motion_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

ratio is motor/output speed ratio; rotor_inertia is motor-shaft kg*m^2; backlash is total output-coordinate gap in radians.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| ratio | 36 | dimensionless motor/output ratio |
| rotor_inertia | 0.00002 | Defined by the explicit chapter model and parameter contract |
| backlash | 0.01 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/15_gear_backlash.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only backlash changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/15_gear_backlash.py --case 0

.venv-book/bin/python expanded_lab/modules/15_gear_backlash.py --case 3

.venv-book/bin/python expanded_lab/run.py gear_backlash --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/15_gear_backlash.py

### H. Walkthrough and design decisions

The output carries memory through previous, so reversal behavior differs from a stateless clipping function. The reflected inertia calculation is independent of the backlash trajectory and must not be conflated with it.

### I. Expected behavior and six worked cases

The controlled variable is backlash. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/15_gear_backlash.png

Figure L15. reflected inertia kg m2 as backlash changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | backlash | reflected inertia kg m2 |
|---|---|---|
| 0 | 0 | 0.02592 |
| 1 | 0.002 | 0.02592 |
| 2 | 0.005 | 0.02592 |
| 3 | 0.01 | 0.02592 |
| 4 | 0.02 | 0.02592 |
| 5 | 0.04 | 0.02592 |

#### Worked case 0: backlash = 0

This case keeps the nominal configuration except for backlash=0. The full input is {"backlash": 0.0, "ratio": 36.0, "rotor_inertia": 2e-05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reflected inertia kg m2 | 0.02592 |
| tracking rmse rad | 0 |
| peak lost motion rad | 0 |
| transmitted range rad | 0.2 |

1. Rotor inertia 2.000e-05 kg*m^2 is reflected through ratio 36.

2. Output-equivalent inertia is 0.02592000 kg*m^2.

3. The commanded output trajectory has 0.1 rad amplitude and 0.5 Hz frequency.

4. Apply a total backlash gap of 0.000000 rad with a stateful play operator.

5. The resulting RMSE is 0.000000 rad; peak error is 0.000000 rad.

#### Worked case 1: backlash = 0.002

This case keeps the nominal configuration except for backlash=0.002. The full input is {"backlash": 0.002, "ratio": 36.0, "rotor_inertia": 2e-05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reflected inertia kg m2 | 0.02592 |
| tracking rmse rad | 0.00098241 |
| peak lost motion rad | 0.001 |
| transmitted range rad | 0.198 |

1. Rotor inertia 2.000e-05 kg*m^2 is reflected through ratio 36.

2. Output-equivalent inertia is 0.02592000 kg*m^2.

3. The commanded output trajectory has 0.1 rad amplitude and 0.5 Hz frequency.

4. Apply a total backlash gap of 0.002000 rad with a stateful play operator.

5. The resulting RMSE is 0.000982 rad; peak error is 0.001000 rad.

#### Worked case 2: backlash = 0.005

This case keeps the nominal configuration except for backlash=0.005. The full input is {"backlash": 0.005, "ratio": 36.0, "rotor_inertia": 2e-05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reflected inertia kg m2 | 0.02592 |
| tracking rmse rad | 0.00242939 |
| peak lost motion rad | 0.0025 |
| transmitted range rad | 0.195 |

1. Rotor inertia 2.000e-05 kg*m^2 is reflected through ratio 36.

2. Output-equivalent inertia is 0.02592000 kg*m^2.

3. The commanded output trajectory has 0.1 rad amplitude and 0.5 Hz frequency.

4. Apply a total backlash gap of 0.005000 rad with a stateful play operator.

5. The resulting RMSE is 0.002429 rad; peak error is 0.002500 rad.

#### Worked case 3: backlash = 0.01

This case keeps the nominal configuration except for backlash=0.01. The full input is {"backlash": 0.01, "ratio": 36.0, "rotor_inertia": 2e-05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reflected inertia kg m2 | 0.02592 |
| tracking rmse rad | 0.00479646 |
| peak lost motion rad | 0.005 |
| transmitted range rad | 0.19 |

1. Rotor inertia 2.000e-05 kg*m^2 is reflected through ratio 36.

2. Output-equivalent inertia is 0.02592000 kg*m^2.

3. The commanded output trajectory has 0.1 rad amplitude and 0.5 Hz frequency.

4. Apply a total backlash gap of 0.010000 rad with a stateful play operator.

5. The resulting RMSE is 0.004796 rad; peak error is 0.005000 rad.

#### Worked case 4: backlash = 0.02

This case keeps the nominal configuration except for backlash=0.02. The full input is {"backlash": 0.02, "ratio": 36.0, "rotor_inertia": 2e-05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reflected inertia kg m2 | 0.02592 |
| tracking rmse rad | 0.00940506 |
| peak lost motion rad | 0.01 |
| transmitted range rad | 0.18 |

1. Rotor inertia 2.000e-05 kg*m^2 is reflected through ratio 36.

2. Output-equivalent inertia is 0.02592000 kg*m^2.

3. The commanded output trajectory has 0.1 rad amplitude and 0.5 Hz frequency.

4. Apply a total backlash gap of 0.020000 rad with a stateful play operator.

5. The resulting RMSE is 0.009405 rad; peak error is 0.010000 rad.

#### Worked case 5: backlash = 0.04

This case keeps the nominal configuration except for backlash=0.04. The full input is {"backlash": 0.04, "ratio": 36.0, "rotor_inertia": 2e-05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reflected inertia kg m2 | 0.02592 |
| tracking rmse rad | 0.01822161 |
| peak lost motion rad | 0.02 |
| transmitted range rad | 0.16 |

1. Rotor inertia 2.000e-05 kg*m^2 is reflected through ratio 36.

2. Output-equivalent inertia is 0.02592000 kg*m^2.

3. The commanded output trajectory has 0.1 rad amplitude and 0.5 Hz frequency.

4. Apply a total backlash gap of 0.040000 rad with a stateful play operator.

5. The resulting RMSE is 0.018222 rad; peak error is 0.020000 rad.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

A stateful dead zone creates hysteresis; adding independent Gaussian noise would model a different phenomenon.

The play model excludes stiffness, friction and load-dependent tooth contact.

### K. Failure modes and troubleshooting

Double-applying gear ratio to an output encoder; assuming all tracking error is sensor noise; ignoring reversal direction.

### L. Practical exercises and extension tasks

1. Add a load direction and compare reversal behavior.

2. Sweep gear ratio separately and show its squared inertia dependence.

3. Fit backlash from a recorded slow bidirectional experiment.

### M. Connection to the Asimov research platform

Actual transmission behavior requires measured reversals and verified encoder placement; do not copy the teaching gap into a physical controller.

### N. Completion record

Record your chosen case, predicted trend, measured reflected_inertia_kg_m2, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 16, Closed-form two-link inverse kinematics and branch choice. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 16 - Closed-form two-link inverse kinematics and branch choice

### A. The engineering question

Inverse kinematics often has several solutions or no solution.

### B. Concepts and mathematical model

A two-link planar arm makes those possibilities explicit: two elbow branches can reach the same point, while targets outside an annulus cannot be reached. Clipping an impossible cosine into [-1,1] without reporting the original violation hides reachability failure. Branch selection should preserve continuity and respect limits. This simple analytic model becomes a reference for numerical IK and for understanding why more joints do not eliminate ambiguity.

cos(q2)=(x^2+y^2-l1^2-l2^2)/(2*l1*l2); q1=atan2(y,x)-atan2(l2*sin(q2),l1+l2*cos(q2)).

### C. Real-world meaning and limits

The humanoid arm has more axes and geometry, but the same reachability, branch, limit and collision questions remain.

### D. Architecture and data flow

Configuration (target_x, target_y) -> numerical model -> reachable, q1_rad, q2_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

target_x and target_y are meters in a fixed planar base frame; q1 and q2 are relative joint angles.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| target_x | 0.35 | Defined by the explicit chapter model and parameter contract |
| target_y | 0.1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/16_planar_ik.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only target_x changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/16_planar_ik.py --case 0

.venv-book/bin/python expanded_lab/modules/16_planar_ik.py --case 3

.venv-book/bin/python expanded_lab/run.py planar_ik --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/16_planar_ik.py

### H. Walkthrough and design decisions

Compute the reachability flag before clipping for numerical evaluation. The forward residual is an independent success metric, while branch continuity requires information from the previous pose.

### I. Expected behavior and six worked cases

The controlled variable is target_x. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/16_planar_ik.png

Figure L16. reachable as target_x changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | target_x | reachable |
|---|---|---|
| 0 | 0.05 | 1 |
| 1 | 0.1 | 1 |
| 2 | 0.2 | 1 |
| 3 | 0.35 | 1 |
| 4 | 0.48 | 1 |
| 5 | 0.6 | 0 |

#### Worked case 0: target_x = 0.05

This case keeps the nominal configuration except for target_x=0.05. The full input is {"target_x": 0.05, "target_y": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reachable | 1 |
| q1 rad | 0.73540395 |
| q2 rad | 2.93711245 |
| residual m | 4.3885418e-17 |
| cosine raw | -0.97916667 |

1. Target is (0.05,0.1) m with link lengths 0.3,0.2 m.

2. Compute the raw elbow cosine -0.97916667; reachability is True.

3. The positive-elbow candidate is q2=2.93711245 rad.

4. Compute shoulder correction to obtain q1=0.73540395 rad.

5. Forward kinematics returns [0.04999999999999999, 0.09999999999999996] m, with residual 0.00000000 m.

#### Worked case 1: target_x = 0.1

This case keeps the nominal configuration except for target_x=0.1. The full input is {"target_x": 0.1, "target_y": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reachable | 1 |
| q1 rad | 0.18472956 |
| q2 rad | 2.73045479 |
| residual m | 6.2063354e-17 |
| cosine raw | -0.91666667 |

1. Target is (0.1,0.1) m with link lengths 0.3,0.2 m.

2. Compute the raw elbow cosine -0.91666667; reachability is True.

3. The positive-elbow candidate is q2=2.73045479 rad.

4. Compute shoulder correction to obtain q1=0.18472956 rad.

5. Forward kinematics returns [0.09999999999999995, 0.09999999999999998] m, with residual 0.00000000 m.

#### Worked case 2: target_x = 0.2

This case keeps the nominal configuration except for target_x=0.2. The full input is {"target_x": 0.2, "target_y": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reachable | 1 |
| q1 rad | -0.26608005 |
| q2 rad | 2.30052398 |
| residual m | 6.2063354e-17 |
| cosine raw | -0.66666667 |

1. Target is (0.2,0.1) m with link lengths 0.3,0.2 m.

2. Compute the raw elbow cosine -0.66666667; reachability is True.

3. The positive-elbow candidate is q2=2.30052398 rad.

4. Compute shoulder correction to obtain q1=-0.26608005 rad.

5. Forward kinematics returns [0.19999999999999996, 0.09999999999999998] m, with residual 0.00000000 m.

#### Worked case 3: target_x = 0.35

This case keeps the nominal configuration except for target_x=0.35. The full input is {"target_x": 0.35, "target_y": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reachable | 1 |
| q1 rad | -0.30325418 |
| q2 rad | 1.54996149 |
| residual m | 5.7219585e-17 |
| cosine raw | 0.02083333 |

1. Target is (0.35,0.1) m with link lengths 0.3,0.2 m.

2. Compute the raw elbow cosine 0.02083333; reachability is True.

3. The positive-elbow candidate is q2=1.54996149 rad.

4. Compute shoulder correction to obtain q1=-0.30325418 rad.

5. Forward kinematics returns [0.3499999999999999, 0.09999999999999999] m, with residual 0.00000000 m.

#### Worked case 4: target_x = 0.48

This case keeps the nominal configuration except for target_x=0.48. The full input is {"target_x": 0.48, "target_y": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reachable | 1 |
| q1 rad | 0.04483964 |
| q2 rad | 0.40271584 |
| residual m | 5.7219585e-17 |
| cosine raw | 0.92 |

1. Target is (0.48,0.1) m with link lengths 0.3,0.2 m.

2. Compute the raw elbow cosine 0.92000000; reachability is True.

3. The positive-elbow candidate is q2=0.40271584 rad.

4. Compute shoulder correction to obtain q1=0.04483964 rad.

5. Forward kinematics returns [0.48000000000000004, 0.09999999999999999] m, with residual 0.00000000 m.

#### Worked case 5: target_x = 0.6

This case keeps the nominal configuration except for target_x=0.6. The full input is {"target_x": 0.6, "target_y": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reachable | 0 |
| q1 rad | 0.16514868 |
| q2 rad | 0 |
| residual m | 0.10827625 |
| cosine raw | 2 |

1. Target is (0.6,0.1) m with link lengths 0.3,0.2 m.

2. Compute the raw elbow cosine 2.00000000; reachability is False.

3. The positive-elbow candidate is q2=0.00000000 rad.

4. Compute shoulder correction to obtain q1=0.16514868 rad.

5. Forward kinematics returns [0.4931969619160719, 0.08219949365267865] m, with residual 0.10827625 m.

The clipped candidate is only a nearest-boundary diagnostic. It must not be returned as a successful IK solution.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The target is geometrically reachable; joint limits and collisions still require separate checks.

Negating q2 and recomputing q1 gives the other elbow branch when the target is not singular.

### K. Failure modes and troubleshooting

Calling a clipped cosine a valid solution; mixing absolute and relative elbow angles; assuming endpoint reachability guarantees collision freedom.

### L. Practical exercises and extension tasks

1. Compute both branches and choose the closest to a previous joint state.

2. Add asymmetric joint limits and identify rejected branches.

3. Follow a Cartesian line through a near-singular pose and inspect continuity.

### M. Connection to the Asimov research platform

The humanoid arm has more axes and geometry, but the same reachability, branch, limit and collision questions remain.

### N. Completion record

Record your chosen case, predicted trend, measured reachable, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 17, Singular values and damped least-squares motion. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 17 - Singular values and damped least-squares motion

### A. The engineering question

Near a kinematic singularity, an inverse Jacobian can demand enormous joint changes to achieve a small endpoint motion.

### B. Concepts and mathematical model

Damped least squares trades exact Cartesian tracking for bounded numerical sensitivity. Singular values reveal which directions are poorly controllable. Damping is not a safety proof: a bounded numerical update can still violate a joint limit or collision constraint. This laboratory exposes the tradeoff with a nearly stretched two-link arm.

dq = J.T*(J*J.T+lambda^2*I)^-1*error; J=U*S*V.T; directional gain=s/(s^2+lambda^2).

### C. Real-world meaning and limits

Use conservative increment, velocity and collision checks around the numerical solver; hardware compliance changes the achieved endpoint.

### D. Architecture and data flow

Configuration (elbow, damping) -> numerical model -> min_singular_value, joint_step_norm_rad, predicted_residual_m -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

elbow is the relative second-joint angle in radians; damping is the regularization scale in the selected Jacobian units.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| elbow | 0.03 | Defined by the explicit chapter model and parameter contract |
| damping | 0.01 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/17_damped_ik.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only damping changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/17_damped_ik.py --case 0

.venv-book/bin/python expanded_lab/modules/17_damped_ik.py --case 3

.venv-book/bin/python expanded_lab/run.py damped_ik --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/17_damped_ik.py

### H. Walkthrough and design decisions

Inspect singular values before choosing damping. Compare joint-step magnitude and residual together; selecting the smallest residual alone rewards unreasonable motion near singularity.

### I. Expected behavior and six worked cases

The controlled variable is damping. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/17_damped_ik.png

Figure L17. min singular value as damping changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | damping | min singular value |
|---|---|---|
| 0 | 0.0001 | 0.00334239 |
| 1 | 0.001 | 0.00334239 |
| 2 | 0.005 | 0.00334239 |
| 3 | 0.01 | 0.00334239 |
| 4 | 0.03 | 0.00334239 |
| 5 | 0.1 | 0.00334239 |

#### Worked case 0: damping = 0.0001

This case keeps the nominal configuration except for damping=0.0001. The full input is {"damping": 0.0001, "elbow": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| min singular value | 0.00334239 |
| joint step norm rad | 2.92070524 |
| predicted residual m | 8.7383648e-06 |
| max joint step rad | 2.71327577 |

1. Use pose q1=0.2, q2=0.03 rad and Cartesian request [0.01, 0.0] m.

2. The Jacobian singular values are [0.5384559707877523, 0.0033423902970501785].

3. Choose damping lambda=0.0001 and solve the regularized 2x2 system.

4. The joint update is [1.0810428867396382, -2.713275765484518] rad.

5. Linearized achieved displacement is [0.009991461844996323, -1.8598193941951011e-06] m; residual is 0.00000874 m.

#### Worked case 1: damping = 0.001

This case keeps the nominal configuration except for damping=0.001. The full input is {"damping": 0.001, "elbow": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| min singular value | 0.00334239 |
| joint step norm rad | 2.68314411 |
| predicted residual m | 0.00080276 |
| max joint step rad | 2.49270528 |

1. Use pose q1=0.2, q2=0.03 rad and Cartesian request [0.01, 0.0] m.

2. The Jacobian singular values are [0.5384559707877523, 0.0033423902970501785].

3. Choose damping lambda=0.001 and solve the regularized 2x2 system.

4. The joint update is [0.9928155294304304, -2.492705281898182] rad.

5. Linearized achieved displacement is [0.00921563121821457, -0.00017085413119924766] m; residual is 0.00080276 m.

#### Worked case 2: damping = 0.005

This case keeps the nominal configuration except for damping=0.005. The full input is {"damping": 0.005, "elbow": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| min singular value | 0.00334239 |
| joint step norm rad | 0.90287369 |
| predicted residual m | 0.00675314 |
| max joint step rad | 0.83975812 |

1. Use pose q1=0.2, q2=0.03 rad and Cartesian request [0.01, 0.0] m.

2. The Jacobian singular values are [0.5384559707877523, 0.0033423902970501785].

3. Choose damping lambda=0.005 and solve the regularized 2x2 system.

4. The joint update is [0.33164317598195225, -0.8397581249487018] rad.

5. Linearized achieved displacement is [0.0034015591968046942, -0.0014371723570492413] m; residual is 0.00675314 m.

#### Worked case 3: damping = 0.01

This case keeps the nominal configuration except for damping=0.01. The full input is {"damping": 0.01, "elbow": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| min singular value | 0.00334239 |
| joint step norm rad | 0.29378916 |
| predicted residual m | 0.008789 |
| max joint step rad | 0.27421959 |

1. Use pose q1=0.2, q2=0.03 rad and Cartesian request [0.01, 0.0] m.

2. The Jacobian singular values are [0.5384559707877523, 0.0033423902970501785].

3. Choose damping lambda=0.01 and solve the regularized 2x2 system.

4. The joint update is [0.10543096784534178, -0.2742195862584573] rad.

5. Linearized achieved displacement is [0.0014122322972766987, -0.001869950765244978] m; residual is 0.00878900 m.

#### Worked case 4: damping = 0.03

This case keeps the nominal configuration except for damping=0.03. The full input is {"damping": 0.03, "elbow": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| min singular value | 0.00334239 |
| joint step norm rad | 0.03605779 |
| predicted residual m | 0.00965107 |
| max joint step rad | 0.03474182 |

1. Use pose q1=0.2, q2=0.03 rad and Cartesian request [0.01, 0.0] m.

2. The Jacobian singular values are [0.5384559707877523, 0.0033423902970501785].

3. Choose damping lambda=0.03 and solve the regularized 2x2 system.

4. The joint update is [0.009652461746241459, -0.03474182456657826] rad.

5. Linearized achieved displacement is [0.0005686677258760275, -0.002047717344637136] m; residual is 0.00965107 m.

#### Worked case 5: damping = 0.1

This case keeps the nominal configuration except for damping=0.1. The full input is {"damping": 0.1, "elbow": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| min singular value | 0.00334239 |
| joint step norm rad | 0.00502414 |
| predicted residual m | 0.00976022 |
| max joint step rad | 0.00444793 |

1. Use pose q1=0.2, q2=0.03 rad and Cartesian request [0.01, 0.0] m.

2. The Jacobian singular values are [0.5384559707877523, 0.0033423902970501785].

3. Choose damping lambda=0.1 and solve the regularized 2x2 system.

4. The joint update is [-0.0023362171727600717, -0.0044479280585467615] rad.

5. Linearized achieved displacement is [0.00044856693651852995, -0.002007993356992157] m; residual is 0.00976022 m.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The linearized prediction is only valid for sufficiently small joint updates; recompute nonlinear FK after each iteration.

A larger damping value can improve numerical behavior while deliberately leaving more task error.

### K. Failure modes and troubleshooting

Inverting J directly near rank loss; comparing damping values across differently scaled translation/orientation tasks without unit normalization.

### L. Practical exercises and extension tasks

1. Sweep elbow angle toward zero while holding damping fixed.

2. Cap joint increments and recompute the actual nonlinear displacement.

3. Add a secondary posture task in the null space of a redundant arm.

### M. Connection to the Asimov research platform

Use conservative increment, velocity and collision checks around the numerical solver; hardware compliance changes the achieved endpoint.

### N. Completion record

Record your chosen case, predicted trend, measured min_singular_value, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 18, Support polygons, center of pressure and load transfer. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 18 - Support polygons, center of pressure and load transfer

### A. The engineering question

A support polygon is determined by active contact geometry, not by a drawing of where the feet might be.

### B. Concepts and mathematical model

Contact loads determine the center of pressure, while COM projection provides a static load-feasibility clue under restrictive assumptions. An unloaded foot should not enlarge the support region. This laboratory uses two point contact resultants to show how vertical load redistribution moves COP and how a horizontal COM shift consumes a chosen geometric margin.

COP_x=sum(Fz_i*x_i)/sum(Fz_i); signed margin=min(x-xmin,xmax-x); Fz_i must be nonnegative for unilateral contact.

### C. Real-world meaning and limits

Foot contact sensing may require estimation; simulation contact truth must not be silently substituted for unavailable hardware force sensors.

### D. Architecture and data flow

Configuration (left_load, mass, com_x) -> numerical model -> cop_x_m, com_margin_m, left_force_N -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

left_load is the fraction of total vertical load; mass is kilograms; com_x is the COM projection in meters.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| left_load | 0.5 | Defined by the explicit chapter model and parameter contract |
| mass | 10 | kilograms |
| com_x | 0.02 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/18_support_polygon.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only left_load changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/18_support_polygon.py --case 0

.venv-book/bin/python expanded_lab/modules/18_support_polygon.py --case 3

.venv-book/bin/python expanded_lab/run.py support_polygon --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/18_support_polygon.py

### H. Walkthrough and design decisions

Compute COP from forces, not masses. The residual pitch moment is a useful sign check but does not model whole-body angular momentum or dynamic ground reaction.

### I. Expected behavior and six worked cases

The controlled variable is left_load. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/18_support_polygon.png

Figure L18. cop x m as left_load changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | left_load | cop x m |
|---|---|---|
| 0 | 0 | 0.1 |
| 1 | 0.1 | 0.08 |
| 2 | 0.25 | 0.05 |
| 3 | 0.5 | 0 |
| 4 | 0.75 | -0.05 |
| 5 | 1 | -0.1 |

#### Worked case 0: left_load = 0

This case keeps the nominal configuration except for left_load=0. The full input is {"com_x": 0.02, "left_load": 0.0, "mass": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| cop x m | 0.1 |
| com margin m | 0.12 |
| left force N | 0 |
| right force N | 98.1 |
| unbalanced pitch moment Nm | -7.848 |

1. Total vertical load is 98.100000 N.

2. Left fraction 0 gives forces [0.0, 98.10000000000001] N at x=-0.1,+0.1 m.

3. The weighted contact location is COP x=0.100000 m.

4. COM x=0.02 m has signed margin 0.120000 m inside the illustrative outer edges.

5. The gravity/COP moment difference is -7.848000 Nm.

#### Worked case 1: left_load = 0.1

This case keeps the nominal configuration except for left_load=0.1. The full input is {"com_x": 0.02, "left_load": 0.1, "mass": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| cop x m | 0.08 |
| com margin m | 0.12 |
| left force N | 9.81 |
| right force N | 88.29 |
| unbalanced pitch moment Nm | -5.886 |

1. Total vertical load is 98.100000 N.

2. Left fraction 0.1 gives forces [9.810000000000002, 88.29] N at x=-0.1,+0.1 m.

3. The weighted contact location is COP x=0.080000 m.

4. COM x=0.02 m has signed margin 0.120000 m inside the illustrative outer edges.

5. The gravity/COP moment difference is -5.886000 Nm.

Both contact resultants are compressive in this static illustration.

#### Worked case 2: left_load = 0.25

This case keeps the nominal configuration except for left_load=0.25. The full input is {"com_x": 0.02, "left_load": 0.25, "mass": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| cop x m | 0.05 |
| com margin m | 0.12 |
| left force N | 24.525 |
| right force N | 73.575 |
| unbalanced pitch moment Nm | -2.943 |

1. Total vertical load is 98.100000 N.

2. Left fraction 0.25 gives forces [24.525000000000002, 73.575] N at x=-0.1,+0.1 m.

3. The weighted contact location is COP x=0.050000 m.

4. COM x=0.02 m has signed margin 0.120000 m inside the illustrative outer edges.

5. The gravity/COP moment difference is -2.943000 Nm.

Both contact resultants are compressive in this static illustration.

#### Worked case 3: left_load = 0.5

This case keeps the nominal configuration except for left_load=0.5. The full input is {"com_x": 0.02, "left_load": 0.5, "mass": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| cop x m | 0 |
| com margin m | 0.12 |
| left force N | 49.05 |
| right force N | 49.05 |
| unbalanced pitch moment Nm | 1.962 |

1. Total vertical load is 98.100000 N.

2. Left fraction 0.5 gives forces [49.050000000000004, 49.050000000000004] N at x=-0.1,+0.1 m.

3. The weighted contact location is COP x=0.000000 m.

4. COM x=0.02 m has signed margin 0.120000 m inside the illustrative outer edges.

5. The gravity/COP moment difference is 1.962000 Nm.

Both contact resultants are compressive in this static illustration.

#### Worked case 4: left_load = 0.75

This case keeps the nominal configuration except for left_load=0.75. The full input is {"com_x": 0.02, "left_load": 0.75, "mass": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| cop x m | -0.05 |
| com margin m | 0.12 |
| left force N | 73.575 |
| right force N | 24.525 |
| unbalanced pitch moment Nm | 6.867 |

1. Total vertical load is 98.100000 N.

2. Left fraction 0.75 gives forces [73.575, 24.525000000000002] N at x=-0.1,+0.1 m.

3. The weighted contact location is COP x=-0.050000 m.

4. COM x=0.02 m has signed margin 0.120000 m inside the illustrative outer edges.

5. The gravity/COP moment difference is 6.867000 Nm.

Both contact resultants are compressive in this static illustration.

#### Worked case 5: left_load = 1

This case keeps the nominal configuration except for left_load=1. The full input is {"com_x": 0.02, "left_load": 1.0, "mass": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| cop x m | -0.1 |
| com margin m | 0.12 |
| left force N | 98.1 |
| right force N | 0 |
| unbalanced pitch moment Nm | 11.772 |

1. Total vertical load is 98.100000 N.

2. Left fraction 1 gives forces [98.10000000000001, 0.0] N at x=-0.1,+0.1 m.

3. The weighted contact location is COP x=-0.100000 m.

4. COM x=0.02 m has signed margin 0.120000 m inside the illustrative outer edges.

5. The gravity/COP moment difference is 11.772000 Nm.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

One contact resultant has zero load; do not treat both point contacts as equally active support.

The .14 m outer edges are teaching geometry; real support requires measured foot patches and contact state.

### K. Failure modes and troubleshooting

Expanding the support hull with unloaded feet; confusing COP and COM; dividing by total contact force near zero.

### L. Practical exercises and extension tasks

1. Vary COM x and find the load split needed for zero pitch moment.

2. Replace point contacts with measured foot corners and compute a convex hull.

3. Simulate a lifting foot and update the active support set.

### M. Connection to the Asimov research platform

Foot contact sensing may require estimation; simulation contact truth must not be silently substituted for unavailable hardware force sensors.

### N. Completion record

Record your chosen case, predicted trend, measured cop_x_m, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 19, Linear inverted pendulum prediction and capture-point intuition. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 19 - Linear inverted pendulum prediction and capture-point intuition

### A. The engineering question

The linear inverted pendulum model approximates horizontal COM motion at fixed height above a support plane.

### B. Concepts and mathematical model

Its unstable mode explains why a small COM displacement can grow without corrective contact placement. The capture point combines position and velocity into a location associated with stopping the divergent motion under the model assumptions. It is useful intuition, but variable height, angular momentum, foot limits and impact dynamics can invalidate the simplified prediction.

omega=sqrt(g/h); x_ddot=omega^2*(x-zmp); capture point xi=x+x_dot/omega.

### C. Real-world meaning and limits

Validate fixed-height and contact assumptions before using LIPM predictions in an actual humanoid controller.

### D. Architecture and data flow

Configuration (height, horizon) -> numerical model -> natural_rate_per_s, final_com_x_m, final_speed_m_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

height is fixed COM height in meters; horizon is seconds; the model assumes a constant planar ZMP.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| height | 0.6 | Defined by the explicit chapter model and parameter contract |
| horizon | 0.3 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/19_lipm.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only height changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/19_lipm.py --case 0

.venv-book/bin/python expanded_lab/modules/19_lipm.py --case 3

.venv-book/bin/python expanded_lab/run.py lipm --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/19_lipm.py

### H. Walkthrough and design decisions

The exact hyperbolic solution avoids confusing integration error with the physical instability of the approximation. Compare the growth factor across heights while keeping initial state fixed.

### I. Expected behavior and six worked cases

The controlled variable is height. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/19_lipm.png

Figure L19. natural rate per s as height changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | height | natural rate per s |
|---|---|---|
| 0 | 0.3 | 5.71839138 |
| 1 | 0.4 | 4.95227221 |
| 2 | 0.5 | 4.42944692 |
| 3 | 0.6 | 4.04351332 |
| 4 | 0.8 | 3.50178526 |
| 5 | 1 | 3.13209195 |

#### Worked case 0: height = 0.3

This case keeps the nominal configuration except for height=0.3. The full input is {"height": 0.3, "horizon": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural rate per s | 5.71839138 |
| final com x m | 0.08091342 |
| final speed m s | 0.45111675 |
| initial capture point m | 0.02874372 |
| divergent growth factor | 5.55955136 |

1. At height 0.3 m, omega=sqrt(9.81/h)=5.718391 per second.

2. Start at x0=0.02 m and v0=0.05 m/s with ZMP zero.

3. Over 0.3 s, the hyperbolic solution predicts x=0.080913 m and v=0.451117 m/s.

4. The initial capture-point coordinate is 0.028744 m.

5. The divergent mode multiplies by exp(omega*T)=5.559551.

#### Worked case 1: height = 0.4

This case keeps the nominal configuration except for height=0.4. The full input is {"height": 0.4, "horizon": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural rate per s | 4.95227221 |
| final com x m | 0.06760336 |
| final speed m s | 0.32368892 |
| initial capture point m | 0.03009638 |
| divergent growth factor | 4.41797595 |

1. At height 0.4 m, omega=sqrt(9.81/h)=4.952272 per second.

2. Start at x0=0.02 m and v0=0.05 m/s with ZMP zero.

3. Over 0.3 s, the hyperbolic solution predicts x=0.067603 m and v=0.323689 m/s.

4. The initial capture-point coordinate is 0.030096 m.

5. The divergent mode multiplies by exp(omega*T)=4.417976.

#### Worked case 2: height = 0.5

This case keeps the nominal configuration except for height=0.5. The full input is {"height": 0.5, "horizon": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural rate per s | 4.42944692 |
| final com x m | 0.06023528 |
| final speed m s | 0.25659119 |
| initial capture point m | 0.03128809 |
| divergent growth factor | 3.77663755 |

1. At height 0.5 m, omega=sqrt(9.81/h)=4.429447 per second.

2. Start at x0=0.02 m and v0=0.05 m/s with ZMP zero.

3. Over 0.3 s, the hyperbolic solution predicts x=0.060235 m and v=0.256591 m/s.

4. The initial capture-point coordinate is 0.031288 m.

5. The divergent mode multiplies by exp(omega*T)=3.776638.

#### Worked case 3: height = 0.6

This case keeps the nominal configuration except for height=0.6. The full input is {"height": 0.6, "horizon": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural rate per s | 4.04351332 |
| final com x m | 0.05556939 |
| final speed m s | 0.21551822 |
| initial capture point m | 0.03236548 |
| divergent growth factor | 3.36374184 |

1. At height 0.6 m, omega=sqrt(9.81/h)=4.043513 per second.

2. Start at x0=0.02 m and v0=0.05 m/s with ZMP zero.

3. Over 0.3 s, the hyperbolic solution predicts x=0.055569 m and v=0.215518 m/s.

4. The initial capture-point coordinate is 0.032365 m.

5. The divergent mode multiplies by exp(omega*T)=3.363742.

#### Worked case 4: height = 0.8

This case keeps the nominal configuration except for height=0.8. The full input is {"height": 0.8, "horizon": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural rate per s | 3.50178526 |
| final com x m | 0.0500047 |
| final speed m s | 0.16809822 |
| initial capture point m | 0.03427843 |
| divergent growth factor | 2.85918202 |

1. At height 0.8 m, omega=sqrt(9.81/h)=3.501785 per second.

2. Start at x0=0.02 m and v0=0.05 m/s with ZMP zero.

3. Over 0.3 s, the hyperbolic solution predicts x=0.050005 m and v=0.168098 m/s.

4. The initial capture-point coordinate is 0.034278 m.

5. The divergent mode multiplies by exp(omega*T)=2.859182.

#### Worked case 5: height = 1

This case keeps the nominal configuration except for height=1. The full input is {"height": 1.0, "horizon": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural rate per s | 3.13209195 |
| final com x m | 0.04680478 |
| final speed m s | 0.14165678 |
| initial capture point m | 0.03596377 |
| divergent growth factor | 2.55902822 |

1. At height 1 m, omega=sqrt(9.81/h)=3.132092 per second.

2. Start at x0=0.02 m and v0=0.05 m/s with ZMP zero.

3. Over 0.3 s, the hyperbolic solution predicts x=0.046805 m and v=0.141657 m/s.

4. The initial capture-point coordinate is 0.035964 m.

5. The divergent mode multiplies by exp(omega*T)=2.559028.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

A fixed support point does not recover the displaced state in this open-loop model.

A predicted capture point outside reachable/contact-feasible support is a warning, not an invitation to command an impossible step.

### K. Failure modes and troubleshooting

Treating the capture point as a complete gait planner; ignoring available foot motion and contact torque limits.

### L. Practical exercises and extension tasks

1. Set initial velocity so the divergent component cancels for a chosen support point.

2. Compare exact prediction with a numerical integrator.

3. Add a bounded ZMP choice and test feasibility against support edges.

### M. Connection to the Asimov research platform

Validate fixed-height and contact assumptions before using LIPM predictions in an actual humanoid controller.

### N. Completion record

Record your chosen case, predicted trend, measured natural_rate_per_s, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 20, Friction cones, slip feasibility and contact margins. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 20 - Friction cones, slip feasibility and contact margins

### A. The engineering question

A contact can push but usually cannot pull, and its tangential force is limited by friction and normal load.

### B. Concepts and mathematical model

This simple inequality couples balance and propulsion: reducing normal load reduces available horizontal force. A friction coefficient is not a universal property independent of surfaces, wear or contamination. This laboratory evaluates a requested horizontal acceleration under a Coulomb-friction approximation and distinguishes feasibility margin from a measured slip guarantee.

||F_t|| <= mu*F_n; F_t_required=m*a; margin=mu*F_n-||F_t_required||.

### C. Real-world meaning and limits

Real foot-ground interaction needs measurement across the intended surfaces and support states; simulation friction tuning is not certification.

### D. Architecture and data flow

Configuration (mass, mu, acceleration, supported_fraction) -> numerical model -> normal_force_N, tangential_required_N, friction_capacity_N -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

mass is kilograms; mu is dimensionless assumed friction; acceleration is m/s^2; supported_fraction scales normal loading.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| mass | 10 | kilograms |
| mu | 0.6 | Defined by the explicit chapter model and parameter contract |
| acceleration | 2 | SI acceleration in the chapter equation |
| supported_fraction | 1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/20_friction_cone.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only mu changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/20_friction_cone.py --case 0

.venv-book/bin/python expanded_lab/modules/20_friction_cone.py --case 3

.venv-book/bin/python expanded_lab/run.py friction_cone --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/20_friction_cone.py

### H. Walkthrough and design decisions

Calculate load before friction capacity and compare force magnitudes. Utilization makes conditions comparable, but remains conditional on the assumed normal force and coefficient.

### I. Expected behavior and six worked cases

The controlled variable is mu. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/20_friction_cone.png

Figure L20. normal force N as mu changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | mu | normal force N |
|---|---|---|
| 0 | 0.1 | 98.1 |
| 1 | 0.2 | 98.1 |
| 2 | 0.3 | 98.1 |
| 3 | 0.4 | 98.1 |
| 4 | 0.6 | 98.1 |
| 5 | 0.8 | 98.1 |

#### Worked case 0: mu = 0.1

This case keeps the nominal configuration except for mu=0.1. The full input is {"acceleration": 2.0, "mass": 10.0, "mu": 0.1, "supported_fraction": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| normal force N | 98.1 |
| tangential required N | 20 |
| friction capacity N | 9.81 |
| force margin N | -10.19 |
| utilization | 2.03873598 |
| cone half angle rad | 0.09966865 |

1. The modeled normal force is 98.100000 N.

2. Acceleration 2 m/s^2 requires horizontal force 20.000000 N.

3. At mu=0.1, Coulomb capacity is 9.810000 N.

4. Margin is -10.190000 N and utilization is 2.038736.

5. The friction-cone half angle is atan(mu)=0.099669 rad.

#### Worked case 1: mu = 0.2

This case keeps the nominal configuration except for mu=0.2. The full input is {"acceleration": 2.0, "mass": 10.0, "mu": 0.2, "supported_fraction": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| normal force N | 98.1 |
| tangential required N | 20 |
| friction capacity N | 19.62 |
| force margin N | -0.38 |
| utilization | 1.01936799 |
| cone half angle rad | 0.19739556 |

1. The modeled normal force is 98.100000 N.

2. Acceleration 2 m/s^2 requires horizontal force 20.000000 N.

3. At mu=0.2, Coulomb capacity is 19.620000 N.

4. Margin is -0.380000 N and utilization is 1.019368.

5. The friction-cone half angle is atan(mu)=0.197396 rad.

#### Worked case 2: mu = 0.3

This case keeps the nominal configuration except for mu=0.3. The full input is {"acceleration": 2.0, "mass": 10.0, "mu": 0.3, "supported_fraction": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| normal force N | 98.1 |
| tangential required N | 20 |
| friction capacity N | 29.43 |
| force margin N | 9.43 |
| utilization | 0.67957866 |
| cone half angle rad | 0.29145679 |

1. The modeled normal force is 98.100000 N.

2. Acceleration 2 m/s^2 requires horizontal force 20.000000 N.

3. At mu=0.3, Coulomb capacity is 29.430000 N.

4. Margin is 9.430000 N and utilization is 0.679579.

5. The friction-cone half angle is atan(mu)=0.291457 rad.

The requested force is inside the modeled friction bound.

#### Worked case 3: mu = 0.4

This case keeps the nominal configuration except for mu=0.4. The full input is {"acceleration": 2.0, "mass": 10.0, "mu": 0.4, "supported_fraction": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| normal force N | 98.1 |
| tangential required N | 20 |
| friction capacity N | 39.24 |
| force margin N | 19.24 |
| utilization | 0.509684 |
| cone half angle rad | 0.38050638 |

1. The modeled normal force is 98.100000 N.

2. Acceleration 2 m/s^2 requires horizontal force 20.000000 N.

3. At mu=0.4, Coulomb capacity is 39.240000 N.

4. Margin is 19.240000 N and utilization is 0.509684.

5. The friction-cone half angle is atan(mu)=0.380506 rad.

The requested force is inside the modeled friction bound.

#### Worked case 4: mu = 0.6

This case keeps the nominal configuration except for mu=0.6. The full input is {"acceleration": 2.0, "mass": 10.0, "mu": 0.6, "supported_fraction": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| normal force N | 98.1 |
| tangential required N | 20 |
| friction capacity N | 58.86 |
| force margin N | 38.86 |
| utilization | 0.33978933 |
| cone half angle rad | 0.5404195 |

1. The modeled normal force is 98.100000 N.

2. Acceleration 2 m/s^2 requires horizontal force 20.000000 N.

3. At mu=0.6, Coulomb capacity is 58.860000 N.

4. Margin is 38.860000 N and utilization is 0.339789.

5. The friction-cone half angle is atan(mu)=0.540420 rad.

The requested force is inside the modeled friction bound.

#### Worked case 5: mu = 0.8

This case keeps the nominal configuration except for mu=0.8. The full input is {"acceleration": 2.0, "mass": 10.0, "mu": 0.8, "supported_fraction": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| normal force N | 98.1 |
| tangential required N | 20 |
| friction capacity N | 78.48 |
| force margin N | 58.48 |
| utilization | 0.254842 |
| cone half angle rad | 0.67474094 |

1. The modeled normal force is 98.100000 N.

2. Acceleration 2 m/s^2 requires horizontal force 20.000000 N.

3. At mu=0.8, Coulomb capacity is 78.480000 N.

4. Margin is 58.480000 N and utilization is 0.254842.

5. The friction-cone half angle is atan(mu)=0.674741 rad.

The requested force is inside the modeled friction bound.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The requested force exceeds the modeled friction capacity; a controller must reduce demand or change support.

This static feasibility check excludes torsional friction, impact, compliance and changing normal force.

### K. Failure modes and troubleshooting

Using visual foot contact as proof of load; making friction arbitrarily large to rescue a bad gait; ignoring unloading during stepping.

### L. Practical exercises and extension tasks

1. Reduce normal support fraction while keeping horizontal demand fixed.

2. Include a lateral acceleration and use the vector norm.

3. Estimate a conservative friction interval and evaluate worst-case feasibility.

### M. Connection to the Asimov research platform

Real foot-ground interaction needs measurement across the intended surfaces and support states; simulation friction tuning is not certification.

### N. Completion record

Record your chosen case, predicted trend, measured normal_force_N, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 21, Second-order joint dynamics and PD tuning. Keep the present result as a reference fixture for diagnosing changes in the larger stack.
