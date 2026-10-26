# Part IV - From simulation evidence to physical hardware
## Lesson 10 - Sim-to-real contracts, identification and rollback
### A. Why this matters
Simulation supplies perfect state, immediate commands and simplified actuators. Physical systems have stale packets, flexible structures, thermal limits and changing batteries. Deployment begins by measuring these differences and making them explicit.
### B. Concepts explained simply
System identification estimates model parameters from experiments. Calibration aligns a measurement to a reference, such as encoder zero or camera geometry. Validation tests whether the calibrated model predicts new data. Domain randomization trains over a range of plausible parameters; it cannot excuse a completely wrong mechanism.

Compare a low-amplitude measured joint response against the simulator using the same sampled command. Fit only parameters the experiment can identify. For example, a static gravity test helps estimate load torque and offset but poorly identifies inertia. A slow reversal can reveal backlash or stiction; it is not a thermal test.
### C. Real-world relevance
Mass distribution, friction, cable forces, motor saturation, encoder quantization, transport delay, compliance, battery voltage and foot-ground contact all change performance. A policy relying on true base velocity cannot deploy until a usable estimator supplies that signal.
### D. Architecture
Simulation artifact -> schema and hash checks -> offline replay -> timing test -> hardware-in-the-loop with output inhibited -> single-joint fixture -> supported module -> protected whole body -> limited autonomous skill. Each stage has a separate go/no-go record.
### E. Prerequisites
Successful numerical tests, held-out policy evaluation if a learned policy is used, release-specific hardware documentation and a reviewed physical support/stop strategy. You can complete offline work before buying actuators.
### F. Step-by-step implementation
Create a deployment manifest with model/firmware/policy hashes, joint and motor orders, SI units, signed zeros, observation names, normalization constants, action scaling, controller frequency, maximum command age and fault response. Replay recorded observations through exported inference and compare with the training implementation.

Then test safety.py entirely offline. Its timestamps are supplied from one assumed monotonic clock; across hosts, redesign the protocol with measured clock synchronization, sequence handling and arrival-time constraints. Do not subtract unrelated host clocks and call the result latency.
```bash
python safety.py
python -m pytest -q tests/test_contracts.py
```
### G. Complete code
File: /data/Robotics_Project/humanoid_lab/safety.py
!code humanoid_lab/safety.py
### H. Code walkthrough
Gate validates timing, sequence, shape, finiteness, range and per-command step envelope. It latches a fault, so a subsequent healthy packet cannot silently resume motion. A deliberate, reviewed reset procedure is required outside this teaching class. The class is an offline exercise, not a complete protective control system.

The step-envelope comparison does not by itself measure actual speed, and a valid position target can still demand unsafe torque. Production supervision also needs measured speed/current/temperature/voltage, travel margin, rate and acceleration limits, estimator health, missed-deadline counters and independent stop authority. Failure handling must be appropriate for a loaded robot: blindly commanding zero torque can release a limb or collapse the machine.
### I. Expected result
A small valid target is accepted. An old packet raises a latched fault. No motor library is imported and no hardware output is possible.
### J. Validation
| Stage | Proposed go criteria | Rollback |
|---|---|---|
| Offline replay | Exact schema; eager/exported outputs agree on recorded dataset; no NaNs | Restore previous policy/config bundle |
| Timing under load | Measured worst-case inference plus transport fits reviewed deadline with margin | Reduce load or restore prior controller |
| HIL inhibited | Correct decoding, joint mapping, timeouts and fault state; output verified disabled | Disconnect transport and inspect logs |
| Single joint | Approved low-energy envelope, bounded tracking and stop response | Isolate power with load mechanically supported |
| Supported module | Repeatable low-speed trajectory; no thermal or deadline violations | Return to single joint and previous calibration |
| Whole-body support | Rig and stop tests passed; all local interfaces verified | Maintain support; isolate hazardous power |
| Physical skill | Repeated supervised trials within declared envelope | Disable skill; restore validated release |

