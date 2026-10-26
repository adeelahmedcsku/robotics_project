# Part IX - Sensors, geometry and state estimation

State estimation is a disciplined explanation of what noisy, delayed measurements say about the robot. It requires units, coordinate frames, clock models and validity conditions. These laboratories make quantization, bias, acceleration contamination, measurement dropout, calibration geometry and slipping-contact assumptions visible. Each estimator is compared with known synthetic truth, allowing a precise diagnosis before the same method is tested against physical reference measurements.

## Laboratory 31 - Encoder counts, quantization, wrapping and velocity estimates

### A. The engineering question

An encoder converts position into a finite representation.

### B. Concepts and mathematical model

Quantization error may be small for position but large after numerical differentiation, especially when the sample period is short. Wrapped single-turn angles also create artificial jumps at the boundary unless unwrapped consistently. This experiment produces a smooth known trajectory, quantizes it to counts, reconstructs angle and estimates velocity. Ground truth allows position and derivative error to be separated.

count=round(angle/(2*pi)*resolution); angle_hat=count*2*pi/resolution; velocity_hat=delta(angle_unwrapped)/dt.

### C. Real-world meaning and limits

Confirm encoder placement, count scaling, wrap convention and absolute-reference persistence for the exact actuator firmware.

### D. Architecture and data flow

Configuration (counts) -> numerical model -> quantization_step_rad, position_rmse_rad, velocity_rmse_rad_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

counts is the assumed effective output counts per revolution; the teaching sample interval is 2 ms.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| counts | 4096 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/31_encoder.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only counts changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/31_encoder.py --case 0

.venv-book/bin/python expanded_lab/modules/31_encoder.py --case 3

.venv-book/bin/python expanded_lab/run.py encoder --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/31_encoder.py

### H. Walkthrough and design decisions

Quantize the wrapped measurement before unwrapping, then compare position and differentiated velocity separately. The raw jump metric makes a wrapping bug visible even when the angle trace looks periodic.

### I. Expected behavior and six worked cases

The controlled variable is counts. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/31_encoder.png

Figure L31. quantization step rad as counts changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | counts | quantization step rad |
|---|---|---|
| 0 | 256 | 0.02454369 |
| 1 | 512 | 0.01227185 |
| 2 | 1024 | 0.00613592 |
| 3 | 4096 | 0.00153398 |
| 4 | 16384 | 0.0003835 |
| 5 | 65536 | 0.00009587 |

#### Worked case 0: counts = 256

This case keeps the nominal configuration except for counts=256. The full input is {"counts": 256}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| quantization step rad | 0.02454369 |
| position rmse rad | 0.01018916 |
| velocity rmse rad s | 2.0439869 |
| raw wrap jump rad | 6.28318531 |

1. Encoder resolution is 256 counts per revolution.

2. One count represents 0.02454369 rad.

3. Generate a trajectory crossing the +/-pi wrapping boundary and quantize it.

4. After unwrap and initial alignment, position RMSE is 0.01018916 rad.

5. Differentiating at 2 ms gives velocity RMSE 2.043987 rad/s.

#### Worked case 1: counts = 512

This case keeps the nominal configuration except for counts=512. The full input is {"counts": 512}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| quantization step rad | 0.01227185 |
| position rmse rad | 0.00595705 |
| velocity rmse rad s | 1.28600645 |
| raw wrap jump rad | 6.28318531 |

1. Encoder resolution is 512 counts per revolution.

2. One count represents 0.01227185 rad.

3. Generate a trajectory crossing the +/-pi wrapping boundary and quantize it.

4. After unwrap and initial alignment, position RMSE is 0.00595705 rad.

5. Differentiating at 2 ms gives velocity RMSE 1.286006 rad/s.

#### Worked case 2: counts = 1024

This case keeps the nominal configuration except for counts=1024. The full input is {"counts": 1024}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| quantization step rad | 0.00613592 |
| position rmse rad | 0.00215223 |
| velocity rmse rad s | 0.66395253 |
| raw wrap jump rad | 6.28318531 |

1. Encoder resolution is 1024 counts per revolution.

2. One count represents 0.00613592 rad.

3. Generate a trajectory crossing the +/-pi wrapping boundary and quantize it.

4. After unwrap and initial alignment, position RMSE is 0.00215223 rad.

5. Differentiating at 2 ms gives velocity RMSE 0.663953 rad/s.

#### Worked case 3: counts = 4096

This case keeps the nominal configuration except for counts=4096. The full input is {"counts": 4096}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| quantization step rad | 0.00153398 |
| position rmse rad | 0.00047604 |
| velocity rmse rad s | 0.15363803 |
| raw wrap jump rad | 6.28011735 |

1. Encoder resolution is 4096 counts per revolution.

2. One count represents 0.00153398 rad.

3. Generate a trajectory crossing the +/-pi wrapping boundary and quantize it.

4. After unwrap and initial alignment, position RMSE is 0.00047604 rad.

5. Differentiating at 2 ms gives velocity RMSE 0.153638 rad/s.

#### Worked case 4: counts = 16384

This case keeps the nominal configuration except for counts=16384. The full input is {"counts": 16384}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| quantization step rad | 0.0003835 |
| position rmse rad | 0.00020665 |
| velocity rmse rad s | 0.03905732 |
| raw wrap jump rad | 6.28050084 |

1. Encoder resolution is 16384 counts per revolution.

2. One count represents 0.00038350 rad.

3. Generate a trajectory crossing the +/-pi wrapping boundary and quantize it.

4. After unwrap and initial alignment, position RMSE is 0.00020665 rad.

5. Differentiating at 2 ms gives velocity RMSE 0.039057 rad/s.

#### Worked case 5: counts = 65536

This case keeps the nominal configuration except for counts=65536. The full input is {"counts": 65536}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| quantization step rad | 0.00009587 |
| position rmse rad | 0.00003237 |
| velocity rmse rad s | 0.00966549 |
| raw wrap jump rad | 6.28069259 |

1. Encoder resolution is 65536 counts per revolution.

2. One count represents 0.00009587 rad.

3. Generate a trajectory crossing the +/-pi wrapping boundary and quantize it.

4. After unwrap and initial alignment, position RMSE is 0.00003237 rad.

5. Differentiating at 2 ms gives velocity RMSE 0.009665 rad/s.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The initial alignment removes an arbitrary integer-turn offset but is not an absolute-zero calibration.

Higher numerical differentiation rate does not create additional encoder position information.

### K. Failure modes and troubleshooting

Applying unwrap after differentiation; assuming nominal encoder bit depth equals effective output accuracy; losing multi-turn reference across reboot.

### L. Practical exercises and extension tasks

1. Add a missed-sample gap and use actual timestamps in differentiation.

2. Compare a short-window slope fit with a two-point difference.

3. Model a motor-side encoder through a gearbox and add backlash.

### M. Connection to the Asimov research platform

Confirm encoder placement, count scaling, wrap convention and absolute-reference persistence for the exact actuator firmware.

### N. Completion record

Record your chosen case, predicted trend, measured quantization_step_rad, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 32, Gyroscope bias calibration and attitude drift. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 32 - Gyroscope bias calibration and attitude drift

### A. The engineering question

A small gyro bias integrates into a large orientation error.

### B. Concepts and mathematical model

Averaging a stationary segment can estimate a constant offset, but temperature drift or motion during calibration violates that assumption. Measurement noise and bias uncertainty affect integrated orientation differently. The experiment estimates bias from a known stationary period, then compares raw and corrected integration against a known angular motion. It separates the calibration samples from the evaluation interval.

omega_measured=omega_true+bias+noise; bias_hat=mean(stationary samples); angle=sum((omega_measured-bias_hat)*dt).

### C. Real-world meaning and limits

Physical IMU calibration requires a known stationary fixture and documented temperature/mounting conditions.

### D. Architecture and data flow

Configuration (calibration_seconds) -> numerical model -> estimated_bias_rad_s, bias_error_rad_s, raw_final_angle_error_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

calibration_seconds is the stationary averaging duration; injected gyro bias and noise are in radians per second.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| calibration_seconds | 2 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/32_gyro_bias.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only calibration_seconds changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/32_gyro_bias.py --case 0

.venv-book/bin/python expanded_lab/modules/32_gyro_bias.py --case 3

.venv-book/bin/python expanded_lab/run.py gyro_bias --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/32_gyro_bias.py

### H. Walkthrough and design decisions

Use separate random samples for calibration and motion. Integrating the same noisy calibration record as evaluation would conceal the actual generalization problem.

### I. Expected behavior and six worked cases

The controlled variable is calibration_seconds. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/32_gyro_bias.png

