# Part X - Software interfaces, timing and supervisory control

Your software-engineering experience is directly useful here, but physical control gives ordinary interface bugs greater consequences. Message ordering, queue age, activation state, packet interpretation and preprocessing versions must be explicit. These laboratories test contracts with deliberate faults and expose the limits of software-only evidence. The fictional wire format is never a motor protocol; no chapter opens a CAN bus or enables a physical actuator.

## Laboratory 41 - Typed joint-command contracts and rejection accounting

### A. The engineering question

A valid JSON object is not necessarily a valid robot command.

### B. Concepts and mathematical model

A command contract must constrain joint names and order, vector length, numeric finiteness, units, range, sequence and age. Validation should occur before a command enters the controller's active state. Rejection counters make faults observable without turning malformed requests into motor motion. This experiment defines a small typed-like schema and injects different kinds of failures into a deterministic message stream.

accept = schema_ok and finite and limits_ok and sequence_new and 0<=age<=max_age.

### C. Real-world meaning and limits

Physical command validation must use the commissioned joint/motor mapping and remain subordinate to local watchdogs and isolation.

### D. Architecture and data flow

Configuration (invalid_fraction) -> numerical model -> accepted_count, rejected_count, rejection_fraction -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

invalid_fraction is the probability of an injected synthetic schema/age/range fault, not a measured network error rate.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| invalid_fraction | 0.1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/41_message_contracts.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only invalid_fraction changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/41_message_contracts.py --case 0

.venv-book/bin/python expanded_lab/modules/41_message_contracts.py --case 3

.venv-book/bin/python expanded_lab/run.py message_contracts --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/41_message_contracts.py

### H. Walkthrough and design decisions

Validation is side-effect free until success is known. The experiment records rejected categories and accepted sequence progression, illustrating observability around a strict boundary.

### I. Expected behavior and six worked cases

The controlled variable is invalid_fraction. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/41_message_contracts.png

Figure L41. accepted count as invalid_fraction changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | invalid_fraction | accepted count |
|---|---|---|
| 0 | 0 | 1000 |
| 1 | 0.01 | 988 |
| 2 | 0.05 | 957 |
| 3 | 0.1 | 908 |
| 4 | 0.25 | 774 |
| 5 | 0.5 | 518 |

#### Worked case 0: invalid_fraction = 0