Record the method used to prove output inhibition and the instrument used to measure timing. A software flag saying 'disabled' is not sufficient evidence of electrical isolation.
### K. Troubleshooting
Export mismatch often means normalization, action squashing, joint ordering or dtype changed. Good nominal timing with rare overruns requires stress tests and worst-case analysis. A policy that fails only after several minutes may be responding to thermal derating or voltage droop rather than perception.
### L. Practical exercise
Replay duplicated, delayed, out-of-order and future-stamped commands through Gate. Confirm all expected faults are recorded and remain latched. Add a schema version mismatch case.
### M. Connection to the physical Asimov 1
Ankle joint coordinates and motor A/B coordinates need a validated mechanism transform. Preserve power consistency: if joint rates equal J times motor rates, motor torques equal J transpose times joint torques under the ideal mapping. Do not reuse a small-angle approximation outside its verified range.
### N. Completion checklist
You have a manifest, reproducible replay, measured timing, explicit stops and rollback procedures, and no dependency on unavailable ground-truth channels. Hardware deployment remains no-go until its own gates pass.
### O. Next lesson preview
Convert an attractive platform into a complete, release-matched procurement decision.

## Lesson 11 - Build a defensible EUR 6,000 budget
### A. Why this matters
Actuator cost is only one part of a humanoid build. Fabrication, interfaces, tooling, protection, support, shipping and VAT can dominate the remaining budget. An unquoted line is an unknown liability, not zero euros.
### B. Concepts explained simply
A bill of materials is a quantity-controlled list tied to a release. A quotation states a supplier, item revision, price, tax basis, availability, shipping and validity period. A budget allowance is an internal spending cap. These are different documents.

Landed total = parts + fabrication + shipping + applicable taxes/duties + tools/protection + spares + contingency. Avoid adding VAT twice to VAT-inclusive EU prices. Treat optional computer upgrades separately until the budget owner confirms inclusion.
### C. Real-world relevance
Replacing a motor with a cheaper torque-equivalent part can change mounting, inertia, encoder semantics, protocol and thermal behavior. Compatibility is an engineering decision, not a price-filter checkbox.
### D. Architecture
Select hardware release -> extract part quantities -> obtain supplier quotes -> verify compatibility -> reconcile landed costs -> reserve contingency -> purchase one stage -> reforecast remaining stages.
### E. Prerequisites
Official BOM access, CAD revision, motor datasheets/protocols, firmware availability, existing tool inventory and a location suitable for a guarded fixture. The public material inspected here did not establish a complete purchasable EU BOM.
### F. Step-by-step implementation
Read the itemized CSV below, keep missing prices blank, and run the audit. It deliberately reports approved=false because a known subtotal is not a feasibility total.
```bash
python audit.py budget config/bom.csv
```
The actuator grouping is derived from the official module checklist: three EC-A6416-P2-25, four EC-A5013-H17-100, four EC-A3814-H14-107, four EC-A4315-P2-36 and ten EC-A4310-P2-36, totaling 25. This is a procurement grouping, not a protocol specification. [S13]

A directly opened BerryBase listing showed EUR 189.00 including VAT, excluding shipping, for a Raspberry Pi 5 8 GB on 25 October 2026. It is a dated price observation, not a reserved quote. Cooling, storage, power accessories and carrier boards are additional. The supplied CSV records this single verified price; all other unresolved costs remain explicit. [S14]
### G. Complete code and procurement ledger
File: /data/Robotics_Project/humanoid_lab/audit.py
!code humanoid_lab/audit.py
File: /data/Robotics_Project/humanoid_lab/config/bom.csv
!csv humanoid_lab/config/bom.csv
The CSV quantity '1' for an assembly set is a pending quote scope, not an assertion that the set contains one fastener or one bearing. Replace set rows with actual part-number rows before ordering. Motor drivers, encoders and IMUs may be integrated: reconcile them to prevent double counting.
### H. Code walkthrough
budget totals only explicitly priced quantities and reports every unquoted category. It never concludes that a robot fits a budget from a partial subtotal. commissioning uses a different path to evaluate recorded readiness; it does not verify physical tests independently.