Figure L32. estimated bias rad s as calibration_seconds changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | calibration_seconds | estimated bias rad s |
|---|---|---|
| 0 | 0.1 | 0.01487279 |
| 1 | 0.25 | 0.01348609 |
| 2 | 0.5 | 0.01481712 |
| 3 | 1 | 0.01353986 |
| 4 | 2 | 0.01446547 |
| 5 | 5 | 0.01498463 |

#### Worked case 0: calibration_seconds = 0.1

This case keeps the nominal configuration except for calibration_seconds=0.1. The full input is {"calibration_seconds": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimated bias rad s | 0.01487279 |
| bias error rad s | -0.00012721 |
| raw final angle error rad | 0.14615633 |
| corrected final angle error rad | -0.00257158 |
| corrected angle rmse rad | 0.00090744 |

1. Collect 10 stationary samples at 100 Hz.

2. True injected bias is 0.015 rad/s; estimated bias is 0.01487279 rad/s.

3. Integrate a 0.2 rad/s motion for 10 s.

4. Raw final attitude error is 0.14615633 rad.

5. After bias correction, final error is -0.00257158 rad.

#### Worked case 1: calibration_seconds = 0.25

This case keeps the nominal configuration except for calibration_seconds=0.25. The full input is {"calibration_seconds": 0.25}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimated bias rad s | 0.01348609 |
| bias error rad s | -0.00151391 |
| raw final angle error rad | 0.14639323 |
| corrected final angle error rad | 0.01153231 |
| corrected angle rmse rad | 0.00823944 |

1. Collect 25 stationary samples at 100 Hz.

2. True injected bias is 0.015 rad/s; estimated bias is 0.01348609 rad/s.

3. Integrate a 0.2 rad/s motion for 10 s.

4. Raw final attitude error is 0.14639323 rad.

5. After bias correction, final error is 0.01153231 rad.

#### Worked case 2: calibration_seconds = 0.5

This case keeps the nominal configuration except for calibration_seconds=0.5. The full input is {"calibration_seconds": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimated bias rad s | 0.01481712 |
| bias error rad s | -0.00018288 |
| raw final angle error rad | 0.14579471 |
| corrected final angle error rad | -0.00237649 |
| corrected angle rmse rad | 0.00103681 |

1. Collect 50 stationary samples at 100 Hz.

2. True injected bias is 0.015 rad/s; estimated bias is 0.01481712 rad/s.

3. Integrate a 0.2 rad/s motion for 10 s.

4. Raw final attitude error is 0.14579471 rad.

5. After bias correction, final error is -0.00237649 rad.

#### Worked case 3: calibration_seconds = 1

This case keeps the nominal configuration except for calibration_seconds=1. The full input is {"calibration_seconds": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimated bias rad s | 0.01353986 |
| bias error rad s | -0.00146014 |
| raw final angle error rad | 0.1477647 |
| corrected final angle error rad | 0.01236609 |
| corrected angle rmse rad | 0.00850044 |

1. Collect 100 stationary samples at 100 Hz.

2. True injected bias is 0.015 rad/s; estimated bias is 0.01353986 rad/s.

3. Integrate a 0.2 rad/s motion for 10 s.

4. Raw final attitude error is 0.14776470 rad.

5. After bias correction, final error is 0.01236609 rad.

#### Worked case 4: calibration_seconds = 2

This case keeps the nominal configuration except for calibration_seconds=2. The full input is {"calibration_seconds": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimated bias rad s | 0.01446547 |
| bias error rad s | -0.00053453 |
| raw final angle error rad | 0.14646226 |
| corrected final angle error rad | 0.00180752 |
| corrected angle rmse rad | 0.00263157 |

1. Collect 200 stationary samples at 100 Hz.

2. True injected bias is 0.015 rad/s; estimated bias is 0.01446547 rad/s.

3. Integrate a 0.2 rad/s motion for 10 s.

4. Raw final attitude error is 0.14646226 rad.

5. After bias correction, final error is 0.00180752 rad.

#### Worked case 5: calibration_seconds = 5

This case keeps the nominal configuration except for calibration_seconds=5. The full input is {"calibration_seconds": 5.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimated bias rad s | 0.01498463 |
| bias error rad s | -0.00001537 |
| raw final angle error rad | 0.14713983 |
| corrected final angle error rad | -0.00270643 |
| corrected angle rmse rad | 0.0028349 |

1. Collect 500 stationary samples at 100 Hz.

2. True injected bias is 0.015 rad/s; estimated bias is 0.01498463 rad/s.

3. Integrate a 0.2 rad/s motion for 10 s.

4. Raw final attitude error is 0.14713983 rad.

5. After bias correction, final error is -0.00270643 rad.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

This calibration assumes zero true angular velocity and constant bias during both intervals.

Longer averaging reduces random estimation error but cannot remove a temperature-dependent bias change.

### K. Failure modes and troubleshooting

Calibrating while the robot vibrates or moves; forgetting sensor-to-body rotation; subtracting degrees-per-second bias from radian data.

### L. Practical exercises and extension tasks

1. Introduce a slow temperature-dependent bias ramp.

2. Repeat across several seeds and quantify calibration variability.

3. Reject calibration intervals with excessive measured variance.

### M. Connection to the Asimov research platform

Physical IMU calibration requires a known stationary fixture and documented temperature/mounting conditions.

### N. Completion record

Record your chosen case, predicted trend, measured estimated_bias_rad_s, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 33, Complementary attitude filtering and acceleration contamination. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 33 - Complementary attitude filtering and acceleration contamination

### A. The engineering question

A gyroscope tracks rapid angular changes but drifts.

### B. Concepts and mathematical model

An accelerometer can provide a gravity-direction reference when other acceleration is small, but cannot distinguish gravity from arbitrary linear acceleration by itself. A complementary filter blends integrated gyro attitude with a slower accelerometer estimate. The blend controls the response to bias and contamination. This scalar roll example makes those competing effects visible before a three-dimensional estimator is introduced.

roll_pred=roll_prev+gyro*dt; roll_next=alpha*roll_pred+(1-alpha)*roll_acc; alpha=tau/(tau+dt).

### C. Real-world meaning and limits

IMU correction assumptions must be tested in supported stationary, moving and contact-transition conditions.

### D. Architecture and data flow

Configuration (time_constant) -> numerical model -> alpha, total_rmse_rad, clean_rmse_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

time_constant is seconds; alpha is derived from it and the fixed 10 ms sample interval.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| time_constant | 0.5 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/33_complementary.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only time_constant changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/33_complementary.py --case 0

.venv-book/bin/python expanded_lab/modules/33_complementary.py --case 3

.venv-book/bin/python expanded_lab/run.py complementary --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/33_complementary.py

### H. Walkthrough and design decisions

Compare clean and contaminated segments separately instead of rewarding a filter for one aggregate metric. Fast accelerometer correction reduces bias drift but follows false gravity cues more strongly.

### I. Expected behavior and six worked cases

The controlled variable is time_constant. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/33_complementary.png

Figure L33. alpha as time_constant changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | time_constant | alpha |
|---|---|---|
| 0 | 0.05 | 0.83333333 |
| 1 | 0.1 | 0.90909091 |
| 2 | 0.25 | 0.96153846 |
| 3 | 0.5 | 0.98039216 |
| 4 | 1 | 0.99009901 |
| 5 | 2 | 0.99502488 |

#### Worked case 0: time_constant = 0.05

This case keeps the nominal configuration except for time_constant=0.05. The full input is {"time_constant": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| alpha | 0.83333333 |
| total rmse rad | 0.05270032 |
| clean rmse rad | 0.00632525 |
| contamination peak error rad | 0.16137189 |
| final error rad | -0.00094408 |

1. Time constant 0.05 s with dt=0.01 s gives alpha=0.83333333.

2. True roll is a 0.15 rad, 0.3 Hz sinusoid; gyro bias is 0.01 rad/s.

3. Contaminate the accelerometer roll proxy by +0.15 rad between three and four seconds.

4. Whole-record RMSE is 0.052700 rad; clean-segment RMSE is 0.006325 rad.

5. Peak error during contamination is 0.161372 rad.

#### Worked case 1: time_constant = 0.1

This case keeps the nominal configuration except for time_constant=0.1. The full input is {"time_constant": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| alpha | 0.90909091 |
| total rmse rad | 0.05129666 |
| clean rmse rad | 0.0047827 |
| contamination peak error rad | 0.15794639 |
| final error rad | -0.0008678 |

1. Time constant 0.1 s with dt=0.01 s gives alpha=0.90909091.

2. True roll is a 0.15 rad, 0.3 Hz sinusoid; gyro bias is 0.01 rad/s.

3. Contaminate the accelerometer roll proxy by +0.15 rad between three and four seconds.

4. Whole-record RMSE is 0.051297 rad; clean-segment RMSE is 0.004783 rad.

5. Peak error during contamination is 0.157946 rad.

#### Worked case 2: time_constant = 0.25

This case keeps the nominal configuration except for time_constant=0.25. The full input is {"time_constant": 0.25}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| alpha | 0.96153846 |
| total rmse rad | 0.04755824 |
| clean rmse rad | 0.00412304 |
| contamination peak error rad | 0.15254579 |
| final error rad | -0.00051307 |

1. Time constant 0.25 s with dt=0.01 s gives alpha=0.96153846.

2. True roll is a 0.15 rad, 0.3 Hz sinusoid; gyro bias is 0.01 rad/s.

3. Contaminate the accelerometer roll proxy by +0.15 rad between three and four seconds.

4. Whole-record RMSE is 0.047558 rad; clean-segment RMSE is 0.004123 rad.

5. Peak error during contamination is 0.152546 rad.

#### Worked case 3: time_constant = 0.5

This case keeps the nominal configuration except for time_constant=0.5. The full input is {"time_constant": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| alpha | 0.98039216 |
| total rmse rad | 0.0429261 |
| clean rmse rad | 0.00790984 |
| contamination peak error rad | 0.13563467 |
| final error rad | 0.00201579 |

1. Time constant 0.5 s with dt=0.01 s gives alpha=0.98039216.

2. True roll is a 0.15 rad, 0.3 Hz sinusoid; gyro bias is 0.01 rad/s.

3. Contaminate the accelerometer roll proxy by +0.15 rad between three and four seconds.

4. Whole-record RMSE is 0.042926 rad; clean-segment RMSE is 0.007910 rad.

5. Peak error during contamination is 0.135635 rad.

#### Worked case 4: time_constant = 1

This case keeps the nominal configuration except for time_constant=1. The full input is {"time_constant": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| alpha | 0.99009901 |
| total rmse rad | 0.03899949 |
| clean rmse rad | 0.01760907 |
| contamination peak error rad | 0.10528095 |
| final error rad | 0.00907646 |

1. Time constant 1 s with dt=0.01 s gives alpha=0.99009901.

2. True roll is a 0.15 rad, 0.3 Hz sinusoid; gyro bias is 0.01 rad/s.

3. Contaminate the accelerometer roll proxy by +0.15 rad between three and four seconds.

4. Whole-record RMSE is 0.038999 rad; clean-segment RMSE is 0.017609 rad.

5. Peak error during contamination is 0.105281 rad.

#### Worked case 5: time_constant = 2

This case keeps the nominal configuration except for time_constant=2. The full input is {"time_constant": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| alpha | 0.99502488 |
| total rmse rad | 0.03870177 |
| clean rmse rad | 0.02874565 |
| contamination peak error rad | 0.07719958 |
| final error rad | 0.02542635 |

1. Time constant 2 s with dt=0.01 s gives alpha=0.99502488.

2. True roll is a 0.15 rad, 0.3 Hz sinusoid; gyro bias is 0.01 rad/s.

3. Contaminate the accelerometer roll proxy by +0.15 rad between three and four seconds.

4. Whole-record RMSE is 0.038702 rad; clean-segment RMSE is 0.028746 rad.

5. Peak error during contamination is 0.077200 rad.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The synthetic accelerometer-angle disturbance represents a limitation of gravity-based attitude correction during motion.

A production estimator needs measurement validity checks and a consistent three-dimensional orientation representation.

### K. Failure modes and troubleshooting

Treating accelerometer-derived roll as ground truth while accelerating; tuning alpha without regard to sampling period.

### L. Practical exercises and extension tasks

1. Gate accelerometer correction when acceleration norm deviates from the stationary reference.

2. Estimate gyro bias as an additional state.

3. Compare a fixed alpha with a fixed time constant under changed sampling rate.

### M. Connection to the Asimov research platform

IMU correction assumptions must be tested in supported stationary, moving and contact-transition conditions.

### N. Completion record

Record your chosen case, predicted trend, measured alpha, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 34, Scalar Kalman filtering and covariance interpretation. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 34 - Scalar Kalman filtering and covariance interpretation

### A. The engineering question

A Kalman filter combines a prediction with a measurement according to their modeled uncertainty.

### B. Concepts and mathematical model

The gain is not an arbitrary smoothing coefficient: it emerges from predicted state variance and measurement variance. If those variances are wrong, the numerical covariance can look precise while the estimate is biased or overconfident. This scalar random-walk model provides a complete update cycle and a direct comparison between empirical error and reported uncertainty.

P_pred=P+Q; K=P_pred/(P_pred+R); x=x_pred+K*(z-x_pred); P=(1-K)^2*P_pred+K^2*R.

### C. Real-world meaning and limits

Robot estimators require a physically defensible process model and measurement covariances based on actual sensing conditions.

### D. Architecture and data flow

Configuration (assumed_measurement_variance) -> numerical model -> estimate_rmse, reported_std, final_gain -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

assumed_measurement_variance is squared measurement units; process variance and actual measurement noise stay fixed.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| assumed_measurement_variance | 0.01 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/34_kalman_scalar.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only assumed_measurement_variance changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/34_kalman_scalar.py --case 0

.venv-book/bin/python expanded_lab/modules/34_kalman_scalar.py --case 3

.venv-book/bin/python expanded_lab/run.py kalman_scalar --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/34_kalman_scalar.py

### H. Walkthrough and design decisions

The Joseph covariance form retains nonnegativity more robustly than a careless subtractive implementation. Compare uncertainty calibration as well as state error.

### I. Expected behavior and six worked cases

The controlled variable is assumed_measurement_variance. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/34_kalman_scalar.png

Figure L34. estimate rmse as assumed_measurement_variance changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | assumed_measurement_variance | estimate rmse |
|---|---|---|
| 0 | 0.0001 | 0.07318392 |
| 1 | 0.001 | 0.04609931 |
| 2 | 0.005 | 0.03697675 |
| 3 | 0.01 | 0.03607727 |
| 4 | 0.05 | 0.0407165 |
| 5 | 0.1 | 0.04561209 |

#### Worked case 0: assumed_measurement_variance = 0.0001

This case keeps the nominal configuration except for assumed_measurement_variance=0.0001. The full input is {"assumed_measurement_variance": 0.0001}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimate rmse | 0.07318392 |
| reported std | 0.00786709 |
| final gain | 0.61803399 |
| empirical two sigma coverage | 0.172 |

1. True process variance per step is 0.0001; true measurement variance is 0.01.

2. The filter assumes measurement variance 0.0001.

3. Predict variance, calculate gain, correct state, then use Joseph-form scalar covariance update.

4. Empirical RMSE is 0.073184; reported RMS standard deviation is 0.007867.

5. Two-sigma empirical coverage is 0.172000.

#### Worked case 1: assumed_measurement_variance = 0.001

This case keeps the nominal configuration except for assumed_measurement_variance=0.001. The full input is {"assumed_measurement_variance": 0.001}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimate rmse | 0.04609931 |
| reported std | 0.01651004 |
| final gain | 0.27015621 |
| empirical two sigma coverage | 0.486 |

1. True process variance per step is 0.0001; true measurement variance is 0.01.

2. The filter assumes measurement variance 0.001.

3. Predict variance, calculate gain, correct state, then use Joseph-form scalar covariance update.

4. Empirical RMSE is 0.046099; reported RMS standard deviation is 0.016510.

5. Two-sigma empirical coverage is 0.486000.

#### Worked case 2: assumed_measurement_variance = 0.005

This case keeps the nominal configuration except for assumed_measurement_variance=0.005. The full input is {"assumed_measurement_variance": 0.005}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimate rmse | 0.03697675 |
| reported std | 0.02603787 |
| final gain | 0.13177447 |
| empirical two sigma coverage | 0.844 |

1. True process variance per step is 0.0001; true measurement variance is 0.01.

2. The filter assumes measurement variance 0.005.

3. Predict variance, calculate gain, correct state, then use Joseph-form scalar covariance update.

4. Empirical RMSE is 0.036977; reported RMS standard deviation is 0.026038.

5. Two-sigma empirical coverage is 0.844000.

#### Worked case 3: assumed_measurement_variance = 0.01

This case keeps the nominal configuration except for assumed_measurement_variance=0.01. The full input is {"assumed_measurement_variance": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimate rmse | 0.03607727 |
| reported std | 0.03155553 |
| final gain | 0.09512492 |
| empirical two sigma coverage | 0.926 |

1. True process variance per step is 0.0001; true measurement variance is 0.01.

2. The filter assumes measurement variance 0.01.

3. Predict variance, calculate gain, correct state, then use Joseph-form scalar covariance update.

4. Empirical RMSE is 0.036077; reported RMS standard deviation is 0.031556.

5. Two-sigma empirical coverage is 0.926000.

#### Worked case 4: assumed_measurement_variance = 0.05

This case keeps the nominal configuration except for assumed_measurement_variance=0.05. The full input is {"assumed_measurement_variance": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimate rmse | 0.0407165 |
| reported std | 0.04980345 |
| final gain | 0.04373254 |
| empirical two sigma coverage | 0.978 |

1. True process variance per step is 0.0001; true measurement variance is 0.01.

2. The filter assumes measurement variance 0.05.

3. Predict variance, calculate gain, correct state, then use Joseph-form scalar covariance update.

4. Empirical RMSE is 0.040717; reported RMS standard deviation is 0.049803.

5. Two-sigma empirical coverage is 0.978000.

#### Worked case 5: assumed_measurement_variance = 0.1

This case keeps the nominal configuration except for assumed_measurement_variance=0.1. The full input is {"assumed_measurement_variance": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| estimate rmse | 0.04561209 |
| reported std | 0.06126555 |
| final gain | 0.03112673 |
| empirical two sigma coverage | 0.984 |

1. True process variance per step is 0.0001; true measurement variance is 0.01.

2. The filter assumes measurement variance 0.1.

3. Predict variance, calculate gain, correct state, then use Joseph-form scalar covariance update.

4. Empirical RMSE is 0.045612; reported RMS standard deviation is 0.061266.

5. Two-sigma empirical coverage is 0.984000.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Coverage is a diagnostic under this synthetic model, not a universal confidence guarantee.

Underestimating measurement variance can increase trust in noisy data and make the reported covariance overconfident.

### K. Failure modes and troubleshooting

Using standard deviation where variance is required; confusing measurement residual with state error; assuming diagonal covariance means physical independence.

### L. Practical exercises and extension tasks

1. Change actual noise without changing filter assumptions.

2. Add a constant measurement bias and inspect covariance failure.

3. Compute normalized innovations and test their scale.

### M. Connection to the Asimov research platform

Robot estimators require a physically defensible process model and measurement covariances based on actual sensing conditions.

### N. Completion record

Record your chosen case, predicted trend, measured estimate_rmse, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 35, Position and velocity estimation with intermittent measurements. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 35 - Position and velocity estimation with intermittent measurements

### A. The engineering question

Velocity is often not measured directly or is too noisy to use after simple differentiation.

### B. Concepts and mathematical model

A constant-velocity Kalman model estimates position and speed together while carrying uncertainty through missing observations. Prediction during a dropout should increase uncertainty; inventing a repeated fresh measurement would hide the lack of information. This laboratory removes a block of position measurements and measures estimation error during that interval.

F=[[1,dt],[0,1]]; H=[1,0]; P_pred=F*P*F.T+Q; K=P_pred*H.T/(H*P_pred*H.T+R).

### C. Real-world meaning and limits

Contact-based velocity updates must be disabled or downweighted when the assumed foot slips or loses load.

### D. Architecture and data flow

Configuration (dropout_seconds) -> numerical model -> velocity_rmse_m_s, dropout_velocity_rmse_m_s, final_velocity_m_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

dropout_seconds is the duration of missing position observations; measurement standard deviation is 0.01 m.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| dropout_seconds | 0.5 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/35_kalman_velocity.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only dropout_seconds changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/35_kalman_velocity.py --case 0

.venv-book/bin/python expanded_lab/modules/35_kalman_velocity.py --case 3

.venv-book/bin/python expanded_lab/run.py kalman_velocity --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/35_kalman_velocity.py

### H. Walkthrough and design decisions

Prediction and correction are separate branches. Inspect covariance positive-semidefiniteness and avoid accidentally updating on stale copies during the dropout.

### I. Expected behavior and six worked cases

The controlled variable is dropout_seconds. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/35_kalman_velocity.png

Figure L35. velocity rmse m s as dropout_seconds changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | dropout_seconds | velocity rmse m s |
|---|---|---|
| 0 | 0 | 0.04689866 |
| 1 | 0.1 | 0.04690584 |
| 2 | 0.25 | 0.04693812 |
| 3 | 0.5 | 0.04702495 |
| 4 | 1 | 0.04738355 |
| 5 | 2 | 0.04804862 |

#### Worked case 0: dropout_seconds = 0

This case keeps the nominal configuration except for dropout_seconds=0. The full input is {"dropout_seconds": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| velocity rmse m s | 0.04689866 |
| dropout velocity rmse m s | 0 |
| final velocity m s | 0.20728961 |
| final position std m | 0.00292494 |
| final velocity std m s | 0.00935228 |

1. Use a two-state position/velocity model with dt=0.02 s.

2. Drop measurements from t=2 s to t=2 s.

3. Predict through missing samples without applying fabricated corrections.

4. Whole-run speed RMSE is 0.046899 m/s.

5. Dropout speed RMSE is 0.000000 m/s; final speed estimate is 0.207290 m/s.

#### Worked case 1: dropout_seconds = 0.1

This case keeps the nominal configuration except for dropout_seconds=0.1. The full input is {"dropout_seconds": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| velocity rmse m s | 0.04690584 |
| dropout velocity rmse m s | 0.01198 |
| final velocity m s | 0.20729009 |
| final position std m | 0.00292494 |
| final velocity std m s | 0.00935228 |

1. Use a two-state position/velocity model with dt=0.02 s.

2. Drop measurements from t=2 s to t=2.1 s.

3. Predict through missing samples without applying fabricated corrections.

4. Whole-run speed RMSE is 0.046906 m/s.

5. Dropout speed RMSE is 0.011980 m/s; final speed estimate is 0.207290 m/s.

#### Worked case 2: dropout_seconds = 0.25

This case keeps the nominal configuration except for dropout_seconds=0.25. The full input is {"dropout_seconds": 0.25}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| velocity rmse m s | 0.04693812 |
| dropout velocity rmse m s | 0.01340119 |
| final velocity m s | 0.20729138 |
| final position std m | 0.00292494 |
| final velocity std m s | 0.00935228 |

1. Use a two-state position/velocity model with dt=0.02 s.

2. Drop measurements from t=2 s to t=2.25 s.

3. Predict through missing samples without applying fabricated corrections.

4. Whole-run speed RMSE is 0.046938 m/s.

5. Dropout speed RMSE is 0.013401 m/s; final speed estimate is 0.207291 m/s.

#### Worked case 3: dropout_seconds = 0.5

This case keeps the nominal configuration except for dropout_seconds=0.5. The full input is {"dropout_seconds": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| velocity rmse m s | 0.04702495 |
| dropout velocity rmse m s | 0.01537378 |
| final velocity m s | 0.20729021 |
| final position std m | 0.00292494 |
| final velocity std m s | 0.00935228 |

1. Use a two-state position/velocity model with dt=0.02 s.

2. Drop measurements from t=2 s to t=2.5 s.

3. Predict through missing samples without applying fabricated corrections.

4. Whole-run speed RMSE is 0.047025 m/s.

5. Dropout speed RMSE is 0.015374 m/s; final speed estimate is 0.207290 m/s.

#### Worked case 4: dropout_seconds = 1

This case keeps the nominal configuration except for dropout_seconds=1. The full input is {"dropout_seconds": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| velocity rmse m s | 0.04738355 |
| dropout velocity rmse m s | 0.01850473 |
| final velocity m s | 0.2072862 |
| final position std m | 0.00292494 |
| final velocity std m s | 0.00935228 |

1. Use a two-state position/velocity model with dt=0.02 s.

2. Drop measurements from t=2 s to t=3 s.

3. Predict through missing samples without applying fabricated corrections.

4. Whole-run speed RMSE is 0.047384 m/s.

5. Dropout speed RMSE is 0.018505 m/s; final speed estimate is 0.207286 m/s.

#### Worked case 5: dropout_seconds = 2

This case keeps the nominal configuration except for dropout_seconds=2. The full input is {"dropout_seconds": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| velocity rmse m s | 0.04804862 |
| dropout velocity rmse m s | 0.01982028 |
| final velocity m s | 0.20735177 |
| final position std m | 0.0029252 |
| final velocity std m s | 0.00935443 |

1. Use a two-state position/velocity model with dt=0.02 s.

2. Drop measurements from t=2 s to t=4 s.

3. Predict through missing samples without applying fabricated corrections.

4. Whole-run speed RMSE is 0.048049 m/s.

5. Dropout speed RMSE is 0.019820 m/s; final speed estimate is 0.207352 m/s.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The true motion contains a small acceleration that is not exactly constant velocity.

The filter state and covariance are expressed in one dimension; full robot base estimation requires orientation and contact models.

### K. Failure modes and troubleshooting

Labeling a held last measurement as newly sampled; measuring velocity truth in a different frame; omitting process noise during unmodeled acceleration.

### L. Practical exercises and extension tasks

1. Add timestamp jitter and rebuild F from actual intervals.

2. Inject a sensor jump and add an innovation gate.

3. Compare with differentiated noisy position.

### M. Connection to the Asimov research platform

Contact-based velocity updates must be disabled or downweighted when the assumed foot slips or loses load.

### N. Completion record

Record your chosen case, predicted trend, measured velocity_rmse_m_s, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 36, Camera intrinsics, projection and pixel-error sensitivity. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 36 - Camera intrinsics, projection and pixel-error sensitivity

### A. The engineering question

A camera converts spatial geometry into pixel measurements.

### B. Concepts and mathematical model

Focal lengths are measured in pixels after calibration; principal point is the pixel location of the optical axis. Projection divides by depth, making near-zero or negative depth invalid for a simple visible-point model. Pixel error maps back into metric lateral error in proportion to depth. This laboratory computes a projection and an inverse reconstruction with known depth, making the missing-depth assumption explicit.

u=fx*X/Z+cx; v=fy*Y/Z+cy; X=(u-cx)*Z/fx; lateral uncertainty approx Z*sigma_pixel/fx.

### C. Real-world meaning and limits

The documented Asimov monocular camera does not by itself provide the known depth used in this numerical exercise.

### D. Architecture and data flow

Configuration (depth, pixel_noise) -> numerical model -> pixel_u, pixel_v, lateral_uncertainty_m -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

depth is positive optical-axis meters; pixel_noise is assumed image-coordinate standard deviation in pixels.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| depth | 1 | Defined by the explicit chapter model and parameter contract |
| pixel_noise | 1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/36_pinhole.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only depth changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/36_pinhole.py --case 0

.venv-book/bin/python expanded_lab/modules/36_pinhole.py --case 3

.venv-book/bin/python expanded_lab/run.py pinhole --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/36_pinhole.py

### H. Walkthrough and design decisions

Perform a projection/inverse round trip before adding noise. The uncertainty scaling then isolates geometric depth sensitivity from calibration and detector accuracy.

### I. Expected behavior and six worked cases

The controlled variable is depth. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/36_pinhole.png

Figure L36. pixel u as depth changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | depth | pixel u |
|---|---|---|
| 0 | 0.2 | 520 |
| 1 | 0.5 | 400 |
| 2 | 1 | 360 |
| 3 | 2 | 340 |
| 4 | 3 | 333.33333333 |
| 5 | 5 | 328 |

#### Worked case 0: depth = 0.2

This case keeps the nominal configuration except for depth=0.2. The full input is {"depth": 0.2, "pixel_noise": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| pixel u | 520 |
| pixel v | 137.5 |
| lateral uncertainty m | 0.0005 |
| roundtrip error m | 0 |
| projection scale px per m | 2000 |

1. Use fx=400, fy=410, cx=320, cy=240 pixels.

2. Project point (0.1,-0.05,0.2) m.

3. Pixel result is u=520.000000, v=137.500000.

4. Assuming exact known depth, inverse projection returns [0.1, -0.05, 0.2] m.

5. Pixel noise sigma=1 px maps to lateral sigma approximately 0.000500 m.

#### Worked case 1: depth = 0.5

This case keeps the nominal configuration except for depth=0.5. The full input is {"depth": 0.5, "pixel_noise": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| pixel u | 400 |
| pixel v | 199 |
| lateral uncertainty m | 0.00125 |
| roundtrip error m | 0 |
| projection scale px per m | 800 |

1. Use fx=400, fy=410, cx=320, cy=240 pixels.

2. Project point (0.1,-0.05,0.5) m.

3. Pixel result is u=400.000000, v=199.000000.

4. Assuming exact known depth, inverse projection returns [0.1, -0.05, 0.5] m.

5. Pixel noise sigma=1 px maps to lateral sigma approximately 0.001250 m.

#### Worked case 2: depth = 1

This case keeps the nominal configuration except for depth=1. The full input is {"depth": 1.0, "pixel_noise": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| pixel u | 360 |
| pixel v | 219.5 |
| lateral uncertainty m | 0.0025 |
| roundtrip error m | 0 |
| projection scale px per m | 400 |

1. Use fx=400, fy=410, cx=320, cy=240 pixels.

2. Project point (0.1,-0.05,1) m.

3. Pixel result is u=360.000000, v=219.500000.

4. Assuming exact known depth, inverse projection returns [0.1, -0.05, 1.0] m.

5. Pixel noise sigma=1 px maps to lateral sigma approximately 0.002500 m.

#### Worked case 3: depth = 2

This case keeps the nominal configuration except for depth=2. The full input is {"depth": 2.0, "pixel_noise": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| pixel u | 340 |
| pixel v | 229.75 |
| lateral uncertainty m | 0.005 |
| roundtrip error m | 0 |
| projection scale px per m | 200 |

1. Use fx=400, fy=410, cx=320, cy=240 pixels.

2. Project point (0.1,-0.05,2) m.

3. Pixel result is u=340.000000, v=229.750000.

4. Assuming exact known depth, inverse projection returns [0.1, -0.05, 2.0] m.

5. Pixel noise sigma=1 px maps to lateral sigma approximately 0.005000 m.

#### Worked case 4: depth = 3

This case keeps the nominal configuration except for depth=3. The full input is {"depth": 3.0, "pixel_noise": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| pixel u | 333.33333333 |
| pixel v | 233.16666667 |
| lateral uncertainty m | 0.0075 |
| roundtrip error m | 1.6768595e-16 |
| projection scale px per m | 133.33333333 |

1. Use fx=400, fy=410, cx=320, cy=240 pixels.

2. Project point (0.1,-0.05,3) m.

3. Pixel result is u=333.333333, v=233.166667.

4. Assuming exact known depth, inverse projection returns [0.09999999999999985, -0.05000000000000007, 3.0] m.

5. Pixel noise sigma=1 px maps to lateral sigma approximately 0.007500 m.

#### Worked case 5: depth = 5

This case keeps the nominal configuration except for depth=5. The full input is {"depth": 5.0, "pixel_noise": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| pixel u | 328 |
| pixel v | 235.9 |
| lateral uncertainty m | 0.0125 |
| roundtrip error m | 6.9388939e-17 |
| projection scale px per m | 80 |

1. Use fx=400, fy=410, cx=320, cy=240 pixels.

2. Project point (0.1,-0.05,5) m.

3. Pixel result is u=328.000000, v=235.900000.

4. Assuming exact known depth, inverse projection returns [0.1, -0.04999999999999993, 5.0] m.

5. Pixel noise sigma=1 px maps to lateral sigma approximately 0.012500 m.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The inverse result requires known depth; a monocular pixel alone does not identify a metric 3-D point.

Distortion, rolling shutter, calibration uncertainty and camera-to-body extrinsics are excluded here.

### K. Failure modes and troubleshooting

Using image width as focal length without calibration; assuming Euclidean range equals optical-axis depth; mixing RGB camera and depth camera frames.

### L. Practical exercises and extension tasks

1. Propagate focal-length uncertainty in addition to pixel noise.

2. Add a calibrated camera-to-base transform.

3. Reject points behind the camera and near the projection singularity.

### M. Connection to the Asimov research platform

The documented Asimov monocular camera does not by itself provide the known depth used in this numerical exercise.

### N. Completion record

Record your chosen case, predicted trend, measured pixel_u, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 37, Stereo depth, disparity uncertainty and range limits. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 37 - Stereo depth, disparity uncertainty and range limits

### A. The engineering question

Stereo geometry can estimate depth from a calibrated baseline and image disparity.

### B. Concepts and mathematical model

Small disparity at long range makes depth highly sensitive to pixel error. Thus a detector may identify an object reliably while its metric position is too uncertain for reaching. The first-order uncertainty calculation is informative near a well-behaved measurement, but poor disparity and outliers need explicit rejection. This is a generic optional sensor study, not a claim that the base Asimov includes stereo depth.

Z=f*B/d; sigma_Z approx f*B*sigma_d/d^2; relative depth uncertainty=sigma_d/d.

### C. Real-world meaning and limits

Adding a depth sensor changes mounting, compute, power and calibration budgets and requires explicit compatibility verification.

### D. Architecture and data flow

Configuration (true_depth, disparity_noise) -> numerical model -> disparity_px, depth_std_m, relative_depth_std -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

true_depth is meters; disparity_noise is pixels; baseline and focal length are fixed calibrated teaching values.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| true_depth | 1 | Defined by the explicit chapter model and parameter contract |
| disparity_noise | 0.5 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/37_stereo_depth.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only true_depth changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/37_stereo_depth.py --case 0

.venv-book/bin/python expanded_lab/modules/37_stereo_depth.py --case 3

.venv-book/bin/python expanded_lab/run.py stereo_depth --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/37_stereo_depth.py

### H. Walkthrough and design decisions

Compare exact perturbed geometry with a derivative-based approximation. This reveals where uncertainty propagation itself needs a nonlinear or robust treatment.

### I. Expected behavior and six worked cases

The controlled variable is true_depth. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/37_stereo_depth.png

Figure L37. disparity px as true_depth changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | true_depth | disparity px |
|---|---|---|
| 0 | 0.3 | 80 |
| 1 | 0.5 | 48 |
| 2 | 1 | 24 |
| 3 | 2 | 12 |
| 4 | 3 | 8 |
| 5 | 5 | 4.8 |

#### Worked case 0: true_depth = 0.3

This case keeps the nominal configuration except for true_depth=0.3. The full input is {"disparity_noise": 0.5, "true_depth": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| disparity px | 80 |
| depth std m | 0.001875 |
| relative depth std | 0.00625 |
| one sigma positive disparity depth m | 0.29813665 |
| linearization error m | 0.00001165 |

1. Use focal length 400 px and calibrated baseline 0.06 m.

2. At true depth 0.3 m, expected disparity is 80.000000 px.

3. Disparity sigma=0.5 px propagates to sigma_Z=0.001875 m.

4. A +1 sigma disparity perturbation gives exact depth 0.298137 m.

5. Compare the first-order prediction Z-sigma_Z; linearization discrepancy is 0.000012 m.

#### Worked case 1: true_depth = 0.5

This case keeps the nominal configuration except for true_depth=0.5. The full input is {"disparity_noise": 0.5, "true_depth": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| disparity px | 48 |
| depth std m | 0.00520833 |
| relative depth std | 0.01041667 |
| one sigma positive disparity depth m | 0.49484536 |
| linearization error m | 0.00005369 |

1. Use focal length 400 px and calibrated baseline 0.06 m.

2. At true depth 0.5 m, expected disparity is 48.000000 px.

3. Disparity sigma=0.5 px propagates to sigma_Z=0.005208 m.

4. A +1 sigma disparity perturbation gives exact depth 0.494845 m.

5. Compare the first-order prediction Z-sigma_Z; linearization discrepancy is 0.000054 m.

#### Worked case 2: true_depth = 1

This case keeps the nominal configuration except for true_depth=1. The full input is {"disparity_noise": 0.5, "true_depth": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| disparity px | 24 |
| depth std m | 0.02083333 |
| relative depth std | 0.02083333 |
| one sigma positive disparity depth m | 0.97959184 |
| linearization error m | 0.00042517 |

1. Use focal length 400 px and calibrated baseline 0.06 m.

2. At true depth 1 m, expected disparity is 24.000000 px.

3. Disparity sigma=0.5 px propagates to sigma_Z=0.020833 m.

4. A +1 sigma disparity perturbation gives exact depth 0.979592 m.

5. Compare the first-order prediction Z-sigma_Z; linearization discrepancy is 0.000425 m.

#### Worked case 3: true_depth = 2

This case keeps the nominal configuration except for true_depth=2. The full input is {"disparity_noise": 0.5, "true_depth": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| disparity px | 12 |
| depth std m | 0.08333333 |
| relative depth std | 0.04166667 |
| one sigma positive disparity depth m | 1.92 |
| linearization error m | 0.00333333 |

1. Use focal length 400 px and calibrated baseline 0.06 m.

2. At true depth 2 m, expected disparity is 12.000000 px.

3. Disparity sigma=0.5 px propagates to sigma_Z=0.083333 m.

4. A +1 sigma disparity perturbation gives exact depth 1.920000 m.

5. Compare the first-order prediction Z-sigma_Z; linearization discrepancy is 0.003333 m.

#### Worked case 4: true_depth = 3

This case keeps the nominal configuration except for true_depth=3. The full input is {"disparity_noise": 0.5, "true_depth": 3.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| disparity px | 8 |
| depth std m | 0.1875 |
| relative depth std | 0.0625 |
| one sigma positive disparity depth m | 2.82352941 |
| linearization error m | 0.01102941 |

1. Use focal length 400 px and calibrated baseline 0.06 m.

2. At true depth 3 m, expected disparity is 8.000000 px.

3. Disparity sigma=0.5 px propagates to sigma_Z=0.187500 m.

4. A +1 sigma disparity perturbation gives exact depth 2.823529 m.

5. Compare the first-order prediction Z-sigma_Z; linearization discrepancy is 0.011029 m.

#### Worked case 5: true_depth = 5

This case keeps the nominal configuration except for true_depth=5. The full input is {"disparity_noise": 0.5, "true_depth": 5.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| disparity px | 4.8 |
| depth std m | 0.52083333 |
| relative depth std | 0.10416667 |
| one sigma positive disparity depth m | 4.52830189 |
| linearization error m | 0.04913522 |

1. Use focal length 400 px and calibrated baseline 0.06 m.

2. At true depth 5 m, expected disparity is 4.800000 px.

3. Disparity sigma=0.5 px propagates to sigma_Z=0.520833 m.

4. A +1 sigma disparity perturbation gives exact depth 4.528302 m.

5. Compare the first-order prediction Z-sigma_Z; linearization discrepancy is 0.049135 m.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Depth uncertainty grows quadratically with range in this fixed-camera approximation.

When disparity approaches its uncertainty scale, Gaussian linearization and naive depth estimates become unreliable.

### K. Failure modes and troubleshooting

Assuming a precise-looking depth number has low uncertainty; ignoring rectification and synchronization; treating disparity outliers as ordinary noise.

### L. Practical exercises and extension tasks

1. Define a maximum permitted relative-depth uncertainty and calculate usable range.

2. Monte Carlo disparity noise and inspect the depth distribution.

3. Combine depth and camera-extrinsic uncertainty in base coordinates.

### M. Connection to the Asimov research platform

Adding a depth sensor changes mounting, compute, power and calibration budgets and requires explicit compatibility verification.

### N. Completion record

Record your chosen case, predicted trend, measured disparity_px, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 38, Timestamps, interpolation and asynchronous sensor streams. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 38 - Timestamps, interpolation and asynchronous sensor streams

### A. The engineering question

Sensors rarely produce measurements at identical times.

### B. Concepts and mathematical model

Comparing an encoder sample at one instant with an IMU sample at another creates a synchronization error even if both values are individually accurate. Interpolation can align streams for analysis, but it needs timestamp validity and does not recover arbitrarily fast unseen motion. This laboratory samples a known signal with a clock offset and compares naive alignment with timestamp-aware interpolation.

y_aligned(t_ref)=interpolate((t_sensor+offset,y_sensor),t_ref); error depends on signal slope, offset and sampling interval.

### C. Real-world meaning and limits

Time alignment affects state estimation, camera localization and replay; document the clock source of every recorded field.

### D. Architecture and data flow

Configuration (offset, sample_rate) -> numerical model -> naive_alignment_rmse, corrected_alignment_rmse, nominal_phase_error_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

offset is seconds added to the actual sampling instant; sample_rate is Hertz; reference timestamps remain independent.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| offset | 0.01 | meters |
| sample_rate | 100 | Hertz |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/38_resampling.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only offset changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/38_resampling.py --case 0

.venv-book/bin/python expanded_lab/modules/38_resampling.py --case 3

.venv-book/bin/python expanded_lab/run.py resampling --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/38_resampling.py

### H. Walkthrough and design decisions

The synthetic signal is evaluated at actual sensor instants so the offset has a precise meaning. Correcting timestamps rather than shifting values preserves the measurement model.

### I. Expected behavior and six worked cases

The controlled variable is offset. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/38_resampling.png

Figure L38. naive alignment rmse as offset changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | offset | naive alignment rmse |
|---|---|---|
| 0 | 0 | 0.00097213 |
| 1 | 0.001 | 0.00906162 |
| 2 | 0.005 | 0.04505083 |
| 3 | 0.01 | 0.09003897 |
| 4 | 0.02 | 0.17967479 |
| 5 | 0.05 | 0.44212903 |

#### Worked case 0: offset = 0

This case keeps the nominal configuration except for offset=0. The full input is {"offset": 0.0, "sample_rate": 100.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| naive alignment rmse | 0.00097213 |
| corrected alignment rmse | 0.00097213 |
| nominal phase error rad | 0 |
| sensor interval s | 0.01 |

1. The signal is a 2 Hz sinusoid sampled at 100 Hz.

2. Sensor timestamp offset is 0 s, equivalent to phase 0.000000 rad.

3. Naive interpolation treats nominal sensor times as correct.

4. Naive RMSE is 0.000972.

5. Adding the known offset before interpolation reduces RMSE to 0.000972.

#### Worked case 1: offset = 0.001

This case keeps the nominal configuration except for offset=0.001. The full input is {"offset": 0.001, "sample_rate": 100.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| naive alignment rmse | 0.00906162 |
| corrected alignment rmse | 0.00099673 |
| nominal phase error rad | 0.01256637 |
| sensor interval s | 0.01 |

1. The signal is a 2 Hz sinusoid sampled at 100 Hz.

2. Sensor timestamp offset is 0.001 s, equivalent to phase 0.012566 rad.

3. Naive interpolation treats nominal sensor times as correct.

4. Naive RMSE is 0.009062.

5. Adding the known offset before interpolation reduces RMSE to 0.000997.

#### Worked case 2: offset = 0.005

This case keeps the nominal configuration except for offset=0.005. The full input is {"offset": 0.005, "sample_rate": 100.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| naive alignment rmse | 0.04505083 |
| corrected alignment rmse | 0.00097225 |
| nominal phase error rad | 0.06283185 |
| sensor interval s | 0.01 |

1. The signal is a 2 Hz sinusoid sampled at 100 Hz.

2. Sensor timestamp offset is 0.005 s, equivalent to phase 0.062832 rad.

3. Naive interpolation treats nominal sensor times as correct.

4. Naive RMSE is 0.045051.

5. Adding the known offset before interpolation reduces RMSE to 0.000972.

#### Worked case 3: offset = 0.01

This case keeps the nominal configuration except for offset=0.01. The full input is {"offset": 0.01, "sample_rate": 100.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| naive alignment rmse | 0.09003897 |
| corrected alignment rmse | 0.00097213 |
| nominal phase error rad | 0.12566371 |
| sensor interval s | 0.01 |

1. The signal is a 2 Hz sinusoid sampled at 100 Hz.

2. Sensor timestamp offset is 0.01 s, equivalent to phase 0.125664 rad.

3. Naive interpolation treats nominal sensor times as correct.

4. Naive RMSE is 0.090039.

5. Adding the known offset before interpolation reduces RMSE to 0.000972.

#### Worked case 4: offset = 0.02

This case keeps the nominal configuration except for offset=0.02. The full input is {"offset": 0.02, "sample_rate": 100.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| naive alignment rmse | 0.17967479 |
| corrected alignment rmse | 0.00097213 |
| nominal phase error rad | 0.25132741 |
| sensor interval s | 0.01 |

1. The signal is a 2 Hz sinusoid sampled at 100 Hz.

2. Sensor timestamp offset is 0.02 s, equivalent to phase 0.251327 rad.

3. Naive interpolation treats nominal sensor times as correct.

4. Naive RMSE is 0.179675.

5. Adding the known offset before interpolation reduces RMSE to 0.000972.

#### Worked case 5: offset = 0.05

This case keeps the nominal configuration except for offset=0.05. The full input is {"offset": 0.05, "sample_rate": 100.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| naive alignment rmse | 0.44212903 |
| corrected alignment rmse | 0.00097213 |
| nominal phase error rad | 0.62831853 |
| sensor interval s | 0.01 |

1. The signal is a 2 Hz sinusoid sampled at 100 Hz.

2. Sensor timestamp offset is 0.05 s, equivalent to phase 0.628319 rad.

3. Naive interpolation treats nominal sensor times as correct.

4. Naive RMSE is 0.442129.

5. Adding the known offset before interpolation reduces RMSE to 0.000972.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Residual after offset correction includes interpolation error from finite sampling.

An unknown or drifting clock offset requires estimation and validity limits; arrival time is not a substitute for sample time.

### K. Failure modes and troubleshooting

Interpolating across long dropouts; subtracting unsynchronized host clocks; using future samples in a real-time algorithm without accounting for latency.

### L. Practical exercises and extension tasks

1. Add linear clock drift and estimate it from matched events.

2. Mark interpolation across large gaps invalid.

3. Compare causal hold, linear interpolation and delayed smoothing.

### M. Connection to the Asimov research platform

Time alignment affects state estimation, camera localization and replay; document the clock source of every recorded field.

### N. Completion record

Record your chosen case, predicted trend, measured naive_alignment_rmse, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 39, Contact detection, thresholds and hysteresis. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 39 - Contact detection, thresholds and hysteresis

### A. The engineering question

A noisy force-like signal can chatter around a single contact threshold, repeatedly changing the controller's assumed support set.

### B. Concepts and mathematical model

Hysteresis uses a higher entry threshold and lower exit threshold, creating memory that reduces switching. It also delays transitions and can miss weak contacts. Evaluate detection against labeled conditions, not merely a smoother-looking plot. This experiment uses synthetic contact loads with noise and reports false positives, false negatives and transition count.

if not_contact and load>=enter: contact=True; if contact and load<=exit: contact=False; exit<enter.

### C. Real-world meaning and limits

If physical force sensors are absent, contact estimation needs a separately validated model and uncertainty treatment.

### D. Architecture and data flow

Configuration (noise_std) -> numerical model -> false_positive_fraction, false_negative_fraction, transition_count -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

noise_std is Newtons of synthetic zero-mean noise; the true supported load is 30 N during the labeled interval.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| noise_std | 5 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/39_contact_hysteresis.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only noise_std changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/39_contact_hysteresis.py --case 0

.venv-book/bin/python expanded_lab/modules/39_contact_hysteresis.py --case 3

.venv-book/bin/python expanded_lab/run.py contact_hysteresis --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/39_contact_hysteresis.py

### H. Walkthrough and design decisions

The detector carries state between samples. Calculate errors separately inside and outside contact; an always-contact classifier can look acceptable if the dataset is imbalanced.

### I. Expected behavior and six worked cases

The controlled variable is noise_std. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/39_contact_hysteresis.png

Figure L39. false positive fraction as noise_std changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | noise_std | false positive fraction |
|---|---|---|
| 0 | 0.5 | 0 |
| 1 | 2 | 0 |
| 2 | 5 | 0 |
| 3 | 8 | 0.04 |
| 4 | 12 | 0.115 |
| 5 | 20 | 0.26 |

#### Worked case 0: noise_std = 0.5

This case keeps the nominal configuration except for noise_std=0.5. The full input is {"noise_std": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| false positive fraction | 0 |
| false negative fraction | 0 |
| transition count | 2 |
| accuracy | 1 |
| signal noise std N | 0.5 |

1. The labeled contact interval is one to three seconds with mean load 30 N.

2. Add Gaussian noise with sigma=0.5 N.

3. Enter contact at 15 N and leave at 5 N using a stateful threshold.

4. False-positive fraction is 0.000000; false-negative fraction is 0.000000.

5. The detector made 2 state transitions instead of the ideal two.

#### Worked case 1: noise_std = 2

This case keeps the nominal configuration except for noise_std=2. The full input is {"noise_std": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| false positive fraction | 0 |
| false negative fraction | 0 |
| transition count | 2 |
| accuracy | 1 |
| signal noise std N | 2 |

1. The labeled contact interval is one to three seconds with mean load 30 N.

2. Add Gaussian noise with sigma=2 N.

3. Enter contact at 15 N and leave at 5 N using a stateful threshold.

4. False-positive fraction is 0.000000; false-negative fraction is 0.000000.

5. The detector made 2 state transitions instead of the ideal two.

#### Worked case 2: noise_std = 5

This case keeps the nominal configuration except for noise_std=5. The full input is {"noise_std": 5.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| false positive fraction | 0 |
| false negative fraction | 0 |
| transition count | 2 |
| accuracy | 1 |
| signal noise std N | 5 |

1. The labeled contact interval is one to three seconds with mean load 30 N.

2. Add Gaussian noise with sigma=5 N.

3. Enter contact at 15 N and leave at 5 N using a stateful threshold.

4. False-positive fraction is 0.000000; false-negative fraction is 0.000000.

5. The detector made 2 state transitions instead of the ideal two.

#### Worked case 3: noise_std = 8

This case keeps the nominal configuration except for noise_std=8. The full input is {"noise_std": 8.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| false positive fraction | 0.04 |
| false negative fraction | 0.005 |
| transition count | 16 |
| accuracy | 0.9775 |
| signal noise std N | 8 |

1. The labeled contact interval is one to three seconds with mean load 30 N.

2. Add Gaussian noise with sigma=8 N.

3. Enter contact at 15 N and leave at 5 N using a stateful threshold.

4. False-positive fraction is 0.040000; false-negative fraction is 0.005000.

5. The detector made 16 state transitions instead of the ideal two.

#### Worked case 4: noise_std = 12

This case keeps the nominal configuration except for noise_std=12. The full input is {"noise_std": 12.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| false positive fraction | 0.115 |
| false negative fraction | 0.03 |
| transition count | 46 |
| accuracy | 0.9275 |
| signal noise std N | 12 |

1. The labeled contact interval is one to three seconds with mean load 30 N.

2. Add Gaussian noise with sigma=12 N.

3. Enter contact at 15 N and leave at 5 N using a stateful threshold.

4. False-positive fraction is 0.115000; false-negative fraction is 0.030000.

5. The detector made 46 state transitions instead of the ideal two.

#### Worked case 5: noise_std = 20

This case keeps the nominal configuration except for noise_std=20. The full input is {"noise_std": 20.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| false positive fraction | 0.26 |
| false negative fraction | 0.11 |
| transition count | 92 |
| accuracy | 0.815 |
| signal noise std N | 20 |

1. The labeled contact interval is one to three seconds with mean load 30 N.

2. Add Gaussian noise with sigma=20 N.

3. Enter contact at 15 N and leave at 5 N using a stateful threshold.

4. False-positive fraction is 0.260000; false-negative fraction is 0.110000.

5. The detector made 92 state transitions instead of the ideal two.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Thresholds are teaching values; a real detector must be calibrated for sensor range, preload, bias and contact dynamics.

A stable contact flag does not prove no slip or a known contact wrench.

### K. Failure modes and troubleshooting

Treating a threshold flag as load measurement; choosing thresholds on the same trials used for final evaluation; ignoring sensor bias.

### L. Practical exercises and extension tasks

1. Compare with a single threshold and count chatter.

2. Add a minimum-duration debounce and measure latency.

3. Introduce slowly increasing preload and test failure behavior.

### M. Connection to the Asimov research platform

If physical force sensors are absent, contact estimation needs a separately validated model and uncertainty treatment.

### N. Completion record

Record your chosen case, predicted trend, measured false_positive_fraction, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 40, Zero-velocity updates, foot constraints and slip bias. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 40 - Zero-velocity updates, foot constraints and slip bias

### A. The engineering question

A stationary contacting foot supplies a useful constraint on body motion.

### B. Concepts and mathematical model

If the foot actually slips, enforcing zero velocity injects a biased pseudo-measurement into the estimator. This illustrates a broader sensor-fusion principle: a model-based constraint is only a valid measurement while its assumptions hold. The laboratory combines integrated acceleration with occasional zero-velocity corrections and then deliberately violates the stationary-contact assumption.

v_pred=v_prev+a*dt; contact correction v_next=(1-K)*v_pred+K*v_contact_assumed.

### C. Real-world meaning and limits

Physical base-velocity estimators must tolerate contact transitions and slipping surfaces before learned policies depend on them.

### D. Architecture and data flow

Configuration (slip_speed) -> numerical model -> constrained_rmse_m_s, unconstrained_rmse_m_s, slip_interval_bias_m_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

slip_speed is meters per second during the deliberately invalid contact-constraint interval.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| slip_speed | 0.05 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/40_zero_velocity.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only slip_speed changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/40_zero_velocity.py --case 0

.venv-book/bin/python expanded_lab/modules/40_zero_velocity.py --case 3

.venv-book/bin/python expanded_lab/run.py zero_velocity --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/40_zero_velocity.py

### H. Walkthrough and design decisions

Run an unconstrained integrator beside the constrained estimate to expose the tradeoff. The contact assumption is intentionally wrong during slip, allowing a controlled failure analysis.

### I. Expected behavior and six worked cases

The controlled variable is slip_speed. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/40_zero_velocity.png

Figure L40. constrained rmse m s as slip_speed changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | slip_speed | constrained rmse m s |
|---|---|---|
| 0 | 0 | 0.00308652 |
| 1 | 0.01 | 0.00459835 |
| 2 | 0.03 | 0.01541259 |
| 3 | 0.05 | 0.02667408 |
| 4 | 0.1 | 0.05498371 |
| 5 | 0.2 | 0.11169503 |

#### Worked case 0: slip_speed = 0

This case keeps the nominal configuration except for slip_speed=0. The full input is {"slip_speed": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| constrained rmse m s | 0.00308652 |
| unconstrained rmse m s | 0.06902091 |
| slip interval bias m s | 0.0030906 |
| final constrained error m s | 0.00509715 |

1. The synthetic foot/body velocity is 0 m/s during a two-second slip interval.

2. Acceleration measurement includes +0.02 m/s^2 bias and 0.01 m/s^2 noise.

3. Every 0.2 s, impose a strong zero-velocity pseudo-measurement regardless of actual slip.

4. Constrained RMSE is 0.003087 m/s; unconstrained RMSE is 0.069021 m/s.

5. Mean bias during slip is 0.003091 m/s.

#### Worked case 1: slip_speed = 0.01

This case keeps the nominal configuration except for slip_speed=0.01. The full input is {"slip_speed": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| constrained rmse m s | 0.00459835 |
| unconstrained rmse m s | 0.06901645 |
| slip interval bias m s | -0.0066844 |
| final constrained error m s | 0.00509715 |

1. The synthetic foot/body velocity is 0.01 m/s during a two-second slip interval.

2. Acceleration measurement includes +0.02 m/s^2 bias and 0.01 m/s^2 noise.

3. Every 0.2 s, impose a strong zero-velocity pseudo-measurement regardless of actual slip.

4. Constrained RMSE is 0.004598 m/s; unconstrained RMSE is 0.069016 m/s.

5. Mean bias during slip is -0.006684 m/s.

#### Worked case 2: slip_speed = 0.03

This case keeps the nominal configuration except for slip_speed=0.03. The full input is {"slip_speed": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| constrained rmse m s | 0.01541259 |
| unconstrained rmse m s | 0.06901115 |
| slip interval bias m s | -0.0262344 |
| final constrained error m s | 0.00509715 |

1. The synthetic foot/body velocity is 0.03 m/s during a two-second slip interval.

2. Acceleration measurement includes +0.02 m/s^2 bias and 0.01 m/s^2 noise.

3. Every 0.2 s, impose a strong zero-velocity pseudo-measurement regardless of actual slip.

4. Constrained RMSE is 0.015413 m/s; unconstrained RMSE is 0.069011 m/s.

5. Mean bias during slip is -0.026234 m/s.

#### Worked case 3: slip_speed = 0.05

This case keeps the nominal configuration except for slip_speed=0.05. The full input is {"slip_speed": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| constrained rmse m s | 0.02667408 |
| unconstrained rmse m s | 0.06901067 |
| slip interval bias m s | -0.0457844 |
| final constrained error m s | 0.00509714 |

1. The synthetic foot/body velocity is 0.05 m/s during a two-second slip interval.

2. Acceleration measurement includes +0.02 m/s^2 bias and 0.01 m/s^2 noise.

3. Every 0.2 s, impose a strong zero-velocity pseudo-measurement regardless of actual slip.

4. Constrained RMSE is 0.026674 m/s; unconstrained RMSE is 0.069011 m/s.

5. Mean bias during slip is -0.045784 m/s.

#### Worked case 4: slip_speed = 0.1

This case keeps the nominal configuration except for slip_speed=0.1. The full input is {"slip_speed": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| constrained rmse m s | 0.05498371 |
| unconstrained rmse m s | 0.06903062 |
| slip interval bias m s | -0.0946594 |
| final constrained error m s | 0.00509714 |

1. The synthetic foot/body velocity is 0.1 m/s during a two-second slip interval.

2. Acceleration measurement includes +0.02 m/s^2 bias and 0.01 m/s^2 noise.

3. Every 0.2 s, impose a strong zero-velocity pseudo-measurement regardless of actual slip.

4. Constrained RMSE is 0.054984 m/s; unconstrained RMSE is 0.069031 m/s.

5. Mean bias during slip is -0.094659 m/s.

#### Worked case 5: slip_speed = 0.2

This case keeps the nominal configuration except for slip_speed=0.2. The full input is {"slip_speed": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| constrained rmse m s | 0.11169503 |
| unconstrained rmse m s | 0.06916093 |
| slip interval bias m s | -0.1924094 |
| final constrained error m s | 0.00509713 |

1. The synthetic foot/body velocity is 0.2 m/s during a two-second slip interval.

2. Acceleration measurement includes +0.02 m/s^2 bias and 0.01 m/s^2 noise.

3. Every 0.2 s, impose a strong zero-velocity pseudo-measurement regardless of actual slip.

4. Constrained RMSE is 0.111695 m/s; unconstrained RMSE is 0.069161 m/s.

5. Mean bias during slip is -0.192409 m/s.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Zero-velocity constraints can reduce drift in valid stationary intervals and create systematic error during slip.

Use contact confidence, slip indicators and innovation checks rather than permanently enforcing the constraint.

### K. Failure modes and troubleshooting

Using foot contact as proof of zero world velocity; confusing a kinematic constraint with an independent sensor; hiding bias in a low covariance.

### L. Practical exercises and extension tasks

1. Gate corrections using an independent slip detector.

2. Add a bias state and compare observability in stationary and moving intervals.

3. Evaluate both drift reduction and slip-induced bias.

### M. Connection to the Asimov research platform

Physical base-velocity estimators must tolerate contact transitions and slipping surfaces before learned policies depend on them.

### N. Completion record

Record your chosen case, predicted trend, measured constrained_rmse_m_s, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 41, Typed joint-command contracts and rejection accounting. Keep the present result as a reference fixture for diagnosing changes in the larger stack.
