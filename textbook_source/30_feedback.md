# Part VIII - Feedback, trajectories and actuator constraints

A command generator, feedback law and actuator are different components. A smooth trajectory can exceed torque authority; a stable ideal controller can become unstable with delay; a motor that meets a peak load can overheat over repeated cycles. The laboratories below keep these boundaries explicit and measure the tradeoffs. Treat every numerical value as an exercise input until it has been replaced by an identified or verified physical parameter.

## Laboratory 21 - Second-order joint dynamics and PD tuning

### A. The engineering question

Feedback gains set a closed-loop dynamic behavior, not merely a preference for stronger correction.

### B. Concepts and mathematical model

For a single inertia with viscous damping, proportional feedback adds stiffness and derivative feedback adds damping. Natural frequency and damping ratio connect these gains to response speed and overshoot. The same numerical gains behave differently when inertia changes. This experiment integrates an ideal one-axis joint with a small target step and reports error and overshoot rather than judging the response by appearance.

I*q_ddot + (b+Kd)*q_dot + Kp*q = Kp*q_target; omega_n=sqrt(Kp/I); zeta=(b+Kd)/(2*sqrt(Kp*I)).

### C. Real-world meaning and limits

Physical gain changes require identified inertia, sensor noise, delay and a guarded test envelope; theoretical tuning is only a starting point.

### D. Architecture and data flow

Configuration (inertia, kp, kd) -> numerical model -> natural_frequency_rad_s, damping_ratio, overshoot_fraction -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

inertia is output-axis kg*m^2; kp is Nm/rad; kd is Nm*s/rad; physical viscous damping is fixed at 0.1 Nm*s/rad.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| inertia | 0.08 | kg*m^2 |
| kp | 20 | Nm/rad |
| kd | 2 | Nm*s/rad |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/21_pd_control.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only kd changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/21_pd_control.py --case 0

.venv-book/bin/python expanded_lab/modules/21_pd_control.py --case 3

.venv-book/bin/python expanded_lab/run.py pd_control --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/21_pd_control.py

### H. Walkthrough and design decisions

The velocity update precedes the position update, giving semi-implicit integration. Compare simulated overshoot with the damping classification; then vary inertia to see why gains are model dependent.

### I. Expected behavior and six worked cases

The controlled variable is kd. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/21_pd_control.png

Figure L21. natural frequency rad s as kd changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | kd | natural frequency rad s |
|---|---|---|
| 0 | 0.1 | 15.8113883 |
| 1 | 0.5 | 15.8113883 |
| 2 | 1 | 15.8113883 |
| 3 | 2 | 15.8113883 |
| 4 | 4 | 15.8113883 |
| 5 | 8 | 15.8113883 |

#### Worked case 0: kd = 0.1