Use priority P0 for required motion/protection dependencies, P1 for the selected research capability, and P2 for deferred expansion. Remove an optional battery from a bench stage only after choosing a suitable power/regen design; do not remove emergency isolation or support to create apparent savings.
### I. Expected result
The priced board subtotal is EUR 189.00, with many unquoted categories and no purchase approval. That honest result is more useful than a fabricated EUR 5,999 full-robot estimate.
### J. Validation and three scenarios
| Scenario | Technical scope | Financial conclusion |
|---|---|---|
| A: complete Asimov 1 | 25-actuator machine, structure, custom boards, matched firmware, rig and tools | Not established within EUR 6,000; published USD 20,000 kit does not fit |
| B: lower-body research | 12 actuators, pelvis, full safety/support, power and estimator | Unquoted; fewer joints do not prove affordability or safe locomotion |
| C: modular bench platform | One joint first, then a small supported limb or head/arm subset | Preferred staged scope; buy only after exact module quote and rig review |

For Scenario C, an illustrative allocation ceiling is: EUR 1,500 actuators/drives; EUR 700 mechanical work; EUR 600 bench power/protection; EUR 400 compute/CAN/sensing; EUR 700 fixture and barriers; EUR 450 tools; EUR 300 spares; EUR 450 shipping/tax adjustments; EUR 900 contingency. Total EUR 6,000. These are planning allowances, not supplier prices or proof that the selected Asimov module fits. If the first compatible actuator exceeds its allocation, reduce scope or revise the funding decision before ordering.

A lower-body pair uses two hip-pitch, two hip-roll, two hip-yaw, two knee and four ankle actuators. Obtain twelve release-matched motor quotes and fabrication estimates before considering Scenario B. A seated or bench arm can support perception/control research without claiming biped locomotion.
### K. Troubleshooting
A cheap listing may exclude the drive, encoder, shipping or tax. A STEP inventory does not encode all purchasing quantities. An available model number may ship with a different firmware. Quote validity and lead time matter as much as the price.
### L. Practical exercise
Obtain quotes for one exact motor, its required interface, compatible power/protection and one mounting fixture. Record manufacturer confirmation of firmware/protocol and mounting compatibility before comparing prices.
### M. Connection to the physical Asimov 1
Use the official release BOM and manufacturer confirmation to choose exact parts. EU electronics suppliers and fabrication bureaus are candidates for quotations; this edition does not assert stock or compatibility for unquoted items.
### N. Completion checklist
All required rows have quantities, exact specifications, tax basis, landed cost and compatibility evidence; contingency remains funded; and the selected stage stays below its approved ceiling. Until then, stay with simulation and procurement research.
### O. Next lesson preview
Inspect and fabricate mechanical parts using load paths and process constraints.

## Lesson 12 - Mechanical design, fabrication and incremental assembly
### A. Why this matters
The model assumes rigid links and known axes. Poor fit, weak layer orientation or a misaligned bearing changes those assumptions and may create a failure under load.
### B. Concepts explained simply
STEP describes solid geometry suitable for engineering exchange. STL describes a triangle surface and normally carries neither a trustworthy unit declaration nor manufacturing tolerances. A pretty mesh is not a complete manufacturing drawing.

