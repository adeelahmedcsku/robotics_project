# Reader's guide - From software experience to physical engineering
## The scope of the complete edition
This edition expands the original project manual into a textbook and laboratory reference. The first five parts establish the Asimov project, its source audit, the runnable simulation and the staged physical-build process. Parts VI-XII then develop the mathematics, mechanics, control, estimation, software interfaces, learning and physical engineering in 70 detailed numerical laboratories. Each laboratory has six executed worked cases, a complete standalone program, a controlled parameter study, a graph, validation reasoning and extension exercises.

The 420 worked cases are not 420 successful robot behaviors. They are controlled calculations and synthetic experiments used to understand individual engineering relationships. Some deliberately violate assumptions, miss targets, saturate a controller, expose stale data or produce a negative feasibility margin. Those are useful results when clearly identified. A complete book should teach you how to recognize and explain failure rather than report every calculation as a success.

Read the original practical lessons as the project spine. Use the extended laboratories before implementing the corresponding idea in the humanoid. For example, complete the rotation and transform studies before editing an IMU mounting transform, the feedback and delay studies before changing controller gains, and the observation-schema/replay studies before exporting a policy. The physical-engineering studies help you assess procurement and test plans; their invented numerical values are not specifications for a real robot.

### What the additional depth changes
The earlier compact guide told you where a Jacobian belongs in the architecture. This edition also asks you to derive a two-link Jacobian, compare analytic and finite-difference columns, inspect singular values, quantify regularization tradeoffs and reject a misleading inverse solution. The same pattern applies across the curriculum: define the quantity, build an independent check, vary one assumption, measure its effect and decide where the model stops being credible.

The publication uses a conventional 7-by-10-inch technical-book page with readable body typography and separate code typography. Chapters and figures are arranged for reading and reference. Page count is verified after compilation; blank leaves, repeated prompt text and enlarged spacing are not used to meet the length requirement. Repeated equations appear only where a worked calculation needs them, while common tooling is introduced once.

## A practical study sequence
| Stage | Read and run | Evidence to retain |
|---|---|---|
| Orientation | Project architecture, source audit, environment setup | Workstation inventory and pinned model identity |
| Mathematical foundations | Laboratories 1-10 | Units, transform round trips, derivative residuals, sampling and uncertainty studies |
| Mechanical reasoning | Laboratories 11-20 | Mass/inertia checks, load budgets, IK reachability and contact-feasibility results |
| First robot motion | Practical simulation and joint-control lessons | Headless test results, viewer inspection, named-joint telemetry |
| Feedback and constraints | Laboratories 21-30 | Tracking, saturation, delay, thermal and power analyses |
| Sensing and estimation | Laboratories 31-40 | Calibration, time alignment, filter error and assumption-failure reports |
| Modular software | ROS practical lesson and Laboratories 41-50 | Message rejection, activation, age, replay and fault tests |
| Learning and perception | RL/perception practical lessons and Laboratories 51-60 | Environment checks, held-out results, policy contract and skill approval tests |
| Physical planning | Procurement/commissioning practical lessons and Laboratories 61-70 | Complete quotes, design reviews, measured calibration and actual commissioning records |
| Integration | Supported simulation demo, then commissioned physical skill | Traceable observation-to-command evidence and tested rollback |

The ordering is deliberately revisitable. You do not need to finish every mathematical extension before seeing the first simulator window. You do need to understand a quantity before relying on it to authorize physical motion. Keep simulation experiments, offline numerical studies and actual hardware tests in distinct result folders.

### Suggested effort and pacing
A small numerical laboratory can take one to three focused sessions if you read the equation, predict two cases by hand, execute all six, inspect the code and complete one extension. Some topics, such as covariance calibration or contact-constrained estimation, may take longer. These estimates are study planning assumptions; your actual pace depends on mathematics background and the depth of the extensions you choose.

The project is better measured by completed evidence gates than by pages read. A week spent finding a frame-sign error can be more productive than a week of copying several advanced algorithms that remain untested. Maintain a short experiment journal with one hypothesis per entry. Explain what result would disprove the hypothesis before running the test.

## How to read a worked numerical case
Start with the parameter contract. Identify which values are physical quantities, which are numerical settings and which are artificial assumptions. Check units before evaluating the equation. Then inspect the output metrics, including unfavorable ones. A large positive power peak can matter even when net energy is small; a small fit residual can coexist with biased calibration; a zero fall rate is meaningless if the base is fixed.

Next follow the numbered derivation. It reports intermediate values produced by the same explicit model so you can locate the first disagreement. Independently reproduce at least one intermediate quantity with a calculator or a short separate script. Independence matters: copying the same wrong formula into both implementation and test does not create strong verification.

Finally ask what would change on the physical robot. Would the input become a noisy sensor estimate? Would a timestamp come from another clock? Would a motor map through a parallel linkage? Would a force be limited by friction, current or temperature? The connection section names the missing evidence rather than silently assuming the numerical model is a physical specification.