This case keeps the nominal configuration except for invalid_fraction=0. The full input is {"invalid_fraction": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| accepted count | 1000 |
| rejected count | 0 |
| rejection fraction | 0 |
| last accepted sequence | 999 |

1. Generate 1000 commands at 50 Hz with corruption probability 0.

2. Corrupt name order, numeric finiteness, age or range in alternating injected cases.

3. Validate the entire candidate before updating last accepted sequence.

4. Accepted 1000 messages; rejected 0.

5. Rejection reasons are {'accepted': 1000}.

#### Worked case 1: invalid_fraction = 0.01

This case keeps the nominal configuration except for invalid_fraction=0.01. The full input is {"invalid_fraction": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| accepted count | 988 |
| rejected count | 12 |
| rejection fraction | 0.012 |
| last accepted sequence | 999 |

1. Generate 1000 commands at 50 Hz with corruption probability 0.01.

2. Corrupt name order, numeric finiteness, age or range in alternating injected cases.

3. Validate the entire candidate before updating last accepted sequence.

4. Accepted 988 messages; rejected 12.

5. Rejection reasons are {'accepted': 988, 'age': 4, 'names': 4, 'nonfinite': 2, 'range': 2}.

#### Worked case 2: invalid_fraction = 0.05

This case keeps the nominal configuration except for invalid_fraction=0.05. The full input is {"invalid_fraction": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| accepted count | 957 |
| rejected count | 43 |
| rejection fraction | 0.043 |
| last accepted sequence | 999 |

1. Generate 1000 commands at 50 Hz with corruption probability 0.05.

2. Corrupt name order, numeric finiteness, age or range in alternating injected cases.

3. Validate the entire candidate before updating last accepted sequence.

4. Accepted 957 messages; rejected 43.

5. Rejection reasons are {'accepted': 957, 'age': 12, 'nonfinite': 15, 'range': 8, 'names': 8}.

#### Worked case 3: invalid_fraction = 0.1

This case keeps the nominal configuration except for invalid_fraction=0.1. The full input is {"invalid_fraction": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| accepted count | 908 |
| rejected count | 92 |
| rejection fraction | 0.092 |
| last accepted sequence | 999 |

1. Generate 1000 commands at 50 Hz with corruption probability 0.1.

2. Corrupt name order, numeric finiteness, age or range in alternating injected cases.

3. Validate the entire candidate before updating last accepted sequence.

4. Accepted 908 messages; rejected 92.

5. Rejection reasons are {'accepted': 908, 'nonfinite': 26, 'age': 26, 'range': 18, 'names': 22}.

#### Worked case 4: invalid_fraction = 0.25

This case keeps the nominal configuration except for invalid_fraction=0.25. The full input is {"invalid_fraction": 0.25}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| accepted count | 774 |
| rejected count | 226 |
| rejection fraction | 0.226 |
| last accepted sequence | 999 |

1. Generate 1000 commands at 50 Hz with corruption probability 0.25.

2. Corrupt name order, numeric finiteness, age or range in alternating injected cases.

3. Validate the entire candidate before updating last accepted sequence.

4. Accepted 774 messages; rejected 226.

5. Rejection reasons are {'accepted': 774, 'range': 57, 'age': 57, 'nonfinite': 59, 'names': 53}.

#### Worked case 5: invalid_fraction = 0.5

This case keeps the nominal configuration except for invalid_fraction=0.5. The full input is {"invalid_fraction": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| accepted count | 518 |
| rejected count | 482 |
| rejection fraction | 0.482 |
| last accepted sequence | 997 |

1. Generate 1000 commands at 50 Hz with corruption probability 0.5.

2. Corrupt name order, numeric finiteness, age or range in alternating injected cases.

3. Validate the entire candidate before updating last accepted sequence.

4. Accepted 518 messages; rejected 482.

5. Rejection reasons are {'accepted': 518, 'age': 115, 'range': 113, 'nonfinite': 126, 'names': 128}.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Rejected messages do not update the accepted sequence or active target in this contract example.

A production parser must also handle missing keys, malicious payload sizes, schema versions and transport authentication.

### K. Failure modes and troubleshooting

Coercing missing targets to zero; partially applying a vector before all fields pass; accepting reordered names because lengths match.

### L. Practical exercises and extension tasks

1. Add explicit schema version and unit fields.

2. Test duplicate and out-of-order sequences.

3. Apply an input-size limit before allocating a vector.

### M. Connection to the Asimov research platform

Physical command validation must use the commissioned joint/motor mapping and remain subordinate to local watchdogs and isolation.

### N. Completion record

Record your chosen case, predicted trend, measured accepted_count, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 42, Message queues, delivery policy and stale-command risk. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 42 - Message queues, delivery policy and stale-command risk

### A. The engineering question

A reliable queue can preserve every message while delivering commands too late to be useful.

### B. Concepts and mathematical model

A latest-value stream favors freshness but intentionally discards intermediate samples. Those are different tradeoffs for telemetry, trajectories and events. This experiment simulates a producer faster than its consumer and compares FIFO delivery with replacing pending state by the newest sample. It illustrates queue-age behavior without pretending to implement all DDS QoS semantics.

age_at_use = consumer_time - production_time; FIFO preserves history; latest-value keeps at most one pending state.

### C. Real-world meaning and limits

ROS QoS configuration must be paired with application-level age checks and control-specific command semantics.

### D. Architecture and data flow

Configuration (consumer_period) -> numerical model -> fifo_mean_age_s, fifo_max_age_s, latest_mean_age_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

consumer_period is seconds; producer period is fixed at 10 ms and experiment duration is five seconds.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| consumer_period | 0.02 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/42_queue_age.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only consumer_period changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/42_queue_age.py --case 0

.venv-book/bin/python expanded_lab/modules/42_queue_age.py --case 3

.venv-book/bin/python expanded_lab/run.py queue_age --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/42_queue_age.py

### H. Walkthrough and design decisions

Compute age at consumption, not at arrival. The FIFO backlog exposes overload that can be hidden by successful delivery acknowledgments.

### I. Expected behavior and six worked cases

The controlled variable is consumer_period. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/42_queue_age.png

Figure L42. fifo mean age s as consumer_period changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | consumer_period | fifo mean age s |
|---|---|---|
| 0 | 0.005 | 0 |
| 1 | 0.01 | 0 |
| 2 | 0.015 | 0.8325 |
| 3 | 0.02 | 1.245 |
| 4 | 0.05 | 1.98 |
| 5 | 0.1 | 2.205 |

#### Worked case 0: consumer_period = 0.005

This case keeps the nominal configuration except for consumer_period=0.005. The full input is {"consumer_period": 0.005}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fifo mean age s | 0 |
| fifo max age s | 0 |
| latest mean age s | 0.0025 |
| latest max age s | 0.005 |
| fifo backlog count | 0 |
| replaced arrivals count | 0 |

1. The producer emits state every 0.01 s.

2. The consumer processes one item every 0.005 s.

3. FIFO retains 0 pending messages after the five-second run.

4. FIFO maximum age is 0.000000 s; latest-value maximum age is 0.005000 s.

5. Latest-value replacement intentionally skips at least 0 intermediate arrivals in this schedule.

#### Worked case 1: consumer_period = 0.01

This case keeps the nominal configuration except for consumer_period=0.01. The full input is {"consumer_period": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fifo mean age s | 0 |
| fifo max age s | 0 |
| latest mean age s | 0 |
| latest max age s | 0 |
| fifo backlog count | 0 |
| replaced arrivals count | 0 |

1. The producer emits state every 0.01 s.

2. The consumer processes one item every 0.01 s.

3. FIFO retains 0 pending messages after the five-second run.

4. FIFO maximum age is 0.000000 s; latest-value maximum age is 0.000000 s.

5. Latest-value replacement intentionally skips at least 0 intermediate arrivals in this schedule.

#### Worked case 2: consumer_period = 0.015

This case keeps the nominal configuration except for consumer_period=0.015. The full input is {"consumer_period": 0.015}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fifo mean age s | 0.8325 |
| fifo max age s | 1.665 |
| latest mean age s | 0.0025 |
| latest max age s | 0.005 |
| fifo backlog count | 166 |
| replaced arrivals count | 166 |

1. The producer emits state every 0.01 s.

2. The consumer processes one item every 0.015 s.

3. FIFO retains 166 pending messages after the five-second run.

4. FIFO maximum age is 1.665000 s; latest-value maximum age is 0.005000 s.

5. Latest-value replacement intentionally skips at least 166 intermediate arrivals in this schedule.

#### Worked case 3: consumer_period = 0.02

This case keeps the nominal configuration except for consumer_period=0.02. The full input is {"consumer_period": 0.02}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fifo mean age s | 1.245 |
| fifo max age s | 2.49 |
| latest mean age s | 0 |
| latest max age s | 0 |
| fifo backlog count | 249 |
| replaced arrivals count | 249 |

1. The producer emits state every 0.01 s.

2. The consumer processes one item every 0.02 s.

3. FIFO retains 249 pending messages after the five-second run.

4. FIFO maximum age is 2.490000 s; latest-value maximum age is 0.000000 s.

5. Latest-value replacement intentionally skips at least 249 intermediate arrivals in this schedule.

#### Worked case 4: consumer_period = 0.05

This case keeps the nominal configuration except for consumer_period=0.05. The full input is {"consumer_period": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fifo mean age s | 1.98 |
| fifo max age s | 3.96 |
| latest mean age s | 6.5225603e-17 |
| latest max age s | 8.8817842e-16 |
| fifo backlog count | 396 |
| replaced arrivals count | 396 |

1. The producer emits state every 0.01 s.

2. The consumer processes one item every 0.05 s.

3. FIFO retains 396 pending messages after the five-second run.

4. FIFO maximum age is 3.960000 s; latest-value maximum age is 0.000000 s.

5. Latest-value replacement intentionally skips at least 396 intermediate arrivals in this schedule.

#### Worked case 5: consumer_period = 0.1

This case keeps the nominal configuration except for consumer_period=0.1. The full input is {"consumer_period": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fifo mean age s | 2.205 |
| fifo max age s | 4.41 |
| latest mean age s | 8.3266727e-17 |
| latest max age s | 8.8817842e-16 |
| fifo backlog count | 441 |
| replaced arrivals count | 441 |

1. The producer emits state every 0.01 s.

2. The consumer processes one item every 0.1 s.

3. FIFO retains 441 pending messages after the five-second run.

4. FIFO maximum age is 4.410000 s; latest-value maximum age is 0.000000 s.

5. Latest-value replacement intentionally skips at least 441 intermediate arrivals in this schedule.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

A trajectory is not always replaceable by its last point; choose semantics appropriate to the command type.

The simulation concerns queue policy only and does not reproduce packet loss, DDS discovery or actual ROS middleware timing.

### K. Failure modes and troubleshooting

Choosing reliable delivery as a substitute for deadlines; using deep queues for current-state commands; dropping events that require ordered processing.

### L. Practical exercises and extension tasks

1. Add a bounded FIFO depth and count dropped old messages.

2. Reject messages older than a declared deadline.

3. Model a buffered trajectory separately from a replaceable velocity target.

### M. Connection to the Asimov research platform

ROS QoS configuration must be paired with application-level age checks and control-specific command semantics.

### N. Completion record

Record your chosen case, predicted trend, measured fifo_mean_age_s, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 43, Lifecycle activation, preconditions and fault latching. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 43 - Lifecycle activation, preconditions and fault latching

### A. The engineering question

A robot process should not become motion-capable merely because it started.

### B. Concepts and mathematical model

Configuration, inactive readiness, active control, fault handling and shutdown are distinct states. A fault should normally require a deliberate recovery path rather than disappear when a healthy packet arrives. This laboratory implements a small supervisor state machine and injects failed preconditions, making activation authority explicit and testable.

configure: unconfigured->inactive; activate requires all readiness flags; fault: active->fault; recovery never directly resumes active motion.

### C. Real-world meaning and limits

Commissioning records, local embedded protection and independent stop behavior must support the activation decision.

### D. Architecture and data flow

Configuration (failed_readiness_probability) -> numerical model -> activation_count, blocked_count, fault_count -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

failed_readiness_probability controls independent simulated readiness flags; it is not an estimated physical reliability rate.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| failed_readiness_probability | 0.1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/43_lifecycle.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only failed_readiness_probability changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/43_lifecycle.py --case 0

.venv-book/bin/python expanded_lab/modules/43_lifecycle.py --case 3

.venv-book/bin/python expanded_lab/run.py lifecycle --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/43_lifecycle.py

### H. Walkthrough and design decisions

Keep transition logic separate from side effects such as enabling a drive. Test forbidden transitions as carefully as the happy path.

### I. Expected behavior and six worked cases

The controlled variable is failed_readiness_probability. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/43_lifecycle.png

Figure L43. activation count as failed_readiness_probability changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | failed_readiness_probability | activation count |
|---|---|---|
| 0 | 0 | 200 |
| 1 | 0.01 | 188 |
| 2 | 0.05 | 161 |
| 3 | 0.1 | 121 |
| 4 | 0.2 | 75 |
| 5 | 0.5 | 17 |

#### Worked case 0: failed_readiness_probability = 0

This case keeps the nominal configuration except for failed_readiness_probability=0. The full input is {"failed_readiness_probability": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| activation count | 200 |
| blocked count | 0 |
| fault count | 200 |
| automatic resume count | 0 |
| activation fraction | 1 |

1. Run 200 readiness trials with per-flag failure probability 0.

2. Configuration moves the supervisor to inactive; activation checks all four readiness flags.

3. Activate 200 trials and block 0.

4. Inject a fault into every active trial, then deliver a healthy packet.

5. Automatic active resumption count is 0; the assertion requires zero.

#### Worked case 1: failed_readiness_probability = 0.01

This case keeps the nominal configuration except for failed_readiness_probability=0.01. The full input is {"failed_readiness_probability": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| activation count | 188 |
| blocked count | 12 |
| fault count | 188 |
| automatic resume count | 0 |
| activation fraction | 0.94 |

1. Run 200 readiness trials with per-flag failure probability 0.01.

2. Configuration moves the supervisor to inactive; activation checks all four readiness flags.

3. Activate 188 trials and block 12.

4. Inject a fault into every active trial, then deliver a healthy packet.

5. Automatic active resumption count is 0; the assertion requires zero.

#### Worked case 2: failed_readiness_probability = 0.05

This case keeps the nominal configuration except for failed_readiness_probability=0.05. The full input is {"failed_readiness_probability": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| activation count | 161 |
| blocked count | 39 |
| fault count | 161 |
| automatic resume count | 0 |
| activation fraction | 0.805 |

1. Run 200 readiness trials with per-flag failure probability 0.05.

2. Configuration moves the supervisor to inactive; activation checks all four readiness flags.

3. Activate 161 trials and block 39.

4. Inject a fault into every active trial, then deliver a healthy packet.

5. Automatic active resumption count is 0; the assertion requires zero.

#### Worked case 3: failed_readiness_probability = 0.1

This case keeps the nominal configuration except for failed_readiness_probability=0.1. The full input is {"failed_readiness_probability": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| activation count | 121 |
| blocked count | 79 |
| fault count | 121 |
| automatic resume count | 0 |
| activation fraction | 0.605 |

1. Run 200 readiness trials with per-flag failure probability 0.1.

2. Configuration moves the supervisor to inactive; activation checks all four readiness flags.

3. Activate 121 trials and block 79.

4. Inject a fault into every active trial, then deliver a healthy packet.

5. Automatic active resumption count is 0; the assertion requires zero.

#### Worked case 4: failed_readiness_probability = 0.2

This case keeps the nominal configuration except for failed_readiness_probability=0.2. The full input is {"failed_readiness_probability": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| activation count | 75 |
| blocked count | 125 |
| fault count | 75 |
| automatic resume count | 0 |
| activation fraction | 0.375 |

1. Run 200 readiness trials with per-flag failure probability 0.2.

2. Configuration moves the supervisor to inactive; activation checks all four readiness flags.

3. Activate 75 trials and block 125.

4. Inject a fault into every active trial, then deliver a healthy packet.

5. Automatic active resumption count is 0; the assertion requires zero.

#### Worked case 5: failed_readiness_probability = 0.5

This case keeps the nominal configuration except for failed_readiness_probability=0.5. The full input is {"failed_readiness_probability": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| activation count | 17 |
| blocked count | 183 |
| fault count | 17 |
| automatic resume count | 0 |
| activation fraction | 0.085 |

1. Run 200 readiness trials with per-flag failure probability 0.5.

2. Configuration moves the supervisor to inactive; activation checks all four readiness flags.

3. Activate 17 trials and block 183.

4. Inject a fault into every active trial, then deliver a healthy packet.

5. Automatic active resumption count is 0; the assertion requires zero.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Readiness flags represent evidence that must exist outside this synthetic state machine.

A reset returns to inactive; a new reviewed activation is required before motion can resume.

### K. Failure modes and troubleshooting

Treating ROS node startup as hardware readiness; clearing a latched fault on fresh data; assuming a software state verifies physical isolation.

### L. Practical exercises and extension tasks

1. Add explicit evidence IDs to each readiness flag.

2. Enumerate every state/event pair and test allowed transitions.

3. Model emergency isolation separately from software inactive state.

### M. Connection to the Asimov research platform

Commissioning records, local embedded protection and independent stop behavior must support the activation decision.

### N. Completion record

Record your chosen case, predicted trend, measured activation_count, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 44, Multi-rate controllers, policy decimation and sample age. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 44 - Multi-rate controllers, policy decimation and sample age

### A. The engineering question

Robotics stacks use several update rates.

### B. Concepts and mathematical model

Fast actuator feedback, slower policy inference and still slower telemetry can coexist if their interfaces specify sample-and-hold behavior and allowed age. Confusing a decimated display rate with the feedback rate can degrade control silently. This laboratory schedules deterministic physics, control, policy and logging events from one integer tick counter, avoiding floating-point modulo tests on accumulated time.

event at tick k when k mod decimation=0; period=base_dt*decimation; held-action age=(k-last_policy_tick)*base_dt.

### C. Real-world meaning and limits

The physical controller must distinguish simulation clock, device sample clock and monotonic deadline clock.

### D. Architecture and data flow

Configuration (policy_decimation) -> numerical model -> policy_rate_Hz, maximum_held_action_age_s, mean_held_action_age_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

policy_decimation is an integer base-tick count; base step is 1 ms, control step 2 ms and telemetry step 100 ms.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| policy_decimation | 20 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/44_timing_schedule.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only policy_decimation changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/44_timing_schedule.py --case 0

.venv-book/bin/python expanded_lab/modules/44_timing_schedule.py --case 3

.venv-book/bin/python expanded_lab/run.py timing_schedule --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/44_timing_schedule.py

### H. Walkthrough and design decisions

Integer scheduling makes rate relationships reproducible. Track action age explicitly so the consumer can enforce a contract even when the producer rate changes.

### I. Expected behavior and six worked cases

The controlled variable is policy_decimation. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/44_timing_schedule.png

Figure L44. policy rate Hz as policy_decimation changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | policy_decimation | policy rate Hz |
|---|---|---|
| 0 | 2 | 500 |
| 1 | 5 | 200 |
| 2 | 10 | 100 |
| 3 | 20 | 50 |
| 4 | 50 | 20 |
| 5 | 100 | 10 |

#### Worked case 0: policy_decimation = 2

This case keeps the nominal configuration except for policy_decimation=2. The full input is {"policy_decimation": 2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy rate Hz | 500 |
| maximum held action age s | 0.001 |
| mean held action age s | 0.0005 |
| control updates | 2500 |
| policy updates | 2500 |
| telemetry updates | 50 |

1. Use 5000 base ticks at 0.001 s per tick.

2. Control runs every two ticks; policy runs every 2 ticks; telemetry every 100.

3. The policy rate is 500.000000 Hz.

4. The oldest held policy action reaches 0.001000 s before replacement.

5. Event counts are {'physics': 5000, 'control': 2500, 'policy': 2500, 'telemetry': 50}.

#### Worked case 1: policy_decimation = 5

This case keeps the nominal configuration except for policy_decimation=5. The full input is {"policy_decimation": 5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy rate Hz | 200 |
| maximum held action age s | 0.004 |
| mean held action age s | 0.002 |
| control updates | 2500 |
| policy updates | 1000 |
| telemetry updates | 50 |

1. Use 5000 base ticks at 0.001 s per tick.

2. Control runs every two ticks; policy runs every 5 ticks; telemetry every 100.

3. The policy rate is 200.000000 Hz.

4. The oldest held policy action reaches 0.004000 s before replacement.

5. Event counts are {'physics': 5000, 'control': 2500, 'policy': 1000, 'telemetry': 50}.

#### Worked case 2: policy_decimation = 10

This case keeps the nominal configuration except for policy_decimation=10. The full input is {"policy_decimation": 10}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy rate Hz | 100 |
| maximum held action age s | 0.009 |
| mean held action age s | 0.0045 |
| control updates | 2500 |
| policy updates | 500 |
| telemetry updates | 50 |

1. Use 5000 base ticks at 0.001 s per tick.

2. Control runs every two ticks; policy runs every 10 ticks; telemetry every 100.

3. The policy rate is 100.000000 Hz.

4. The oldest held policy action reaches 0.009000 s before replacement.

5. Event counts are {'physics': 5000, 'control': 2500, 'policy': 500, 'telemetry': 50}.

#### Worked case 3: policy_decimation = 20

This case keeps the nominal configuration except for policy_decimation=20. The full input is {"policy_decimation": 20}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy rate Hz | 50 |
| maximum held action age s | 0.019 |
| mean held action age s | 0.0095 |
| control updates | 2500 |
| policy updates | 250 |
| telemetry updates | 50 |

1. Use 5000 base ticks at 0.001 s per tick.

2. Control runs every two ticks; policy runs every 20 ticks; telemetry every 100.

3. The policy rate is 50.000000 Hz.

4. The oldest held policy action reaches 0.019000 s before replacement.

5. Event counts are {'physics': 5000, 'control': 2500, 'policy': 250, 'telemetry': 50}.

#### Worked case 4: policy_decimation = 50

This case keeps the nominal configuration except for policy_decimation=50. The full input is {"policy_decimation": 50}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy rate Hz | 20 |
| maximum held action age s | 0.049 |
| mean held action age s | 0.0245 |
| control updates | 2500 |
| policy updates | 100 |
| telemetry updates | 50 |

1. Use 5000 base ticks at 0.001 s per tick.

2. Control runs every two ticks; policy runs every 50 ticks; telemetry every 100.

3. The policy rate is 20.000000 Hz.

4. The oldest held policy action reaches 0.049000 s before replacement.

5. Event counts are {'physics': 5000, 'control': 2500, 'policy': 100, 'telemetry': 50}.

#### Worked case 5: policy_decimation = 100

This case keeps the nominal configuration except for policy_decimation=100. The full input is {"policy_decimation": 100}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy rate Hz | 10 |
| maximum held action age s | 0.099 |
| mean held action age s | 0.0495 |
| control updates | 2500 |
| policy updates | 50 |
| telemetry updates | 50 |

1. Use 5000 base ticks at 0.001 s per tick.

2. Control runs every two ticks; policy runs every 100 ticks; telemetry every 100.

3. The policy rate is 10.000000 Hz.

4. The oldest held policy action reaches 0.099000 s before replacement.

5. Event counts are {'physics': 5000, 'control': 2500, 'policy': 50, 'telemetry': 50}.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

This schedule is logical simulation time and assumes every computation completes before its deadline.

Wall-time execution still needs measured compute/transport budgets and an overrun response.

### K. Failure modes and troubleshooting

Using accumulated float time modulo a period; assuming nominal loop rates equal measured wall rates; forgetting action holds during missed inference.

### L. Practical exercises and extension tasks

1. Add an inference-overrun event and specify the held-action timeout.

2. Reschedule a 60 Hz camera on a 1 kHz tick using a fractional accumulator.

3. Record every producer/consumer sample age in a replay trace.

### M. Connection to the Asimov research platform

The physical controller must distinguish simulation clock, device sample clock and monotonic deadline clock.

### N. Completion record

Record your chosen case, predicted trend, measured policy_rate_Hz, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 45, CAN bandwidth screening without invented motor commands. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 45 - CAN bandwidth screening without invented motor commands

### A. The engineering question

A communication link has finite capacity, and payload bits are not the entire frame cost.

### B. Concepts and mathematical model

Arbitration, framing, acknowledgment, inter-frame spacing, bit stuffing and retransmission consume time. This laboratory uses an explicit assumed worst-case frame length to screen a bus budget. It does not define motor packet semantics or resolve the Asimov bus assignment. The purpose is to reject implausible update-rate plans before implementing a transport.

bus utilization = joints*frames_per_joint_per_cycle*cycle_rate*assumed_frame_bits/bitrate.

### C. Real-world meaning and limits

Obtain the exact actuator protocol and release-specific Asimov bus mapping before choosing bitrates or connecting a populated bus.

### D. Architecture and data flow

Configuration (joints, cycle_rate, frame_bits, bitrate, frames_per_joint) -> numerical model -> frames_per_second, required_bits_per_second, utilization_fraction -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

joints is actuator count on one hypothetical segment; frame_bits is an explicit total-wire-length assumption; bitrate is bits/s.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| joints | 6 | Defined by the explicit chapter model and parameter contract |
| cycle_rate | 500 | Defined by the explicit chapter model and parameter contract |
| frame_bits | 135 | Defined by the explicit chapter model and parameter contract |
| bitrate | 1.0000000e+06 | Defined by the explicit chapter model and parameter contract |
| frames_per_joint | 2 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/45_can_budget.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only cycle_rate changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/45_can_budget.py --case 0

.venv-book/bin/python expanded_lab/modules/45_can_budget.py --case 3

.venv-book/bin/python expanded_lab/run.py can_budget --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/45_can_budget.py

### H. Walkthrough and design decisions

Start from traffic semantics: one command plus one response gives a different budget from broadcast commands and asynchronous telemetry. Treat utilization above one as a mathematical impossibility, not a tuning issue.

### I. Expected behavior and six worked cases

The controlled variable is cycle_rate. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/45_can_budget.png

Figure L45. frames per second as cycle_rate changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | cycle_rate | frames per second |
|---|---|---|
| 0 | 50 | 600 |
| 1 | 100 | 1200 |
| 2 | 200 | 2400 |
| 3 | 300 | 3600 |
| 4 | 500 | 6000 |
| 5 | 1000 | 12000 |

#### Worked case 0: cycle_rate = 50

This case keeps the nominal configuration except for cycle_rate=50. The full input is {"bitrate": 1000000.0, "cycle_rate": 50.0, "frame_bits": 135.0, "frames_per_joint": 2.0, "joints": 6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| frames per second | 600 |
| required bits per second | 81000 |
| utilization fraction | 0.081 |
| one frame wire time us | 135 |
| minimum cycle wire time ms | 1.62 |

1. Plan 6 joints at 50 cycles/s with 2 frames per joint per cycle.

2. Frame demand is 600.000000 per second.

3. Assume 135 total wire bits per frame at 1e+06 bit/s.

4. Required wire throughput is 81000.000000 bit/s and utilization is 0.081000.

5. The minimum cycle wire time is 1.620000 ms before additional contention or error handling.

#### Worked case 1: cycle_rate = 100

This case keeps the nominal configuration except for cycle_rate=100. The full input is {"bitrate": 1000000.0, "cycle_rate": 100.0, "frame_bits": 135.0, "frames_per_joint": 2.0, "joints": 6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| frames per second | 1200 |
| required bits per second | 1.6200000e+05 |
| utilization fraction | 0.162 |
| one frame wire time us | 135 |
| minimum cycle wire time ms | 1.62 |

1. Plan 6 joints at 100 cycles/s with 2 frames per joint per cycle.

2. Frame demand is 1200.000000 per second.

3. Assume 135 total wire bits per frame at 1e+06 bit/s.

4. Required wire throughput is 162000.000000 bit/s and utilization is 0.162000.

5. The minimum cycle wire time is 1.620000 ms before additional contention or error handling.

#### Worked case 2: cycle_rate = 200

This case keeps the nominal configuration except for cycle_rate=200. The full input is {"bitrate": 1000000.0, "cycle_rate": 200.0, "frame_bits": 135.0, "frames_per_joint": 2.0, "joints": 6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| frames per second | 2400 |
| required bits per second | 3.2400000e+05 |
| utilization fraction | 0.324 |
| one frame wire time us | 135 |
| minimum cycle wire time ms | 1.62 |

1. Plan 6 joints at 200 cycles/s with 2 frames per joint per cycle.

2. Frame demand is 2400.000000 per second.

3. Assume 135 total wire bits per frame at 1e+06 bit/s.

4. Required wire throughput is 324000.000000 bit/s and utilization is 0.324000.

5. The minimum cycle wire time is 1.620000 ms before additional contention or error handling.

#### Worked case 3: cycle_rate = 300

This case keeps the nominal configuration except for cycle_rate=300. The full input is {"bitrate": 1000000.0, "cycle_rate": 300.0, "frame_bits": 135.0, "frames_per_joint": 2.0, "joints": 6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| frames per second | 3600 |
| required bits per second | 4.8600000e+05 |
| utilization fraction | 0.486 |
| one frame wire time us | 135 |
| minimum cycle wire time ms | 1.62 |

1. Plan 6 joints at 300 cycles/s with 2 frames per joint per cycle.

2. Frame demand is 3600.000000 per second.

3. Assume 135 total wire bits per frame at 1e+06 bit/s.

4. Required wire throughput is 486000.000000 bit/s and utilization is 0.486000.

5. The minimum cycle wire time is 1.620000 ms before additional contention or error handling.

#### Worked case 4: cycle_rate = 500

This case keeps the nominal configuration except for cycle_rate=500. The full input is {"bitrate": 1000000.0, "cycle_rate": 500.0, "frame_bits": 135.0, "frames_per_joint": 2.0, "joints": 6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| frames per second | 6000 |
| required bits per second | 8.1000000e+05 |
| utilization fraction | 0.81 |
| one frame wire time us | 135 |
| minimum cycle wire time ms | 1.62 |

1. Plan 6 joints at 500 cycles/s with 2 frames per joint per cycle.

2. Frame demand is 6000.000000 per second.

3. Assume 135 total wire bits per frame at 1e+06 bit/s.

4. Required wire throughput is 810000.000000 bit/s and utilization is 0.810000.

5. The minimum cycle wire time is 1.620000 ms before additional contention or error handling.

#### Worked case 5: cycle_rate = 1000

This case keeps the nominal configuration except for cycle_rate=1000. The full input is {"bitrate": 1000000.0, "cycle_rate": 1000.0, "frame_bits": 135.0, "frames_per_joint": 2.0, "joints": 6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| frames per second | 12000 |
| required bits per second | 1.6200000e+06 |
| utilization fraction | 1.62 |
| one frame wire time us | 135 |
| minimum cycle wire time ms | 1.62 |

1. Plan 6 joints at 1000 cycles/s with 2 frames per joint per cycle.

2. Frame demand is 12000.000000 per second.

3. Assume 135 total wire bits per frame at 1e+06 bit/s.

4. Required wire throughput is 1620000.000000 bit/s and utilization is 1.620000.

5. The minimum cycle wire time is 1.620000 ms before additional contention or error handling.

The budget exceeds nominal bus capacity and is infeasible under these assumptions.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Nominal capacity is not exceeded, but margin and worst-case latency still need analysis.

The assumed frame length is a teaching budget input; confirm the actual bus generation, protocol and traffic pattern.

### K. Failure modes and troubleshooting

Counting only the eight-byte payload; ignoring response traffic and retransmissions; assuming all published interfaces share one bus.

### L. Practical exercises and extension tasks

1. Allocate traffic across two confirmed independent buses and compare.

2. Add periodic diagnostic frames and reserved fault traffic.

3. Analyze worst-case response age under arbitration priorities.

### M. Connection to the Asimov research platform

Obtain the exact actuator protocol and release-specific Asimov bus mapping before choosing bitrates or connecting a populated bus.

### N. Completion record

Record your chosen case, predicted trend, measured frames_per_second, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 46, A synthetic packet codec and corruption tests. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 46 - A synthetic packet codec and corruption tests

### A. The engineering question

Binary protocols need an explicit wire contract: field order, byte order, numeric representation, version, length and integrity checks.

### B. Concepts and mathematical model

A successful unpack operation does not prove the values are safe. This laboratory defines a fictional teaching packet carrying one target and sequence number, then corrupts random bytes to test CRC-based rejection. It is deliberately incompatible with real actuators and must never be transmitted to them.

packet = magic + version + sequence + float target + CRC16(payload); validate length, magic, CRC, finiteness and range.

### C. Real-world meaning and limits

Implement real motor encoding only from confirmed manufacturer protocol documentation, with inhibited-output tests and reviewed configuration.

### D. Architecture and data flow

Configuration (target) -> numerical model -> packet_bytes, target_roundtrip_error_rad, single_bit_faults_rejected -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

target is a fictional joint angle in radians; sequence, magic, version and CRC format are fixed by this exercise only.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| target | 0.1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/46_packet_codec.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only target changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/46_packet_codec.py --case 0

.venv-book/bin/python expanded_lab/modules/46_packet_codec.py --case 3

.venv-book/bin/python expanded_lab/run.py packet_codec --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/46_packet_codec.py

### H. Walkthrough and design decisions

Separate codec integrity from application validity. Length and CRC are checked before interpreting fields; numerical range and schema checks occur after unpacking.

### I. Expected behavior and six worked cases

The controlled variable is target. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/46_packet_codec.png

Figure L46. packet bytes as target changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | target | packet bytes |
|---|---|---|
| 0 | -0.4 | 13 |
| 1 | -0.1 | 13 |
| 2 | 0 | 13 |
| 3 | 0.1 | 13 |
| 4 | 0.25 | 13 |
| 5 | 0.4 | 13 |

#### Worked case 0: target = -0.4

This case keeps the nominal configuration except for target=-0.4. The full input is {"target": -0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| packet bytes | 13 |
| target roundtrip error rad | 5.9604645e-09 |
| single bit faults rejected | 500 |
| rejection fraction | 1 |

1. Encode sequence 7 and target -0.4 rad with explicit little-endian fields.

2. The complete fictional packet occupies 13 bytes.

3. Float32 round-trip error is 5.960464455e-09 rad.

4. Inject 500 random single-bit corruptions across payload and checksum.

5. Reject 500 corrupted packets; no physical transport exists.

#### Worked case 1: target = -0.1

This case keeps the nominal configuration except for target=-0.1. The full input is {"target": -0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| packet bytes | 13 |
| target roundtrip error rad | 1.4901161e-09 |
| single bit faults rejected | 500 |
| rejection fraction | 1 |

1. Encode sequence 7 and target -0.1 rad with explicit little-endian fields.

2. The complete fictional packet occupies 13 bytes.

3. Float32 round-trip error is 1.490116114e-09 rad.

4. Inject 500 random single-bit corruptions across payload and checksum.

5. Reject 500 corrupted packets; no physical transport exists.

#### Worked case 2: target = 0

This case keeps the nominal configuration except for target=0. The full input is {"target": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| packet bytes | 13 |
| target roundtrip error rad | 0 |
| single bit faults rejected | 500 |
| rejection fraction | 1 |

1. Encode sequence 7 and target 0 rad with explicit little-endian fields.

2. The complete fictional packet occupies 13 bytes.

3. Float32 round-trip error is 0.000000000e+00 rad.

4. Inject 500 random single-bit corruptions across payload and checksum.

5. Reject 500 corrupted packets; no physical transport exists.

#### Worked case 3: target = 0.1

This case keeps the nominal configuration except for target=0.1. The full input is {"target": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| packet bytes | 13 |
| target roundtrip error rad | 1.4901161e-09 |
| single bit faults rejected | 500 |
| rejection fraction | 1 |

1. Encode sequence 7 and target 0.1 rad with explicit little-endian fields.

2. The complete fictional packet occupies 13 bytes.

3. Float32 round-trip error is 1.490116114e-09 rad.

4. Inject 500 random single-bit corruptions across payload and checksum.

5. Reject 500 corrupted packets; no physical transport exists.

#### Worked case 4: target = 0.25

This case keeps the nominal configuration except for target=0.25. The full input is {"target": 0.25}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| packet bytes | 13 |
| target roundtrip error rad | 0 |
| single bit faults rejected | 500 |
| rejection fraction | 1 |

1. Encode sequence 7 and target 0.25 rad with explicit little-endian fields.

2. The complete fictional packet occupies 13 bytes.

3. Float32 round-trip error is 0.000000000e+00 rad.

4. Inject 500 random single-bit corruptions across payload and checksum.

5. Reject 500 corrupted packets; no physical transport exists.

#### Worked case 5: target = 0.4

This case keeps the nominal configuration except for target=0.4. The full input is {"target": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| packet bytes | 13 |
| target roundtrip error rad | 5.9604645e-09 |
| single bit faults rejected | 500 |
| rejection fraction | 1 |

1. Encode sequence 7 and target 0.4 rad with explicit little-endian fields.

2. The complete fictional packet occupies 13 bytes.

3. Float32 round-trip error is 5.960464455e-09 rad.

4. Inject 500 random single-bit corruptions across payload and checksum.

5. Reject 500 corrupted packets; no physical transport exists.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

CRC detects accidental corruption; it is not authentication or a defense against a deliberate sender.

This CRC and packet layout are teaching choices, not the CAN wire format or Asimov motor protocol.

### K. Failure modes and troubleshooting

Assuming a checksum authenticates a sender; relying on native byte order; sending an educational packet to real hardware.

### L. Practical exercises and extension tasks

1. Add a unit field and reject a mismatched unit.

2. Test truncated, appended and invalid-version packets.

3. Design replay protection independently of CRC.

### M. Connection to the Asimov research platform

Implement real motor encoding only from confirmed manufacturer protocol documentation, with inhibited-output tests and reviewed configuration.

### N. Completion record

Record your chosen case, predicted trend, measured packet_bytes, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 47, Observation ordering, normalization and schema hashes. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 47 - Observation ordering, normalization and schema hashes

### A. The engineering question

A learned policy sees an ordered vector, not a collection of semantically labeled Python variables.

### B. Concepts and mathematical model

Reordering two fields can produce plausible finite numbers and completely wrong actions. Normalization is also part of the policy interface and must be frozen for deployment. A schema hash can identify the ordered names and units, but only if the entire preprocessing contract is included. This laboratory demonstrates a silent ordering error and validates a canonical schema representation.

z_i=(x_i-mean_i)/std_i; policy_input order is part of the model; hash=SHA256(canonical schema bytes).

### C. Real-world meaning and limits

Hardware estimators must supply the same units, frames, order, timing and normalization used in policy training.

### D. Architecture and data flow

Configuration (gyro_offset) -> numerical model -> reference_action, correct_action, reordered_action -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

gyro_offset is an added angular-rate offset in rad/s; all normalized fields follow the explicitly named ordered schema.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| gyro_offset | 0 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/47_observation_schema.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only gyro_offset changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/47_observation_schema.py --case 0

.venv-book/bin/python expanded_lab/modules/47_observation_schema.py --case 3

.venv-book/bin/python expanded_lab/run.py observation_schema --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/47_observation_schema.py

### H. Walkthrough and design decisions

The reference linear actor is deliberately simple so the action difference can be traced exactly to preprocessing. Canonical serialization avoids hashes changing with dictionary formatting alone.

### I. Expected behavior and six worked cases

The controlled variable is gyro_offset. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/47_observation_schema.png

Figure L47. reference action as gyro_offset changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | gyro_offset | reference action |
|---|---|---|
| 0 | -0.2 | 0.4 |
| 1 | -0.1 | 0.4 |
| 2 | 0 | 0.4 |
| 3 | 0.1 | 0.4 |
| 4 | 0.2 | 0.4 |
| 5 | 0.5 | 0.4 |

#### Worked case 0: gyro_offset = -0.2

This case keeps the nominal configuration except for gyro_offset=-0.2. The full input is {"gyro_offset": -0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reference action | 0.4 |
| correct action | 0.3 |
| reordered action | 0.33 |
| reordering action error | 0.03 |
| normalized gyro | 1 |

1. Ordered fields are ['elbow_rad', 'knee_rad', 'gyro_rad_s'].

2. Means are [0.0, 0.0, 0.1] and standard deviations are [0.5, 0.5, 0.2].

3. Apply gyro offset -0.2 rad/s and normalize in the declared order.

4. Correct action is 0.300000; a silent field swap produces 0.330000.

5. Canonical schema SHA256 is 170b1c90844d3b85720078bbb063de561268d6bed4cf43601e2269735f9c48f8.

#### Worked case 1: gyro_offset = -0.1

This case keeps the nominal configuration except for gyro_offset=-0.1. The full input is {"gyro_offset": -0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reference action | 0.4 |
| correct action | 0.35 |
| reordered action | 0.41 |
| reordering action error | 0.06 |
| normalized gyro | 1.5 |

1. Ordered fields are ['elbow_rad', 'knee_rad', 'gyro_rad_s'].

2. Means are [0.0, 0.0, 0.1] and standard deviations are [0.5, 0.5, 0.2].

3. Apply gyro offset -0.1 rad/s and normalize in the declared order.

4. Correct action is 0.350000; a silent field swap produces 0.410000.

5. Canonical schema SHA256 is 170b1c90844d3b85720078bbb063de561268d6bed4cf43601e2269735f9c48f8.

#### Worked case 2: gyro_offset = 0

This case keeps the nominal configuration except for gyro_offset=0. The full input is {"gyro_offset": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reference action | 0.4 |
| correct action | 0.4 |
| reordered action | 0.49 |
| reordering action error | 0.09 |
| normalized gyro | 2 |

1. Ordered fields are ['elbow_rad', 'knee_rad', 'gyro_rad_s'].

2. Means are [0.0, 0.0, 0.1] and standard deviations are [0.5, 0.5, 0.2].

3. Apply gyro offset 0 rad/s and normalize in the declared order.

4. Correct action is 0.400000; a silent field swap produces 0.490000.

5. Canonical schema SHA256 is 170b1c90844d3b85720078bbb063de561268d6bed4cf43601e2269735f9c48f8.

#### Worked case 3: gyro_offset = 0.1

This case keeps the nominal configuration except for gyro_offset=0.1. The full input is {"gyro_offset": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reference action | 0.4 |
| correct action | 0.45 |
| reordered action | 0.57 |
| reordering action error | 0.12 |
| normalized gyro | 2.5 |

1. Ordered fields are ['elbow_rad', 'knee_rad', 'gyro_rad_s'].

2. Means are [0.0, 0.0, 0.1] and standard deviations are [0.5, 0.5, 0.2].

3. Apply gyro offset 0.1 rad/s and normalize in the declared order.

4. Correct action is 0.450000; a silent field swap produces 0.570000.

5. Canonical schema SHA256 is 170b1c90844d3b85720078bbb063de561268d6bed4cf43601e2269735f9c48f8.

#### Worked case 4: gyro_offset = 0.2

This case keeps the nominal configuration except for gyro_offset=0.2. The full input is {"gyro_offset": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reference action | 0.4 |
| correct action | 0.5 |
| reordered action | 0.65 |
| reordering action error | 0.15 |
| normalized gyro | 3 |

1. Ordered fields are ['elbow_rad', 'knee_rad', 'gyro_rad_s'].

2. Means are [0.0, 0.0, 0.1] and standard deviations are [0.5, 0.5, 0.2].

3. Apply gyro offset 0.2 rad/s and normalize in the declared order.

4. Correct action is 0.500000; a silent field swap produces 0.650000.

5. Canonical schema SHA256 is 170b1c90844d3b85720078bbb063de561268d6bed4cf43601e2269735f9c48f8.

#### Worked case 5: gyro_offset = 0.5

This case keeps the nominal configuration except for gyro_offset=0.5. The full input is {"gyro_offset": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| reference action | 0.4 |
| correct action | 0.65 |
| reordered action | 0.89 |
| reordering action error | 0.24 |
| normalized gyro | 4.5 |

1. Ordered fields are ['elbow_rad', 'knee_rad', 'gyro_rad_s'].

2. Means are [0.0, 0.0, 0.1] and standard deviations are [0.5, 0.5, 0.2].

3. Apply gyro offset 0.5 rad/s and normalize in the declared order.

4. Correct action is 0.650000; a silent field swap produces 0.890000.

5. Canonical schema SHA256 is 170b1c90844d3b85720078bbb063de561268d6bed4cf43601e2269735f9c48f8.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

A schema hash detects version mismatch only when both producer and consumer actually enforce it.

Include clipping, frame conventions, history stacking and action scaling in a real deployment contract.

### K. Failure modes and troubleshooting

Hashing unordered names without normalization; updating running statistics during evaluation; interpreting finite actions as evidence of correct semantics.

### L. Practical exercises and extension tasks

1. Add action scales and clipping to the schema hash.

2. Create a migration test for an added observation field.

3. Compare batched and single-observation preprocessing.

### M. Connection to the Asimov research platform

Hardware estimators must supply the same units, frames, order, timing and normalization used in policy training.

### N. Completion record

Record your chosen case, predicted trend, measured reference_action, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 48, Offline replay, action parity and fault localization. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 48 - Offline replay, action parity and fault localization

### A. The engineering question

Replay separates policy inference from the physical plant so interface changes can be investigated without motion.

### B. Concepts and mathematical model

A useful replay artifact includes ordered observations, timestamps, policy version, preprocessing state and expected actions. Comparing only a single zero input misses errors that appear in the operating distribution. This experiment uses a deterministic nonlinear actor and injects a preprocessing scale mismatch, then reports action disagreement over a dataset rather than one sample.

action=tanh(W*observation+b); parity metrics include maximum absolute error, RMSE and threshold-exceedance fraction.

### C. Real-world meaning and limits

Replay is a required intermediate step, but still must be followed by inhibited-output and supported physical validation.

### D. Architecture and data flow

Configuration (scale_error_factor) -> numerical model -> action_rmse, maximum_absolute_action_error, mismatch_fraction -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

scale_error_factor multiplies one candidate observation channel; one is the intentionally matching baseline.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| scale_error_factor | 1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/48_replay.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only scale_error_factor changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/48_replay.py --case 0

.venv-book/bin/python expanded_lab/modules/48_replay.py --case 3

.venv-book/bin/python expanded_lab/run.py replay --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/48_replay.py

### H. Walkthrough and design decisions

Keep the actor identical while changing only preprocessing. Dataset-level metrics locate the regression before any controller or hardware backend is involved.

### I. Expected behavior and six worked cases

The controlled variable is scale_error_factor. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/48_replay.png

Figure L48. action rmse as scale_error_factor changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | scale_error_factor | action rmse |
|---|---|---|
| 0 | 0.5 | 0.08955793 |
| 1 | 0.9 | 0.01731354 |
| 2 | 0.99 | 0.00171569 |
| 3 | 1 | 0 |
| 4 | 1.01 | 0.00171212 |
| 5 | 1.1 | 0.01695659 |

#### Worked case 0: scale_error_factor = 0.5

This case keeps the nominal configuration except for scale_error_factor=0.5. The full input is {"scale_error_factor": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| action rmse | 0.08955793 |
| maximum absolute action error | 0.45855058 |
| mismatch fraction | 1 |
| mean action magnitude | 0.34551997 |

1. Generate 1000 four-dimensional observations from a fixed seeded distribution.

2. The candidate preprocessing multiplies field 2 by 0.5.

3. Run the same tanh actor for reference and candidate pipelines.

4. Action RMSE is 0.08955793; maximum disagreement is 0.45855058.

5. Fraction exceeding 1e-5 action error is 1.000000.

#### Worked case 1: scale_error_factor = 0.9

This case keeps the nominal configuration except for scale_error_factor=0.9. The full input is {"scale_error_factor": 0.9}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| action rmse | 0.01731354 |
| maximum absolute action error | 0.09223477 |
| mismatch fraction | 1 |
| mean action magnitude | 0.34551997 |

1. Generate 1000 four-dimensional observations from a fixed seeded distribution.

2. The candidate preprocessing multiplies field 2 by 0.9.

3. Run the same tanh actor for reference and candidate pipelines.

4. Action RMSE is 0.01731354; maximum disagreement is 0.09223477.

5. Fraction exceeding 1e-5 action error is 1.000000.

#### Worked case 2: scale_error_factor = 0.99

This case keeps the nominal configuration except for scale_error_factor=0.99. The full input is {"scale_error_factor": 0.99}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| action rmse | 0.00171569 |
| maximum absolute action error | 0.00920524 |
| mismatch fraction | 0.994 |
| mean action magnitude | 0.34551997 |

1. Generate 1000 four-dimensional observations from a fixed seeded distribution.

2. The candidate preprocessing multiplies field 2 by 0.99.

3. Run the same tanh actor for reference and candidate pipelines.

4. Action RMSE is 0.00171569; maximum disagreement is 0.00920524.

5. Fraction exceeding 1e-5 action error is 0.994000.

#### Worked case 3: scale_error_factor = 1

This case keeps the nominal configuration except for scale_error_factor=1. The full input is {"scale_error_factor": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| action rmse | 0 |
| maximum absolute action error | 0 |
| mismatch fraction | 0 |
| mean action magnitude | 0.34551997 |

1. Generate 1000 four-dimensional observations from a fixed seeded distribution.

2. The candidate preprocessing multiplies field 2 by 1.

3. Run the same tanh actor for reference and candidate pipelines.

4. Action RMSE is 0.00000000; maximum disagreement is 0.00000000.

5. Fraction exceeding 1e-5 action error is 0.000000.

#### Worked case 4: scale_error_factor = 1.01

This case keeps the nominal configuration except for scale_error_factor=1.01. The full input is {"scale_error_factor": 1.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| action rmse | 0.00171212 |
| maximum absolute action error | 0.00919545 |
| mismatch fraction | 0.994 |
| mean action magnitude | 0.34551997 |

1. Generate 1000 four-dimensional observations from a fixed seeded distribution.

2. The candidate preprocessing multiplies field 2 by 1.01.

3. Run the same tanh actor for reference and candidate pipelines.

4. Action RMSE is 0.00171212; maximum disagreement is 0.00919545.

5. Fraction exceeding 1e-5 action error is 0.994000.

#### Worked case 5: scale_error_factor = 1.1

This case keeps the nominal configuration except for scale_error_factor=1.1. The full input is {"scale_error_factor": 1.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| action rmse | 0.01695659 |
| maximum absolute action error | 0.09126159 |
| mismatch fraction | 1 |
| mean action magnitude | 0.34551997 |

1. Generate 1000 four-dimensional observations from a fixed seeded distribution.

2. The candidate preprocessing multiplies field 2 by 1.1.

3. Run the same tanh actor for reference and candidate pipelines.

4. Action RMSE is 0.01695659; maximum disagreement is 0.09126159.

5. Fraction exceeding 1e-5 action error is 1.000000.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The replay distribution is synthetic; physical logs and edge cases must be included before deployment.

Exact inference parity does not validate the policy behavior or the physical actuator mapping.

### K. Failure modes and troubleshooting

Testing only zero observations; comparing unclipped exported actions with clipped framework outputs; using unrelated normalization checkpoints.

### L. Practical exercises and extension tasks

1. Add timestamp-based observation history and replay it exactly.

2. Compare float32 and float64 inference tolerances.

3. Inject a joint-name permutation and identify the affected action channels.

### M. Connection to the Asimov research platform

Replay is a required intermediate step, but still must be followed by inhibited-output and supported physical validation.

### N. Completion record

Record your chosen case, predicted trend, measured action_rmse, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 49, Ring buffers, bounded memory and time-window diagnostics. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 49 - Ring buffers, bounded memory and time-window diagnostics

### A. The engineering question

Long-running robot processes cannot retain every high-rate sample in an unbounded Python list.

### B. Concepts and mathematical model

A ring buffer bounds memory by overwriting old data, but that choice defines the available diagnostic horizon. Logging and visualization should consume copied snapshots without blocking the control loop. This laboratory implements a fixed-size numerical buffer and verifies wraparound, chronology and horizon as capacity changes.

write_index=total_samples mod capacity; chronological snapshot starts at the oldest retained index after wrap.

### C. Real-world meaning and limits

Telemetry transport and rendering must remain outside the timing-critical actuator path and expose dropped-sample counts.

### D. Architecture and data flow

Configuration (capacity) -> numerical model -> retained_samples, horizon_s, allocated_bytes -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

capacity is samples; three float64 columns store timestamp and two diagnostic signals at 500 Hz.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| capacity | 1000 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/49_telemetry_buffer.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only capacity changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/49_telemetry_buffer.py --case 0

.venv-book/bin/python expanded_lab/modules/49_telemetry_buffer.py --case 3

.venv-book/bin/python expanded_lab/run.py telemetry_buffer --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/49_telemetry_buffer.py

### H. Walkthrough and design decisions

The wrap index and chronological view are separate concerns. Copying the returned snapshot prevents a plot from reading values while the producer overwrites them.

### I. Expected behavior and six worked cases

The controlled variable is capacity. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/49_telemetry_buffer.png

Figure L49. retained samples as capacity changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | capacity | retained samples |
|---|---|---|
| 0 | 100 | 100 |
| 1 | 250 | 250 |
| 2 | 500 | 500 |
| 3 | 1000 | 1000 |
| 4 | 2000 | 2000 |
| 5 | 5000 | 5000 |

#### Worked case 0: capacity = 100

This case keeps the nominal configuration except for capacity=100. The full input is {"capacity": 100}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| retained samples | 100 |
| horizon s | 0.198 |
| allocated bytes | 2400 |
| oldest timestamp s | 9.8 |
| latest timestamp s | 9.998 |

1. Write 5000 samples at 500 Hz into capacity 100.

2. The allocated numerical storage is 2400 bytes.

3. After wrapping, retain 100 most recent samples.

4. Chronological snapshot runs from 9.800000 to 9.998000 s.

5. The retained diagnostic horizon is 0.198000 s.

#### Worked case 1: capacity = 250

This case keeps the nominal configuration except for capacity=250. The full input is {"capacity": 250}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| retained samples | 250 |
| horizon s | 0.498 |
| allocated bytes | 6000 |
| oldest timestamp s | 9.5 |
| latest timestamp s | 9.998 |

1. Write 5000 samples at 500 Hz into capacity 250.

2. The allocated numerical storage is 6000 bytes.

3. After wrapping, retain 250 most recent samples.

4. Chronological snapshot runs from 9.500000 to 9.998000 s.

5. The retained diagnostic horizon is 0.498000 s.

#### Worked case 2: capacity = 500

This case keeps the nominal configuration except for capacity=500. The full input is {"capacity": 500}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| retained samples | 500 |
| horizon s | 0.998 |
| allocated bytes | 12000 |
| oldest timestamp s | 9 |
| latest timestamp s | 9.998 |

1. Write 5000 samples at 500 Hz into capacity 500.

2. The allocated numerical storage is 12000 bytes.

3. After wrapping, retain 500 most recent samples.

4. Chronological snapshot runs from 9.000000 to 9.998000 s.

5. The retained diagnostic horizon is 0.998000 s.

#### Worked case 3: capacity = 1000

This case keeps the nominal configuration except for capacity=1000. The full input is {"capacity": 1000}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| retained samples | 1000 |
| horizon s | 1.998 |
| allocated bytes | 24000 |
| oldest timestamp s | 8 |
| latest timestamp s | 9.998 |

1. Write 5000 samples at 500 Hz into capacity 1000.

2. The allocated numerical storage is 24000 bytes.

3. After wrapping, retain 1000 most recent samples.

4. Chronological snapshot runs from 8.000000 to 9.998000 s.

5. The retained diagnostic horizon is 1.998000 s.

#### Worked case 4: capacity = 2000

This case keeps the nominal configuration except for capacity=2000. The full input is {"capacity": 2000}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| retained samples | 2000 |
| horizon s | 3.998 |
| allocated bytes | 48000 |
| oldest timestamp s | 6 |
| latest timestamp s | 9.998 |

1. Write 5000 samples at 500 Hz into capacity 2000.

2. The allocated numerical storage is 48000 bytes.

3. After wrapping, retain 2000 most recent samples.

4. Chronological snapshot runs from 6.000000 to 9.998000 s.

5. The retained diagnostic horizon is 3.998000 s.

#### Worked case 5: capacity = 5000

This case keeps the nominal configuration except for capacity=5000. The full input is {"capacity": 5000}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| retained samples | 5000 |
| horizon s | 9.998 |
| allocated bytes | 1.2000000e+05 |
| oldest timestamp s | 0 |
| latest timestamp s | 9.998 |

1. Write 5000 samples at 500 Hz into capacity 5000.

2. The allocated numerical storage is 120000 bytes.

3. After wrapping, retain 5000 most recent samples.

4. Chronological snapshot runs from 0.000000 to 9.998000 s.

5. The retained diagnostic horizon is 9.998000 s.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Memory accounting covers the array payload, not interpreter, transport or rendering overhead.

The example is single-threaded; concurrent producers/consumers require a reviewed synchronization or lock-free design.

### K. Failure modes and troubleshooting

Unbounded logging in a control process; plotting mutable array views; assuming bounded storage guarantees nonblocking disk writes.

### L. Practical exercises and extension tasks

1. Add a consumer that decimates by timestamp rather than index.

2. Define a disk-writer queue with a bounded drop policy.

3. Measure control-loop impact of snapshot copies.

### M. Connection to the Asimov research platform

Telemetry transport and rendering must remain outside the timing-critical actuator path and expose dropped-sample counts.

### N. Completion record

Record your chosen case, predicted trend, measured retained_samples, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 50, Fault persistence, debounce and explicit re-arming. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 50 - Fault persistence, debounce and explicit re-arming

### A. The engineering question

A single transient threshold crossing may be noise, while a persistent violation may require a stop.

### B. Concepts and mathematical model

Debounce trades false alarms against detection delay. After a real fault is latched, a return to normal measurements should not automatically re-enable motion. This laboratory injects both short spikes and a sustained thermal-like violation, then measures detection latency under different debounce durations. It distinguishes detection policy from the physical action that a real supervisor must execute.

consecutive_bad+=1 while violation; latch when consecutive_bad>=N; latched state persists until an explicit validated reset.

### C. Real-world meaning and limits

Physical fault responses depend on load support, stored energy and independent isolation; this numerical detector is not the protective system.

### D. Architecture and data flow

Configuration (debounce_seconds) -> numerical model -> required_bad_samples, first_latch_time_s, detection_latency_from_sustained_fault_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

debounce_seconds is the required persistence duration at a fixed 10 ms measurement interval.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| debounce_seconds | 0.05 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/50_fault_supervisor.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only debounce_seconds changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/50_fault_supervisor.py --case 0

.venv-book/bin/python expanded_lab/modules/50_fault_supervisor.py --case 3

.venv-book/bin/python expanded_lab/run.py fault_supervisor --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/50_fault_supervisor.py

### H. Walkthrough and design decisions

The fault latch changes only once, while the persistence counter can reset on healthy measurements. Early spikes deliberately expose the difference between nuisance rejection and delayed true detection.

### I. Expected behavior and six worked cases

The controlled variable is debounce_seconds. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/50_fault_supervisor.png

Figure L50. required bad samples as debounce_seconds changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | debounce_seconds | required bad samples |
|---|---|---|
| 0 | 0.01 | 1 |
| 1 | 0.02 | 2 |
| 2 | 0.03 | 3 |
| 3 | 0.05 | 5 |
| 4 | 0.1 | 10 |
| 5 | 0.2 | 20 |

#### Worked case 0: debounce_seconds = 0.01

This case keeps the nominal configuration except for debounce_seconds=0.01. The full input is {"debounce_seconds": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| required bad samples | 1 |
| first latch time s | 0.5 |
| detection latency from sustained fault s | -2.5 |
| false latch before fault | 1 |
| latched final | 1 |

1. At 100 Hz, debounce duration 0.01 s becomes 1 consecutive samples.

2. Inject a one-sample spike at 0.5 s and a two-sample spike at 1 s.

3. At 3 s, begin a sustained threshold violation.

4. First latched fault occurs at 0.5 s; early false-latch count is 1.

5. Relative to sustained-fault onset, reported latency is -2.500000 s; a negative value means an earlier spike already latched.

#### Worked case 1: debounce_seconds = 0.02

This case keeps the nominal configuration except for debounce_seconds=0.02. The full input is {"debounce_seconds": 0.02}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| required bad samples | 2 |
| first latch time s | 1.01 |
| detection latency from sustained fault s | -1.99 |
| false latch before fault | 1 |
| latched final | 1 |

1. At 100 Hz, debounce duration 0.02 s becomes 2 consecutive samples.

2. Inject a one-sample spike at 0.5 s and a two-sample spike at 1 s.

3. At 3 s, begin a sustained threshold violation.

4. First latched fault occurs at 1.01 s; early false-latch count is 1.

5. Relative to sustained-fault onset, reported latency is -1.990000 s; a negative value means an earlier spike already latched.

#### Worked case 2: debounce_seconds = 0.03

This case keeps the nominal configuration except for debounce_seconds=0.03. The full input is {"debounce_seconds": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| required bad samples | 3 |
| first latch time s | 3.02 |
| detection latency from sustained fault s | 0.02 |
| false latch before fault | 0 |
| latched final | 1 |

1. At 100 Hz, debounce duration 0.03 s becomes 3 consecutive samples.

2. Inject a one-sample spike at 0.5 s and a two-sample spike at 1 s.

3. At 3 s, begin a sustained threshold violation.

4. First latched fault occurs at 3.02 s; early false-latch count is 0.

5. Relative to sustained-fault onset, reported latency is 0.020000 s; a negative value means an earlier spike already latched.

#### Worked case 3: debounce_seconds = 0.05

This case keeps the nominal configuration except for debounce_seconds=0.05. The full input is {"debounce_seconds": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| required bad samples | 5 |
| first latch time s | 3.04 |
| detection latency from sustained fault s | 0.04 |
| false latch before fault | 0 |
| latched final | 1 |

1. At 100 Hz, debounce duration 0.05 s becomes 5 consecutive samples.

2. Inject a one-sample spike at 0.5 s and a two-sample spike at 1 s.

3. At 3 s, begin a sustained threshold violation.

4. First latched fault occurs at 3.04 s; early false-latch count is 0.

5. Relative to sustained-fault onset, reported latency is 0.040000 s; a negative value means an earlier spike already latched.

#### Worked case 4: debounce_seconds = 0.1

This case keeps the nominal configuration except for debounce_seconds=0.1. The full input is {"debounce_seconds": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| required bad samples | 10 |
| first latch time s | 3.09 |
| detection latency from sustained fault s | 0.09 |
| false latch before fault | 0 |
| latched final | 1 |

1. At 100 Hz, debounce duration 0.1 s becomes 10 consecutive samples.

2. Inject a one-sample spike at 0.5 s and a two-sample spike at 1 s.

3. At 3 s, begin a sustained threshold violation.

4. First latched fault occurs at 3.09 s; early false-latch count is 0.

5. Relative to sustained-fault onset, reported latency is 0.090000 s; a negative value means an earlier spike already latched.

#### Worked case 5: debounce_seconds = 0.2

This case keeps the nominal configuration except for debounce_seconds=0.2. The full input is {"debounce_seconds": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| required bad samples | 20 |
| first latch time s | 3.19 |
| detection latency from sustained fault s | 0.19 |
| false latch before fault | 0 |
| latched final | 1 |

1. At 100 Hz, debounce duration 0.2 s becomes 20 consecutive samples.

2. Inject a one-sample spike at 0.5 s and a two-sample spike at 1 s.

3. At 3 s, begin a sustained threshold violation.

4. First latched fault occurs at 3.19 s; early false-latch count is 0.

5. Relative to sustained-fault onset, reported latency is 0.190000 s; a negative value means an earlier spike already latched.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The temperature values and threshold are synthetic and do not specify a physical motor limit.

Detection delay must be included in the reviewed response envelope; debouncing every fault category identically is inappropriate.

### K. Failure modes and troubleshooting

Automatically clearing a fault on healthy data; debouncing an emergency input without design justification; ignoring total reaction travel during debounce.

### L. Practical exercises and extension tasks

1. Use different policies for stale feedback, overcurrent and thermal drift.

2. Add an explicit inactive reset state and prohibit direct active resumption.

3. Log the first triggering sample and pre-fault buffer.

### M. Connection to the Asimov research platform

Physical fault responses depend on load support, stored energy and independent isolation; this numerical detector is not the protective system.

### N. Completion record

Record your chosen case, predicted trend, measured required_bad_samples, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 51, Markov decision processes and discounted reward. Keep the present result as a reference fixture for diagnosing changes in the larger stack.