A load path traces force through joints, bearings, fasteners and structure into the support. A 2 kg mass at a 0.2 m lever arm produces about 3.92 Nm of static gravity torque before acceleration or impacts. An illustrative 10 Nm torque applied through a 0.05 m lever corresponds to 200 N. Those simple calculations help identify where detailed analysis is needed, but do not size a human-safe support rig.
### C. Real-world relevance
Fastener preload, bearing fits, shaft alignment and cyclic fatigue affect service life. A cable crossing a joint can apply unmodeled torque or be cut by a moving edge.
### D. Architecture
Released CAD and drawings -> process/material specification -> load and fit review -> first article -> dimensional inspection -> unpowered assembly -> guarded joint test -> limb -> torso integration.
### E. Prerequisites
Exact release documents, competent mechanical review for load-bearing parts and rig, suitable metrology, a parts traveler and a de-energized work area. Never infer a tightening torque from the bolt diameter alone; material, grade, lubrication and joint design matter.
### F. Step-by-step implementation
1. Inventory the selected module's released part numbers, drawing revisions and required quantities.
2. Trace gravity, acceleration and stop loads through the module and its fixture. Review bending, bearing and fastener loads.
3. Identify every fit and datum from drawings. Confirm units with a known dimension before exporting STL or ordering machining.
4. Fabricate one first article. Measure critical holes, bearing seats, flatness and mating distances before ordering the rest.
5. Dry-assemble unpowered. Confirm free movement, alignment, cable clearance, end stops and access for service.
6. Apply only documented assembly practices, lubrication and fastener treatments. Record torque tool identity and inspection results.
7. Reinspect after the first guarded motion and thermal cycle before expanding to a limb.
### G. Complete inspection program
This lesson's executable artifact checks a simple dimensional traveler. Numerical tolerances below are examples of a file format, not approved Asimov tolerances.
```python
# /data/Robotics_Project/humanoid_lab/inspect_parts.py
import csv
import sys

def inspect(path):
    failures=[]
    for row in csv.DictReader(open(path, newline='')):
        value=float(row['measured_mm'])
        lo, hi=float(row['min_mm']), float(row['max_mm'])
        if not lo <= value <= hi:
            failures.append(row['part']+':'+row['feature'])
    return failures

if __name__ == '__main__':
    failed=inspect(sys.argv[1])
    print('FAILED FEATURES:', failed)
    raise SystemExit(bool(failed))
```
CSV header: part,feature,min_mm,max_mm,measured_mm. Populate its bounds from the approved drawing, never from an illustrative tutorial number.
### H. Walkthrough and material choices
The program compares measured dimensions to released bounds and returns a failing exit code for a nonconforming feature. It does not inspect material strength, surface condition or preload. Keep instrument uncertainty and calibration in the traveler.

PETG is useful for noncritical fixtures and covers when heat/creep constraints permit. ABS/ASA may suit warmer noncritical housings with appropriate printing practice. Nylon performance depends on moisture, formulation and process. MJF PA12 has different process properties from FDM nylon. None is an automatic substitute for a released load-bearing part. Machined aluminum or steel features require the specified alloy, heat treatment, fit and finish.

FDM strength is anisotropic: a load across layer interfaces can fail differently from a load along continuous extrusion. Orientation, inserts, wall geometry and temperature affect the result. Test coupons and representative joints under the relevant load cases. Do not replace a specified 7075 component with a printed replica merely because the shape fits.
### I. Expected result
A dimensionally inspected, unpowered module that moves freely through its reviewed travel without cable strain or interference. Any critical nonconformance blocks powered testing.
### J. Validation
Check identification, material/process certificates where needed, drawing dimensions, bearing fit, fastener engagement, end-stop clearance, cable bend radius and fixture attachment. Measure backlash and axis alignment. Have a qualified designer determine proof-load procedures for the support; do not improvise a drop test with a robot attached.
### K. Troubleshooting
Binding often indicates misalignment, warped prints or an overconstrained bearing arrangement. A loose fit should not be hidden with adhesive unless approved. Threads that strip during assembly require a design/process review, not more tightening.
### L. Practical exercise
Create a serviceability drawing showing how to remove one actuator without cutting cables or unloading another unsupported structure.
### M. Connection to the physical Asimov 1
The repository includes process-labeled fabrication directories. Preserve their material/process intent and reconcile part numbers to the exact assembly manual revision before manufacture.
### N. Completion checklist
Critical dimensions pass; material/process choices are justified; all loads have a continuous path into a reviewed fixture; and a second person can follow the traveler.
### O. Next lesson preview
Design the power and communication experiment before energizing a single actuator.

## Lesson 13 - Electrical and embedded engineering on a single joint
### A. Why this matters
A motor can generate torque unexpectedly, and a stopped motor can still draw substantial current. Electrical protection and mechanical support must work before software is trusted.
### B. Concepts explained simply
Voltage sets an electrical potential; current produces heating and magnetic force; power is V*I. A 48 V, 2 A example consumes 96 W electrically. This is an arithmetic example, not a recommended supply setting. Motor phase current and battery bus current are different quantities. Peak currents, acceleration, regeneration and duty cycle matter.

