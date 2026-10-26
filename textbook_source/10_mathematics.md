# Part VI - Mathematical foundations in depth

The following ten laboratories develop the language used by every later robot component: units, vectors, rotations, transforms, derivatives, fitting, numerical integration, uncertainty and sampling. Work through the derivations before running the code. A number should carry its unit and frame all the way from a sensor through an algorithm into a log. The examples are intentionally small enough to calculate by hand and large enough to expose errors that disappear in a trivial zero-pose test.

## Laboratory 1 - Units, dimensional reasoning and motor-speed conversion

### A. The engineering question

A number without a unit is an incomplete interface.

### B. Concepts and mathematical model

Radians are dimensionless in dimensional analysis, but treating an angle as interchangeable with a count or degree is a software error. Start from the quantity you want, write the conversion chain, and cancel the units before calculating. A gearbox changes both angular speed and available torque; it does not create power. Efficiency represents loss, while a gear ratio represents an ideal geometric relationship. This experiment keeps input and output shaft quantities separate and exposes why an RPM value cannot be sent straight to a radians-per-second controller.

omega_motor = RPM*2*pi/60; omega_joint = omega_motor/G; tau_joint = eta*G*tau_motor; P = tau*omega.

### C. Real-world meaning and limits

Confirm whether a vendor encoder reports motor-shaft or output-shaft position before applying a ratio. Actual Asimov actuator settings must come from its confirmed release.

### D. Architecture and data flow

Configuration (rpm, ratio, motor_torque, efficiency) -> numerical model -> joint_speed_rad_s, joint_torque_Nm, input_power_W -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

RPM is motor-shaft speed; ratio is motor revolutions per output revolution; motor_torque is shaft Nm; efficiency is a fraction.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| rpm | 1200 | motor revolutions per minute |
| ratio | 36 | dimensionless motor/output ratio |
| motor_torque | 0.3 | Nm |
| efficiency | 0.8 | fraction |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/01_units.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only ratio changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/01_units.py --case 0

.venv-book/bin/python expanded_lab/modules/01_units.py --case 3

.venv-book/bin/python expanded_lab/run.py units --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/01_units.py

### H. Walkthrough and design decisions

Trace the speed conversion first, then the torque relation, then check power. The recovered RPM assertion is a round-trip invariant; it catches a conversion direction error that a plausible-looking output torque would not.

### I. Expected behavior and six worked cases

The controlled variable is ratio. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/01_units.png

Figure L1. joint speed rad s as ratio changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | ratio | joint speed rad s |
|---|---|---|
| 0 | 6 | 20.94395102 |
| 1 | 12 | 10.47197551 |
| 2 | 25 | 5.02654825 |
| 3 | 36 | 3.4906585 |
| 4 | 50 | 2.51327412 |
| 5 | 100 | 1.25663706 |

#### Worked case 0: ratio = 6