This case keeps the nominal configuration except for kd=0.1. The full input is {"inertia": 0.08, "kd": 0.1, "kp": 20.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural frequency rad s | 15.8113883 |
| damping ratio | 0.07905694 |
| overshoot fraction | 0.77936206 |
| final error rad | -0.00232973 |
| trajectory rmse rad | 0.0260547 |

1. Joint inertia is 0.08 kg*m^2; Kp=20 Nm/rad; Kd=0.1 Nm*s/rad.

2. The implied natural frequency is 15.811388 rad/s and damping ratio is 0.079057.

3. Apply a 0.1 rad target and integrate semi-implicitly at 1 ms for three seconds.

4. Peak position is 0.177936 rad, producing overshoot fraction 0.779362.

5. Final tracking error is -0.00232973 rad; trajectory RMSE is 0.026055 rad.

#### Worked case 1: kd = 0.5

This case keeps the nominal configuration except for kd=0.5. The full input is {"inertia": 0.08, "kd": 0.5, "kp": 20.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural frequency rad s | 15.8113883 |
| damping ratio | 0.23717082 |
| overshoot fraction | 0.46371639 |
| final error rad | -4.7227297e-07 |
| trajectory rmse rad | 0.01637283 |

1. Joint inertia is 0.08 kg*m^2; Kp=20 Nm/rad; Kd=0.5 Nm*s/rad.

2. The implied natural frequency is 15.811388 rad/s and damping ratio is 0.237171.

3. Apply a 0.1 rad target and integrate semi-implicitly at 1 ms for three seconds.

4. Peak position is 0.146372 rad, producing overshoot fraction 0.463716.

5. Final tracking error is -0.00000047 rad; trajectory RMSE is 0.016373 rad.

#### Worked case 2: kd = 1

This case keeps the nominal configuration except for kd=1. The full input is {"inertia": 0.08, "kd": 1.0, "kp": 20.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural frequency rad s | 15.8113883 |
| damping ratio | 0.43481318 |
| overshoot fraction | 0.21797678 |
| final error rad | -2.8162611e-12 |
| trajectory rmse rad | 0.01444713 |

1. Joint inertia is 0.08 kg*m^2; Kp=20 Nm/rad; Kd=1 Nm*s/rad.

2. The implied natural frequency is 15.811388 rad/s and damping ratio is 0.434813.

3. Apply a 0.1 rad target and integrate semi-implicitly at 1 ms for three seconds.

4. Peak position is 0.121798 rad, producing overshoot fraction 0.217977.

5. Final tracking error is -0.00000000 rad; trajectory RMSE is 0.014447 rad.

#### Worked case 3: kd = 2

This case keeps the nominal configuration except for kd=2. The full input is {"inertia": 0.08, "kd": 2.0, "kp": 20.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural frequency rad s | 15.8113883 |
| damping ratio | 0.83009789 |
| overshoot fraction | 0.00840482 |
| final error rad | -2.2204460e-16 |
| trajectory rmse rad | 0.01530782 |

1. Joint inertia is 0.08 kg*m^2; Kp=20 Nm/rad; Kd=2 Nm*s/rad.

2. The implied natural frequency is 15.811388 rad/s and damping ratio is 0.830098.

3. Apply a 0.1 rad target and integrate semi-implicitly at 1 ms for three seconds.

4. Peak position is 0.100840 rad, producing overshoot fraction 0.008405.

5. Final tracking error is -0.00000000 rad; trajectory RMSE is 0.015308 rad.

#### Worked case 4: kd = 4

This case keeps the nominal configuration except for kd=4. The full input is {"inertia": 0.08, "kd": 4.0, "kp": 20.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural frequency rad s | 15.8113883 |
| damping ratio | 1.6206673 |
| overshoot fraction | 0 |
| final error rad | 9.1892507e-09 |
| trajectory rmse rad | 0.01923597 |

1. Joint inertia is 0.08 kg*m^2; Kp=20 Nm/rad; Kd=4 Nm*s/rad.

2. The implied natural frequency is 15.811388 rad/s and damping ratio is 1.620667.

3. Apply a 0.1 rad target and integrate semi-implicitly at 1 ms for three seconds.

4. Peak position is 0.100000 rad, producing overshoot fraction 0.000000.

5. Final tracking error is 0.00000001 rad; trajectory RMSE is 0.019236 rad.

This model is critically damped or overdamped.

#### Worked case 5: kd = 8

This case keeps the nominal configuration except for kd=8. The full input is {"inertia": 0.08, "kd": 8.0, "kp": 20.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| natural frequency rad s | 15.8113883 |
| damping ratio | 3.20180613 |
| overshoot fraction | 0 |
| final error rad | 0.00005188 |
| trajectory rmse rad | 0.02621631 |

1. Joint inertia is 0.08 kg*m^2; Kp=20 Nm/rad; Kd=8 Nm*s/rad.

2. The implied natural frequency is 15.811388 rad/s and damping ratio is 3.201806.

3. Apply a 0.1 rad target and integrate semi-implicitly at 1 ms for three seconds.

4. Peak position is 0.099948 rad, producing overshoot fraction 0.000000.

5. Final tracking error is 0.00005188 rad; trajectory RMSE is 0.026216 rad.

This model is critically damped or overdamped.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

This model is underdamped.

There is no torque saturation, delay, gravity or contact in this identification-friendly reference.

### K. Failure modes and troubleshooting

Increasing Kp to compensate for torque saturation; differentiating a noisy setpoint instead of defining derivative action carefully.

### L. Practical exercises and extension tasks

1. Double inertia and recover the original natural frequency and damping ratio.

2. Add a torque cap and compare the linear prediction to the actual response.

3. Measure settling within a predeclared error band.

### M. Connection to the Asimov research platform

Physical gain changes require identified inertia, sensor noise, delay and a guarded test envelope; theoretical tuning is only a starting point.

### N. Completion record

Record your chosen case, predicted trend, measured natural_frequency_rad_s, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 22, Integral action, saturation and anti-windup. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 22 - Integral action, saturation and anti-windup

### A. The engineering question

Integral action accumulates persistent error and can compensate an unknown constant disturbance.

### B. Concepts and mathematical model

When an actuator saturates, continued integration stores a demand that the plant cannot realize. After the target changes, this stored integral can keep the output saturated in the wrong direction. Conditional integration is a simple anti-windup method: integrate only when unsaturated or when the error would move the demand back toward the permitted range. The experiment explicitly compares the same plant with and without this logic.

u_raw=Kp*e+Ki*integral-Kd*v; u=clip(u_raw); integrate if unsaturated or e*(u_raw-u)<=0.

### C. Real-world meaning and limits

Integral action can command sustained physical torque; thermal and fault behavior must be part of its design.

### D. Architecture and data flow

Configuration (torque_cap) -> numerical model -> plain_final_error_rad, protected_final_error_rad, plain_integral -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

torque_cap is the symmetric teaching actuator limit in Nm; plant inertia is 0.2 kg*m^2 and timestep is 2 ms.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| torque_cap | 1 | Nm |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/22_antiwindup.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only torque_cap changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/22_antiwindup.py --case 0

.venv-book/bin/python expanded_lab/modules/22_antiwindup.py --case 3

.venv-book/bin/python expanded_lab/run.py antiwindup --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/22_antiwindup.py

### H. Walkthrough and design decisions

The paired simulations share target, gains and plant. Only the integral update rule changes, making the comparison causal. Inspect the return-to-zero segment rather than only the initial rise.

### I. Expected behavior and six worked cases

The controlled variable is torque_cap. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/22_antiwindup.png

Figure L22. plain final error rad as torque_cap changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | torque_cap | plain final error rad |
|---|---|---|
| 0 | 0.1 | 0.12410345 |
| 1 | 0.25 | 0.29555289 |
| 2 | 0.5 | 0.02649489 |
| 3 | 1 | 0.00841963 |
| 4 | 2 | 0.00530972 |
| 5 | 5 | 0.00387863 |

#### Worked case 0: torque_cap = 0.1

This case keeps the nominal configuration except for torque_cap=0.1. The full input is {"torque_cap": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| plain final error rad | 0.12410345 |
| protected final error rad | 0.00146551 |
| plain integral | -0.03609486 |
| protected integral | -0.00169588 |
| plain saturation fraction | 0.98 |
| protected saturation fraction | 0.77 |

1. Use symmetric actuator limit +/-0.1 Nm.

2. Request 0.5 rad for one second, then return the target to zero.

3. Without anti-windup, saturation fraction is 0.980000 and final integral is -0.036095.

4. Conditional integration gives saturation fraction 0.770000 and integral -0.001696.

5. Final absolute errors are 0.124103 and 0.001466 rad respectively.

#### Worked case 1: torque_cap = 0.25

This case keeps the nominal configuration except for torque_cap=0.25. The full input is {"torque_cap": 0.25}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| plain final error rad | 0.29555289 |
| protected final error rad | 0.00011126 |
| plain integral | -0.01474504 |
| protected integral | 0.00015196 |
| plain saturation fraction | 0.989 |
| protected saturation fraction | 0.669 |

1. Use symmetric actuator limit +/-0.25 Nm.

2. Request 0.5 rad for one second, then return the target to zero.

3. Without anti-windup, saturation fraction is 0.989000 and final integral is -0.014745.

4. Conditional integration gives saturation fraction 0.669000 and integral 0.000152.

5. Final absolute errors are 0.295553 and 0.000111 rad respectively.

#### Worked case 2: torque_cap = 0.5

This case keeps the nominal configuration except for torque_cap=0.5. The full input is {"torque_cap": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| plain final error rad | 0.02649489 |
| protected final error rad | 0.00052309 |
| plain integral | -0.02626605 |
| protected integral | -0.00052365 |
| plain saturation fraction | 0.645 |
| protected saturation fraction | 0.345 |

1. Use symmetric actuator limit +/-0.5 Nm.

2. Request 0.5 rad for one second, then return the target to zero.

3. Without anti-windup, saturation fraction is 0.645000 and final integral is -0.026266.

4. Conditional integration gives saturation fraction 0.345000 and integral -0.000524.

5. Final absolute errors are 0.026495 and 0.000523 rad respectively.

#### Worked case 3: torque_cap = 1

This case keeps the nominal configuration except for torque_cap=1. The full input is {"torque_cap": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| plain final error rad | 0.00841963 |
| protected final error rad | 0.00132785 |
| plain integral | -0.00841603 |
| protected integral | -0.00132748 |
| plain saturation fraction | 0.177 |
| protected saturation fraction | 0.147 |

1. Use symmetric actuator limit +/-1 Nm.

2. Request 0.5 rad for one second, then return the target to zero.

3. Without anti-windup, saturation fraction is 0.177000 and final integral is -0.008416.

4. Conditional integration gives saturation fraction 0.147000 and integral -0.001327.

5. Final absolute errors are 0.008420 and 0.001328 rad respectively.

#### Worked case 4: torque_cap = 2

This case keeps the nominal configuration except for torque_cap=2. The full input is {"torque_cap": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| plain final error rad | 0.00530972 |
| protected final error rad | 0.00208745 |
| plain integral | -0.00530725 |
| protected integral | -0.00208652 |
| plain saturation fraction | 0.084 |
| protected saturation fraction | 0.073 |

1. Use symmetric actuator limit +/-2 Nm.

2. Request 0.5 rad for one second, then return the target to zero.

3. Without anti-windup, saturation fraction is 0.084000 and final integral is -0.005307.

4. Conditional integration gives saturation fraction 0.073000 and integral -0.002087.

5. Final absolute errors are 0.005310 and 0.002087 rad respectively.

#### Worked case 5: torque_cap = 5

This case keeps the nominal configuration except for torque_cap=5. The full input is {"torque_cap": 5.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| plain final error rad | 0.00387863 |
| protected final error rad | 0.00350293 |
| plain integral | -0.00387674 |
| protected integral | -0.00350123 |
| plain saturation fraction | 0.0105 |
| protected saturation fraction | 0.0095 |

1. Use symmetric actuator limit +/-5 Nm.

2. Request 0.5 rad for one second, then return the target to zero.

3. Without anti-windup, saturation fraction is 0.010500 and final integral is -0.003877.

4. Conditional integration gives saturation fraction 0.009500 and integral -0.003501.

5. Final absolute errors are 0.003879 and 0.003503 rad respectively.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Anti-windup improves consistency with actuator authority but does not guarantee every transient metric improves.

Integral state must also be handled explicitly when changing modes, resetting faults or switching controllers.

### K. Failure modes and troubleshooting

Clamping the output while leaving integral unbounded; resetting integral unexpectedly during a loaded transition; claiming one example proves all PID tuning.

### L. Practical exercises and extension tasks

1. Add back-calculation anti-windup and compare with conditional integration.

2. Apply a constant load and examine steady-state error.

3. Define a bumpless transfer from PD to PID.

### M. Connection to the Asimov research platform

Integral action can command sustained physical torque; thermal and fault behavior must be part of its design.

### N. Completion record

Record your chosen case, predicted trend, measured plain_final_error_rad, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 23, Minimum-jerk trajectories and duration constraints. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 23 - Minimum-jerk trajectories and duration constraints

### A. The engineering question

A position step implies unbounded ideal velocity and acceleration.

### B. Concepts and mathematical model

A fifth-order minimum-jerk interpolation has zero endpoint velocity and acceleration, making it a useful smooth reference for a point-to-point move. Smoothness does not establish feasibility: shortening the duration increases velocity, acceleration and jerk by different powers. This laboratory computes those quantities analytically and compares them with finite sampled values so a trajectory can be rejected before being sent to a controller.

s=10*r^3-15*r^4+6*r^5; q=q0+delta*s; q_dot=delta*s_prime/T; q_ddot=delta*s_second/T^2.

### C. Real-world meaning and limits

Physical trajectories need torque, collision, cable and thermal feasibility in addition to smooth kinematic references.

### D. Architecture and data flow

Configuration (duration, excursion) -> numerical model -> peak_speed_rad_s, peak_acceleration_rad_s2, peak_jerk_rad_s3 -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

duration is seconds; excursion is output-joint radians. The interpolation starts from zero relative displacement.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| duration | 2 | seconds |
| excursion | 0.4 | radians |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/23_minimum_jerk.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only duration changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/23_minimum_jerk.py --case 0

.venv-book/bin/python expanded_lab/modules/23_minimum_jerk.py --case 3

.venv-book/bin/python expanded_lab/run.py minimum_jerk --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/23_minimum_jerk.py

### H. Walkthrough and design decisions

Use normalized time to separate trajectory shape from duration. The endpoint assertions check boundary conditions, while derivative scaling exposes why a fast smooth move can still be infeasible.

### I. Expected behavior and six worked cases

The controlled variable is duration. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/23_minimum_jerk.png

Figure L23. peak speed rad s as duration changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | duration | peak speed rad s |
|---|---|---|
| 0 | 0.25 | 3 |
| 1 | 0.5 | 1.5 |
| 2 | 1 | 0.75 |
| 3 | 2 | 0.375 |
| 4 | 3 | 0.25 |
| 5 | 5 | 0.15 |

#### Worked case 0: duration = 0.25

This case keeps the nominal configuration except for duration=0.25. The full input is {"duration": 0.25, "excursion": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| peak speed rad s | 3 |
| peak acceleration rad s2 | 36.95034701 |
| peak jerk rad s3 | 1536 |
| final position rad | 0.4 |
| speed limit margin rad s | -2.5 |

1. Move through delta=0.4 rad over duration T=0.25 s.

2. Evaluate the polynomial and its first three derivatives at 1001 normalized positions.

3. Peak speed is 3.000000 rad/s.

4. Peak acceleration is 36.950347 rad/s^2; peak jerk is 1536.000000 rad/s^3.

5. Against an illustrative 0.5 rad/s speed envelope, margin is -2.500000 rad/s.

#### Worked case 1: duration = 0.5

This case keeps the nominal configuration except for duration=0.5. The full input is {"duration": 0.5, "excursion": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| peak speed rad s | 1.5 |
| peak acceleration rad s2 | 9.23758675 |
| peak jerk rad s3 | 192 |
| final position rad | 0.4 |
| speed limit margin rad s | -1 |

1. Move through delta=0.4 rad over duration T=0.5 s.

2. Evaluate the polynomial and its first three derivatives at 1001 normalized positions.

3. Peak speed is 1.500000 rad/s.

4. Peak acceleration is 9.237587 rad/s^2; peak jerk is 192.000000 rad/s^3.

5. Against an illustrative 0.5 rad/s speed envelope, margin is -1.000000 rad/s.

#### Worked case 2: duration = 1

This case keeps the nominal configuration except for duration=1. The full input is {"duration": 1.0, "excursion": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| peak speed rad s | 0.75 |
| peak acceleration rad s2 | 2.30939669 |
| peak jerk rad s3 | 24 |
| final position rad | 0.4 |
| speed limit margin rad s | -0.25 |

1. Move through delta=0.4 rad over duration T=1 s.

2. Evaluate the polynomial and its first three derivatives at 1001 normalized positions.

3. Peak speed is 0.750000 rad/s.

4. Peak acceleration is 2.309397 rad/s^2; peak jerk is 24.000000 rad/s^3.

5. Against an illustrative 0.5 rad/s speed envelope, margin is -0.250000 rad/s.

#### Worked case 3: duration = 2

This case keeps the nominal configuration except for duration=2. The full input is {"duration": 2.0, "excursion": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| peak speed rad s | 0.375 |
| peak acceleration rad s2 | 0.57734917 |
| peak jerk rad s3 | 3 |
| final position rad | 0.4 |
| speed limit margin rad s | 0.125 |

1. Move through delta=0.4 rad over duration T=2 s.

2. Evaluate the polynomial and its first three derivatives at 1001 normalized positions.

3. Peak speed is 0.375000 rad/s.

4. Peak acceleration is 0.577349 rad/s^2; peak jerk is 3.000000 rad/s^3.

5. Against an illustrative 0.5 rad/s speed envelope, margin is 0.125000 rad/s.

#### Worked case 4: duration = 3

This case keeps the nominal configuration except for duration=3. The full input is {"duration": 3.0, "excursion": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| peak speed rad s | 0.25 |
| peak acceleration rad s2 | 0.25659963 |
| peak jerk rad s3 | 0.88888889 |
| final position rad | 0.4 |
| speed limit margin rad s | 0.25 |

1. Move through delta=0.4 rad over duration T=3 s.

2. Evaluate the polynomial and its first three derivatives at 1001 normalized positions.

3. Peak speed is 0.250000 rad/s.

4. Peak acceleration is 0.256600 rad/s^2; peak jerk is 0.888889 rad/s^3.

5. Against an illustrative 0.5 rad/s speed envelope, margin is 0.250000 rad/s.

#### Worked case 5: duration = 5

This case keeps the nominal configuration except for duration=5. The full input is {"duration": 5.0, "excursion": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| peak speed rad s | 0.15 |
| peak acceleration rad s2 | 0.09237587 |
| peak jerk rad s3 | 0.192 |
| final position rad | 0.4 |
| speed limit margin rad s | 0.35 |

1. Move through delta=0.4 rad over duration T=5 s.

2. Evaluate the polynomial and its first three derivatives at 1001 normalized positions.

3. Peak speed is 0.150000 rad/s.

4. Peak acceleration is 0.092376 rad/s^2; peak jerk is 0.192000 rad/s^3.

5. Against an illustrative 0.5 rad/s speed envelope, margin is 0.350000 rad/s.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The speed envelope is a teaching assumption and must not be substituted for a released actuator limit.

Zero endpoint velocity and acceleration do not ensure the controller can supply the required intermediate torque.

### K. Failure modes and troubleshooting

Checking position limits but not derivatives; differentiating noisy numerical samples when analytic derivatives are available; ignoring start velocity.

### L. Practical exercises and extension tasks

1. Derive a minimum duration from a chosen speed limit.

2. Check an acceleration limit and choose the stricter duration.

3. Generalize to nonzero initial velocity using a boundary-value polynomial.

### M. Connection to the Asimov research platform

Physical trajectories need torque, collision, cable and thermal feasibility in addition to smooth kinematic references.

### N. Completion record

Record your chosen case, predicted trend, measured peak_speed_rad_s, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 24, Position envelopes, slew limits and stopping distance. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 24 - Position envelopes, slew limits and stopping distance

### A. The engineering question

A position limit alone does not protect a joint already moving toward a stop.

### B. Concepts and mathematical model

The controller also needs enough distance to decelerate within its available authority. A slew limiter bounds requested changes but can introduce tracking lag, while an emergency stop requires a separate physically reviewed outcome. This experiment applies a velocity-limited target and calculates an ideal stopping-distance screen including reaction delay. It is a planning calculation, not a certified stopping model.

q_next=q_prev+clip(q_request-q_prev,+/-vmax*dt); d_stop=v*delay+v^2/(2*a_brake).

### C. Real-world meaning and limits

Physical limits require independent sensing, conservative travel margins and a stop strategy compatible with the support rig.

### D. Architecture and data flow

Configuration (speed, dt, delay, deceleration) -> numerical model -> final_target_rad, ideal_stopping_distance_rad, remaining_travel_margin_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

speed is rad/s; dt and delay are seconds; deceleration is a positive assumed rad/s^2 magnitude.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| speed | 0.4 | angular speed in the chapter equation |
| dt | 0.01 | seconds |
| delay | 0.05 | seconds |
| deceleration | 2 | rad/s^2 |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/24_rate_limits.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only speed changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/24_rate_limits.py --case 0

.venv-book/bin/python expanded_lab/modules/24_rate_limits.py --case 3

.venv-book/bin/python expanded_lab/run.py rate_limits --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/24_rate_limits.py

### H. Walkthrough and design decisions

Calculate reaction travel and braking travel separately. The target slew limiter governs requests, whereas actual velocity and stopping must be monitored from feedback.

### I. Expected behavior and six worked cases

The controlled variable is speed. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/24_rate_limits.png

Figure L24. final target rad as speed changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | speed | final target rad |
|---|---|---|
| 0 | 0.1 | 0.5 |
| 1 | 0.2 | 0.5 |
| 2 | 0.4 | 0.5 |
| 3 | 0.6 | 0.5 |
| 4 | 0.8 | 0.5 |
| 5 | 1 | 0.5 |

#### Worked case 0: speed = 0.1

This case keeps the nominal configuration except for speed=0.1. The full input is {"deceleration": 2.0, "delay": 0.05, "dt": 0.01, "speed": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final target rad | 0.5 |
| ideal stopping distance rad | 0.0075 |
| remaining travel margin rad | 0.1125 |
| per update step rad | 0.001 |
| time to target s | 5 |

1. At vmax=0.1 rad/s and dt=0.01 s, each target increment is capped at 0.001000 rad.

2. Reaction delay contributes 0.005000 rad of travel.

3. Ideal constant deceleration 2 rad/s^2 contributes 0.002500 rad.

4. Total screened stopping distance is 0.007500 rad.

5. With 0.12 rad assumed remaining travel, margin is 0.112500 rad.

#### Worked case 1: speed = 0.2

This case keeps the nominal configuration except for speed=0.2. The full input is {"deceleration": 2.0, "delay": 0.05, "dt": 0.01, "speed": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final target rad | 0.5 |
| ideal stopping distance rad | 0.02 |
| remaining travel margin rad | 0.1 |
| per update step rad | 0.002 |
| time to target s | 2.5 |

1. At vmax=0.2 rad/s and dt=0.01 s, each target increment is capped at 0.002000 rad.

2. Reaction delay contributes 0.010000 rad of travel.

3. Ideal constant deceleration 2 rad/s^2 contributes 0.010000 rad.

4. Total screened stopping distance is 0.020000 rad.

5. With 0.12 rad assumed remaining travel, margin is 0.100000 rad.

#### Worked case 2: speed = 0.4

This case keeps the nominal configuration except for speed=0.4. The full input is {"deceleration": 2.0, "delay": 0.05, "dt": 0.01, "speed": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final target rad | 0.5 |
| ideal stopping distance rad | 0.06 |
| remaining travel margin rad | 0.06 |
| per update step rad | 0.004 |
| time to target s | 1.25 |

1. At vmax=0.4 rad/s and dt=0.01 s, each target increment is capped at 0.004000 rad.

2. Reaction delay contributes 0.020000 rad of travel.

3. Ideal constant deceleration 2 rad/s^2 contributes 0.040000 rad.

4. Total screened stopping distance is 0.060000 rad.

5. With 0.12 rad assumed remaining travel, margin is 0.060000 rad.

#### Worked case 3: speed = 0.6

This case keeps the nominal configuration except for speed=0.6. The full input is {"deceleration": 2.0, "delay": 0.05, "dt": 0.01, "speed": 0.6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final target rad | 0.5 |
| ideal stopping distance rad | 0.12 |
| remaining travel margin rad | 0 |
| per update step rad | 0.006 |
| time to target s | 0.83333333 |

1. At vmax=0.6 rad/s and dt=0.01 s, each target increment is capped at 0.006000 rad.

2. Reaction delay contributes 0.030000 rad of travel.

3. Ideal constant deceleration 2 rad/s^2 contributes 0.090000 rad.

4. Total screened stopping distance is 0.120000 rad.

5. With 0.12 rad assumed remaining travel, margin is 0.000000 rad.

#### Worked case 4: speed = 0.8

This case keeps the nominal configuration except for speed=0.8. The full input is {"deceleration": 2.0, "delay": 0.05, "dt": 0.01, "speed": 0.8}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final target rad | 0.5 |
| ideal stopping distance rad | 0.2 |
| remaining travel margin rad | -0.08 |
| per update step rad | 0.008 |
| time to target s | 0.625 |

1. At vmax=0.8 rad/s and dt=0.01 s, each target increment is capped at 0.008000 rad.

2. Reaction delay contributes 0.040000 rad of travel.

3. Ideal constant deceleration 2 rad/s^2 contributes 0.160000 rad.

4. Total screened stopping distance is 0.200000 rad.

5. With 0.12 rad assumed remaining travel, margin is -0.080000 rad.

The ideal calculation already exceeds available travel; reduce speed or increase clearance before considering uncertainty.

#### Worked case 5: speed = 1

This case keeps the nominal configuration except for speed=1. The full input is {"deceleration": 2.0, "delay": 0.05, "dt": 0.01, "speed": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final target rad | 0.5 |
| ideal stopping distance rad | 0.3 |
| remaining travel margin rad | -0.18 |
| per update step rad | 0.01 |
| time to target s | 0.5 |

1. At vmax=1 rad/s and dt=0.01 s, each target increment is capped at 0.010000 rad.

2. Reaction delay contributes 0.050000 rad of travel.

3. Ideal constant deceleration 2 rad/s^2 contributes 0.250000 rad.

4. Total screened stopping distance is 0.300000 rad.

5. With 0.12 rad assumed remaining travel, margin is -0.180000 rad.

The ideal calculation already exceeds available travel; reduce speed or increase clearance before considering uncertainty.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The ideal calculation leaves positive travel margin.

Load, control delay, brake authority and power-loss behavior must be measured for a physical stopping claim.

### K. Failure modes and troubleshooting

Calling a setpoint limiter a measured speed limiter; assuming torque remains available after power isolation; ignoring gravity-assisted motion.

### L. Practical exercises and extension tasks

1. Propagate uncertainty in delay and deceleration to a conservative margin.

2. Add acceleration-limited setpoint generation.

3. Compare command motion and measured motion under saturation.

### M. Connection to the Asimov research platform

Physical limits require independent sensing, conservative travel margins and a stop strategy compatible with the support rig.

### N. Completion record

Record your chosen case, predicted trend, measured final_target_rad, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 25, Gravity compensation and model-mismatch torque. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 25 - Gravity compensation and model-mismatch torque

### A. The engineering question

Gravity compensation predicts load torque from configuration and feeds it forward so feedback need not create all supporting effort through error.

### B. Concepts and mathematical model

A biased mass or lever estimate creates a pose-dependent residual. This is different from a constant encoder offset or viscous friction. The experiment synthesizes static measurements over a range of angles and estimates the gravity coefficient from a cosine basis. It then quantifies the residual if the controller uses an incorrect payload mass.

gravity torque = A*cos(q); A=m*g*l; A_hat=(cos(q).T*y)/(cos(q).T*cos(q)).

### C. Real-world meaning and limits

Actual gravity compensation requires verified model conventions and low-energy measurements with load support.

### D. Architecture and data flow

Configuration (model_mass) -> numerical model -> feedforward_rmse_Nm, peak_residual_Nm, identified_mass_kg -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

model_mass is the controller payload estimate in kilograms; true teaching mass is 2 kg at a 0.25 m lever.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| model_mass | 1.8 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/25_gravity_identification.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only model_mass changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/25_gravity_identification.py --case 0

.venv-book/bin/python expanded_lab/modules/25_gravity_identification.py --case 3

.venv-book/bin/python expanded_lab/run.py gravity_identification --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/25_gravity_identification.py

### H. Walkthrough and design decisions

The identification uses independent synthetic measurements rather than fitting the controller prediction. Report fit residual and feedforward-model residual separately; they answer different questions.

### I. Expected behavior and six worked cases

The controlled variable is model_mass. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/25_gravity_identification.png

Figure L25. feedforward rmse Nm as model_mass changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | model_mass | feedforward rmse Nm |
|---|---|---|
| 0 | 1 | 2.07598012 |
| 1 | 1.5 | 1.03799006 |
| 2 | 1.8 | 0.41519602 |
| 3 | 2 | 0 |
| 4 | 2.2 | 0.41519602 |
| 5 | 2.5 | 1.03799006 |

#### Worked case 0: model_mass = 1

This case keeps the nominal configuration except for model_mass=1. The full input is {"model_mass": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| feedforward rmse Nm | 2.07598012 |
| peak residual Nm | 2.4525 |
| identified mass kg | 2.00010562 |
| fit residual rmse Nm | 0.03442849 |

1. The true static gravity coefficient is 4.905000 Nm.

2. The assumed model uses mass 1 kg and coefficient 2.452500 Nm.

3. Generate static samples over -1 to +1 rad with 0.03 Nm standard-deviation noise.

4. Project measurements onto cos(q), obtaining A_hat=4.905259 Nm.

5. The inferred mass is 2.000106 kg; feedforward mismatch RMSE is 2.075980 Nm.

#### Worked case 1: model_mass = 1.5

This case keeps the nominal configuration except for model_mass=1.5. The full input is {"model_mass": 1.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| feedforward rmse Nm | 1.03799006 |
| peak residual Nm | 1.22625 |
| identified mass kg | 2.00010562 |
| fit residual rmse Nm | 0.03442849 |

1. The true static gravity coefficient is 4.905000 Nm.

2. The assumed model uses mass 1.5 kg and coefficient 3.678750 Nm.

3. Generate static samples over -1 to +1 rad with 0.03 Nm standard-deviation noise.

4. Project measurements onto cos(q), obtaining A_hat=4.905259 Nm.

5. The inferred mass is 2.000106 kg; feedforward mismatch RMSE is 1.037990 Nm.

#### Worked case 2: model_mass = 1.8

This case keeps the nominal configuration except for model_mass=1.8. The full input is {"model_mass": 1.8}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| feedforward rmse Nm | 0.41519602 |
| peak residual Nm | 0.4905 |
| identified mass kg | 2.00010562 |
| fit residual rmse Nm | 0.03442849 |

1. The true static gravity coefficient is 4.905000 Nm.

2. The assumed model uses mass 1.8 kg and coefficient 4.414500 Nm.

3. Generate static samples over -1 to +1 rad with 0.03 Nm standard-deviation noise.

4. Project measurements onto cos(q), obtaining A_hat=4.905259 Nm.

5. The inferred mass is 2.000106 kg; feedforward mismatch RMSE is 0.415196 Nm.

#### Worked case 3: model_mass = 2

This case keeps the nominal configuration except for model_mass=2. The full input is {"model_mass": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| feedforward rmse Nm | 0 |
| peak residual Nm | 0 |
| identified mass kg | 2.00010562 |
| fit residual rmse Nm | 0.03442849 |

1. The true static gravity coefficient is 4.905000 Nm.

2. The assumed model uses mass 2 kg and coefficient 4.905000 Nm.

3. Generate static samples over -1 to +1 rad with 0.03 Nm standard-deviation noise.

4. Project measurements onto cos(q), obtaining A_hat=4.905259 Nm.

5. The inferred mass is 2.000106 kg; feedforward mismatch RMSE is 0.000000 Nm.

#### Worked case 4: model_mass = 2.2

This case keeps the nominal configuration except for model_mass=2.2. The full input is {"model_mass": 2.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| feedforward rmse Nm | 0.41519602 |
| peak residual Nm | 0.4905 |
| identified mass kg | 2.00010562 |
| fit residual rmse Nm | 0.03442849 |

1. The true static gravity coefficient is 4.905000 Nm.

2. The assumed model uses mass 2.2 kg and coefficient 5.395500 Nm.

3. Generate static samples over -1 to +1 rad with 0.03 Nm standard-deviation noise.

4. Project measurements onto cos(q), obtaining A_hat=4.905259 Nm.

5. The inferred mass is 2.000106 kg; feedforward mismatch RMSE is 0.415196 Nm.

#### Worked case 5: model_mass = 2.5

This case keeps the nominal configuration except for model_mass=2.5. The full input is {"model_mass": 2.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| feedforward rmse Nm | 1.03799006 |
| peak residual Nm | 1.22625 |
| identified mass kg | 2.00010562 |
| fit residual rmse Nm | 0.03442849 |

1. The true static gravity coefficient is 4.905000 Nm.

2. The assumed model uses mass 2.5 kg and coefficient 6.131250 Nm.

3. Generate static samples over -1 to +1 rad with 0.03 Nm standard-deviation noise.

4. Project measurements onto cos(q), obtaining A_hat=4.905259 Nm.

5. The inferred mass is 2.000106 kg; feedforward mismatch RMSE is 1.037990 Nm.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The cosine model assumes a known angle convention, lever and negligible dynamic/friction torque during the measurement.

A good gravity fit does not identify inertia, backlash or transient motor limits.

### K. Failure modes and troubleshooting

Using moving samples as static gravity data; absorbing encoder-zero error into an incorrect mass estimate; ignoring multi-link coupling.

### L. Practical exercises and extension tasks

1. Add a constant torque bias and fit both cosine and offset terms.

2. Introduce a small angle-zero error and inspect residual structure.

3. Compare fit and validation angle ranges.

### M. Connection to the Asimov research platform

Actual gravity compensation requires verified model conventions and low-energy measurements with load support.

### N. Completion record

Record your chosen case, predicted trend, measured feedforward_rmse_Nm, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 26, Torque-speed envelopes and trajectory feasibility. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 26 - Torque-speed envelopes and trajectory feasibility

### A. The engineering question

An actuator does not provide its maximum torque at every speed.

### B. Concepts and mathematical model

Electrical voltage, current limits, losses and thermal constraints shape a feasible envelope. A simple linear torque-speed model is useful for screening and for understanding why a trajectory can become infeasible as speed rises. It is not a substitute for a vendor curve. Here the torque demand is fixed while speed varies, making reserve and mechanical power easy to compare.

tau_available=tau_stall*max(0,1-|omega|/omega_no_load); reserve=tau_available-|tau_required|.

### C. Real-world meaning and limits

Use measured or manufacturer-supplied actuator curves, firmware current limits and duty-cycle constraints for actual motors.

### D. Architecture and data flow

Configuration (speed, stall_torque, no_load_speed, required_torque) -> numerical model -> available_torque_Nm, reserve_Nm, required_mechanical_power_W -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

speed is output rad/s; stall_torque and required_torque are Nm; no_load_speed is the assumed output speed at negligible torque.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| speed | 2 | angular speed in the chapter equation |
| stall_torque | 10 | Defined by the explicit chapter model and parameter contract |
| no_load_speed | 8 | Defined by the explicit chapter model and parameter contract |
| required_torque | 4 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/26_motor_envelope.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only speed changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/26_motor_envelope.py --case 0

.venv-book/bin/python expanded_lab/modules/26_motor_envelope.py --case 3

.venv-book/bin/python expanded_lab/run.py motor_envelope --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/26_motor_envelope.py

### H. Walkthrough and design decisions

Separate the model of available authority from the load demand. The feasibility flag is derived from the reserve rather than from whether the numerical simulator keeps running.

### I. Expected behavior and six worked cases

The controlled variable is speed. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/26_motor_envelope.png

Figure L26. available torque Nm as speed changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | speed | available torque Nm |
|---|---|---|
| 0 | 0 | 10 |
| 1 | 1 | 8.75 |
| 2 | 2 | 7.5 |
| 3 | 4 | 5 |
| 4 | 6 | 2.5 |
| 5 | 8 | 0 |

#### Worked case 0: speed = 0

This case keeps the nominal configuration except for speed=0. The full input is {"no_load_speed": 8.0, "required_torque": 4.0, "speed": 0.0, "stall_torque": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| available torque Nm | 10 |
| reserve Nm | 6 |
| required mechanical power W | 0 |
| envelope power W | 0 |
| feasible | 1 |

1. The teaching envelope has zero-speed torque 10 Nm and no-load speed 8 rad/s.

2. At speed 0 rad/s the linear speed factor is 1.000000.

3. Available torque is 10.000000 Nm while demand is 4 Nm.

4. Reserve is 6.000000 Nm; feasibility flag is True.

5. Demanded mechanical power is 0.000000 W.

#### Worked case 1: speed = 1

This case keeps the nominal configuration except for speed=1. The full input is {"no_load_speed": 8.0, "required_torque": 4.0, "speed": 1.0, "stall_torque": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| available torque Nm | 8.75 |
| reserve Nm | 4.75 |
| required mechanical power W | 4 |
| envelope power W | 8.75 |
| feasible | 1 |

1. The teaching envelope has zero-speed torque 10 Nm and no-load speed 8 rad/s.

2. At speed 1 rad/s the linear speed factor is 0.875000.

3. Available torque is 8.750000 Nm while demand is 4 Nm.

4. Reserve is 4.750000 Nm; feasibility flag is True.

5. Demanded mechanical power is 4.000000 W.

#### Worked case 2: speed = 2

This case keeps the nominal configuration except for speed=2. The full input is {"no_load_speed": 8.0, "required_torque": 4.0, "speed": 2.0, "stall_torque": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| available torque Nm | 7.5 |
| reserve Nm | 3.5 |
| required mechanical power W | 8 |
| envelope power W | 15 |
| feasible | 1 |

1. The teaching envelope has zero-speed torque 10 Nm and no-load speed 8 rad/s.

2. At speed 2 rad/s the linear speed factor is 0.750000.

3. Available torque is 7.500000 Nm while demand is 4 Nm.

4. Reserve is 3.500000 Nm; feasibility flag is True.

5. Demanded mechanical power is 8.000000 W.

#### Worked case 3: speed = 4

This case keeps the nominal configuration except for speed=4. The full input is {"no_load_speed": 8.0, "required_torque": 4.0, "speed": 4.0, "stall_torque": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| available torque Nm | 5 |
| reserve Nm | 1 |
| required mechanical power W | 16 |
| envelope power W | 20 |
| feasible | 1 |

1. The teaching envelope has zero-speed torque 10 Nm and no-load speed 8 rad/s.

2. At speed 4 rad/s the linear speed factor is 0.500000.

3. Available torque is 5.000000 Nm while demand is 4 Nm.

4. Reserve is 1.000000 Nm; feasibility flag is True.

5. Demanded mechanical power is 16.000000 W.

#### Worked case 4: speed = 6

This case keeps the nominal configuration except for speed=6. The full input is {"no_load_speed": 8.0, "required_torque": 4.0, "speed": 6.0, "stall_torque": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| available torque Nm | 2.5 |
| reserve Nm | -1.5 |
| required mechanical power W | 24 |
| envelope power W | 15 |
| feasible | 0 |

1. The teaching envelope has zero-speed torque 10 Nm and no-load speed 8 rad/s.

2. At speed 6 rad/s the linear speed factor is 0.250000.

3. Available torque is 2.500000 Nm while demand is 4 Nm.

4. Reserve is -1.500000 Nm; feasibility flag is False.

5. Demanded mechanical power is 24.000000 W.

#### Worked case 5: speed = 8

This case keeps the nominal configuration except for speed=8. The full input is {"no_load_speed": 8.0, "required_torque": 4.0, "speed": 8.0, "stall_torque": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| available torque Nm | 0 |
| reserve Nm | -4 |
| required mechanical power W | 32 |
| envelope power W | 0 |
| feasible | 0 |

1. The teaching envelope has zero-speed torque 10 Nm and no-load speed 8 rad/s.

2. At speed 8 rad/s the linear speed factor is 0.000000.

3. Available torque is 0.000000 Nm while demand is 4 Nm.

4. Reserve is -4.000000 Nm; feasibility flag is False.

5. Demanded mechanical power is 32.000000 W.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The illustrative envelope is instantaneous and excludes continuous thermal derating and regenerative quadrants.

A positive reserve is only one constraint; position, load path, current and thermal checks remain separate.

### K. Failure modes and troubleshooting

Treating stall torque as continuous; mixing motor-shaft and output-shaft speed; extrapolating a linear toy curve beyond the data range.

### L. Practical exercises and extension tasks

1. Evaluate an entire minimum-jerk torque/speed trajectory against the envelope.

2. Add a voltage-dependent no-load speed.

3. Separate motoring and regenerative operation.

### M. Connection to the Asimov research platform

Use measured or manufacturer-supplied actuator curves, firmware current limits and duty-cycle constraints for actual motors.

### N. Completion record

Record your chosen case, predicted trend, measured available_torque_Nm, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 27, Feedback delay, sample-and-hold and tracking degradation. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 27 - Feedback delay, sample-and-hold and tracking degradation

### A. The engineering question

A controller acts on information from the past.

### B. Concepts and mathematical model

Even if each packet is delivered reliably, delayed position feedback changes the phase of the loop and can create oscillation. Sample-and-hold output adds another timing effect. This experiment stores a queue of previous states and makes the feedback delay explicit in samples. The plant and gains remain fixed, so changes in error can be attributed to the delay model rather than a simultaneous retuning.

u[k]=Kp*(reference-q[k-d])-Kd*v[k-d]; delay_seconds=d*dt.

### C. Real-world meaning and limits

Physical timing measurements must include sensing, transport, scheduling and actuator application, not only network round-trip time.

### D. Architecture and data flow

Configuration (delay) -> numerical model -> actual_delay_s, tracking_rmse_rad, peak_error_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

delay is seconds of feedback age; plant integration is 1 ms and torque limit is an illustrative 3 Nm.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| delay | 0.01 | seconds |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/27_delay_control.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only delay changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/27_delay_control.py --case 0

.venv-book/bin/python expanded_lab/modules/27_delay_control.py --case 3

.venv-book/bin/python expanded_lab/run.py delay_control --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/27_delay_control.py

### H. Walkthrough and design decisions

The state history implements delay without altering the integration timestep. Inspect the actual rounded delay because requested values may not be exactly representable in samples.

### I. Expected behavior and six worked cases

The controlled variable is delay. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/27_delay_control.png

Figure L27. actual delay s as delay changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | delay | actual delay s |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0.002 | 0.002 |
| 2 | 0.005 | 0.005 |
| 3 | 0.01 | 0.01 |
| 4 | 0.02 | 0.02 |
| 5 | 0.05 | 0.05 |

#### Worked case 0: delay = 0

This case keeps the nominal configuration except for delay=0. The full input is {"delay": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| actual delay s | 0 |
| tracking rmse rad | 0.02216252 |
| peak error rad | 0.03238331 |
| saturation fraction | 0 |

1. Request delay 0 s; rounding to 1 ms samples gives 0 delayed samples.

2. The reference is a 0.1 rad, 0.5 Hz sinusoid; gains remain Kp=20 and Kd=2.

3. Use delayed position and velocity but the current reference to calculate torque.

4. After three seconds, RMSE is 0.022163 rad.

5. Peak error is 0.032383 rad and saturation fraction is 0.000000.

#### Worked case 1: delay = 0.002

This case keeps the nominal configuration except for delay=0.002. The full input is {"delay": 0.002}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| actual delay s | 0.002 |
| tracking rmse rad | 0.02173876 |
| peak error rad | 0.03175124 |
| saturation fraction | 0 |

1. Request delay 0.002 s; rounding to 1 ms samples gives 2 delayed samples.

2. The reference is a 0.1 rad, 0.5 Hz sinusoid; gains remain Kp=20 and Kd=2.

3. Use delayed position and velocity but the current reference to calculate torque.

4. After three seconds, RMSE is 0.021739 rad.

5. Peak error is 0.031751 rad and saturation fraction is 0.000000.

#### Worked case 2: delay = 0.005

This case keeps the nominal configuration except for delay=0.005. The full input is {"delay": 0.005}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| actual delay s | 0.005 |
| tracking rmse rad | 0.02110144 |
| peak error rad | 0.0308021 |
| saturation fraction | 0 |

1. Request delay 0.005 s; rounding to 1 ms samples gives 5 delayed samples.

2. The reference is a 0.1 rad, 0.5 Hz sinusoid; gains remain Kp=20 and Kd=2.

3. Use delayed position and velocity but the current reference to calculate torque.

4. After three seconds, RMSE is 0.021101 rad.

5. Peak error is 0.030802 rad and saturation fraction is 0.000000.

#### Worked case 3: delay = 0.01

This case keeps the nominal configuration except for delay=0.01. The full input is {"delay": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| actual delay s | 0.01 |
| tracking rmse rad | 0.02003481 |
| peak error rad | 0.02921747 |
| saturation fraction | 0 |

1. Request delay 0.01 s; rounding to 1 ms samples gives 10 delayed samples.

2. The reference is a 0.1 rad, 0.5 Hz sinusoid; gains remain Kp=20 and Kd=2.

3. Use delayed position and velocity but the current reference to calculate torque.

4. After three seconds, RMSE is 0.020035 rad.

5. Peak error is 0.029217 rad and saturation fraction is 0.000000.

#### Worked case 4: delay = 0.02

This case keeps the nominal configuration except for delay=0.02. The full input is {"delay": 0.02}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| actual delay s | 0.02 |
| tracking rmse rad | 0.01788516 |
| peak error rad | 0.02603855 |
| saturation fraction | 0 |

1. Request delay 0.02 s; rounding to 1 ms samples gives 20 delayed samples.

2. The reference is a 0.1 rad, 0.5 Hz sinusoid; gains remain Kp=20 and Kd=2.

3. Use delayed position and velocity but the current reference to calculate torque.

4. After three seconds, RMSE is 0.017885 rad.

5. Peak error is 0.026039 rad and saturation fraction is 0.000000.

#### Worked case 5: delay = 0.05

This case keeps the nominal configuration except for delay=0.05. The full input is {"delay": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| actual delay s | 0.05 |
| tracking rmse rad | 0.03399182 |
| peak error rad | 0.08598412 |
| saturation fraction | 0.12 |

1. Request delay 0.05 s; rounding to 1 ms samples gives 50 delayed samples.

2. The reference is a 0.1 rad, 0.5 Hz sinusoid; gains remain Kp=20 and Kd=2.

3. Use delayed position and velocity but the current reference to calculate torque.

4. After three seconds, RMSE is 0.033992 rad.

5. Peak error is 0.085984 rad and saturation fraction is 0.120000.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The chosen delay is deterministic; real transport also has jitter, dropouts and timestamp uncertainty.

A simulator with immediate state access can substantially overestimate the usable gain margin.

### K. Failure modes and troubleshooting

Ignoring packet age because delivery is reliable; compensating delay with unvalidated gain increases; comparing different reference timing conventions.

### L. Practical exercises and extension tasks

1. Add bounded seeded jitter to the feedback index.

2. Drop a burst of feedback samples and define a watchdog response.

3. Compare delayed feedback with predicted current state.

### M. Connection to the Asimov research platform

Physical timing measurements must include sensing, transport, scheduling and actuator application, not only network round-trip time.

### N. Completion record

Record your chosen case, predicted trend, measured actual_delay_s, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 28, First-order thermal models and duty-cycle limits. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 28 - First-order thermal models and duty-cycle limits

### A. The engineering question

Temperature accumulates the history of losses.

### B. Concepts and mathematical model

A motor can satisfy an instantaneous torque requirement while exceeding its thermal capacity over a longer duty cycle. A first-order resistance-capacitance model represents thermal storage and heat flow to ambient. Its time constant explains why short successful tests cannot prove continuous capability. The parameters below are illustrative and deliberately separate electrical loss from the thermal model.

C_th*T_dot=P_loss-(T-T_ambient)/R_th; steady rise=P_loss*R_th; time_constant=R_th*C_th.

### C. Real-world meaning and limits

Use manufacturer temperature limits and identified thermal behavior to design real derating and stop thresholds.

### D. Architecture and data flow

Configuration (loss_power, thermal_resistance, thermal_capacity, duration) -> numerical model -> final_temperature_C, steady_temperature_C, time_constant_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

loss_power is Watts dissipated as heat; thermal_resistance is K/W; thermal_capacity is J/K; duration is seconds.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| loss_power | 20 | Watts |
| thermal_resistance | 2 | K/W |
| thermal_capacity | 100 | J/K |
| duration | 300 | seconds |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/28_thermal.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only loss_power changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/28_thermal.py --case 0

.venv-book/bin/python expanded_lab/modules/28_thermal.py --case 3

.venv-book/bin/python expanded_lab/run.py thermal --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/28_thermal.py

### H. Walkthrough and design decisions

The analytical solution gives both transient and steady behavior. An unreachable threshold is encoded explicitly rather than confusing infinity with a safe physical guarantee.

### I. Expected behavior and six worked cases

The controlled variable is loss_power. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/28_thermal.png

Figure L28. final temperature C as loss_power changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | loss_power | final temperature C |
|---|---|---|
| 0 | 5 | 32.7686984 |
| 1 | 10 | 40.5373968 |
| 2 | 15 | 48.3060952 |
| 3 | 20 | 56.07479359 |
| 4 | 30 | 71.61219039 |
| 5 | 40 | 87.14958719 |

#### Worked case 0: loss_power = 5

This case keeps the nominal configuration except for loss_power=5. The full input is {"duration": 300.0, "loss_power": 5.0, "thermal_capacity": 100.0, "thermal_resistance": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final temperature C | 32.7686984 |
| steady temperature C | 35 |
| time constant s | 200 |
| screening margin C | 37.2313016 |
| threshold crossing s | -1 |

1. Assume loss power 5 W, Rth=2 K/W and Cth=100 J/K.

2. The thermal time constant is 200.000000 s.

3. After 300 s, temperature rise is 7.768698 K above 25 C ambient.

4. Predicted final temperature is 32.768698 C and steady temperature is 35.000000 C.

5. The 70 C teaching threshold crossing time is -1.000000 s; -1 means no crossing in the ideal constant-loss model.

#### Worked case 1: loss_power = 10

This case keeps the nominal configuration except for loss_power=10. The full input is {"duration": 300.0, "loss_power": 10.0, "thermal_capacity": 100.0, "thermal_resistance": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final temperature C | 40.5373968 |
| steady temperature C | 45 |
| time constant s | 200 |
| screening margin C | 29.4626032 |
| threshold crossing s | -1 |

1. Assume loss power 10 W, Rth=2 K/W and Cth=100 J/K.

2. The thermal time constant is 200.000000 s.

3. After 300 s, temperature rise is 15.537397 K above 25 C ambient.

4. Predicted final temperature is 40.537397 C and steady temperature is 45.000000 C.

5. The 70 C teaching threshold crossing time is -1.000000 s; -1 means no crossing in the ideal constant-loss model.

#### Worked case 2: loss_power = 15

This case keeps the nominal configuration except for loss_power=15. The full input is {"duration": 300.0, "loss_power": 15.0, "thermal_capacity": 100.0, "thermal_resistance": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final temperature C | 48.3060952 |
| steady temperature C | 55 |
| time constant s | 200 |
| screening margin C | 21.6939048 |
| threshold crossing s | -1 |

1. Assume loss power 15 W, Rth=2 K/W and Cth=100 J/K.

2. The thermal time constant is 200.000000 s.

3. After 300 s, temperature rise is 23.306095 K above 25 C ambient.

4. Predicted final temperature is 48.306095 C and steady temperature is 55.000000 C.

5. The 70 C teaching threshold crossing time is -1.000000 s; -1 means no crossing in the ideal constant-loss model.

#### Worked case 3: loss_power = 20

This case keeps the nominal configuration except for loss_power=20. The full input is {"duration": 300.0, "loss_power": 20.0, "thermal_capacity": 100.0, "thermal_resistance": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final temperature C | 56.07479359 |
| steady temperature C | 65 |
| time constant s | 200 |
| screening margin C | 13.92520641 |
| threshold crossing s | -1 |

1. Assume loss power 20 W, Rth=2 K/W and Cth=100 J/K.

2. The thermal time constant is 200.000000 s.

3. After 300 s, temperature rise is 31.074794 K above 25 C ambient.

4. Predicted final temperature is 56.074794 C and steady temperature is 65.000000 C.

5. The 70 C teaching threshold crossing time is -1.000000 s; -1 means no crossing in the ideal constant-loss model.

#### Worked case 4: loss_power = 30

This case keeps the nominal configuration except for loss_power=30. The full input is {"duration": 300.0, "loss_power": 30.0, "thermal_capacity": 100.0, "thermal_resistance": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final temperature C | 71.61219039 |
| steady temperature C | 85 |
| time constant s | 200 |
| screening margin C | -1.61219039 |
| threshold crossing s | 277.25887222 |

1. Assume loss power 30 W, Rth=2 K/W and Cth=100 J/K.

2. The thermal time constant is 200.000000 s.

3. After 300 s, temperature rise is 46.612190 K above 25 C ambient.

4. Predicted final temperature is 71.612190 C and steady temperature is 85.000000 C.

5. The 70 C teaching threshold crossing time is 277.258872 s; -1 means no crossing in the ideal constant-loss model.

#### Worked case 5: loss_power = 40

This case keeps the nominal configuration except for loss_power=40. The full input is {"duration": 300.0, "loss_power": 40.0, "thermal_capacity": 100.0, "thermal_resistance": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final temperature C | 87.14958719 |
| steady temperature C | 105 |
| time constant s | 200 |
| screening margin C | -17.14958719 |
| threshold crossing s | 165.33571464 |

1. Assume loss power 40 W, Rth=2 K/W and Cth=100 J/K.

2. The thermal time constant is 200.000000 s.

3. After 300 s, temperature rise is 62.149587 K above 25 C ambient.

4. Predicted final temperature is 87.149587 C and steady temperature is 105.000000 C.

5. The 70 C teaching threshold crossing time is 165.335715 s; -1 means no crossing in the ideal constant-loss model.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The 70 C threshold is an exercise parameter, not a motor or material rating.

Actual winding, housing, drive and gearbox temperatures have different dynamics and measurement locations.

### K. Failure modes and troubleshooting

Using mechanical output power as heat loss; trusting a housing sensor to represent winding temperature instantly; ignoring ambient and airflow.

### L. Practical exercises and extension tasks

1. Integrate a square-wave duty cycle numerically and compare average-loss approximations.

2. Fit Rth and Cth from a safe measured heating/cooling trace.

3. Repeat at a higher ambient temperature.

### M. Connection to the Asimov research platform

Use manufacturer temperature limits and identified thermal behavior to design real derating and stop thresholds.

### N. Completion record

Record your chosen case, predicted trend, measured final_temperature_C, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 29, Mechanical energy, electrical demand and regeneration. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 29 - Mechanical energy, electrical demand and regeneration

### A. The engineering question

Electrical supply design depends on energy flow as well as peak current.

### B. Concepts and mathematical model

Motoring consumes electrical energy; decelerating or lowering a load may return energy to the bus. A bench supply that sources current may not safely sink it. Separating positive mechanical work, negative mechanical work, conversion losses and regenerated energy avoids the misleading assumption that average motor power describes every electrical condition.

P_mech=tau*omega; P_elec=P_mech/eta for motoring, eta_regen*P_mech for regenerative operation; E=integral(P dt).

### C. Real-world meaning and limits

Regeneration handling must be approved for the actual supply, battery, drive and isolation scheme before a loaded actuator test.

### D. Architecture and data flow

Configuration (efficiency, regen_efficiency) -> numerical model -> energy_drawn_J, energy_returned_J, net_energy_J -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

efficiency is motoring mechanical/electrical power ratio; regen_efficiency is the fraction of negative mechanical energy returned electrically.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| efficiency | 0.8 | fraction |
| regen_efficiency | 0.5 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/29_energy_regen.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only regen_efficiency changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/29_energy_regen.py --case 0

.venv-book/bin/python expanded_lab/modules/29_energy_regen.py --case 3

.venv-book/bin/python expanded_lab/run.py energy_regen --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/29_energy_regen.py

### H. Walkthrough and design decisions

Use signed power before integrating and keep motoring and regeneration totals separate. Clipping all negative power to zero would conceal a supply design requirement.

### I. Expected behavior and six worked cases

The controlled variable is regen_efficiency. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/29_energy_regen.png

Figure L29. energy drawn J as regen_efficiency changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | regen_efficiency | energy drawn J |
|---|---|---|
| 0 | 0 | 2.65257797 |
| 1 | 0.2 | 2.65257797 |
| 2 | 0.4 | 2.65257797 |
| 3 | 0.6 | 2.65257797 |
| 4 | 0.8 | 2.65257797 |
| 5 | 1 | 2.65257797 |

#### Worked case 0: regen_efficiency = 0

This case keeps the nominal configuration except for regen_efficiency=0. The full input is {"efficiency": 0.8, "regen_efficiency": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| energy drawn J | 2.65257797 |
| energy returned J | 0 |
| net energy J | 2.65257797 |
| peak draw W | 2.80545561 |
| peak return W | 0 |

1. Generate a four-second signed torque and speed cycle.

2. Motoring efficiency is 0.8; regenerative efficiency is 0.

3. Convert positive and negative mechanical power using their respective efficiencies.

4. Integrate positive electrical power: 2.652578 J drawn.

5. Integrate negative electrical power: -0.000000 J returned; net is 2.652578 J.

#### Worked case 1: regen_efficiency = 0.2

This case keeps the nominal configuration except for regen_efficiency=0.2. The full input is {"efficiency": 0.8, "regen_efficiency": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| energy drawn J | 2.65257797 |
| energy returned J | 0.42441247 |
| net energy J | 2.22816549 |
| peak draw W | 2.80545561 |
| peak return W | 0.4488729 |

1. Generate a four-second signed torque and speed cycle.

2. Motoring efficiency is 0.8; regenerative efficiency is 0.2.

3. Convert positive and negative mechanical power using their respective efficiencies.

4. Integrate positive electrical power: 2.652578 J drawn.

5. Integrate negative electrical power: 0.424412 J returned; net is 2.228165 J.

#### Worked case 2: regen_efficiency = 0.4

This case keeps the nominal configuration except for regen_efficiency=0.4. The full input is {"efficiency": 0.8, "regen_efficiency": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| energy drawn J | 2.65257797 |
| energy returned J | 0.84882495 |
| net energy J | 1.80375302 |
| peak draw W | 2.80545561 |
| peak return W | 0.89774579 |

1. Generate a four-second signed torque and speed cycle.

2. Motoring efficiency is 0.8; regenerative efficiency is 0.4.

3. Convert positive and negative mechanical power using their respective efficiencies.

4. Integrate positive electrical power: 2.652578 J drawn.

5. Integrate negative electrical power: 0.848825 J returned; net is 1.803753 J.

#### Worked case 3: regen_efficiency = 0.6

This case keeps the nominal configuration except for regen_efficiency=0.6. The full input is {"efficiency": 0.8, "regen_efficiency": 0.6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| energy drawn J | 2.65257797 |
| energy returned J | 1.27323742 |
| net energy J | 1.37934054 |
| peak draw W | 2.80545561 |
| peak return W | 1.34661869 |

1. Generate a four-second signed torque and speed cycle.

2. Motoring efficiency is 0.8; regenerative efficiency is 0.6.

3. Convert positive and negative mechanical power using their respective efficiencies.

4. Integrate positive electrical power: 2.652578 J drawn.

5. Integrate negative electrical power: 1.273237 J returned; net is 1.379341 J.

#### Worked case 4: regen_efficiency = 0.8

This case keeps the nominal configuration except for regen_efficiency=0.8. The full input is {"efficiency": 0.8, "regen_efficiency": 0.8}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| energy drawn J | 2.65257797 |
| energy returned J | 1.6976499 |
| net energy J | 0.95492807 |
| peak draw W | 2.80545561 |
| peak return W | 1.79549159 |

1. Generate a four-second signed torque and speed cycle.

2. Motoring efficiency is 0.8; regenerative efficiency is 0.8.

3. Convert positive and negative mechanical power using their respective efficiencies.

4. Integrate positive electrical power: 2.652578 J drawn.

5. Integrate negative electrical power: 1.697650 J returned; net is 0.954928 J.

#### Worked case 5: regen_efficiency = 1

This case keeps the nominal configuration except for regen_efficiency=1. The full input is {"efficiency": 0.8, "regen_efficiency": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| energy drawn J | 2.65257797 |
| energy returned J | 2.12206237 |
| net energy J | 0.53051559 |
| peak draw W | 2.80545561 |
| peak return W | 2.24436449 |

1. Generate a four-second signed torque and speed cycle.

2. Motoring efficiency is 0.8; regenerative efficiency is 1.

3. Convert positive and negative mechanical power using their respective efficiencies.

4. Integrate positive electrical power: 2.652578 J drawn.

5. Integrate negative electrical power: 2.122062 J returned; net is 0.530516 J.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Negative mechanical power represents energy leaving the mechanical system; the electrical destination depends on the actual drive and power topology.

A low net-energy cycle can still impose large instantaneous source and sink requirements.

### K. Failure modes and troubleshooting

Calculating battery current from average mechanical power alone; assuming every supply can absorb regeneration; ignoring driver protection behavior.

### L. Practical exercises and extension tasks

1. Estimate bus-capacitor voltage rise from returned energy.

2. Compare peak and average demand for the same cycle.

3. Add constant electronics power and recompute net energy.

### M. Connection to the Asimov research platform

Regeneration handling must be approved for the actual supply, battery, drive and isolation scheme before a loaded actuator test.

### N. Completion record

Record your chosen case, predicted trend, measured energy_drawn_J, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 30, Control deadlines, jitter and tail-latency budgets. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 30 - Control deadlines, jitter and tail-latency budgets

### A. The engineering question

Average runtime is insufficient for a feedback deadline.

### B. Concepts and mathematical model

Rare scheduling delays or long inference calls can age a command enough to matter physically. A timing budget should account for sensing, transport, estimation, control, inference and application. This experiment uses a seeded synthetic workload with occasional long delays to compare average and high-percentile completion times. It demonstrates a measurement method, not the timing performance of your laptop or a real-time operating system.

completion = sensing+transport+compute+scheduler_jitter; deadline_miss = completion>period.

### C. Real-world meaning and limits

Use local embedded deadlines and independently tested stop authority where the physical control design requires them.

### D. Architecture and data flow

Configuration (period_ms, jitter_mean_ms) -> numerical model -> mean_completion_ms, p99_completion_ms, max_completion_ms -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

period_ms is the target cycle deadline in milliseconds; jitter_mean_ms controls a synthetic scheduler-delay distribution.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| period_ms | 2 | Defined by the explicit chapter model and parameter contract |
| jitter_mean_ms | 0.1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/30_scheduler.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only jitter_mean_ms changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/30_scheduler.py --case 0

.venv-book/bin/python expanded_lab/modules/30_scheduler.py --case 3

.venv-book/bin/python expanded_lab/run.py scheduler --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/30_scheduler.py

### H. Walkthrough and design decisions

Retain the entire latency distribution long enough to calculate misses and tails. The rare-delay mechanism explains why a reassuring mean can coexist with unacceptable behavior.

### I. Expected behavior and six worked cases

The controlled variable is jitter_mean_ms. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/30_scheduler.png

Figure L30. mean completion ms as jitter_mean_ms changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | jitter_mean_ms | mean completion ms |
|---|---|---|
| 0 | 0.01 | 1.17679553 |
| 1 | 0.05 | 1.21628458 |
| 2 | 0.1 | 1.26564589 |
| 3 | 0.2 | 1.3643685 |
| 4 | 0.5 | 1.66053634 |
| 5 | 1 | 2.1541494 |

#### Worked case 0: jitter_mean_ms = 0.01

This case keeps the nominal configuration except for jitter_mean_ms=0.01. The full input is {"jitter_mean_ms": 0.01, "period_ms": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean completion ms | 1.17679553 |
| p99 completion ms | 1.55870418 |
| max completion ms | 4.60076518 |
| deadline miss fraction | 0.0048 |
| minimum observed margin ms | -2.60076518 |

1. Generate 10000 synthetic cycles with period 2 ms.

2. Exponential jitter mean is 0.01 ms, plus a 0.5% long-delay mechanism.

3. Mean completion is 1.176796 ms.

4. The 99th percentile is 1.558704 ms and worst observed is 4.600765 ms.

5. Missed-deadline fraction is 0.004800.

#### Worked case 1: jitter_mean_ms = 0.05

This case keeps the nominal configuration except for jitter_mean_ms=0.05. The full input is {"jitter_mean_ms": 0.05, "period_ms": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean completion ms | 1.21628458 |
| p99 completion ms | 1.62069344 |
| max completion ms | 4.62485526 |
| deadline miss fraction | 0.0048 |
| minimum observed margin ms | -2.62485526 |

1. Generate 10000 synthetic cycles with period 2 ms.

2. Exponential jitter mean is 0.05 ms, plus a 0.5% long-delay mechanism.

3. Mean completion is 1.216285 ms.

4. The 99th percentile is 1.620693 ms and worst observed is 4.624855 ms.

5. Missed-deadline fraction is 0.004800.

#### Worked case 2: jitter_mean_ms = 0.1

This case keeps the nominal configuration except for jitter_mean_ms=0.1. The full input is {"jitter_mean_ms": 0.1, "period_ms": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean completion ms | 1.26564589 |
| p99 completion ms | 1.78166362 |
| max completion ms | 4.72837516 |
| deadline miss fraction | 0.0054 |
| minimum observed margin ms | -2.72837516 |

1. Generate 10000 synthetic cycles with period 2 ms.

2. Exponential jitter mean is 0.1 ms, plus a 0.5% long-delay mechanism.

3. Mean completion is 1.265646 ms.

4. The 99th percentile is 1.781664 ms and worst observed is 4.728375 ms.

5. Missed-deadline fraction is 0.005400.

#### Worked case 3: jitter_mean_ms = 0.2

This case keeps the nominal configuration except for jitter_mean_ms=0.2. The full input is {"jitter_mean_ms": 0.2, "period_ms": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean completion ms | 1.3643685 |
| p99 completion ms | 2.24949344 |
| max completion ms | 5.04997158 |
| deadline miss fraction | 0.0224 |
| minimum observed margin ms | -3.04997158 |

1. Generate 10000 synthetic cycles with period 2 ms.

2. Exponential jitter mean is 0.2 ms, plus a 0.5% long-delay mechanism.

3. Mean completion is 1.364368 ms.

4. The 99th percentile is 2.249493 ms and worst observed is 5.049972 ms.

5. Missed-deadline fraction is 0.022400.

#### Worked case 4: jitter_mean_ms = 0.5

This case keeps the nominal configuration except for jitter_mean_ms=0.5. The full input is {"jitter_mean_ms": 0.5, "period_ms": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean completion ms | 1.66053634 |
| p99 completion ms | 3.77698821 |
| max completion ms | 6.01476083 |
| deadline miss fraction | 0.1902 |
| minimum observed margin ms | -4.01476083 |

1. Generate 10000 synthetic cycles with period 2 ms.

2. Exponential jitter mean is 0.5 ms, plus a 0.5% long-delay mechanism.

3. Mean completion is 1.660536 ms.

4. The 99th percentile is 3.776988 ms and worst observed is 6.014761 ms.

5. Missed-deadline fraction is 0.190200.

#### Worked case 5: jitter_mean_ms = 1

This case keeps the nominal configuration except for jitter_mean_ms=1. The full input is {"jitter_mean_ms": 1.0, "period_ms": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mean completion ms | 2.1541494 |
| p99 completion ms | 5.77391455 |
| max completion ms | 9.67822931 |
| deadline miss fraction | 0.4325 |
| minimum observed margin ms | -7.67822931 |

1. Generate 10000 synthetic cycles with period 2 ms.

2. Exponential jitter mean is 1 ms, plus a 0.5% long-delay mechanism.

3. Mean completion is 2.154149 ms.

4. The 99th percentile is 5.773915 ms and worst observed is 9.678229 ms.

5. Missed-deadline fraction is 0.432500.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Worst observed latency is not a proven worst-case bound; finite sampling can miss rarer events.

The random workload is pedagogical. Real timing claims require instrumented measurements under declared stress conditions.

### K. Failure modes and troubleshooting

Calling Python timer intervals hard-real-time guarantees; measuring only warm unloaded inference; ignoring clock overhead and missed samples.

### L. Practical exercises and extension tasks

1. Add a separate inference task every tenth cycle and calculate the shared budget.

2. Compare a deadline watchdog with a packet-count watchdog.

3. Measure actual workload latency on the current workstation and replace the synthetic distribution.

### M. Connection to the Asimov research platform

Use local embedded deadlines and independently tested stop authority where the physical control design requires them.

### N. Completion record

Record your chosen case, predicted trend, measured mean_completion_ms, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 31, Encoder counts, quantization, wrapping and velocity estimates. Keep the present result as a reference fixture for diagnosing changes in the larger stack.