A fuse protects a circuit against specified fault conditions; it does not necessarily react fast enough to protect a person or motor semiconductor. A contactor must be rated to interrupt the actual DC circuit. An emergency-stop button is only one component of a reviewed isolation system. Regeneration can raise bus voltage when a motor is driven by a falling load; some bench supplies cannot absorb it.
### C. Real-world relevance
Connector shell names do not establish pin order, polarity or current rating. The public design contains board files and wiring inventories, but a release-specific schematic and manufacturer protocol are still required for your exact assembly.
### D. Architecture
!diagram power
The figure is a functional energy/control architecture, not a wiring schematic. Wire gauges, fuse values, contactor ratings, pinouts, precharge and regen provisions must be selected from approved hardware data and load analysis.
### E. Prerequisites
Exact actuator datasheet/protocol revision, drive configuration tool, verified harness/schematic, current-limited supply approved for the actuator and regen case, suitable instruments, guarded fixture, independent isolation and competent electrical review.
### F. Step-by-step implementation
1. De-energize and disconnect all energy sources. Verify isolation with a suitable instrument and protect stored-energy outputs.
2. Inspect conductor identification, polarity, insulation, strain relief, terminal retention and continuity against the approved schematic.
3. Verify supply range, current limiting, short-circuit protection, inrush/precharge and regeneration handling before attaching the actuator.
4. Support the output mechanically and clear the swept volume. Set released low-energy commissioning limits using the vendor tool before motion is possible.
5. Connect one actuator only. Read identity, firmware and feedback with torque disabled using documented commands.
6. Assign a unique ID using the official procedure. Record the physical label and bus mapping.
7. Test the independent isolation and watchdog with the mechanical load secured. Record whether the actuator actually stops producing hazardous motion.
8. Enable a small bounded motion only after direction, zero, limits and fault behavior are verified. Stop and inspect before adding another joint.

No guessed CAN payloads, voltage settings or connector pinouts are supplied. The public materials inspected do not establish a complete validated transport for your purchased release. A fabricated runnable motor command would be worse than an explicit gate.
### G. Complete offline verification code
Use safety.py from Lesson 10 and audit.py from Lesson 11 to validate command envelopes and recorded readiness before any transport exists. A physical driver must be implemented from the confirmed protocol and tested on an inhibited-output fixture. The complete commissioning record template is:
!code humanoid_lab/config/commissioning.json
### H. Walkthrough and CAN fundamentals
CAN uses a differential pair on a terminated bus. A conventional high-speed CAN segment normally has a 120-ohm termination at each physical end; two in parallel produce about 60 ohms in a de-energized resistance check when the design permits that measurement. This is a general diagnostic, not permission to add resistors without checking existing integrated termination and the release topology. Avoid arbitrary star wiring and long stubs.

Confirm bit rate, transceiver type, termination location, common-mode/ground strategy and ID uniqueness. A USB-to-CAN adapter's connector or software API does not prove protocol compatibility. A custom embedded loop should verify command age/sequence and sensor freshness locally, reject malformed data, and transition to a mechanically safe reviewed state if the host disappears.
### I. Expected result
One identified actuator reports credible telemetry with its output initially disabled. The isolation and communication-failure experiments are documented before low-amplitude motion is attempted.
### J. Validation
Require signed polarity/continuity inspection, supply behavior under a dummy load where appropriate, documented current limiting, unique ID, encoder-direction agreement, configuration readback, watchdog timing and emergency-isolation effect. Compare measured stop behavior against the reviewed risk envelope. A 'PASS' typed into JSON without evidence is not a test.
### K. Troubleshooting
Intermittent CAN errors may indicate termination, ground, bit-rate or signal-integrity issues. Brownouts may be inrush or shared return impedance. A bus voltage spike during deceleration suggests regen handling. Stop to diagnose rather than repeatedly re-enabling a faulting drive.
### L. Practical exercise
Capture an inhibited-output communication log and annotate request, response, sequence, timestamp, error flags and timeout. Confirm the same log decodes identically offline.
### M. Connection to the physical Asimov 1
The manual requires assigning IDs individually before assembly. Follow its release-specific procedure; do not send a broadcast assignment on a populated robot bus. [S15]
### N. Completion checklist
One joint passes identity, power, communication, feedback, limits and independent stop tests. No unresolved pinout, voltage, protocol or support assumption remains. Only then duplicate the validated module.
### O. Next lesson preview
Commission a supported system while preserving local timing and safety authority.