### Predict, execute, explain
For the first and last cases in each sweep, predict the direction of change before running the program. State the reason using the equation. For example, gear-reflected inertia grows with the square of the ratio, cable heating grows with the square of current in a fixed-resistance model, and first-order stereo depth uncertainty grows with the square of range under fixed focal length and disparity noise.

A prediction can be wrong for a useful reason. Perhaps a nonlinear clipping boundary was crossed, an estimator changed its gain, a discrete timestep rounded a requested delay, or a previously active constraint became inactive. Record the reason. Do not smooth away these boundaries to make a graph look cleaner; they often define the engineering problem.

## Running the extended code
All extended modules are saved under /data/Robotics_Project/expanded_lab/modules/. They use NumPy and the Python standard library. The standalone programs accept a case index from zero to five and print parameters, metrics, derivation and interpretive notes as JSON. The catalog runner offers the same experiments by a stable short key and can execute all published cases in one command.
```bash
cd /data/Robotics_Project
.venv-book/bin/python expanded_lab/run.py list
.venv-book/bin/python expanded_lab/run.py units --case 0
.venv-book/bin/python expanded_lab/run.py test_all --output expanded_lab/results/recheck.json
```
The .venv-book path identifies the environment used on this task's host. A virtual environment is not a portable deliverable across operating systems, Python installations or machines. On another machine, create the Lesson 0 environment and substitute its python command. The extended numerical laboratories need only the pinned NumPy baseline; simulator, ROS and learning dependencies are needed for their corresponding practical projects.

The results folder contains the executed JSON cases and the graphs included in the book. Those files are preparation evidence and regression fixtures. Recompute them after editing equations or assumptions. Keep the original results so a changed answer can be traced to a changed source rather than mistaken for an unexplained regression.

### Shared numerical runner
The runner is printed here once. Every individual laboratory also includes a standalone module, so you can inspect or run it without relying on dynamic catalog execution.
!code expanded_lab/run.py

## What numerical validation can establish
A transform round trip can establish consistency of a mathematical implementation. A finite-difference check can detect an analytic derivative error at tested configurations. A seeded simulation can establish repeatability of a stated model. None of these proves that a fabricated link has the modeled mass, that an IMU has the assumed timing or that a drive stops in the required time.

Use several kinds of evidence. Algebraic identities check internal consistency. Independent reference calculations check formulas. Synthetic ground truth checks estimation and metric definitions. Model-based simulation tests interaction. Bench measurements check actual interfaces and parameters. Protected physical trials check behavior within a reviewed envelope. Each level answers a different question and has a different scope.

The extended suite executes 420 published parameter cases and checks finite output. Many modules also contain explicit identities or invariant assertions. The accompanying semantic test suite checks cross-case behavior and known reference properties. These are software and numerical checks. They do not imply that every arbitrary edited input is valid or that any physical system has been commissioned.

## Managing evidence, changes and scope
Name each result with experiment, source identity, parameter configuration, seed and timestamp. Keep raw data separate from derived plots. If an explanation changes after looking at the result, preserve the original hypothesis and label the new one. This simple practice reduces the temptation to retrofit a story around a favorable number.

When a laboratory introduces a threshold, inspect its provenance. Some thresholds are mathematical boundaries, such as a raw inverse-kinematics cosine outside [-1,1]. Some are proposed exercise criteria, such as an error target for a supported simulated elbow. Others must come from approved physical data, such as voltage, current, temperature, connector and structural limits. Do not transfer a threshold from one category to another.

A change to joint ordering, observation normalization, camera extrinsics, a physical ankle mechanism or motor firmware can invalidate several downstream tests. Use the dependency/evidence studies to determine what must be repeated. Retain a known-good software bundle and a physically appropriate shutdown/rollback procedure. A robot under load must remain supported while a software release is reverted.

## The EUR 6,000 boundary
The robot budget remains EUR 6,000. You also mentioned a possible EUR 2,000-3,000 laptop purchase; it remains a separate optional budget decision unless you explicitly include it in the robot total. The existing Intel Core i7 and GeForce RTX system should be inventoried and benchmarked before buying another machine. No laptop model or future GPU capability is invented in this edition.

The book does not establish a complete self-source Asimov 1 within EUR 6,000. The source audit and procurement ledger explain the unresolved quotations and release dependencies. The later budget laboratory uses fictional allowances to teach arithmetic; those allowances do not replace the ledger or become supplier prices. A small supported module remains the practical staged physical scope until a compatible, complete landed-cost estimate is available.

## An honest final capability statement
At the end of the software work you should be able to load and inspect the actual pinned Asimov model, run bounded supported-joint trajectories, validate nearby position IK, analyze telemetry, train and evaluate a small supported learning task, export a policy artifact, test perception and execute a bounded simulated skill. Standing and walking remain research capabilities to earn through their own declared tests, not promises generated by including the relevant chapter.

For physical work, your first credible milestone is a release-matched, inspected, guarded and commissioned joint or small supported module. Its stopping behavior, feedback mapping, limits, calibration and power handling must be demonstrated on actual hardware. A full humanoid and unsupported locomotion require further verified design, funding and evidence. The point of the complete book is to equip you to make those engineering decisions independently.