This case keeps the nominal configuration except for ratio=6. The full input is {"efficiency": 0.8, "motor_torque": 0.3, "ratio": 6.0, "rpm": 1200.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| joint speed rad s | 20.94395102 |
| joint torque Nm | 1.44 |
| input power W | 37.69911184 |
| output power W | 30.15928947 |
| loss W | 7.53982237 |

1. Motor speed: 1200 rev/min times 2*pi/60 = 125.663706 rad/s.

2. Divide by ratio 6: output speed = 20.943951 rad/s.

3. Multiply input torque 0.3 Nm by ratio and efficiency: 1.440000 Nm.

4. Input mechanical power = 37.699112 W; output = 30.159289 W.

5. The difference, 7.539822 W, is modeled mechanical loss.

#### Worked case 1: ratio = 12

This case keeps the nominal configuration except for ratio=12. The full input is {"efficiency": 0.8, "motor_torque": 0.3, "ratio": 12.0, "rpm": 1200.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| joint speed rad s | 10.47197551 |
| joint torque Nm | 2.88 |
| input power W | 37.69911184 |
| output power W | 30.15928947 |
| loss W | 7.53982237 |

1. Motor speed: 1200 rev/min times 2*pi/60 = 125.663706 rad/s.

2. Divide by ratio 12: output speed = 10.471976 rad/s.

3. Multiply input torque 0.3 Nm by ratio and efficiency: 2.880000 Nm.

4. Input mechanical power = 37.699112 W; output = 30.159289 W.

5. The difference, 7.539822 W, is modeled mechanical loss.

#### Worked case 2: ratio = 25

This case keeps the nominal configuration except for ratio=25. The full input is {"efficiency": 0.8, "motor_torque": 0.3, "ratio": 25.0, "rpm": 1200.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| joint speed rad s | 5.02654825 |
| joint torque Nm | 6 |
| input power W | 37.69911184 |
| output power W | 30.15928947 |
| loss W | 7.53982237 |

1. Motor speed: 1200 rev/min times 2*pi/60 = 125.663706 rad/s.

2. Divide by ratio 25: output speed = 5.026548 rad/s.

3. Multiply input torque 0.3 Nm by ratio and efficiency: 6.000000 Nm.

4. Input mechanical power = 37.699112 W; output = 30.159289 W.

5. The difference, 7.539822 W, is modeled mechanical loss.

#### Worked case 3: ratio = 36

This case keeps the nominal configuration except for ratio=36. The full input is {"efficiency": 0.8, "motor_torque": 0.3, "ratio": 36.0, "rpm": 1200.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| joint speed rad s | 3.4906585 |
| joint torque Nm | 8.64 |
| input power W | 37.69911184 |
| output power W | 30.15928947 |
| loss W | 7.53982237 |

1. Motor speed: 1200 rev/min times 2*pi/60 = 125.663706 rad/s.

2. Divide by ratio 36: output speed = 3.490659 rad/s.

3. Multiply input torque 0.3 Nm by ratio and efficiency: 8.640000 Nm.

4. Input mechanical power = 37.699112 W; output = 30.159289 W.

5. The difference, 7.539822 W, is modeled mechanical loss.

#### Worked case 4: ratio = 50

This case keeps the nominal configuration except for ratio=50. The full input is {"efficiency": 0.8, "motor_torque": 0.3, "ratio": 50.0, "rpm": 1200.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| joint speed rad s | 2.51327412 |
| joint torque Nm | 12 |
| input power W | 37.69911184 |
| output power W | 30.15928947 |
| loss W | 7.53982237 |

1. Motor speed: 1200 rev/min times 2*pi/60 = 125.663706 rad/s.

2. Divide by ratio 50: output speed = 2.513274 rad/s.

3. Multiply input torque 0.3 Nm by ratio and efficiency: 12.000000 Nm.

4. Input mechanical power = 37.699112 W; output = 30.159289 W.

5. The difference, 7.539822 W, is modeled mechanical loss.

#### Worked case 5: ratio = 100

This case keeps the nominal configuration except for ratio=100. The full input is {"efficiency": 0.8, "motor_torque": 0.3, "ratio": 100.0, "rpm": 1200.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| joint speed rad s | 1.25663706 |
| joint torque Nm | 24 |
| input power W | 37.69911184 |
| output power W | 30.15928947 |
| loss W | 7.53982237 |

1. Motor speed: 1200 rev/min times 2*pi/60 = 125.663706 rad/s.

2. Divide by ratio 100: output speed = 1.256637 rad/s.

3. Multiply input torque 0.3 Nm by ratio and efficiency: 24.000000 Nm.

4. Input mechanical power = 37.699112 W; output = 30.159289 W.

5. The difference, 7.539822 W, is modeled mechanical loss.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The ideal power ratio is reduced to 0.800; a torque increase does not imply a power increase.

This constant-efficiency model excludes speed-dependent loss, driver current and thermal limits.

### K. Failure modes and troubleshooting

Confusing motor current with output torque; forgetting 60 seconds per minute; using peak torque as a continuous operating point.

### L. Practical exercises and extension tasks

1. Hold output speed constant while increasing ratio: calculate the required motor speed.

2. Set efficiency to one and prove input/output mechanical power agree.

3. Introduce a 5% torque-constant error and propagate it to output torque.

### M. Connection to the Asimov research platform

Confirm whether a vendor encoder reports motor-shaft or output-shaft position before applying a ratio. Actual Asimov actuator settings must come from its confirmed release.

### N. Completion record

Record your chosen case, predicted trend, measured joint_speed_rad_s, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 2, Vectors, projections and joint-axis torque. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 2 - Vectors, projections and joint-axis torque

### A. The engineering question

A force vector contains both magnitude and direction.

### B. Concepts and mathematical model

The moment about an origin is r cross F, where r points from that origin to the point of application. A joint only responds to the component of that moment along its rotation axis. This explains why the same external force can produce different joint torques at different poses. A projection is meaningful only when both vectors are expressed in the same coordinate frame and the axis is normalized. In this laboratory the changing lever length is geometric; it is not an actuator specification.

moment = r cross F; tau_axis = axis dot moment; F_parallel = axis*(axis dot F).

### C. Real-world meaning and limits

A limb load must be transformed into each joint frame along the chain; this is the foundation of Jacobian-transpose force mapping.

### D. Architecture and data flow

Configuration (length, force, angle_deg) -> numerical model -> axis_torque_Nm, force_perpendicular_N, force_magnitude_N -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

length is the lever in meters; force is Newtons; angle_deg is the angle from the lever toward the applied force.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| length | 0.2 | meters |
| force | 50 | Newtons |
| angle_deg | 60 | degrees |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/02_vectors.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only angle_deg changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/02_vectors.py --case 0

.venv-book/bin/python expanded_lab/modules/02_vectors.py --case 3

.venv-book/bin/python expanded_lab/run.py vectors --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/02_vectors.py

### H. Walkthrough and design decisions

Cross-product order determines sign. The scalar check against length times perpendicular force gives a separate geometric verification. Negative angles are a useful extension because the sign should reverse.

### I. Expected behavior and six worked cases

The controlled variable is angle_deg. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/02_vectors.png

Figure L2. axis torque Nm as angle_deg changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | angle_deg | axis torque Nm |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 15 | 2.58819045 |
| 2 | 30 | 5 |
| 3 | 45 | 7.07106781 |
| 4 | 60 | 8.66025404 |
| 5 | 90 | 10 |

#### Worked case 0: angle_deg = 0

This case keeps the nominal configuration except for angle_deg=0. The full input is {"angle_deg": 0.0, "force": 50.0, "length": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| axis torque Nm | 0 |
| force perpendicular N | 0 |
| force magnitude N | 50 |
| lever m | 0.2 |

1. Force components in the chosen frame: Fx=50.000000 N, Fy=0.000000 N.

2. The lever is (0.200000, 0, 0) m, so only Fy contributes to the z moment.

3. r cross F gives Mz=0.000000 Nm.

4. Projection onto the unit z axis gives torque 0.000000 Nm.

#### Worked case 1: angle_deg = 15

This case keeps the nominal configuration except for angle_deg=15. The full input is {"angle_deg": 15.0, "force": 50.0, "length": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| axis torque Nm | 2.58819045 |
| force perpendicular N | 12.94095226 |
| force magnitude N | 50 |
| lever m | 0.2 |

1. Force components in the chosen frame: Fx=48.296291 N, Fy=12.940952 N.

2. The lever is (0.200000, 0, 0) m, so only Fy contributes to the z moment.

3. r cross F gives Mz=2.588190 Nm.

4. Projection onto the unit z axis gives torque 2.588190 Nm.

The effective perpendicular force is 12.940952 N, rather than the full 50 N.

#### Worked case 2: angle_deg = 30

This case keeps the nominal configuration except for angle_deg=30. The full input is {"angle_deg": 30.0, "force": 50.0, "length": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| axis torque Nm | 5 |
| force perpendicular N | 25 |
| force magnitude N | 50 |
| lever m | 0.2 |

1. Force components in the chosen frame: Fx=43.301270 N, Fy=25.000000 N.

2. The lever is (0.200000, 0, 0) m, so only Fy contributes to the z moment.

3. r cross F gives Mz=5.000000 Nm.

4. Projection onto the unit z axis gives torque 5.000000 Nm.

The effective perpendicular force is 25.000000 N, rather than the full 50 N.

#### Worked case 3: angle_deg = 45

This case keeps the nominal configuration except for angle_deg=45. The full input is {"angle_deg": 45.0, "force": 50.0, "length": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| axis torque Nm | 7.07106781 |
| force perpendicular N | 35.35533906 |
| force magnitude N | 50 |
| lever m | 0.2 |

1. Force components in the chosen frame: Fx=35.355339 N, Fy=35.355339 N.

2. The lever is (0.200000, 0, 0) m, so only Fy contributes to the z moment.

3. r cross F gives Mz=7.071068 Nm.

4. Projection onto the unit z axis gives torque 7.071068 Nm.

The effective perpendicular force is 35.355339 N, rather than the full 50 N.

#### Worked case 4: angle_deg = 60

This case keeps the nominal configuration except for angle_deg=60. The full input is {"angle_deg": 60.0, "force": 50.0, "length": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| axis torque Nm | 8.66025404 |
| force perpendicular N | 43.30127019 |
| force magnitude N | 50 |
| lever m | 0.2 |

1. Force components in the chosen frame: Fx=25.000000 N, Fy=43.301270 N.

2. The lever is (0.200000, 0, 0) m, so only Fy contributes to the z moment.

3. r cross F gives Mz=8.660254 Nm.

4. Projection onto the unit z axis gives torque 8.660254 Nm.

The effective perpendicular force is 43.301270 N, rather than the full 50 N.

#### Worked case 5: angle_deg = 90

This case keeps the nominal configuration except for angle_deg=90. The full input is {"angle_deg": 90.0, "force": 50.0, "length": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| axis torque Nm | 10 |
| force perpendicular N | 50 |
| force magnitude N | 50 |
| lever m | 0.2 |

1. Force components in the chosen frame: Fx=0.000000 N, Fy=50.000000 N.

2. The lever is (0.200000, 0, 0) m, so only Fy contributes to the z moment.

3. r cross F gives Mz=10.000000 Nm.

4. Projection onto the unit z axis gives torque 10.000000 Nm.

The effective perpendicular force is 50.000000 N, rather than the full 50 N.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The effective perpendicular force is 0.000000 N, rather than the full 50 N.

Changing origin changes moment; changing coordinates consistently does not change its physical meaning.

### K. Failure modes and troubleshooting

Using an unnormalized axis; swapping r cross F with F cross r; adding vectors from world and body coordinates.

### L. Practical exercises and extension tasks

1. Rotate r and F by the same rotation and verify the transformed moment.

2. Reverse the force and verify torque sign reversal.

3. Find the force angle that produces half the maximum joint moment.

### M. Connection to the Asimov research platform

A limb load must be transformed into each joint frame along the chain; this is the foundation of Jacobian-transpose force mapping.

### N. Completion record

Record your chosen case, predicted trend, measured axis_torque_Nm, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 3, Rotation matrices and the Rodrigues formula. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 3 - Rotation matrices and the Rodrigues formula

### A. The engineering question

A valid rotation preserves lengths and angles.

### B. Concepts and mathematical model

Its columns form an orthonormal right-handed basis. The Rodrigues formula constructs a rotation from a unit axis and an angle using the skew-symmetric cross-product matrix. This is more informative than memorizing three unrelated Euler-angle matrices because it makes the axis explicit. Rotation composition is generally noncommutative: rotating about x and then z differs from rotating about z and then x. Numerical checks should test orthogonality and determinant, not only whether a transformed vector looks plausible.

R = I + sin(theta)*K + (1-cos(theta))*K*K, where K*v = axis cross v.

### C. Real-world meaning and limits

IMU-to-pelvis and camera-to-head rotations must be calibrated and tested with physical reference orientations.

### D. Architecture and data flow

Configuration (angle_deg) -> numerical model -> rotated_x_m, rotated_y_m, rotated_z_m -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

angle_deg is a right-handed active rotation about the normalized axis (1,2,3). Input and output vectors use one fixed basis.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| angle_deg | 45 | degrees |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/03_rotations.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only angle_deg changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/03_rotations.py --case 0

.venv-book/bin/python expanded_lab/modules/03_rotations.py --case 3

.venv-book/bin/python expanded_lab/run.py rotations --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/03_rotations.py

### H. Walkthrough and design decisions

The skew matrix encodes the cross product. The quadratic term leaves the component along the axis unchanged while rotating the perpendicular component. Transpose is the inverse only after the rotation validity checks pass.

### I. Expected behavior and six worked cases

The controlled variable is angle_deg. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/03_rotations.png

Figure L3. rotated x m as angle_deg changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | angle_deg | rotated x m |
|---|---|---|
| 0 | 0 | 0.3 |
| 1 | 15 | 0.40386084 |
| 2 | 45 | 0.54379293 |
| 3 | 90 | 0.52761799 |
| 4 | 135 | 0.26095022 |
| 5 | 180 | -0.1 |

#### Worked case 0: angle_deg = 0

This case keeps the nominal configuration except for angle_deg=0. The full input is {"angle_deg": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| rotated x m | 0.3 |
| rotated y m | -0.2 |
| rotated z m | 0.5 |
| orthogonality error | 0 |
| roundtrip error m | 0 |

1. Normalize axis (1,2,3) to [0.2672612419124244, 0.5345224838248488, 0.8017837257372732].

2. Convert 0 degrees to 0.000000 radians.

3. Assemble the skew matrix and evaluate Rodrigues; determinant is 1.000000000000.

4. R times (0.3,-0.2,0.5) gives [0.3, -0.2, 0.5] meters.

5. Transpose the rotation to recover the original vector; residual is 0.000e+00 m.

#### Worked case 1: angle_deg = 15

This case keeps the nominal configuration except for angle_deg=15. The full input is {"angle_deg": 15.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| rotated x m | 0.40386084 |
| rotated y m | -0.15870141 |
| rotated z m | 0.43784733 |
| orthogonality error | 1.2244318e-16 |
| roundtrip error m | 5.5511151e-17 |

1. Normalize axis (1,2,3) to [0.2672612419124244, 0.5345224838248488, 0.8017837257372732].

2. Convert 15 degrees to 0.261799 radians.

3. Assemble the skew matrix and evaluate Rodrigues; determinant is 1.000000000000.

4. R times (0.3,-0.2,0.5) gives [0.4038608443373136, -0.15870141074575236, 0.4378473257180637] meters.

5. Transpose the rotation to recover the original vector; residual is 5.551e-17 m.

#### Worked case 2: angle_deg = 45

This case keeps the nominal configuration except for angle_deg=45. The full input is {"angle_deg": 45.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| rotated x m | 0.54379293 |
| rotated y m | -0.00724982 |
| rotated z m | 0.29023557 |
| orthogonality error | 2.4194837e-16 |
| roundtrip error m | 6.2063354e-17 |

1. Normalize axis (1,2,3) to [0.2672612419124244, 0.5345224838248488, 0.8017837257372732].

2. Convert 45 degrees to 0.785398 radians.

3. Assemble the skew matrix and evaluate Rodrigues; determinant is 1.000000000000.

4. R times (0.3,-0.2,0.5) gives [0.5437929346446913, -0.007249817872773581, 0.29023556703361864] meters.

5. Transpose the rotation to recover the original vector; residual is 6.206e-17 m.

#### Worked case 3: angle_deg = 90

This case keeps the nominal configuration except for angle_deg=90. The full input is {"angle_deg": 90.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| rotated x m | 0.52761799 |
| rotated y m | 0.3069045 |
| rotated z m | 0.08619101 |
| orthogonality error | 3.3322248e-16 |
| roundtrip error m | 7.8504623e-17 |

1. Normalize axis (1,2,3) to [0.2672612419124244, 0.5345224838248488, 0.8017837257372732].

2. Convert 90 degrees to 1.570796 radians.

3. Assemble the skew matrix and evaluate Rodrigues; determinant is 1.000000000000.

4. R times (0.3,-0.2,0.5) gives [0.5276179870598791, 0.3069044967649697, 0.08619100647006048] meters.

5. Transpose the rotation to recover the original vector; residual is 7.850e-17 m.

#### Worked case 4: angle_deg = 135

This case keeps the nominal configuration except for angle_deg=135. The full input is {"angle_deg": 135.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| rotated x m | 0.26095022 |
| rotated y m | 0.55843561 |
| rotated z m | 0.00739285 |
| orthogonality error | 3.3907847e-16 |
| roundtrip error m | 1.3877788e-16 |

1. Normalize axis (1,2,3) to [0.2672612419124244, 0.5345224838248488, 0.8017837257372732].

2. Convert 135 degrees to 2.356194 radians.

3. Assemble the skew matrix and evaluate Rodrigues; determinant is 1.000000000000.

4. R times (0.3,-0.2,0.5) gives [0.26095022217007235, 0.5584356070764644, 0.00739285455899949] meters.

5. Transpose the rotation to recover the original vector; residual is 1.388e-16 m.

#### Worked case 5: angle_deg = 180

This case keeps the nominal configuration except for angle_deg=180. The full input is {"angle_deg": 180.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| rotated x m | -0.1 |
| rotated y m | 0.6 |
| rotated z m | 0.1 |
| orthogonality error | 3.7233036e-16 |
| roundtrip error m | 1.3597400e-16 |

1. Normalize axis (1,2,3) to [0.2672612419124244, 0.5345224838248488, 0.8017837257372732].

2. Convert 180 degrees to 3.141593 radians.

3. Assemble the skew matrix and evaluate Rodrigues; determinant is 1.000000000000.

4. R times (0.3,-0.2,0.5) gives [-0.09999999999999995, 0.6000000000000001, 0.0999999999999999] meters.

5. Transpose the rotation to recover the original vector; residual is 1.360e-16 m.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

A determinant near one does not alone guarantee orthogonality; both tests are retained.

The chosen axis and vector are teaching geometry, unrelated to an unverified motor mounting.

### K. Failure modes and troubleshooting

Treating a reflection with determinant -1 as a rotation; transposing only one factor in a composed transformation.

### L. Practical exercises and extension tasks

1. Verify the axis vector is unchanged by its own rotation.

2. Compare x-then-z and z-then-x rotations.

3. Add a small matrix perturbation and observe which validity test detects it.

### M. Connection to the Asimov research platform

IMU-to-pelvis and camera-to-head rotations must be calibrated and tested with physical reference orientations.

### N. Completion record

Record your chosen case, predicted trend, measured rotated_x_m, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 4, Unit quaternions, sign equivalence and incremental attitude. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 4 - Unit quaternions, sign equivalence and incremental attitude

### A. The engineering question

Quaternions avoid the coordinate singularities of a three-angle parameterization, but they introduce a unit constraint and a component-order convention.

### B. Concepts and mathematical model

A quaternion and its negative represent the same physical rotation. Comparing their components with ordinary Euclidean distance can therefore report a large difference for identical attitudes. For constant angular velocity, an exact axis-angle increment can be composed each timestep. This is a simple reference against which to test a differential integrator and normalization policy.

q_increment = [cos(|omega|*dt/2), axis*sin(|omega|*dt/2)]; q_next = q*q_increment; angular error = 2*acos(|q1 dot q2|).

### C. Real-world meaning and limits

Real gyro integration needs calibrated axes, bias estimation, timestamp handling and external correction for drift.

### D. Architecture and data flow

Configuration (dt, duration, rate) -> numerical model -> final_w, final_z, angle_error_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

dt and duration are seconds; rate is constant body-z angular speed in rad/s; quaternion order is w,x,y,z.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| dt | 0.01 | seconds |
| duration | 2 | seconds |
| rate | 0.7 | rad/s |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/04_quaternions.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only dt changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/04_quaternions.py --case 0

.venv-book/bin/python expanded_lab/modules/04_quaternions.py --case 3

.venv-book/bin/python expanded_lab/run.py quaternions --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/04_quaternions.py

### H. Walkthrough and design decisions

The Hamilton product is written explicitly so component order and multiplication side are inspectable. Normalizing after composition controls floating-point drift, while the exact solution supplies an independent check.

### I. Expected behavior and six worked cases

The controlled variable is dt. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/04_quaternions.png

Figure L4. final w as dt changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | dt | final w |
|---|---|---|
| 0 | 0.001 | 0.76484219 |
| 1 | 0.002 | 0.76484219 |
| 2 | 0.005 | 0.76484219 |
| 3 | 0.01 | 0.76484219 |
| 4 | 0.02 | 0.76484219 |
| 5 | 0.05 | 0.76484219 |

#### Worked case 0: dt = 0.001

This case keeps the nominal configuration except for dt=0.001. The full input is {"dt": 0.001, "duration": 2.0, "rate": 0.7}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final w | 0.76484219 |
| final z | 0.64421769 |
| angle error rad | 0 |
| sign equivalence error rad | 0 |
| actual duration s | 2 |

1. One increment rotates 0.000700 rad about local z.

2. Apply 2000 increments, giving actual duration 2.000000 s.

3. The final scalar-first quaternion is [0.7648421872844843, 0.0, 0.0, 0.644217687237696].

4. Use the absolute dot product for sign-invariant error: 0.000000000 rad.

5. Compare q with -q using the same metric: 0.000000000 rad.

#### Worked case 1: dt = 0.002

This case keeps the nominal configuration except for dt=0.002. The full input is {"dt": 0.002, "duration": 2.0, "rate": 0.7}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final w | 0.76484219 |
| final z | 0.64421769 |
| angle error rad | 0 |
| sign equivalence error rad | 0 |
| actual duration s | 2 |

1. One increment rotates 0.001400 rad about local z.

2. Apply 1000 increments, giving actual duration 2.000000 s.

3. The final scalar-first quaternion is [0.7648421872844865, 0.0, 0.0, 0.6442176872376935].

4. Use the absolute dot product for sign-invariant error: 0.000000000 rad.

5. Compare q with -q using the same metric: 0.000000000 rad.

#### Worked case 2: dt = 0.005

This case keeps the nominal configuration except for dt=0.005. The full input is {"dt": 0.005, "duration": 2.0, "rate": 0.7}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final w | 0.76484219 |
| final z | 0.64421769 |
| angle error rad | 0 |
| sign equivalence error rad | 0 |
| actual duration s | 2 |

1. One increment rotates 0.003500 rad about local z.

2. Apply 400 increments, giving actual duration 2.000000 s.

3. The final scalar-first quaternion is [0.7648421872844876, 0.0, 0.0, 0.644217687237692].

4. Use the absolute dot product for sign-invariant error: 0.000000000 rad.

5. Compare q with -q using the same metric: 0.000000000 rad.

#### Worked case 3: dt = 0.01

This case keeps the nominal configuration except for dt=0.01. The full input is {"dt": 0.01, "duration": 2.0, "rate": 0.7}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final w | 0.76484219 |
| final z | 0.64421769 |
| angle error rad | 0 |
| sign equivalence error rad | 0 |
| actual duration s | 2 |

1. One increment rotates 0.007000 rad about local z.

2. Apply 200 increments, giving actual duration 2.000000 s.

3. The final scalar-first quaternion is [0.7648421872844878, 0.0, 0.0, 0.6442176872376917].

4. Use the absolute dot product for sign-invariant error: 0.000000000 rad.

5. Compare q with -q using the same metric: 0.000000000 rad.

#### Worked case 4: dt = 0.02

This case keeps the nominal configuration except for dt=0.02. The full input is {"dt": 0.02, "duration": 2.0, "rate": 0.7}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final w | 0.76484219 |
| final z | 0.64421769 |
| angle error rad | 0 |
| sign equivalence error rad | 0 |
| actual duration s | 2 |

1. One increment rotates 0.014000 rad about local z.

2. Apply 100 increments, giving actual duration 2.000000 s.

3. The final scalar-first quaternion is [0.7648421872844882, 0.0, 0.0, 0.6442176872376915].

4. Use the absolute dot product for sign-invariant error: 0.000000000 rad.

5. Compare q with -q using the same metric: 0.000000000 rad.

#### Worked case 5: dt = 0.05

This case keeps the nominal configuration except for dt=0.05. The full input is {"dt": 0.05, "duration": 2.0, "rate": 0.7}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final w | 0.76484219 |
| final z | 0.64421769 |
| angle error rad | 0 |
| sign equivalence error rad | 0 |
| actual duration s | 2 |

1. One increment rotates 0.035000 rad about local z.

2. Apply 40 increments, giving actual duration 2.000000 s.

3. The final scalar-first quaternion is [0.7648421872844885, 0.0, 0.0, 0.6442176872376909].

4. Use the absolute dot product for sign-invariant error: 0.000000000 rad.

5. Compare q with -q using the same metric: 0.000000000 rad.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Constant-axis exact increments are a reference case, not a full noisy IMU estimator.

Changing the multiplication side changes whether increments are interpreted in body or world coordinates.

### K. Failure modes and troubleshooting

Comparing q and -q directly; passing scalar-first values into an API expecting scalar-last; integrating degrees per second as radians.

### L. Practical exercises and extension tasks

1. Replace exact increments by first-order quaternion integration and compare timestep sensitivity.

2. Alternate x and y angular increments and examine composition order.

3. Test conversion to ROS scalar-last message ordering and back.

### M. Connection to the Asimov research platform

Real gyro integration needs calibrated axes, bias estimation, timestamp handling and external correction for drift.

### N. Completion record

Record your chosen case, predicted trend, measured final_w, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 5, Homogeneous transforms and frame-chain round trips. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 5 - Homogeneous transforms and frame-chain round trips

### A. The engineering question

A rigid transform combines a rotation and translation without losing the frame relationship between them.

### B. Concepts and mathematical model

The notation T_AB means coordinates expressed in B are converted to A. Adjacent frame labels cancel during composition: T_AB*T_BC gives T_AC. This mnemonic is safer than deciding matrix multiplication order from visual intuition. Points carry translation; direction vectors do not. A transform inverse uses the transposed rotation and a rotated negative translation, not simply negating the position column.

T_AB = [[R_AB,p_AB],[0,1]]; T_AC = T_AB*T_BC; T_BA = [[R_AB.T,-R_AB.T*p_AB],[0,1]].

### C. Real-world meaning and limits

Camera-to-base transforms are reusable only after matching link definitions, mounting offsets and timestamps to the assembled robot.

### D. Architecture and data flow

Configuration (angle_deg, offset) -> numerical model -> point_x_m, point_y_m, point_z_m -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

angle_deg is the A-from-B active z rotation; offset is B-to-C origin displacement in meters.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| angle_deg | 45 | degrees |
| offset | 0.15 | meters |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/05_transforms.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only angle_deg changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/05_transforms.py --case 0

.venv-book/bin/python expanded_lab/modules/05_transforms.py --case 3

.venv-book/bin/python expanded_lab/run.py transforms --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/05_transforms.py

### H. Walkthrough and design decisions

Build each transform independently, compose in the frame-label order, and check both nested multiplication and inverse recovery. These two checks expose different classes of implementation error.

### I. Expected behavior and six worked cases

The controlled variable is angle_deg. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/05_transforms.png

Figure L5. point x m as angle_deg changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | angle_deg | point x m |
|---|---|---|
| 0 | 0 | 0.47061932 |
| 1 | 15 | 0.4485621 |
| 2 | 30 | 0.40275094 |
| 3 | 45 | 0.33630781 |
| 4 | 60 | 0.25376069 |
| 5 | 90 | 0.06357039 |

#### Worked case 0: angle_deg = 0

This case keeps the nominal configuration except for angle_deg=0. The full input is {"angle_deg": 0.0, "offset": 0.15}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| point x m | 0.47061932 |
| point y m | 0.23642961 |
| point z m | 0.35 |
| roundtrip error m | 6.2063354e-17 |
| translation norm m | 0.47434165 |

1. T_BC translation is (0.150000,0,0.05) m.

2. T_AB rotates by 0.000000 rad before adding its translation.

3. Compose T_AC; the resulting translation is [0.25, 0.2, 0.35] m.

4. Point (0.2,0.1,0) in C becomes [0.47061931849125516, 0.23642960758029272, 0.35] in A.

5. Apply the analytic inverse; recovery error is 6.206e-17 m.

#### Worked case 1: angle_deg = 15

This case keeps the nominal configuration except for angle_deg=15. The full input is {"angle_deg": 15.0, "offset": 0.15}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| point x m | 0.4485621 |
| point y m | 0.33111164 |
| point z m | 0.35 |
| roundtrip error m | 7.8504623e-17 |
| translation norm m | 0.48939444 |

1. T_BC translation is (0.150000,0,0.05) m.

2. T_AB rotates by 0.261799 rad before adding its translation.

3. Compose T_AC; the resulting translation is [0.24488887394336026, 0.23882285676537812, 0.35] m.

4. Point (0.2,0.1,0) in C becomes [0.44856209520496615, 0.3311116369118344, 0.35] in A.

5. Apply the analytic inverse; recovery error is 7.850e-17 m.

#### Worked case 2: angle_deg = 30

This case keeps the nominal configuration except for angle_deg=30. The full input is {"angle_deg": 30.0, "offset": 0.15}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| point x m | 0.40275094 |
| point y m | 0.41685862 |
| point z m | 0.35 |
| roundtrip error m | 6.2063354e-17 |
| translation norm m | 0.5009798 |

1. T_BC translation is (0.150000,0,0.05) m.

2. T_AB rotates by 0.523599 rad before adding its translation.

3. Compose T_AC; the resulting translation is [0.22990381056766582, 0.275, 0.35] m.

4. Point (0.2,0.1,0) in C becomes [0.4027509411565564, 0.4168586248600592, 0.35] in A.

5. Apply the analytic inverse; recovery error is 6.206e-17 m.

#### Worked case 3: angle_deg = 45

This case keeps the nominal configuration except for angle_deg=45. The full input is {"angle_deg": 45.0, "offset": 0.15}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| point x m | 0.33630781 |
| point y m | 0.48782706 |
| point z m | 0.35 |
| roundtrip error m | 2.7755576e-17 |
| translation norm m | 0.50856623 |

1. T_BC translation is (0.150000,0,0.05) m.

2. T_AB rotates by 0.785398 rad before adding its translation.

3. Compose T_AC; the resulting translation is [0.20606601717798212, 0.3060660171779821, 0.35] m.

4. Point (0.2,0.1,0) in C becomes [0.3363078107879135, 0.48782705589989317, 0.35] in A.

5. Apply the analytic inverse; recovery error is 2.776e-17 m.

#### Worked case 4: angle_deg = 60

This case keeps the nominal configuration except for angle_deg=60. The full input is {"angle_deg": 60.0, "offset": 0.15}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| point x m | 0.25376069 |
| point y m | 0.53918055 |
| point z m | 0.35 |
| roundtrip error m | 3.9252311e-17 |
| translation norm m | 0.51182177 |

1. T_BC translation is (0.150000,0,0.05) m.

2. T_AB rotates by 1.047198 rad before adding its translation.

3. Compose T_AC; the resulting translation is [0.17500000000000002, 0.3299038105676658, 0.35] m.

4. Point (0.2,0.1,0) in C becomes [0.25376069363119597, 0.5391805487368491, 0.35] in A.

5. Apply the analytic inverse; recovery error is 3.925e-17 m.

#### Worked case 5: angle_deg = 90

This case keeps the nominal configuration except for angle_deg=90. The full input is {"angle_deg": 90.0, "offset": 0.15}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| point x m | 0.06357039 |
| point y m | 0.57061932 |
| point z m | 0.35 |
| roundtrip error m | 2.7755576e-17 |
| translation norm m | 0.50497525 |

1. T_BC translation is (0.150000,0,0.05) m.

2. T_AB rotates by 1.570796 rad before adding its translation.

3. Compose T_AC; the resulting translation is [0.10000000000000002, 0.35, 0.35] m.

4. Point (0.2,0.1,0) in C becomes [0.06357039241970733, 0.5706193184912551, 0.35] in A.

5. Apply the analytic inverse; recovery error is 2.776e-17 m.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The point result includes both translations in the correct rotated directions.

A direction encoded with homogeneous last element zero would ignore translation.

### K. Failure modes and troubleshooting

Using -translation directly for the inverse; multiplying a three-vector by a 4x4 matrix; confusing a point with a direction.

### L. Practical exercises and extension tasks

1. Replace the point last coordinate with zero and explain the changed result.

2. Insert a head-to-camera transform and verify a four-frame chain.

3. Perturb camera translation by 5 mm and calculate world-position error.

### M. Connection to the Asimov research platform

Camera-to-base transforms are reusable only after matching link definitions, mounting offsets and timestamps to the assembled robot.

### N. Completion record

Record your chosen case, predicted trend, measured point_x_m, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 6, Finite-difference Jacobians and derivative verification. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 6 - Finite-difference Jacobians and derivative verification

### A. The engineering question

The Jacobian answers a local question: how much does an endpoint move for a small joint displacement? Analytic derivatives are efficient, but a sign or index error can hide inside plausible motion.

### B. Concepts and mathematical model

Central finite differences provide a separate numerical check. The perturbation must be small enough to approximate a derivative but not so small that subtraction roundoff dominates. This laboratory compares the two methods at a nonsingular two-link pose and makes epsilon an experimental variable.

J_ij = partial f_i/partial q_j; central difference = [f(q+epsilon*e_j)-f(q-epsilon*e_j)]/(2*epsilon).

### C. Real-world meaning and limits

The same column test should validate the selected MuJoCo or hardware-model Jacobian before Cartesian controllers depend on it.

### D. Architecture and data flow

Configuration (epsilon) -> numerical model -> derivative_error, velocity_x_m_s, velocity_y_m_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

epsilon is a central-difference joint perturbation in radians; lengths are 0.3 and 0.2 meters.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| epsilon | 0.00001 | radian perturbation |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/06_jacobian.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only epsilon changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/06_jacobian.py --case 0

.venv-book/bin/python expanded_lab/modules/06_jacobian.py --case 3

.venv-book/bin/python expanded_lab/run.py jacobian --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/06_jacobian.py

### H. Walkthrough and design decisions

The two columns correspond to the two independent joint perturbations. Multiplying by a joint-rate vector produces a local Cartesian velocity, whose units provide another check on the derivative.

### I. Expected behavior and six worked cases

The controlled variable is epsilon. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/06_jacobian.png

Figure L6. derivative error as epsilon changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | epsilon | derivative error |
|---|---|---|
| 0 | 0.1 | 0.00085232 |
| 1 | 0.01 | 8.5273815e-06 |
| 2 | 0.001 | 8.5274238e-08 |
| 3 | 0.00001 | 1.0136602e-11 |
| 4 | 1.0000000e-07 | 4.8850740e-10 |
| 5 | 1.0000000e-09 | 2.8168134e-08 |

#### Worked case 0: epsilon = 0.1

This case keeps the nominal configuration except for epsilon=0.1. The full input is {"epsilon": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| derivative error | 0.00085232 |
| velocity x m s | -0.01759295 |
| velocity y m s | 0.0085251 |
| jacobian condition | 6.62156114 |

1. At joint pose [0.4, -0.7] rad, endpoint is [0.4673855960259867, 0.05772146136032724] m.

2. Use symmetric perturbations of 1.000e-01 rad for each joint.

3. The analytic first column is [-0.05772146136032724, 0.4673855960259867] m/rad.

4. The estimated first column is [-0.05762530701449331, 0.46660700942788436] m/rad.

5. Full matrix residual norm is 8.523e-04; predicted endpoint velocity is [-0.017592954402486306, 0.008525100037574427] m/s.

#### Worked case 1: epsilon = 0.01

This case keeps the nominal configuration except for epsilon=0.01. The full input is {"epsilon": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| derivative error | 8.5273815e-06 |
| velocity x m s | -0.01759295 |
| velocity y m s | 0.0085251 |
| jacobian condition | 6.62156114 |

1. At joint pose [0.4, -0.7] rad, endpoint is [0.4673855960259867, 0.05772146136032724] m.

2. Use symmetric perturbations of 1.000e-02 rad for each joint.

3. The analytic first column is [-0.05772146136032724, 0.4673855960259867] m/rad.

4. The estimated first column is [-0.05772049934078538, 0.46737780630500236] m/rad.

5. Full matrix residual norm is 8.527e-06; predicted endpoint velocity is [-0.017592954402486306, 0.008525100037574427] m/s.

#### Worked case 2: epsilon = 0.001

This case keeps the nominal configuration except for epsilon=0.001. The full input is {"epsilon": 0.001}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| derivative error | 8.5274238e-08 |
| velocity x m s | -0.01759295 |
| velocity y m s | 0.0085251 |
| jacobian condition | 6.62156114 |

1. At joint pose [0.4, -0.7] rad, endpoint is [0.4673855960259867, 0.05772146136032724] m.

2. Use symmetric perturbations of 1.000e-03 rad for each joint.

3. The analytic first column is [-0.05772146136032724, 0.4673855960259867] m/rad.

4. The estimated first column is [-0.05772145174004484, 0.4673855181283916] m/rad.

5. Full matrix residual norm is 8.527e-08; predicted endpoint velocity is [-0.017592954402486306, 0.008525100037574427] m/s.

#### Worked case 3: epsilon = 0.00001

This case keeps the nominal configuration except for epsilon=0.00001. The full input is {"epsilon": 1e-05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| derivative error | 1.0136602e-11 |
| velocity x m s | -0.01759295 |
| velocity y m s | 0.0085251 |
| jacobian condition | 6.62156114 |

1. At joint pose [0.4, -0.7] rad, endpoint is [0.4673855960259867, 0.05772146136032724] m.

2. Use symmetric perturbations of 1.000e-05 rad for each joint.

3. The analytic first column is [-0.05772146136032724, 0.4673855960259867] m/rad.

4. The estimated first column is [-0.05772146136062694, 0.4673855960181383] m/rad.

5. Full matrix residual norm is 1.014e-11; predicted endpoint velocity is [-0.017592954402486306, 0.008525100037574427] m/s.

#### Worked case 4: epsilon = 1.0000000e-07

This case keeps the nominal configuration except for epsilon=1.0000000e-07. The full input is {"epsilon": 1e-07}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| derivative error | 4.8850740e-10 |
| velocity x m s | -0.01759295 |
| velocity y m s | 0.0085251 |
| jacobian condition | 6.62156114 |

1. At joint pose [0.4, -0.7] rad, endpoint is [0.4673855960259867, 0.05772146136032724] m.

2. Use symmetric perturbations of 1.000e-07 rad for each joint.

3. The analytic first column is [-0.05772146136032724, 0.4673855960259867] m/rad.

4. The estimated first column is [-0.05772146177696058, 0.4673855960590778] m/rad.

5. Full matrix residual norm is 4.885e-10; predicted endpoint velocity is [-0.017592954402486306, 0.008525100037574427] m/s.

#### Worked case 5: epsilon = 1.0000000e-09

This case keeps the nominal configuration except for epsilon=1.0000000e-09. The full input is {"epsilon": 1e-09}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| derivative error | 2.8168134e-08 |
| velocity x m s | -0.01759295 |
| velocity y m s | 0.0085251 |
| jacobian condition | 6.62156114 |

1. At joint pose [0.4, -0.7] rad, endpoint is [0.4673855960259867, 0.05772146136032724] m.

2. Use symmetric perturbations of 1.000e-09 rad for each joint.

3. The analytic first column is [-0.05772146136032724, 0.4673855960259867] m/rad.

4. The estimated first column is [-0.05772143873983281, 0.46738560244286015] m/rad.

5. Full matrix residual norm is 2.817e-08; predicted endpoint velocity is [-0.017592954402486306, 0.008525100037574427] m/s.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Reducing epsilon eventually makes floating-point cancellation important.

Compare columns in the same frame and at the same configuration; otherwise the residual is not a derivative test.

### K. Failure modes and troubleshooting

Reusing a mutable q array without restoring it; comparing degrees-based perturbations to radian derivatives; testing only at zero pose.

### L. Practical exercises and extension tasks

1. Repeat with forward differences and compare convergence order.

2. Check every column at ten seeded nonsingular poses.

3. Move near a stretched configuration and track conditioning separately from derivative accuracy.

### M. Connection to the Asimov research platform

The same column test should validate the selected MuJoCo or hardware-model Jacobian before Cartesian controllers depend on it.

### N. Completion record

Record your chosen case, predicted trend, measured derivative_error, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 7, Least-squares identification and residual diagnosis. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 7 - Least-squares identification and residual diagnosis

### A. The engineering question

Many calibration tasks are linear in their unknown parameters even when the robot is complicated.

### B. Concepts and mathematical model

A simple example estimates a sensor scale and offset from known references. Least squares chooses parameters minimizing squared residuals, but a small residual does not guarantee the experiment identified both parameters well. Excitation range determines conditioning. Noise, repeated references and validation data must be considered before accepting a fit.

y = a*x+b+noise; theta_hat = argmin ||X*theta-y||^2; X=[x,1].

### C. Real-world meaning and limits

Encoder zero, current-to-torque scale and camera calibration require trusted independent references and validation outside the fit data.

### D. Architecture and data flow

Configuration (samples, noise, span) -> numerical model -> scale_error, offset_error_rad, residual_rmse_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

samples is the number of references; noise is measurement standard deviation in radians; span is the symmetric excitation half-range.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| samples | 40 | count |
| noise | 0.005 | measurement standard deviation |
| span | 0.5 | radians |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/07_least_squares.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only span changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/07_least_squares.py --case 0

.venv-book/bin/python expanded_lab/modules/07_least_squares.py --case 3

.venv-book/bin/python expanded_lab/run.py least_squares --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/07_least_squares.py

### H. Walkthrough and design decisions

Use lstsq rather than explicitly inverting the normal equations for the estimate. The covariance calculation is kept separate to inspect its assumptions. Compare parameter errors to the injected truth and residual magnitude.

### I. Expected behavior and six worked cases

The controlled variable is span. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/07_least_squares.png

Figure L7. scale error as span changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | span | scale error |
|---|---|---|
| 0 | 0.01 | -0.12639436 |
| 1 | 0.025 | -0.05055774 |
| 2 | 0.05 | -0.02527887 |
| 3 | 0.1 | -0.01263944 |
| 4 | 0.5 | -0.00252789 |
| 5 | 1 | -0.00126394 |

#### Worked case 0: span = 0.01

This case keeps the nominal configuration except for span=0.01. The full input is {"noise": 0.005, "samples": 40, "span": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| scale error | -0.12639436 |
| offset error rad | -0.00040906 |
| residual rmse rad | 0.00416545 |
| design condition | 168.92775191 |
| scale std estimate | 0.11414873 |

1. Collect 40 reference positions spanning [-0.01,0.01] rad.

2. True scale and offset are [1.04, 0.025]; inject noise sigma=0.005 rad.

3. Least-squares estimate is [0.9136056388714553, 0.024590942846796585].

4. Residual degrees of freedom are 38; variance estimate is 1.826418e-05.

5. The design matrix condition is 168.927752; estimated scale uncertainty is 0.114149.

#### Worked case 1: span = 0.025

This case keeps the nominal configuration except for span=0.025. The full input is {"noise": 0.005, "samples": 40, "span": 0.025}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| scale error | -0.05055774 |
| offset error rad | -0.00040906 |
| residual rmse rad | 0.00416545 |
| design condition | 67.57110076 |
| scale std estimate | 0.04565949 |

1. Collect 40 reference positions spanning [-0.025,0.025] rad.

2. True scale and offset are [1.04, 0.025]; inject noise sigma=0.005 rad.

3. Least-squares estimate is [0.9894422555485823, 0.024590942846796585].

4. Residual degrees of freedom are 38; variance estimate is 1.826418e-05.

5. The design matrix condition is 67.571101; estimated scale uncertainty is 0.045659.

The identification range is 0.05 rad; narrowing it weakens scale estimation even if the offset remains observable.

#### Worked case 2: span = 0.05

This case keeps the nominal configuration except for span=0.05. The full input is {"noise": 0.005, "samples": 40, "span": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| scale error | -0.02527887 |
| offset error rad | -0.00040906 |
| residual rmse rad | 0.00416545 |
| design condition | 33.78555038 |
| scale std estimate | 0.02282975 |

1. Collect 40 reference positions spanning [-0.05,0.05] rad.

2. True scale and offset are [1.04, 0.025]; inject noise sigma=0.005 rad.

3. Least-squares estimate is [1.0147211277742911, 0.024590942846796585].

4. Residual degrees of freedom are 38; variance estimate is 1.826418e-05.

5. The design matrix condition is 33.785550; estimated scale uncertainty is 0.022830.

The identification range is 0.1 rad; narrowing it weakens scale estimation even if the offset remains observable.

#### Worked case 3: span = 0.1

This case keeps the nominal configuration except for span=0.1. The full input is {"noise": 0.005, "samples": 40, "span": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| scale error | -0.01263944 |
| offset error rad | -0.00040906 |
| residual rmse rad | 0.00416545 |
| design condition | 16.89277519 |
| scale std estimate | 0.01141487 |

1. Collect 40 reference positions spanning [-0.1,0.1] rad.

2. True scale and offset are [1.04, 0.025]; inject noise sigma=0.005 rad.

3. Least-squares estimate is [1.0273605638871455, 0.024590942846796585].

4. Residual degrees of freedom are 38; variance estimate is 1.826418e-05.

5. The design matrix condition is 16.892775; estimated scale uncertainty is 0.011415.

The identification range is 0.2 rad; narrowing it weakens scale estimation even if the offset remains observable.

#### Worked case 4: span = 0.5

This case keeps the nominal configuration except for span=0.5. The full input is {"noise": 0.005, "samples": 40, "span": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| scale error | -0.00252789 |
| offset error rad | -0.00040906 |
| residual rmse rad | 0.00416545 |
| design condition | 3.37855504 |
| scale std estimate | 0.00228297 |

1. Collect 40 reference positions spanning [-0.5,0.5] rad.

2. True scale and offset are [1.04, 0.025]; inject noise sigma=0.005 rad.

3. Least-squares estimate is [1.0374721127774293, 0.024590942846796582].

4. Residual degrees of freedom are 38; variance estimate is 1.826418e-05.

5. The design matrix condition is 3.378555; estimated scale uncertainty is 0.002283.

The identification range is 1 rad; narrowing it weakens scale estimation even if the offset remains observable.

#### Worked case 5: span = 1

This case keeps the nominal configuration except for span=1. The full input is {"noise": 0.005, "samples": 40, "span": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| scale error | -0.00126394 |
| offset error rad | -0.00040906 |
| residual rmse rad | 0.00416545 |
| design condition | 1.68927752 |
| scale std estimate | 0.00114149 |

1. Collect 40 reference positions spanning [-1,1] rad.

2. True scale and offset are [1.04, 0.025]; inject noise sigma=0.005 rad.

3. Least-squares estimate is [1.0387360563887147, 0.024590942846796582].

4. Residual degrees of freedom are 38; variance estimate is 1.826418e-05.

5. The design matrix condition is 1.689278; estimated scale uncertainty is 0.001141.

The identification range is 2 rad; narrowing it weakens scale estimation even if the offset remains observable.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The identification range is 0.02 rad; narrowing it weakens scale estimation even if the offset remains observable.

Covariance assumes the linear noise model and does not account for backlash, systematic reference error or temperature drift.

### K. Failure modes and troubleshooting

Judging calibration only on training residuals; confusing standard deviation with a hard error bound; assuming repeated identical inputs identify scale.

### L. Practical exercises and extension tasks

1. Fit a separate held-out reference set and report prediction error.

2. Add a quadratic distortion and inspect residual versus position.

3. Change sample count and compare uncertainty to excitation range.

### M. Connection to the Asimov research platform

Encoder zero, current-to-torque scale and camera calibration require trusted independent references and validation outside the fit data.

### N. Completion record

Record your chosen case, predicted trend, measured scale_error, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 8, Discrete integration and numerical stability. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 8 - Discrete integration and numerical stability

### A. The engineering question

A stable continuous equation can become unstable after a poor discretization.

### B. Concepts and mathematical model

The scalar decay equation is simple enough to solve exactly, making it a useful laboratory for numerical reasoning. Explicit Euler predicts the next state from the current derivative. Implicit Euler evaluates the derivative at the next state and solves the resulting equation. Smaller timesteps reduce error but increase computation; choosing them blindly can conceal a model or controller problem.

x_dot=-k*x; exact x(t)=x0*exp(-k*t); explicit x_next=(1-k*dt)*x; implicit x_next=x/(1+k*dt).

### C. Real-world meaning and limits

A MuJoCo timestep, controller period and policy period are separate choices; document their relationship and validate contact/controller behavior together.

### D. Architecture and data flow

Configuration (dt, decay_rate, duration) -> numerical model -> explicit_final, implicit_final, exact_final -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

dt is seconds; decay_rate is inverse seconds; duration is desired integration horizon. Actual duration is an integer number of steps.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| dt | 0.02 | seconds |
| decay_rate | 10 | inverse seconds |
| duration | 1 | seconds |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/08_integration.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only dt changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/08_integration.py --case 0

.venv-book/bin/python expanded_lab/modules/08_integration.py --case 3

.venv-book/bin/python expanded_lab/run.py integration --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/08_integration.py

### H. Walkthrough and design decisions

Track the recurrence multiplier before the final state. The exact exponential allows an accuracy comparison independent of either integrator. A negative explicit multiplier alternates sign even when the continuous solution does not.

### I. Expected behavior and six worked cases

The controlled variable is dt. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/08_integration.png

Figure L8. explicit final as dt changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | dt | explicit final |
|---|---|---|
| 0 | 0.005 | 0.00003505 |
| 1 | 0.01 | 0.00002656 |
| 2 | 0.02 | 0.00001427 |
| 3 | 0.05 | 9.5367432e-07 |
| 4 | 0.1 | 0 |
| 5 | 0.25 | 5.0625 |

#### Worked case 0: dt = 0.005

This case keeps the nominal configuration except for dt=0.005. The full input is {"decay_rate": 10.0, "dt": 0.005, "duration": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| explicit final | 0.00003505 |
| implicit final | 0.00005783 |
| exact final | 0.0000454 |
| explicit abs error | 0.00001035 |
| implicit abs error | 0.00001243 |
| explicit amplification | 0.95 |

1. Choose dt=0.005 s and decay rate k=10 per second.

2. Advance 200 steps to actual time 1.000000 s.

3. Explicit one-step multiplier is 0.950000; its magnitude is 0.950000.

4. Exact final value is 0.00004540; explicit gives 0.00003505.

5. Implicit final value is 0.00005783; compare absolute errors in the table.

#### Worked case 1: dt = 0.01

This case keeps the nominal configuration except for dt=0.01. The full input is {"decay_rate": 10.0, "dt": 0.01, "duration": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| explicit final | 0.00002656 |
| implicit final | 0.00007257 |
| exact final | 0.0000454 |
| explicit abs error | 0.00001884 |
| implicit abs error | 0.00002717 |
| explicit amplification | 0.9 |

1. Choose dt=0.01 s and decay rate k=10 per second.

2. Advance 100 steps to actual time 1.000000 s.

3. Explicit one-step multiplier is 0.900000; its magnitude is 0.900000.

4. Exact final value is 0.00004540; explicit gives 0.00002656.

5. Implicit final value is 0.00007257; compare absolute errors in the table.

#### Worked case 2: dt = 0.02

This case keeps the nominal configuration except for dt=0.02. The full input is {"decay_rate": 10.0, "dt": 0.02, "duration": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| explicit final | 0.00001427 |
| implicit final | 0.00010988 |
| exact final | 0.0000454 |
| explicit abs error | 0.00003113 |
| implicit abs error | 0.00006448 |
| explicit amplification | 0.8 |

1. Choose dt=0.02 s and decay rate k=10 per second.

2. Advance 50 steps to actual time 1.000000 s.

3. Explicit one-step multiplier is 0.800000; its magnitude is 0.800000.

4. Exact final value is 0.00004540; explicit gives 0.00001427.

5. Implicit final value is 0.00010988; compare absolute errors in the table.

#### Worked case 3: dt = 0.05

This case keeps the nominal configuration except for dt=0.05. The full input is {"decay_rate": 10.0, "dt": 0.05, "duration": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| explicit final | 9.5367432e-07 |
| implicit final | 0.00030073 |
| exact final | 0.0000454 |
| explicit abs error | 0.00004445 |
| implicit abs error | 0.00025533 |
| explicit amplification | 0.5 |

1. Choose dt=0.05 s and decay rate k=10 per second.

2. Advance 20 steps to actual time 1.000000 s.

3. Explicit one-step multiplier is 0.500000; its magnitude is 0.500000.

4. Exact final value is 0.00004540; explicit gives 0.00000095.

5. Implicit final value is 0.00030073; compare absolute errors in the table.

#### Worked case 4: dt = 0.1

This case keeps the nominal configuration except for dt=0.1. The full input is {"decay_rate": 10.0, "dt": 0.1, "duration": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| explicit final | 0 |
| implicit final | 0.00097656 |
| exact final | 0.0000454 |
| explicit abs error | 0.0000454 |
| implicit abs error | 0.00093116 |
| explicit amplification | 0 |

1. Choose dt=0.1 s and decay rate k=10 per second.

2. Advance 10 steps to actual time 1.000000 s.

3. Explicit one-step multiplier is 0.000000; its magnitude is 0.000000.

4. Exact final value is 0.00004540; explicit gives 0.00000000.

5. Implicit final value is 0.00097656; compare absolute errors in the table.

#### Worked case 5: dt = 0.25

This case keeps the nominal configuration except for dt=0.25. The full input is {"decay_rate": 10.0, "dt": 0.25, "duration": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| explicit final | 5.0625 |
| implicit final | 0.00666389 |
| exact final | 0.0000454 |
| explicit abs error | 5.0624546 |
| implicit abs error | 0.00661849 |
| explicit amplification | 1.5 |

1. Choose dt=0.25 s and decay rate k=10 per second.

2. Advance 4 steps to actual time 1.000000 s.

3. Explicit one-step multiplier is -1.500000; its magnitude is 1.500000.

4. Exact final value is 0.00004540; explicit gives 5.06250000.

5. Implicit final value is 0.00666389; compare absolute errors in the table.

The explicit recurrence is on or outside its stability boundary; reducing dt changes the numerical problem.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The explicit recurrence is stable for this scalar decay.

Implicit stability does not mean high accuracy; a heavily damped numerical result can still be wrong.

### K. Failure modes and troubleshooting

Equating absence of NaNs with accuracy; changing dt without scaling controller updates; comparing runs with different actual horizons.

### L. Practical exercises and extension tasks

1. Find the explicit stability boundary analytically and confirm it numerically.

2. Compare equal actual horizons for non-dividing timesteps.

3. Apply the same methodology to a mass-spring system.

### M. Connection to the Asimov research platform

A MuJoCo timestep, controller period and policy period are separate choices; document their relationship and validate contact/controller behavior together.

### N. Completion record

Record your chosen case, predicted trend, measured explicit_final, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 9, Monte Carlo uncertainty propagation and repeatability. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 9 - Monte Carlo uncertainty propagation and repeatability

### A. The engineering question

A nominal calculation hides variability.

### B. Concepts and mathematical model

Monte Carlo propagation samples uncertain inputs, evaluates the same physical relationship repeatedly, and summarizes the output distribution. It is useful when several uncertainties combine nonlinearly, but its answer is only as credible as the input distributions and correlations. A fixed seed makes an experiment repeatable; multiple independent seeds are needed to assess sampling variability rather than overfit a convenient random realization.

tau = m*g*l*cos(theta); sample uncertain m, l and theta; summarize mean, standard deviation and quantiles.

### C. Real-world meaning and limits

Use measured calibration and manufacturing variation to justify randomization ranges rather than arbitrary broad noise.

### D. Architecture and data flow

Configuration (seed, samples, angle_noise) -> numerical model -> mean_torque_Nm, std_torque_Nm, lower_quantile_Nm -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

seed identifies a pseudorandom stream; samples controls numerical sample count; angle_noise is standard deviation in radians.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| seed | 17 | integer random seed |
| samples | 5000 | count |
| angle_noise | 0.02 | radians |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/09_uncertainty.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only angle_noise changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/09_uncertainty.py --case 0

.venv-book/bin/python expanded_lab/modules/09_uncertainty.py --case 3

.venv-book/bin/python expanded_lab/run.py uncertainty --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/09_uncertainty.py

### H. Walkthrough and design decisions

Generate uncertain quantities first, then evaluate the same torque equation vectorially. Compare the nonlinear mean with the nominal prediction. Distinguish the distribution width from the standard error of a mean estimate.

### I. Expected behavior and six worked cases

The controlled variable is angle_noise. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/09_uncertainty.png

Figure L9. mean torque Nm as angle_noise changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | angle_noise | mean torque Nm |
|---|---|---|
| 0 | 0.001 | 4.05003363 |
| 1 | 0.005 | 4.05005263 |
| 2 | 0.01 | 4.04998425 |
| 3 | 0.02 | 4.04954036 |
| 4 | 0.05 | 4.04575343 |
| 5 | 0.1 | 4.03128607 |

#### Worked case 0: angle_noise = 0.001

This case keeps the nominal configuration except for angle_noise=0.001. The full input is {"angle_noise": 0.001, "samples": 5000, "seed": 17}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean torque Nm | 4.05003363 |
| std torque Nm | 0.08737753 |
| lower quantile Nm | 3.88050878 |
| upper quantile Nm | 4.2218778 |
| nominal torque Nm | 4.04827119 |

1. Draw 5000 samples with generator seed 17.

2. Mass sigma is 0.04 kg, lever sigma is 0.002 m, angle sigma is 0.001 rad.

3. Evaluate gravity torque for each sample; nominal value is 4.048271 Nm.

4. Sample mean is 4.050034 Nm and sample standard deviation is 0.087378 Nm.

5. Central empirical 95% interval is [3.880509,4.221878] Nm.

#### Worked case 1: angle_noise = 0.005

This case keeps the nominal configuration except for angle_noise=0.005. The full input is {"angle_noise": 0.005, "samples": 5000, "seed": 17}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean torque Nm | 4.05005263 |
| std torque Nm | 0.08844329 |
| lower quantile Nm | 3.87723807 |
| upper quantile Nm | 4.22493927 |
| nominal torque Nm | 4.04827119 |

1. Draw 5000 samples with generator seed 17.

2. Mass sigma is 0.04 kg, lever sigma is 0.002 m, angle sigma is 0.005 rad.

3. Evaluate gravity torque for each sample; nominal value is 4.048271 Nm.

4. Sample mean is 4.050053 Nm and sample standard deviation is 0.088443 Nm.

5. Central empirical 95% interval is [3.877238,4.224939] Nm.

#### Worked case 2: angle_noise = 0.01

This case keeps the nominal configuration except for angle_noise=0.01. The full input is {"angle_noise": 0.01, "samples": 5000, "seed": 17}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean torque Nm | 4.04998425 |
| std torque Nm | 0.09168126 |
| lower quantile Nm | 3.87142732 |
| upper quantile Nm | 4.22996162 |
| nominal torque Nm | 4.04827119 |

1. Draw 5000 samples with generator seed 17.

2. Mass sigma is 0.04 kg, lever sigma is 0.002 m, angle sigma is 0.01 rad.

3. Evaluate gravity torque for each sample; nominal value is 4.048271 Nm.

4. Sample mean is 4.049984 Nm and sample standard deviation is 0.091681 Nm.

5. Central empirical 95% interval is [3.871427,4.229962] Nm.

#### Worked case 3: angle_noise = 0.02

This case keeps the nominal configuration except for angle_noise=0.02. The full input is {"angle_noise": 0.02, "samples": 5000, "seed": 17}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean torque Nm | 4.04954036 |
| std torque Nm | 0.10360821 |
| lower quantile Nm | 3.84319415 |
| upper quantile Nm | 4.24903658 |
| nominal torque Nm | 4.04827119 |

1. Draw 5000 samples with generator seed 17.

2. Mass sigma is 0.04 kg, lever sigma is 0.002 m, angle sigma is 0.02 rad.

3. Evaluate gravity torque for each sample; nominal value is 4.048271 Nm.

4. Sample mean is 4.049540 Nm and sample standard deviation is 0.103608 Nm.

5. Central empirical 95% interval is [3.843194,4.249037] Nm.

#### Worked case 4: angle_noise = 0.05

This case keeps the nominal configuration except for angle_noise=0.05. The full input is {"angle_noise": 0.05, "samples": 5000, "seed": 17}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean torque Nm | 4.04575343 |
| std torque Nm | 0.16435706 |
| lower quantile Nm | 3.70817561 |
| upper quantile Nm | 4.36225416 |
| nominal torque Nm | 4.04827119 |

1. Draw 5000 samples with generator seed 17.

2. Mass sigma is 0.04 kg, lever sigma is 0.002 m, angle sigma is 0.05 rad.

3. Evaluate gravity torque for each sample; nominal value is 4.048271 Nm.

4. Sample mean is 4.045753 Nm and sample standard deviation is 0.164357 Nm.

5. Central empirical 95% interval is [3.708176,4.362254] Nm.

#### Worked case 5: angle_noise = 0.1

This case keeps the nominal configuration except for angle_noise=0.1. The full input is {"angle_noise": 0.1, "samples": 5000, "seed": 17}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean torque Nm | 4.03128607 |
| std torque Nm | 0.29164591 |
| lower quantile Nm | 3.40336391 |
| upper quantile Nm | 4.55447884 |
| nominal torque Nm | 4.04827119 |

1. Draw 5000 samples with generator seed 17.

2. Mass sigma is 0.04 kg, lever sigma is 0.002 m, angle sigma is 0.1 rad.

3. Evaluate gravity torque for each sample; nominal value is 4.048271 Nm.

4. Sample mean is 4.031286 Nm and sample standard deviation is 0.291646 Nm.

5. Central empirical 95% interval is [3.403364,4.554479] Nm.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

These quantiles describe the assumed population, not a confidence interval for the sample mean.

Independent Gaussian inputs are a declared teaching assumption; shared calibration errors can create correlations.

### K. Failure modes and troubleshooting

Calling a percentile interval a guarantee; assuming independent errors without evidence; selecting a seed because it gives an attractive answer.

### L. Practical exercises and extension tasks

1. Compare repeated seeds at 100 and 10,000 samples.

2. Correlate mass and lever length and inspect the output spread.

3. Use a bounded distribution for angle and compare tail behavior.

### M. Connection to the Asimov research platform

Use measured calibration and manufacturing variation to justify randomization ranges rather than arbitrary broad noise.

### N. Completion record

Record your chosen case, predicted trend, measured mean_torque_Nm, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 10, Sampling, aliasing and the difference between signal and display rate. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 10 - Sampling, aliasing and the difference between signal and display rate

### A. The engineering question

Sampling converts a continuous-time signal into discrete observations.

### B. Concepts and mathematical model

Different underlying frequencies can produce the same sampled sequence, so a plot can look smooth and still misrepresent motion. The Nyquist condition is a minimum for reconstructing a band-limited signal; real sensors require anti-alias filtering and margin. Display decimation is separate from measurement sampling and should never reduce the feedback rate accidentally.

x[n]=sin(2*pi*f*n/fs); aliased frequency = abs((f+fs/2) mod fs - fs/2).

### C. Real-world meaning and limits

High-frequency encoder/IMU motion and low-rate network telemetry serve different purposes; the dashboard is not a control sensor.

### D. Architecture and data flow

Configuration (sample_rate, signal_frequency, duration) -> numerical model -> nyquist_Hz, alias_Hz, fft_peak_Hz -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

sample_rate and signal_frequency are Hertz; duration is seconds. Samples begin at zero phase in this controlled example.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| sample_rate | 100 | Hertz |
| signal_frequency | 35 | Hertz |
| duration | 2 | seconds |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/10_signals.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only sample_rate changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/10_signals.py --case 0

.venv-book/bin/python expanded_lab/modules/10_signals.py --case 3

.venv-book/bin/python expanded_lab/run.py signals --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/10_signals.py

### H. Walkthrough and design decisions

Calculate the expected alias independently before looking at the FFT. The frequency-bin calculation prevents overclaiming resolution from a short record. Consider anti-alias filtering before a physical sampling boundary.

### I. Expected behavior and six worked cases

The controlled variable is sample_rate. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/10_signals.png

Figure L10. nyquist Hz as sample_rate changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | sample_rate | nyquist Hz |
|---|---|---|
| 0 | 20 | 10 |
| 1 | 40 | 20 |
| 2 | 60 | 30 |
| 3 | 80 | 40 |
| 4 | 100 | 50 |
| 5 | 200 | 100 |

#### Worked case 0: sample_rate = 20

This case keeps the nominal configuration except for sample_rate=20. The full input is {"duration": 2.0, "sample_rate": 20.0, "signal_frequency": 35.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| nyquist Hz | 10 |
| alias Hz | 5 |
| fft peak Hz | 5 |
| samples | 40 |
| sampled rms | 0.70710678 |

1. Sample a 35 Hz sinusoid at 20 samples per second.

2. The sample interval is 0.050000 s and Nyquist frequency is 10.000000 Hz.

3. The analytical alias frequency is 5.000000 Hz.

4. An 40-sample FFT resolves bins spaced 0.500000 Hz; peak bin is 5.000000 Hz.

5. Sampled RMS is 0.707107; exact coincidences can produce misleading zeros.

#### Worked case 1: sample_rate = 40

This case keeps the nominal configuration except for sample_rate=40. The full input is {"duration": 2.0, "sample_rate": 40.0, "signal_frequency": 35.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| nyquist Hz | 20 |
| alias Hz | 5 |
| fft peak Hz | 5 |
| samples | 80 |
| sampled rms | 0.70710678 |

1. Sample a 35 Hz sinusoid at 40 samples per second.

2. The sample interval is 0.025000 s and Nyquist frequency is 20.000000 Hz.

3. The analytical alias frequency is 5.000000 Hz.

4. An 80-sample FFT resolves bins spaced 0.500000 Hz; peak bin is 5.000000 Hz.

5. Sampled RMS is 0.707107; exact coincidences can produce misleading zeros.

#### Worked case 2: sample_rate = 60

This case keeps the nominal configuration except for sample_rate=60. The full input is {"duration": 2.0, "sample_rate": 60.0, "signal_frequency": 35.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| nyquist Hz | 30 |
| alias Hz | 25 |
| fft peak Hz | 25 |
| samples | 120 |
| sampled rms | 0.70710678 |

1. Sample a 35 Hz sinusoid at 60 samples per second.

2. The sample interval is 0.016667 s and Nyquist frequency is 30.000000 Hz.

3. The analytical alias frequency is 25.000000 Hz.

4. An 120-sample FFT resolves bins spaced 0.500000 Hz; peak bin is 25.000000 Hz.

5. Sampled RMS is 0.707107; exact coincidences can produce misleading zeros.

#### Worked case 3: sample_rate = 80

This case keeps the nominal configuration except for sample_rate=80. The full input is {"duration": 2.0, "sample_rate": 80.0, "signal_frequency": 35.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| nyquist Hz | 40 |
| alias Hz | 35 |
| fft peak Hz | 35 |
| samples | 160 |
| sampled rms | 0.70710678 |

1. Sample a 35 Hz sinusoid at 80 samples per second.

2. The sample interval is 0.012500 s and Nyquist frequency is 40.000000 Hz.

3. The analytical alias frequency is 35.000000 Hz.

4. An 160-sample FFT resolves bins spaced 0.500000 Hz; peak bin is 35.000000 Hz.

5. Sampled RMS is 0.707107; exact coincidences can produce misleading zeros.

Signal lies below Nyquist, but practical reconstruction still needs filtering assumptions.

#### Worked case 4: sample_rate = 100

This case keeps the nominal configuration except for sample_rate=100. The full input is {"duration": 2.0, "sample_rate": 100.0, "signal_frequency": 35.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| nyquist Hz | 50 |
| alias Hz | 35 |
| fft peak Hz | 35 |
| samples | 200 |
| sampled rms | 0.70710678 |

1. Sample a 35 Hz sinusoid at 100 samples per second.

2. The sample interval is 0.010000 s and Nyquist frequency is 50.000000 Hz.

3. The analytical alias frequency is 35.000000 Hz.

4. An 200-sample FFT resolves bins spaced 0.500000 Hz; peak bin is 35.000000 Hz.

5. Sampled RMS is 0.707107; exact coincidences can produce misleading zeros.

Signal lies below Nyquist, but practical reconstruction still needs filtering assumptions.

#### Worked case 5: sample_rate = 200

This case keeps the nominal configuration except for sample_rate=200. The full input is {"duration": 2.0, "sample_rate": 200.0, "signal_frequency": 35.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| nyquist Hz | 100 |
| alias Hz | 35 |
| fft peak Hz | 35 |
| samples | 400 |
| sampled rms | 0.70710678 |

1. Sample a 35 Hz sinusoid at 200 samples per second.

2. The sample interval is 0.005000 s and Nyquist frequency is 100.000000 Hz.

3. The analytical alias frequency is 35.000000 Hz.

4. An 400-sample FFT resolves bins spaced 0.500000 Hz; peak bin is 35.000000 Hz.

5. Sampled RMS is 0.707107; exact coincidences can produce misleading zeros.

Signal lies below Nyquist, but practical reconstruction still needs filtering assumptions.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The original signal cannot be uniquely recovered from these samples without extra information.

FFT leakage depends on record duration and windowing; a peak bin alone is not a precision frequency estimate.

### K. Failure modes and troubleshooting

Inferring physical oscillation frequency from a low-rate dashboard; reducing sample rate without filtering; trusting a line drawn between sparse points.

### L. Practical exercises and extension tasks

1. Change sinusoid phase and inspect exact-coincidence cases.

2. Compare a two-second and ten-second FFT record.

3. Design a display decimator while preserving the original controller samples.

### M. Connection to the Asimov research platform

High-frequency encoder/IMU motion and low-rate network telemetry serve different purposes; the dashboard is not a control sensor.

### N. Completion record

Record your chosen case, predicted trend, measured nyquist_Hz, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 11, Link masses, payload shifts and center of mass. Keep the present result as a reference fixture for diagnosing changes in the larger stack.