## Lesson 14 - Assembly, calibration and supported commissioning
### A. Why this matters
Integration creates faults that single-component tests miss: reversed encoders, overloaded supplies, cable interference, mixed firmware and incorrect model zeros. Commissioning should isolate these faults in a controlled sequence.
### B. Concepts explained simply
A zero offset aligns the encoder coordinate to the model reference pose. A direction sign aligns positive rotation. Gear ratio and parallel linkages may require a nonlinear mapping. Calibration is incomplete until a separate measurement validates the result over the intended range.
### C. Real-world relevance
A biped with motor power removed may collapse. A supported fixture can reduce consequences, but it must be designed for the machine, test envelope and foreseeable failures. A tether that merely keeps the robot nearby is not necessarily a fall-arrest system.
### D. Architecture
Mechanical support and isolation -> embedded protection -> real-time joint loop -> state estimator -> ROS supervision -> allowed skill. Activation requires evidence from every lower layer.
### E. Prerequisites
Release-matched hardware, completed single-joint tests, load-reviewed rig, clear exclusion zone, accessible isolation, trained observer and documented shutdown/rollback procedures.
### F. Step-by-step implementation
| Step | Measurement and pass criterion | If it fails |
|---|---|---|
| Inspection | Correct parts, retained cables, fasteners and support attachment | Repair unpowered and reinspect |
| Power | Polarity, current limiting, protection and bus behavior match reviewed design | Disconnect and correct power design |
| Isolation | Each E-stop/disconnect achieves reviewed physical outcome under support | Remain no-go; repair isolation chain |
| Identity | Every actuator ID and firmware matches the release inventory | Test one actuator at a time |
| Direction | Small commanded positive change matches independent observation | Disable; correct mapping and retest |
| Zero | Measured reference pose matches model within approved tolerance | Recalibrate with support |
| Limits | Conservative position/current/speed limits read back correctly | Reconfigure while inhibited |
| IMU | Static orientations and zero-rate bias agree with references | Correct mounting transform/calibration |
| Limb motion | Small slow trajectory tracks without binding or unexplained heating | Return to joint-level investigation |
| Supported body | No deadline, power or mapping violations across repeated trials | Disable higher-level skill |
| Contact tests | Rig, foot load and contact observations match declared setup | Reassess support and model |
| Progression | Previous gates and reviewer approval recorded | Remain at supported stage |

Set numerical tolerances from measurement uncertainty, the manufacturer and the reviewed experiment envelope. Do not use a generic 1-degree or temperature limit merely because it looks reasonable. Store the threshold and rationale with each test.
### G. Complete readiness-check command
```bash
python audit.py commission config/commissioning.json
```
The complete program is printed in Lesson 11. Its default record is NOT_TESTED for every item, so the supplied result is no-go. Add evidence identifiers and reviewer names to a controlled record; do not replace real tests with automated approval.
### H. Walkthrough and physical software boundaries
High-level compute handles ROS, perception, planning, orchestration and telemetry. The timing-critical controller validates feedback age, limits, setpoints and inference deadlines. Embedded drivers enforce local watchdogs, protection and bus semantics. Record measured cycle-time histograms and missed deadlines under realistic CPU/network load; ordinary WebSockets or MQTT are suitable for telemetry and high-level requests, not the direct stabilization loop.

Calibrate the parallel ankle in motor coordinates and joint coordinates using a verified geometric mapping and independent measurement. Validate its position and torque transforms together. A left/right sign fix in the UI must not hide an inconsistent lower-level convention.
### I. Expected result
A calibrated supported module or body executes a small reviewed trajectory while feedback, temperatures, current, timing and faults are logged. You can trigger the documented stop and explain how loads remain supported.
### J. Validation
Repeat each trial after a cold start, a software restart and a fault reset. Disconnect host communication intentionally with output support in place. Confirm no automatic motion resumes when packets return. Require manual re-arming through the reviewed procedure. Initial commissioning excludes unsupported dynamic walking.
### K. Troubleshooting
A growing tracking error can be binding, saturation or bad zeroing. A different pose after reboot can indicate unsaved offsets or absolute-encoder interpretation. Thermal drift needs measured duty-cycle and cooling analysis. Do not hide intermittent faults by increasing watchdog timeouts without a timing justification.
### L. Practical exercise
Perform an unpowered shutdown rehearsal with two people: name who isolates energy, who controls the rig, where stored energy remains, and how the faulted configuration is preserved for diagnosis.
### M. Connection to the physical Asimov 1
Use the manufacturer's matched firmware/images and released procedures. A public API describing STAND/MOVE modes does not establish readiness of your assembly. Keep software compliance modes distinct from emergency isolation.
### N. Completion checklist
Inspection, calibration, limits, timing, rig, isolation, watchdog and rollback all have dated evidence. A physical policy is disabled until those records pass.
### O. Next lesson preview
Integrate perception with a small validated behavior and publish its evidence.

# Part V - The end-to-end research demonstration
## Lesson 15 - Recognize an object and execute a validated skill
### A. Why this matters
An end-to-end demonstration should prove a traceable chain from observation to bounded motion and feedback. Limit the first task to the physical platform you actually have.
### B. Concepts explained simply
A behavior state machine separates OBSERVE, VALIDATE, EXECUTE, VERIFY, COMPLETE and FAULT. Each transition has a condition. A skill has preconditions, bounded parameters, timeout, success criteria and cancellation behavior. 'Object seen' is not the same event as 'task complete'.
### C. Real-world relevance
A one-joint supported platform can detect a colored object and make a gesture. A full-body platform with unresolved walking cannot safely promise approach or grasp. Match the demonstration to verified capability.
### D. Architecture
Synthetic or camera frame -> classical detector -> permitted supported gesture -> command-envelope check -> bounded controller -> feedback log -> completion report. A future language planner may select the same gesture through a strict allowlisted schema.
### E. Prerequisites
Perception tests, supported control, offline command-gate tests and logging. A physical run additionally requires every hardware commissioning gate and a verified transport implementation.
### F. Step-by-step implementation
```bash
python perception.py
python demo.py
cat logs/demo.json
```
The included run uses a synthetic image and the fixed-pelvis Asimov model. It moves the left elbow through a smooth three-second out-and-back gesture. This completes the software chain without claiming a camera is mounted on actual hardware.
### G. Complete code
File: /data/Robotics_Project/humanoid_lab/demo.py
!code humanoid_lab/demo.py
### H. Code walkthrough
The detector produces a centroid with unknown depth. The behavior chooses a predefined gesture, avoiding an unjustified metric reach. Each setpoint is checked against the command envelope before PD execution. The gate checks consecutive command steps in this demonstration; a separate tracking monitor must compare actual joint motion and measured speed before physical use.

The simulator logs feedback and writes a final JSON state. A physical skill implementation needs measured success criteria and an explicit FAULT/cancel path; a completed for-loop alone is not physical task verification. Extend the test with no-object input and fault injection before extending its motion.
### I. Expected result
logs/demo.json reports COMPLETE_SIMULATION, 1,500 physics steps and an object observation. logs/demo.csv records elbow feedback. The prepared run's peak elbow angle was about .8843 rad; it includes the model's initial reference angle, so it is not a .8843 rad excursion.
### J. Validation
Require detector positive and negative cases, finite feedback, bounded commands, final tracking-error measurement and cancellation tests. Demonstrate rejection of a stale command, invalid target and unsupported skill request. A physical first demo should pass repeated supervised trials without protection trips, unusual heating or missed-deadline violations under the same declared setup.
### K. Troubleshooting
If motion occurs without a valid observation, the behavior transition is wrong. If detection succeeds but no command is sent, inspect preconditions and gate reasons. If commands are sent but tracking fails, diagnose the controller/physical layer separately from vision.
### L. Practical exercise
Replace the synthetic image with a recorded, calibrated camera frame and keep the skill amplitude unchanged. Add three-frame observation consistency and a skill timeout before using a live camera stream.
### M. Connection to the physical Asimov 1
Reuse the detector, state-machine design, schemas and logs. Replace only the verified simulation backend with a commissioned hardware interface; then revalidate timing, tracking, thermal behavior and stop handling. The full Asimov and a smaller module need different preconditions.
### N. Completion checklist
You can trace a command to its observation, identify every gate, measure actual feedback and demonstrate a no-motion result on invalid input. Label the result as simulation, supported physical module or protected whole-body test accurately.
### O. Next lesson preview
Turn a demonstration into a reproducible research result that another engineer can evaluate.

## Lesson 16 - Research quality, maintenance and the next build
### A. Why this matters
A working demonstration can still be fragile. Research value comes from repeatability, documented limits, baseline comparisons and an honest account of failures.
### B. Concepts explained simply
Unit tests verify small properties. Integration tests verify components together. Simulation regressions detect changes in behavior under fixed conditions. Bench tests check actual interfaces. Validation measures the capability claimed; verification checks implementation against specified requirements. Both are necessary.
### C. Real-world relevance
A version update, replacement actuator or changed cable routing can invalidate previous evidence. Configuration changes need explicit impact review and a path back to a known-good release.
### D. Architecture
Commit -> pinned environment -> model/config hashes -> numerical tests -> simulation matrix -> release artifact -> commissioning record -> monitored deployment -> logged evidence -> issue and revision.
### E. Prerequisites
All relevant earlier gates, a clear capability statement and retained raw data. Failed experiments belong in the record.
### F. Step-by-step implementation
Create a release folder containing source revision, environment freeze, model hash, policy metadata, calibration IDs, test commands, numeric outputs, evaluation matrix and rollback instructions. Keep personal credentials and large raw training files out of git. Make logs immutable or uniquely named per experiment.
```bash
cd /data/Robotics_Project/humanoid_lab
python -m pytest -q
python learning.py check --task reach
python simulate.py --headless --seconds 10
python demo.py
python -m pip freeze > requirements-lock.txt
```
Use headless CI for numerical and fault tests. Add a separate manually controlled hardware test stage so an automatic software push cannot unexpectedly energize a mechanism. Pin CI runner images by digest for a release; do not assume a floating ubuntu-latest runner is your Ubuntu 24.04 environment.
### G. Complete code
The complete numerical and contract tests are printed in Appendix A. Use them unchanged as the first regression suite. The commands above define the minimal release check; physical tests remain separately gated.
### H. Walkthrough
A test asserting only that a constant equals itself adds no engineering evidence. Useful tests here check model dimensions, bounded torque, nonfinite-target rejection, IK residual, fault latching, missing depth and seeded resets. Broader tests should target changed risks: frame conversions, policy parity, transport decoding, observation age and physical limit readback.

Benchmark simulated seconds per wall second, inference latency percentiles and worst observed latency, deadline misses, memory use and log throughput. Report hardware, sample count, load, seeds and warm-up. An average latency alone hides rare overruns.
### I. Expected result
Another engineer can reproduce the supported simulation demo and understand exactly which ROS, learning and physical milestones still require evidence. The completed book remains a working laboratory guide rather than a promise of a finished walking machine.
### J. Validation
Perform a clean-environment rebuild, rerun the suite, reproduce one positive and one negative demonstration, and verify the rollback bundle restores the previous measured result. For every claimed capability, identify the raw evidence and the conditions where it has not been tested.
### K. Troubleshooting
A result that cannot be reproduced may depend on an untracked model, seed, environment variable or calibration. A regression hidden by wider tolerances needs explanation. Restore the last good release, isolate the change and rerun the narrow relevant experiment first.
### L. Practical exercise
Write a one-page research report: hypothesis, baseline, intervention, test matrix, quantitative results, failures, limits and next experiment. Make the next experiment answer one concrete uncertainty.
### M. Connection to the physical Asimov 1
The same release discipline supports future limb additions and whole-body work. Re-run impact-relevant commissioning after any structural, power, firmware, estimator or policy change.
### N. Completion checklist
Your demo has a precise capability statement, reproducible software, preserved logs, known limitations and tested rollback. The next build decision is grounded in measured gaps and a complete procurement forecast.
### O. Next lesson preview
Choose the next research question from evidence: better state estimation, a calibrated physical joint, a more reliable skill, or contact-rich locomotion. Keep the same gates as scope increases.
