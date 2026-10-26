# Part XII - Physical engineering, evidence and integration

These laboratories develop procurement arithmetic, fit variation, load screening, electrical energy reasoning, bidirectional calibration and evidence management. Their values are fictional teaching inputs unless the earlier source register explicitly identifies a verified fact. They support better questions and better experiments; they do not approve a fabricated structure, power system or complete robot. The final synthetic capstone integrates the same authority boundaries used by the practical Asimov simulation.

## Laboratory 61 - Landed cost, VAT, contingency and scope decisions

### A. The engineering question

A feasible project budget is a release-matched bill of materials with quantities, tax basis, shipping, fabrication, tools, protection and contingency.

### B. Concepts and mathematical model

A partially priced list cannot prove affordability. This laboratory uses an explicitly fictional procurement scenario to teach reconciliation and sensitivity. It separates VAT-inclusive EU items from net-priced imports, then reserves contingency before deciding whether the stage fits the robot budget. The invented values are not supplier prices and must never be presented as a verified Asimov BOM.

landed = EU_gross + (import_net+shipping)*(1+tax_fraction) + fabrication + protection; total=landed*(1+contingency).

### C. Real-world meaning and limits

The earlier verified-source procurement ledger remains authoritative about what was and was not priced; this scenario provides no new live quotes.

### D. Architecture and data flow

Configuration (motor_count, motor_allowance) -> numerical model -> import_landed_EUR, subtotal_EUR, reserve_EUR -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

motor_count is the hypothetical stage count; motor_allowance is an invented net EUR budget amount, not a quotation.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| motor_count | 3 | Defined by the explicit chapter model and parameter contract |
| motor_allowance | 400 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/61_landed_budget.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only motor_count changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/61_landed_budget.py --case 0

.venv-book/bin/python expanded_lab/modules/61_landed_budget.py --case 3

.venv-book/bin/python expanded_lab/run.py landed_budget --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/61_landed_budget.py

### H. Walkthrough and design decisions

The tax basis is explicit and VAT-inclusive EU items are not taxed a second time. The reserve remains a distinct line so it cannot be mistaken for component spending.

### I. Expected behavior and six worked cases

The controlled variable is motor_count. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/61_landed_budget.png

Figure L61. import landed EUR as motor_count changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | motor_count | import landed EUR |
|---|---|---|
| 0 | 1 | 618.8 |
| 1 | 2 | 1094.8 |
| 2 | 3 | 1570.8 |
| 3 | 4 | 2046.8 |
| 4 | 6 | 2998.8 |
| 5 | 12 | 5854.8 |

#### Worked case 0: motor_count = 1

This case keeps the nominal configuration except for motor_count=1. The full input is {"motor_allowance": 400.0, "motor_count": 1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| import landed EUR | 618.8 |
| subtotal EUR | 2268.8 |
| reserve EUR | 340.32 |
| total stage EUR | 2609.12 |
| budget margin EUR | 3390.88 |

1. This hypothetical stage contains 1 motors at an internal allowance of EUR 400 each.

2. Net import allowance EUR 400 plus EUR 120 shipping is taxed at an assumed 19%.

3. Import landed cost is EUR 618.80; EU gross, fabrication and protection give subtotal EUR 2268.80.

4. Reserve 15% contingency: EUR 340.32.

5. Total is EUR 2609.12; margin against EUR 6,000 is EUR 3390.88.

#### Worked case 1: motor_count = 2

This case keeps the nominal configuration except for motor_count=2. The full input is {"motor_allowance": 400.0, "motor_count": 2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| import landed EUR | 1094.8 |
| subtotal EUR | 2744.8 |
| reserve EUR | 411.72 |
| total stage EUR | 3156.52 |
| budget margin EUR | 2843.48 |

1. This hypothetical stage contains 2 motors at an internal allowance of EUR 400 each.

2. Net import allowance EUR 800 plus EUR 120 shipping is taxed at an assumed 19%.

3. Import landed cost is EUR 1094.80; EU gross, fabrication and protection give subtotal EUR 2744.80.

4. Reserve 15% contingency: EUR 411.72.

5. Total is EUR 3156.52; margin against EUR 6,000 is EUR 2843.48.

#### Worked case 2: motor_count = 3

This case keeps the nominal configuration except for motor_count=3. The full input is {"motor_allowance": 400.0, "motor_count": 3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| import landed EUR | 1570.8 |
| subtotal EUR | 3220.8 |
| reserve EUR | 483.12 |
| total stage EUR | 3703.92 |
| budget margin EUR | 2296.08 |

1. This hypothetical stage contains 3 motors at an internal allowance of EUR 400 each.

2. Net import allowance EUR 1200 plus EUR 120 shipping is taxed at an assumed 19%.

3. Import landed cost is EUR 1570.80; EU gross, fabrication and protection give subtotal EUR 3220.80.

4. Reserve 15% contingency: EUR 483.12.

5. Total is EUR 3703.92; margin against EUR 6,000 is EUR 2296.08.

#### Worked case 3: motor_count = 4

This case keeps the nominal configuration except for motor_count=4. The full input is {"motor_allowance": 400.0, "motor_count": 4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| import landed EUR | 2046.8 |
| subtotal EUR | 3696.8 |
| reserve EUR | 554.52 |
| total stage EUR | 4251.32 |
| budget margin EUR | 1748.68 |

1. This hypothetical stage contains 4 motors at an internal allowance of EUR 400 each.

2. Net import allowance EUR 1600 plus EUR 120 shipping is taxed at an assumed 19%.

3. Import landed cost is EUR 2046.80; EU gross, fabrication and protection give subtotal EUR 3696.80.

4. Reserve 15% contingency: EUR 554.52.

5. Total is EUR 4251.32; margin against EUR 6,000 is EUR 1748.68.

#### Worked case 4: motor_count = 6

This case keeps the nominal configuration except for motor_count=6. The full input is {"motor_allowance": 400.0, "motor_count": 6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| import landed EUR | 2998.8 |
| subtotal EUR | 4648.8 |
| reserve EUR | 697.32 |
| total stage EUR | 5346.12 |
| budget margin EUR | 653.88 |

1. This hypothetical stage contains 6 motors at an internal allowance of EUR 400 each.

2. Net import allowance EUR 2400 plus EUR 120 shipping is taxed at an assumed 19%.

3. Import landed cost is EUR 2998.80; EU gross, fabrication and protection give subtotal EUR 4648.80.

4. Reserve 15% contingency: EUR 697.32.

5. Total is EUR 5346.12; margin against EUR 6,000 is EUR 653.88.

#### Worked case 5: motor_count = 12

This case keeps the nominal configuration except for motor_count=12. The full input is {"motor_allowance": 400.0, "motor_count": 12}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| import landed EUR | 5854.8 |
| subtotal EUR | 7504.8 |
| reserve EUR | 1125.72 |
| total stage EUR | 8630.52 |
| budget margin EUR | -2630.52 |

1. This hypothetical stage contains 12 motors at an internal allowance of EUR 400 each.

2. Net import allowance EUR 4800 plus EUR 120 shipping is taxed at an assumed 19%.

3. Import landed cost is EUR 5854.80; EU gross, fabrication and protection give subtotal EUR 7504.80.

4. Reserve 15% contingency: EUR 1125.72.

5. Total is EUR 8630.52; margin against EUR 6,000 is EUR -2630.52.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Every amount here is a teaching allowance. Actual VAT jurisdiction, customs treatment, supplier terms and compatibility must be checked.

A negative margin means reduce scope or increase funding; essential protection is not the balancing item.

### K. Failure modes and troubleshooting

Counting unquoted parts as zero; double-adding VAT; omitting tools/support; treating a compatible torque number as a compatible actuator.

### L. Practical exercises and extension tasks

1. Replace allowances with dated exact supplier quotes and recompute.

2. Separate optional laptop spending from the robot budget.

3. Calculate the maximum motor allowance compatible with the remaining stage budget.

### M. Connection to the Asimov research platform

The earlier verified-source procurement ledger remains authoritative about what was and was not priced; this scenario provides no new live quotes.

### N. Completion record

Record your chosen case, predicted trend, measured import_landed_EUR, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 62, Dimensional tolerances, stack-ups and manufacturing variation. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 62 - Dimensional tolerances, stack-ups and manufacturing variation

### A. The engineering question

An assembly can fail to fit even when each part looks close to nominal.

### B. Concepts and mathematical model

Tolerance stacks accumulate dimensional variation along a functional path. Worst-case addition provides a deterministic bound under bounded independent specifications, while root-sum-square estimates rely on statistical assumptions. Manufacturing bias and correlation can invalidate the reassuring statistical result. This laboratory compares both calculations with seeded manufactured samples and makes the probability model explicit.

worst_case=sum(abs(t_i)); RSS=sqrt(sum(sigma_i^2)); assembly_error=sum(component_errors).

### C. Real-world meaning and limits

Critical bearing, shaft and fastener fits must follow approved drawings and inspection procedures; the example window is not an Asimov tolerance.

### D. Architecture and data flow

Configuration (scale, correlation) -> numerical model -> independent_RSS_std_mm, empirical_std_mm, three_sigma_worst_case_mm -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

scale multiplies component dimensional standard deviations; correlation is the nonnegative common-factor fraction.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| scale | 1 | Defined by the explicit chapter model and parameter contract |
| correlation | 0 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/62_tolerance_stack.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only correlation changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/62_tolerance_stack.py --case 0

.venv-book/bin/python expanded_lab/modules/62_tolerance_stack.py --case 3

.venv-book/bin/python expanded_lab/run.py tolerance_stack --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/62_tolerance_stack.py

### H. Walkthrough and design decisions

Correlated errors are constructed from shared and independent Gaussian factors. Compare empirical variability with the RSS assumption before using the statistical result for fit decisions.

### I. Expected behavior and six worked cases

The controlled variable is correlation. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/62_tolerance_stack.png

Figure L62. independent RSS std mm as correlation changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | correlation | independent RSS std mm |
|---|---|---|
| 0 | 0 | 0.03905125 |
| 1 | 0.1 | 0.03905125 |
| 2 | 0.25 | 0.03905125 |
| 3 | 0.5 | 0.03905125 |
| 4 | 0.75 | 0.03905125 |
| 5 | 1 | 0.03905125 |

#### Worked case 0: correlation = 0

This case keeps the nominal configuration except for correlation=0. The full input is {"correlation": 0.0, "scale": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| independent RSS std mm | 0.03905125 |
| empirical std mm | 0.03924028 |
| three sigma worst case mm | 0.195 |
| fit violation fraction | 0.00005 |
| empirical 95 percentile abs mm | 0.07765769 |

1. Component standard deviations are [0.02, 0.03, 0.015] mm.

2. Use pairwise correlation generated by a common factor with rho=0.

3. Independent RSS prediction is 0.039051 mm.

4. Empirical stack standard deviation is 0.039240 mm.

5. Against an illustrative +/-0.15 mm assembly window, violation fraction is 0.000050.

#### Worked case 1: correlation = 0.1

This case keeps the nominal configuration except for correlation=0.1. The full input is {"correlation": 0.1, "scale": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| independent RSS std mm | 0.03905125 |
| empirical std mm | 0.04263978 |
| three sigma worst case mm | 0.195 |
| fit violation fraction | 0.0006 |
| empirical 95 percentile abs mm | 0.08334629 |

1. Component standard deviations are [0.02, 0.03, 0.015] mm.

2. Use pairwise correlation generated by a common factor with rho=0.1.

3. Independent RSS prediction is 0.039051 mm.

4. Empirical stack standard deviation is 0.042640 mm.

5. Against an illustrative +/-0.15 mm assembly window, violation fraction is 0.000600.

#### Worked case 2: correlation = 0.25

This case keeps the nominal configuration except for correlation=0.25. The full input is {"correlation": 0.25, "scale": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| independent RSS std mm | 0.03905125 |
| empirical std mm | 0.04715121 |
| three sigma worst case mm | 0.195 |
| fit violation fraction | 0.00165 |
| empirical 95 percentile abs mm | 0.09233163 |

1. Component standard deviations are [0.02, 0.03, 0.015] mm.

2. Use pairwise correlation generated by a common factor with rho=0.25.

3. Independent RSS prediction is 0.039051 mm.

4. Empirical stack standard deviation is 0.047151 mm.

5. Against an illustrative +/-0.15 mm assembly window, violation fraction is 0.001650.

#### Worked case 3: correlation = 0.5

This case keeps the nominal configuration except for correlation=0.5. The full input is {"correlation": 0.5, "scale": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| independent RSS std mm | 0.03905125 |
| empirical std mm | 0.05378017 |
| three sigma worst case mm | 0.195 |
| fit violation fraction | 0.005 |
| empirical 95 percentile abs mm | 0.10534384 |

1. Component standard deviations are [0.02, 0.03, 0.015] mm.

2. Use pairwise correlation generated by a common factor with rho=0.5.

3. Independent RSS prediction is 0.039051 mm.

4. Empirical stack standard deviation is 0.053780 mm.

5. Against an illustrative +/-0.15 mm assembly window, violation fraction is 0.005000.

#### Worked case 4: correlation = 0.75

This case keeps the nominal configuration except for correlation=0.75. The full input is {"correlation": 0.75, "scale": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| independent RSS std mm | 0.03905125 |
| empirical std mm | 0.0596332 |
| three sigma worst case mm | 0.195 |
| fit violation fraction | 0.0113 |
| empirical 95 percentile abs mm | 0.11682198 |

1. Component standard deviations are [0.02, 0.03, 0.015] mm.

2. Use pairwise correlation generated by a common factor with rho=0.75.

3. Independent RSS prediction is 0.039051 mm.

4. Empirical stack standard deviation is 0.059633 mm.

5. Against an illustrative +/-0.15 mm assembly window, violation fraction is 0.011300.

#### Worked case 5: correlation = 1

This case keeps the nominal configuration except for correlation=1. The full input is {"correlation": 1.0, "scale": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| independent RSS std mm | 0.03905125 |
| empirical std mm | 0.06485032 |
| three sigma worst case mm | 0.195 |
| fit violation fraction | 0.0214 |
| empirical 95 percentile abs mm | 0.12672294 |

1. Component standard deviations are [0.02, 0.03, 0.015] mm.

2. Use pairwise correlation generated by a common factor with rho=1.

3. Independent RSS prediction is 0.039051 mm.

4. Empirical stack standard deviation is 0.064850 mm.

5. Against an illustrative +/-0.15 mm assembly window, violation fraction is 0.021400.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The three-sigma sum is a bounded-specification illustration, not an absolute bound for unbounded Gaussian samples.

Actual drawing tolerances, process capability, datum strategy and measurement uncertainty determine the proper analysis.

### K. Failure modes and troubleshooting

Treating drawing limits as Gaussian sigma; ignoring common fixture bias; mixing dimensions from inconsistent datums.

### L. Practical exercises and extension tasks

1. Add a systematic machining offset to all parts.

2. Replace Gaussian errors with bounded uniform errors.

3. Include instrument uncertainty in acceptance decisions.

### M. Connection to the Asimov research platform

Critical bearing, shaft and fastener fits must follow approved drawings and inspection procedures; the example window is not an Asimov tolerance.

### N. Completion record

Record your chosen case, predicted trend, measured independent_RSS_std_mm, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 63, Load paths, bolt-group screening and nominal stress. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 63 - Load paths, bolt-group screening and nominal stress

### A. The engineering question

Fastener calculations begin with the load path and joint geometry.

### B. Concepts and mathematical model

Dividing a total force equally among bolts can be wrong when an applied moment creates nonuniform load. Preload, joint stiffness, friction, prying, fatigue and thread engagement further complicate real design. This laboratory screens an ideal symmetric bolt circle under direct axial force plus a moment, reporting the largest modeled bolt load and nominal tensile stress. It intentionally stops short of approving a joint.

F_i=F_total/n + M*y_i/sum(y_j^2); nominal stress=F_max/assumed_tensile_area.

### C. Real-world meaning and limits

Load-bearing robot and support-rig joints require competent mechanical design review, released fastener specifications and documented assembly.

### D. Architecture and data flow

Configuration (radius, axial_force, moment) -> numerical model -> maximum_bolt_load_N, minimum_bolt_load_N, nominal_max_tensile_stress_MPa -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

radius is meters; axial_force is Newtons; moment is Nm; the assumed tensile area is only a numerical teaching input.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| radius | 0.025 | Defined by the explicit chapter model and parameter contract |
| axial_force | 400 | Defined by the explicit chapter model and parameter contract |
| moment | 5 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/63_fastener_screen.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only radius changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/63_fastener_screen.py --case 0

.venv-book/bin/python expanded_lab/modules/63_fastener_screen.py --case 3

.venv-book/bin/python expanded_lab/run.py fastener_screen --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/63_fastener_screen.py

### H. Walkthrough and design decisions

The moment contribution depends on bolt position, while its sum is zero for the symmetric group. Check recovered force before trusting peak stress.

### I. Expected behavior and six worked cases

The controlled variable is radius. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/63_fastener_screen.png

Figure L63. maximum bolt load N as radius changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | radius | maximum bolt load N |
|---|---|---|
| 0 | 0.015 | 266.66666667 |
| 1 | 0.02 | 225 |
| 2 | 0.025 | 200 |
| 3 | 0.03 | 183.33333333 |
| 4 | 0.04 | 162.5 |
| 5 | 0.05 | 150 |

#### Worked case 0: radius = 0.015

This case keeps the nominal configuration except for radius=0.015. The full input is {"axial_force": 400.0, "moment": 5.0, "radius": 0.015}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| maximum bolt load N | 266.66666667 |
| minimum bolt load N | -66.66666667 |
| nominal max tensile stress MPa | 33.33333333 |
| bolt circle radius m | 0.015 |
| recovered total force N | 400 |

1. Four ideal bolts lie on radius 0.015 m with y coordinates [0.0, 0.015, 1.8369701987210296e-18, -0.015] m.

2. Apply direct axial force 400 N and bending moment 5 Nm.

3. The simplified bolt loads are [100.0, 266.66666666666663, 100.00000000000001, -66.66666666666666] N.

4. Maximum load 266.666667 N divided by assumed area 8 mm^2 gives 33.333333 MPa.

5. Summed axial force recovers 400.000000 N as a consistency check.

#### Worked case 1: radius = 0.02

This case keeps the nominal configuration except for radius=0.02. The full input is {"axial_force": 400.0, "moment": 5.0, "radius": 0.02}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| maximum bolt load N | 225 |
| minimum bolt load N | -25 |
| nominal max tensile stress MPa | 28.125 |
| bolt circle radius m | 0.02 |
| recovered total force N | 400 |

1. Four ideal bolts lie on radius 0.02 m with y coordinates [0.0, 0.02, 2.4492935982947064e-18, -0.02] m.

2. Apply direct axial force 400 N and bending moment 5 Nm.

3. The simplified bolt loads are [100.0, 225.0, 100.00000000000001, -25.0] N.

4. Maximum load 225.000000 N divided by assumed area 8 mm^2 gives 28.125000 MPa.

5. Summed axial force recovers 400.000000 N as a consistency check.

#### Worked case 2: radius = 0.025

This case keeps the nominal configuration except for radius=0.025. The full input is {"axial_force": 400.0, "moment": 5.0, "radius": 0.025}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| maximum bolt load N | 200 |
| minimum bolt load N | 1.4210855e-14 |
| nominal max tensile stress MPa | 25 |
| bolt circle radius m | 0.025 |
| recovered total force N | 400 |

1. Four ideal bolts lie on radius 0.025 m with y coordinates [0.0, 0.025, 3.061616997868383e-18, -0.025] m.

2. Apply direct axial force 400 N and bending moment 5 Nm.

3. The simplified bolt loads are [100.0, 200.0, 100.00000000000001, 1.4210854715202004e-14] N.

4. Maximum load 200.000000 N divided by assumed area 8 mm^2 gives 25.000000 MPa.

5. Summed axial force recovers 400.000000 N as a consistency check.

#### Worked case 3: radius = 0.03

This case keeps the nominal configuration except for radius=0.03. The full input is {"axial_force": 400.0, "moment": 5.0, "radius": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| maximum bolt load N | 183.33333333 |
| minimum bolt load N | 16.66666667 |
| nominal max tensile stress MPa | 22.91666667 |
| bolt circle radius m | 0.03 |
| recovered total force N | 400 |

1. Four ideal bolts lie on radius 0.03 m with y coordinates [0.0, 0.03, 3.673940397442059e-18, -0.03] m.

2. Apply direct axial force 400 N and bending moment 5 Nm.

3. The simplified bolt loads are [100.0, 183.33333333333331, 100.00000000000001, 16.66666666666667] N.

4. Maximum load 183.333333 N divided by assumed area 8 mm^2 gives 22.916667 MPa.

5. Summed axial force recovers 400.000000 N as a consistency check.

#### Worked case 4: radius = 0.04

This case keeps the nominal configuration except for radius=0.04. The full input is {"axial_force": 400.0, "moment": 5.0, "radius": 0.04}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| maximum bolt load N | 162.5 |
| minimum bolt load N | 37.5 |
| nominal max tensile stress MPa | 20.3125 |
| bolt circle radius m | 0.04 |
| recovered total force N | 400 |

1. Four ideal bolts lie on radius 0.04 m with y coordinates [0.0, 0.04, 4.898587196589413e-18, -0.04] m.

2. Apply direct axial force 400 N and bending moment 5 Nm.

3. The simplified bolt loads are [100.0, 162.5, 100.00000000000001, 37.5] N.

4. Maximum load 162.500000 N divided by assumed area 8 mm^2 gives 20.312500 MPa.

5. Summed axial force recovers 400.000000 N as a consistency check.

#### Worked case 5: radius = 0.05

This case keeps the nominal configuration except for radius=0.05. The full input is {"axial_force": 400.0, "moment": 5.0, "radius": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| maximum bolt load N | 150 |
| minimum bolt load N | 50 |
| nominal max tensile stress MPa | 18.75 |
| bolt circle radius m | 0.05 |
| recovered total force N | 400 |

1. Four ideal bolts lie on radius 0.05 m with y coordinates [0.0, 0.05, 6.123233995736766e-18, -0.05] m.

2. Apply direct axial force 400 N and bending moment 5 Nm.

3. The simplified bolt loads are [100.0, 150.0, 100.0, 50.00000000000001] N.

4. Maximum load 150.000000 N divided by assumed area 8 mm^2 gives 18.750000 MPa.

5. Summed axial force recovers 400.000000 N as a consistency check.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Negative calculated load indicates the simple tension-only interpretation needs joint contact/separation analysis.

No allowable stress, bolt grade, preload or tightening torque is specified; this is not a structural approval.

### K. Failure modes and troubleshooting

Assuming equal bolt loading under moment; using nominal shank area instead of the appropriate tensile area; selecting torque without joint/preload analysis.

### L. Practical exercises and extension tasks

1. Change the bolt-group geometry and recompute the moment distribution.

2. Add a conservative dynamic load case.

3. List the missing evidence needed for a real design approval.

### M. Connection to the Asimov research platform

Load-bearing robot and support-rig joints require competent mechanical design review, released fastener specifications and documented assembly.

### N. Completion record

Record your chosen case, predicted trend, measured maximum_bolt_load_N, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 64, Cable resistance, voltage drop and heat screening. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 64 - Cable resistance, voltage drop and heat screening

### A. The engineering question

A conductor's resistance creates both voltage drop and heat.

### B. Concepts and mathematical model

The return path contributes to loop resistance and must be included. A short cable can still heat at high current, while a longer cable can cause a controller brownout before a thermal problem becomes obvious. This calculation screens resistance effects with an assumed copper resistivity; it does not choose a safe wire gauge, fuse or connector rating. Installation method, insulation, bundling, temperature and fault protection require separate review.

R_loop=rho*(2*length)/area; voltage_drop=I*R_loop; heating=I^2*R_loop.

### C. Real-world meaning and limits

Actual conductor, connector, fuse and insulation selection requires verified hardware specifications and installation-specific electrical review.

### D. Architecture and data flow

Configuration (one_way_length, area_mm2, current) -> numerical model -> loop_resistance_ohm, voltage_drop_V, conductor_heat_W -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

one_way_length is meters; area_mm2 is conductor cross-section in mm^2; current is Amperes.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| one_way_length | 1 | Defined by the explicit chapter model and parameter contract |
| area_mm2 | 1.5 | Defined by the explicit chapter model and parameter contract |
| current | 5 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/64_cable_loss.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only current changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/64_cable_loss.py --case 0

.venv-book/bin/python expanded_lab/modules/64_cable_loss.py --case 3

.venv-book/bin/python expanded_lab/run.py cable_loss --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/64_cable_loss.py

### H. Walkthrough and design decisions

Convert square millimeters into square meters before applying resistivity. Voltage drop scales linearly with current while heating scales quadratically, so one nominal-voltage check cannot establish a thermal margin.

### I. Expected behavior and six worked cases

The controlled variable is current. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/64_cable_loss.png

Figure L64. loop resistance ohm as current changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | current | loop resistance ohm |
|---|---|---|
| 0 | 1 | 0.02293333 |
| 1 | 2 | 0.02293333 |
| 2 | 5 | 0.02293333 |
| 3 | 10 | 0.02293333 |
| 4 | 15 | 0.02293333 |
| 5 | 20 | 0.02293333 |

#### Worked case 0: current = 1

This case keeps the nominal configuration except for current=1. The full input is {"area_mm2": 1.5, "current": 1.0, "one_way_length": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| loop resistance ohm | 0.02293333 |
| voltage drop V | 0.02293333 |
| conductor heat W | 0.02293333 |
| drop fraction of 48V | 0.00047778 |
| heat per one way meter W m | 0.02293333 |

1. Assume rho=1.720e-08 ohm*m, one-way length 1 m and area 1.5 mm^2.

2. Include outgoing and return conductors: loop resistance is 0.02293333 ohm.

3. At current 1 A, voltage drop is 0.022933 V.

4. Joule heating is I^2*R=0.022933 W across the loop.

5. Drop is 0.047778% of an illustrative 48 V bus.

#### Worked case 1: current = 2

This case keeps the nominal configuration except for current=2. The full input is {"area_mm2": 1.5, "current": 2.0, "one_way_length": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| loop resistance ohm | 0.02293333 |
| voltage drop V | 0.04586667 |
| conductor heat W | 0.09173333 |
| drop fraction of 48V | 0.00095556 |
| heat per one way meter W m | 0.09173333 |

1. Assume rho=1.720e-08 ohm*m, one-way length 1 m and area 1.5 mm^2.

2. Include outgoing and return conductors: loop resistance is 0.02293333 ohm.

3. At current 2 A, voltage drop is 0.045867 V.

4. Joule heating is I^2*R=0.091733 W across the loop.

5. Drop is 0.095556% of an illustrative 48 V bus.

#### Worked case 2: current = 5

This case keeps the nominal configuration except for current=5. The full input is {"area_mm2": 1.5, "current": 5.0, "one_way_length": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| loop resistance ohm | 0.02293333 |
| voltage drop V | 0.11466667 |
| conductor heat W | 0.57333333 |
| drop fraction of 48V | 0.00238889 |
| heat per one way meter W m | 0.57333333 |

1. Assume rho=1.720e-08 ohm*m, one-way length 1 m and area 1.5 mm^2.

2. Include outgoing and return conductors: loop resistance is 0.02293333 ohm.

3. At current 5 A, voltage drop is 0.114667 V.

4. Joule heating is I^2*R=0.573333 W across the loop.

5. Drop is 0.238889% of an illustrative 48 V bus.

#### Worked case 3: current = 10

This case keeps the nominal configuration except for current=10. The full input is {"area_mm2": 1.5, "current": 10.0, "one_way_length": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| loop resistance ohm | 0.02293333 |
| voltage drop V | 0.22933333 |
| conductor heat W | 2.29333333 |
| drop fraction of 48V | 0.00477778 |
| heat per one way meter W m | 2.29333333 |

1. Assume rho=1.720e-08 ohm*m, one-way length 1 m and area 1.5 mm^2.

2. Include outgoing and return conductors: loop resistance is 0.02293333 ohm.

3. At current 10 A, voltage drop is 0.229333 V.

4. Joule heating is I^2*R=2.293333 W across the loop.

5. Drop is 0.477778% of an illustrative 48 V bus.

#### Worked case 4: current = 15

This case keeps the nominal configuration except for current=15. The full input is {"area_mm2": 1.5, "current": 15.0, "one_way_length": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| loop resistance ohm | 0.02293333 |
| voltage drop V | 0.344 |
| conductor heat W | 5.16 |
| drop fraction of 48V | 0.00716667 |
| heat per one way meter W m | 5.16 |

1. Assume rho=1.720e-08 ohm*m, one-way length 1 m and area 1.5 mm^2.

2. Include outgoing and return conductors: loop resistance is 0.02293333 ohm.

3. At current 15 A, voltage drop is 0.344000 V.

4. Joule heating is I^2*R=5.160000 W across the loop.

5. Drop is 0.716667% of an illustrative 48 V bus.

#### Worked case 5: current = 20

This case keeps the nominal configuration except for current=20. The full input is {"area_mm2": 1.5, "current": 20.0, "one_way_length": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| loop resistance ohm | 0.02293333 |
| voltage drop V | 0.45866667 |
| conductor heat W | 9.17333333 |
| drop fraction of 48V | 0.00955556 |
| heat per one way meter W m | 9.17333333 |

1. Assume rho=1.720e-08 ohm*m, one-way length 1 m and area 1.5 mm^2.

2. Include outgoing and return conductors: loop resistance is 0.02293333 ohm.

3. At current 20 A, voltage drop is 0.458667 V.

4. Joule heating is I^2*R=9.173333 W across the loop.

5. Drop is 0.955556% of an illustrative 48 V bus.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The 48 V reference and resistivity are declared arithmetic assumptions, not an approved operating voltage or wire rating.

Connector contact resistance, flex life, thermal environment and protective-device coordination are excluded.

### K. Failure modes and troubleshooting

Forgetting the return conductor; using current averages to assess peak drop; assuming a connector shell name establishes current capacity.

### L. Practical exercises and extension tasks

1. Add measured connector contact resistance.

2. Evaluate duty-cycle RMS current for heating.

3. Propagate a warm-conductor resistance increase and compare drop.

### M. Connection to the Asimov research platform

Actual conductor, connector, fuse and insulation selection requires verified hardware specifications and installation-specific electrical review.

### N. Completion record

Record your chosen case, predicted trend, measured loop_resistance_ohm, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 65, Capacitor charging, stored energy and inrush screening. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 65 - Capacitor charging, stored energy and inrush screening

### A. The engineering question

Power electronics often contain input capacitance.

### B. Concepts and mathematical model

Connecting an uncharged capacitor to a voltage source can create a large transient limited by source and circuit impedance. A resistor-capacitor model explains initial current, charging time and stored energy, but real switching devices, supplies and precharge sequences require a reviewed design. This exercise does not prescribe a physical precharge circuit or safe component values; it makes the energy and timing quantities explicit.

I0=V/R; Vc(t)=V*(1-exp(-t/(R*C))); E_stored=0.5*C*V^2; t_95=-R*C*ln(0.05).

### C. Real-world meaning and limits

Use the released power topology and competent electrical review for actual actuator supply, battery, protection and discharge design.

### D. Architecture and data flow

Configuration (voltage, resistance, capacitance) -> numerical model -> initial_current_A, time_constant_s, charge_95_percent_time_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

voltage is Volts; resistance is ohms; capacitance is Farads. Values are educational, not a build prescription.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| voltage | 24 | Defined by the explicit chapter model and parameter contract |
| resistance | 10 | Defined by the explicit chapter model and parameter contract |
| capacitance | 0.002 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/65_inrush.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only resistance changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/65_inrush.py --case 0

.venv-book/bin/python expanded_lab/modules/65_inrush.py --case 3

.venv-book/bin/python expanded_lab/run.py inrush --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/65_inrush.py

### H. Walkthrough and design decisions

Analyze current, energy and charging time together. A large resistance reduces initial current but lengthens the charging interval; a nominal power rating alone does not specify pulse capability.

### I. Expected behavior and six worked cases

The controlled variable is resistance. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/65_inrush.png

Figure L65. initial current A as resistance changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | resistance | initial current A |
|---|---|---|
| 0 | 1 | 24 |
| 1 | 2 | 12 |
| 2 | 5 | 4.8 |
| 3 | 10 | 2.4 |
| 4 | 20 | 1.2 |
| 5 | 50 | 0.48 |

#### Worked case 0: resistance = 1

This case keeps the nominal configuration except for resistance=1. The full input is {"capacitance": 0.002, "resistance": 1.0, "voltage": 24.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial current A | 24 |
| time constant s | 0.002 |
| charge 95 percent time s | 0.00599146 |
| stored energy J | 0.576 |
| initial resistor power W | 576 |

1. Use illustrative source V=24 V, R=1 ohm and C=0.002 F.

2. Initial ideal charging current is 24.000000 A.

3. The RC time constant is 0.002000 s and 95% charge time is 0.005991 s.

4. Capacitor stored energy at full voltage is 0.576000 J.

5. Initial resistor power is 576.000000 W and decays with charging.

#### Worked case 1: resistance = 2

This case keeps the nominal configuration except for resistance=2. The full input is {"capacitance": 0.002, "resistance": 2.0, "voltage": 24.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial current A | 12 |
| time constant s | 0.004 |
| charge 95 percent time s | 0.01198293 |
| stored energy J | 0.576 |
| initial resistor power W | 288 |

1. Use illustrative source V=24 V, R=2 ohm and C=0.002 F.

2. Initial ideal charging current is 12.000000 A.

3. The RC time constant is 0.004000 s and 95% charge time is 0.011983 s.

4. Capacitor stored energy at full voltage is 0.576000 J.

5. Initial resistor power is 288.000000 W and decays with charging.

#### Worked case 2: resistance = 5

This case keeps the nominal configuration except for resistance=5. The full input is {"capacitance": 0.002, "resistance": 5.0, "voltage": 24.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial current A | 4.8 |
| time constant s | 0.01 |
| charge 95 percent time s | 0.02995732 |
| stored energy J | 0.576 |
| initial resistor power W | 115.2 |

1. Use illustrative source V=24 V, R=5 ohm and C=0.002 F.

2. Initial ideal charging current is 4.800000 A.

3. The RC time constant is 0.010000 s and 95% charge time is 0.029957 s.

4. Capacitor stored energy at full voltage is 0.576000 J.

5. Initial resistor power is 115.200000 W and decays with charging.

#### Worked case 3: resistance = 10

This case keeps the nominal configuration except for resistance=10. The full input is {"capacitance": 0.002, "resistance": 10.0, "voltage": 24.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial current A | 2.4 |
| time constant s | 0.02 |
| charge 95 percent time s | 0.05991465 |
| stored energy J | 0.576 |
| initial resistor power W | 57.6 |

1. Use illustrative source V=24 V, R=10 ohm and C=0.002 F.

2. Initial ideal charging current is 2.400000 A.

3. The RC time constant is 0.020000 s and 95% charge time is 0.059915 s.

4. Capacitor stored energy at full voltage is 0.576000 J.

5. Initial resistor power is 57.600000 W and decays with charging.

#### Worked case 4: resistance = 20

This case keeps the nominal configuration except for resistance=20. The full input is {"capacitance": 0.002, "resistance": 20.0, "voltage": 24.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial current A | 1.2 |
| time constant s | 0.04 |
| charge 95 percent time s | 0.11982929 |
| stored energy J | 0.576 |
| initial resistor power W | 28.8 |

1. Use illustrative source V=24 V, R=20 ohm and C=0.002 F.

2. Initial ideal charging current is 1.200000 A.

3. The RC time constant is 0.040000 s and 95% charge time is 0.119829 s.

4. Capacitor stored energy at full voltage is 0.576000 J.

5. Initial resistor power is 28.800000 W and decays with charging.

#### Worked case 5: resistance = 50

This case keeps the nominal configuration except for resistance=50. The full input is {"capacitance": 0.002, "resistance": 50.0, "voltage": 24.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial current A | 0.48 |
| time constant s | 0.1 |
| charge 95 percent time s | 0.29957323 |
| stored energy J | 0.576 |
| initial resistor power W | 11.52 |

1. Use illustrative source V=24 V, R=50 ohm and C=0.002 F.

2. Initial ideal charging current is 0.480000 A.

3. The RC time constant is 0.100000 s and 95% charge time is 0.299573 s.

4. Capacitor stored energy at full voltage is 0.576000 J.

5. Initial resistor power is 11.520000 W and decays with charging.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Stored energy can remain after source disconnection; a physical discharge/isolation procedure must verify it.

Resistor pulse energy, switching ratings, failure modes and supply behavior are not established by the ideal RC equation.

### K. Failure modes and troubleshooting

Ignoring stored energy after disconnect; assuming a supply current limit substitutes for all inrush protection; choosing components from one scalar calculation.

### L. Practical exercises and extension tasks

1. Calculate energy dissipated in the ideal resistor over the charge.

2. Model a partial charge before reconnection.

3. List fault cases a real precharge controller would have to detect.

### M. Connection to the Asimov research platform

Use the released power topology and competent electrical review for actual actuator supply, battery, protection and discharge design.

### N. Completion record

Record your chosen case, predicted trend, measured initial_current_A, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 66, Bidirectional calibration and hidden hysteresis. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 66 - Bidirectional calibration and hidden hysteresis

### A. The engineering question

A sensor calibration fitted in one direction may fail on reversal.

### B. Concepts and mathematical model

Backlash, friction and structural compliance can create direction-dependent observations that a single scale-and-offset model cannot represent. The correct response is to expose the residual structure rather than silently widen a tolerance. This experiment generates forward and reverse measurements with a known hysteresis term, fits a shared linear calibration and quantifies the remaining directional bias.

measurement=a*reference+b+direction*hysteresis+noise; a shared fit cannot remove opposite signed direction offsets.

### C. Real-world meaning and limits

Joint and ankle calibration should include reversals, load conditions and temperature ranges relevant to the intended physical skill.

### D. Architecture and data flow

Configuration (hysteresis) -> numerical model -> fitted_scale, fitted_offset_rad, pooled_residual_rmse_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

hysteresis is the signed measurement offset magnitude in radians for forward versus reverse motion.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| hysteresis | 0.005 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/66_hysteresis_calibration.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only hysteresis changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/66_hysteresis_calibration.py --case 0

.venv-book/bin/python expanded_lab/modules/66_hysteresis_calibration.py --case 3

.venv-book/bin/python expanded_lab/run.py hysteresis_calibration --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/66_hysteresis_calibration.py

### H. Walkthrough and design decisions

Preserve direction labels during data collection. A residual-versus-direction comparison distinguishes hysteresis from ordinary zero-mean measurement noise.

### I. Expected behavior and six worked cases

The controlled variable is hysteresis. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/66_hysteresis_calibration.png

Figure L66. fitted scale as hysteresis changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | hysteresis | fitted scale |
|---|---|---|
| 0 | 0 | 1.0197408 |
| 1 | 0.001 | 1.0197408 |
| 2 | 0.002 | 1.0197408 |
| 3 | 0.005 | 1.0197408 |
| 4 | 0.01 | 1.0197408 |
| 5 | 0.02 | 1.0197408 |

#### Worked case 0: hysteresis = 0

This case keeps the nominal configuration except for hysteresis=0. The full input is {"hysteresis": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fitted scale | 1.0197408 |
| fitted offset rad | 0.00998084 |
| pooled residual rmse rad | 0.00094312 |
| forward bias rad | -0.00005539 |
| reverse bias rad | 0.00005539 |
| directional separation rad | -0.00011078 |

1. True scale is 1.02 and offset 0.01 rad.

2. Add directional offset +/-0 rad and 0.001 rad noise.

3. Fit one shared scale/offset to both directions: [1.0197407959775369, 0.00998083550852672].

4. Forward residual mean is -0.000055 rad; reverse mean is 0.000055 rad.

5. Directional separation is -0.000111 rad, revealing structure hidden by a pooled fit.

#### Worked case 1: hysteresis = 0.001

This case keeps the nominal configuration except for hysteresis=0.001. The full input is {"hysteresis": 0.001}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fitted scale | 1.0197408 |
| fitted offset rad | 0.00998084 |
| pooled residual rmse rad | 0.00133368 |
| forward bias rad | 0.00094461 |
| reverse bias rad | -0.00094461 |
| directional separation rad | 0.00188922 |

1. True scale is 1.02 and offset 0.01 rad.

2. Add directional offset +/-0.001 rad and 0.001 rad noise.

3. Fit one shared scale/offset to both directions: [1.0197407959775364, 0.009980835508526728].

4. Forward residual mean is 0.000945 rad; reverse mean is -0.000945 rad.

5. Directional separation is 0.001889 rad, revealing structure hidden by a pooled fit.

#### Worked case 2: hysteresis = 0.002

This case keeps the nominal configuration except for hysteresis=0.002. The full input is {"hysteresis": 0.002}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fitted scale | 1.0197408 |
| fitted offset rad | 0.00998084 |
| pooled residual rmse rad | 0.00216054 |
| forward bias rad | 0.00194461 |
| reverse bias rad | -0.00194461 |
| directional separation rad | 0.00388922 |

1. True scale is 1.02 and offset 0.01 rad.

2. Add directional offset +/-0.002 rad and 0.001 rad noise.

3. Fit one shared scale/offset to both directions: [1.0197407959775364, 0.009980835508526721].

4. Forward residual mean is 0.001945 rad; reverse mean is -0.001945 rad.

5. Directional separation is 0.003889 rad, revealing structure hidden by a pooled fit.

#### Worked case 3: hysteresis = 0.005

This case keeps the nominal configuration except for hysteresis=0.005. The full input is {"hysteresis": 0.005}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fitted scale | 1.0197408 |
| fitted offset rad | 0.00998084 |
| pooled residual rmse rad | 0.00503345 |
| forward bias rad | 0.00494461 |
| reverse bias rad | -0.00494461 |
| directional separation rad | 0.00988922 |

1. True scale is 1.02 and offset 0.01 rad.

2. Add directional offset +/-0.005 rad and 0.001 rad noise.

3. Fit one shared scale/offset to both directions: [1.0197407959775364, 0.009980835508526726].

4. Forward residual mean is 0.004945 rad; reverse mean is -0.004945 rad.

5. Directional separation is 0.009889 rad, revealing structure hidden by a pooled fit.

#### Worked case 4: hysteresis = 0.01

This case keeps the nominal configuration except for hysteresis=0.01. The full input is {"hysteresis": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fitted scale | 1.0197408 |
| fitted offset rad | 0.00998084 |
| pooled residual rmse rad | 0.00998908 |
| forward bias rad | 0.00994461 |
| reverse bias rad | -0.00994461 |
| directional separation rad | 0.01988922 |

1. True scale is 1.02 and offset 0.01 rad.

2. Add directional offset +/-0.01 rad and 0.001 rad noise.

3. Fit one shared scale/offset to both directions: [1.0197407959775364, 0.009980835508526726].

4. Forward residual mean is 0.009945 rad; reverse mean is -0.009945 rad.

5. Directional separation is 0.019889 rad, revealing structure hidden by a pooled fit.

#### Worked case 5: hysteresis = 0.02

This case keeps the nominal configuration except for hysteresis=0.02. The full input is {"hysteresis": 0.02}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| fitted scale | 1.0197408 |
| fitted offset rad | 0.00998084 |
| pooled residual rmse rad | 0.01996682 |
| forward bias rad | 0.01994461 |
| reverse bias rad | -0.01994461 |
| directional separation rad | 0.03988922 |

1. True scale is 1.02 and offset 0.01 rad.

2. Add directional offset +/-0.02 rad and 0.001 rad noise.

3. Fit one shared scale/offset to both directions: [1.0197407959775366, 0.009980835508526723].

4. Forward residual mean is 0.019945 rad; reverse mean is -0.019945 rad.

5. Directional separation is 0.039889 rad, revealing structure hidden by a pooled fit.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

A low aggregate fit error can still conceal a consistent direction-dependent error relevant to reaching or balance.

A calibration model should match the phenomenon and be validated on independent bidirectional trajectories.

### K. Failure modes and troubleshooting

Fitting only one sweep direction; treating backlash as a fixed zero offset; using the same calibration trajectories as final validation.

### L. Practical exercises and extension tasks

1. Fit an explicit direction-dependent term and compare held-out residuals.

2. Add temperature dependence and test a two-factor model.

3. Detect reversals from velocity with a deadband.

### M. Connection to the Asimov research platform

Joint and ankle calibration should include reversals, load conditions and temperature ranges relevant to the intended physical skill.

### N. Completion record

Record your chosen case, predicted trend, measured fitted_scale, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 67, Commissioning evidence as a dependency graph. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 67 - Commissioning evidence as a dependency graph

### A. The engineering question

Readiness is not a single checklist checkbox.

### B. Concepts and mathematical model

A higher-level test depends on lower-level evidence, and an updated hardware or software revision can invalidate earlier results. A dependency graph makes that structure explicit. This laboratory evaluates synthetic evidence records and calculates which capabilities are blocked when one prerequisite becomes stale. The software audit cannot independently verify a physical test; it can only enforce completeness and revision consistency of recorded evidence.

gate passes iff its own record is PASS and revision-matched and every prerequisite recursively passes.

### C. Real-world meaning and limits

Physical readiness remains no-go until actual tests and reviewed evidence replace synthetic fixtures and all required protections pass.

### D. Architecture and data flow

Configuration (stale_gate_index) -> numerical model -> passing_gate_count, blocked_gate_count, supported_limb_ready -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

stale_gate_index selects a synthetic record with an old revision; -1 leaves every artificial record current.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| stale_gate_index | 2 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/67_commissioning_evidence.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only stale_gate_index changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/67_commissioning_evidence.py --case 0

.venv-book/bin/python expanded_lab/modules/67_commissioning_evidence.py --case 3

.venv-book/bin/python expanded_lab/run.py commissioning_evidence --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/67_commissioning_evidence.py

### H. Walkthrough and design decisions

Recursive evaluation propagates a lower-level invalidation upward. Memoization avoids repeated work; a production graph should also reject dependency cycles.

### I. Expected behavior and six worked cases

The controlled variable is stale_gate_index. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/67_commissioning_evidence.png

Figure L67. passing gate count as stale_gate_index changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | stale_gate_index | passing gate count |
|---|---|---|
| 0 | -1 | 7 |
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 2 | 2 |
| 4 | 4 | 4 |
| 5 | 6 | 6 |

#### Worked case 0: stale_gate_index = -1

This case keeps the nominal configuration except for stale_gate_index=-1. The full input is {"stale_gate_index": -1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| passing gate count | 7 |
| blocked gate count | 0 |
| supported limb ready | 1 |
| physical skill ready | 1 |
| walking ready | 1 |

1. The synthetic gate order is ['inspection', 'isolation', 'single_joint', 'calibration', 'supported_limb', 'physical_skill', 'walking'].

2. Stale gate index is -1; records must match revision r1.

3. Evaluate each gate recursively, requiring all prerequisite evidence.

4. Results are {'inspection': True, 'isolation': True, 'single_joint': True, 'calibration': True, 'supported_limb': True, 'physical_skill': True, 'walking': True}.

5. Total passing count is 7; blocked count is 0.

#### Worked case 1: stale_gate_index = 0

This case keeps the nominal configuration except for stale_gate_index=0. The full input is {"stale_gate_index": 0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| passing gate count | 0 |
| blocked gate count | 7 |
| supported limb ready | 0 |
| physical skill ready | 0 |
| walking ready | 0 |

1. The synthetic gate order is ['inspection', 'isolation', 'single_joint', 'calibration', 'supported_limb', 'physical_skill', 'walking'].

2. Stale gate index is 0; records must match revision r1.

3. Evaluate each gate recursively, requiring all prerequisite evidence.

4. Results are {'inspection': False, 'isolation': False, 'single_joint': False, 'calibration': False, 'supported_limb': False, 'physical_skill': False, 'walking': False}.

5. Total passing count is 0; blocked count is 7.

#### Worked case 2: stale_gate_index = 1

This case keeps the nominal configuration except for stale_gate_index=1. The full input is {"stale_gate_index": 1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| passing gate count | 1 |
| blocked gate count | 6 |
| supported limb ready | 0 |
| physical skill ready | 0 |
| walking ready | 0 |

1. The synthetic gate order is ['inspection', 'isolation', 'single_joint', 'calibration', 'supported_limb', 'physical_skill', 'walking'].

2. Stale gate index is 1; records must match revision r1.

3. Evaluate each gate recursively, requiring all prerequisite evidence.

4. Results are {'inspection': True, 'isolation': False, 'single_joint': False, 'calibration': False, 'supported_limb': False, 'physical_skill': False, 'walking': False}.

5. Total passing count is 1; blocked count is 6.

#### Worked case 3: stale_gate_index = 2

This case keeps the nominal configuration except for stale_gate_index=2. The full input is {"stale_gate_index": 2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| passing gate count | 2 |
| blocked gate count | 5 |
| supported limb ready | 0 |
| physical skill ready | 0 |
| walking ready | 0 |

1. The synthetic gate order is ['inspection', 'isolation', 'single_joint', 'calibration', 'supported_limb', 'physical_skill', 'walking'].

2. Stale gate index is 2; records must match revision r1.

3. Evaluate each gate recursively, requiring all prerequisite evidence.

4. Results are {'inspection': True, 'isolation': True, 'single_joint': False, 'calibration': False, 'supported_limb': False, 'physical_skill': False, 'walking': False}.

5. Total passing count is 2; blocked count is 5.

#### Worked case 4: stale_gate_index = 4

This case keeps the nominal configuration except for stale_gate_index=4. The full input is {"stale_gate_index": 4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| passing gate count | 4 |
| blocked gate count | 3 |
| supported limb ready | 0 |
| physical skill ready | 0 |
| walking ready | 0 |

1. The synthetic gate order is ['inspection', 'isolation', 'single_joint', 'calibration', 'supported_limb', 'physical_skill', 'walking'].

2. Stale gate index is 4; records must match revision r1.

3. Evaluate each gate recursively, requiring all prerequisite evidence.

4. Results are {'inspection': True, 'isolation': True, 'single_joint': True, 'calibration': True, 'supported_limb': False, 'physical_skill': False, 'walking': False}.

5. Total passing count is 4; blocked count is 3.

#### Worked case 5: stale_gate_index = 6

This case keeps the nominal configuration except for stale_gate_index=6. The full input is {"stale_gate_index": 6}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| passing gate count | 6 |
| blocked gate count | 1 |
| supported limb ready | 1 |
| physical skill ready | 1 |
| walking ready | 0 |

1. The synthetic gate order is ['inspection', 'isolation', 'single_joint', 'calibration', 'supported_limb', 'physical_skill', 'walking'].

2. Stale gate index is 6; records must match revision r1.

3. Evaluate each gate recursively, requiring all prerequisite evidence.

4. Results are {'inspection': True, 'isolation': True, 'single_joint': True, 'calibration': True, 'supported_limb': True, 'physical_skill': True, 'walking': False}.

5. Total passing count is 6; blocked count is 1.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

All PASS records here are artificial test fixtures, not physical commissioning evidence.

A real record should include procedure, threshold rationale, instrument, raw artifact, date, reviewer and exact configuration.

### K. Failure modes and troubleshooting

Treating a completed checkbox as permanent across revisions; skipping independent evidence verification; inferring physical readiness from a software result.

### L. Practical exercises and extension tasks

1. Add model, firmware and calibration hashes to each record.

2. Detect dependency cycles and missing gate definitions.

3. Generate a minimal retest plan after one configuration change.

### M. Connection to the Asimov research platform

Physical readiness remains no-go until actual tests and reviewed evidence replace synthetic fixtures and all required protections pass.

### N. Completion record

Record your chosen case, predicted trend, measured passing_gate_count, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 68, Immutable experiment manifests and configuration identity. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 68 - Immutable experiment manifests and configuration identity

### A. The engineering question

Reproducibility depends on more than a Git commit.

### B. Concepts and mathematical model

Model files, calibration, policy weights, normalizer parameters, environment packages and test conditions can change behavior independently. A manifest should identify every relevant artifact and distinguish content identity from a filename. Canonical serialization and cryptographic hashes help detect changes, but they do not establish that an artifact is correct or trusted. This laboratory changes one configuration field and traces the resulting manifest identity.

artifact_hash=SHA256(bytes); manifest_hash=SHA256(canonical JSON containing artifact hashes and experiment parameters).

### C. Real-world meaning and limits

Physical deployment records need exact model, firmware, calibration and policy identities plus a documented rollback bundle.

### D. Architecture and data flow

Configuration (action_scale) -> numerical model -> content_identity_changed, changed_field_count, action_scale -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

action_scale is the normalized-to-joint action multiplier in this manifest example; it is not a physical command recommendation.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| action_scale | 0.15 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/68_manifest_hashes.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only action_scale changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/68_manifest_hashes.py --case 0

.venv-book/bin/python expanded_lab/modules/68_manifest_hashes.py --case 3

.venv-book/bin/python expanded_lab/run.py manifest_hashes --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/68_manifest_hashes.py

### H. Walkthrough and design decisions

Canonical serialization avoids irrelevant formatting differences. The changed-field list explains the semantic change rather than leaving reviewers with only two opaque hashes.

### I. Expected behavior and six worked cases

The controlled variable is action_scale. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/68_manifest_hashes.png

Figure L68. content identity changed as action_scale changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | action_scale | content identity changed |
|---|---|---|
| 0 | 0.05 | 1 |
| 1 | 0.1 | 1 |
| 2 | 0.15 | 0 |
| 3 | 0.2 | 1 |
| 4 | 0.25 | 1 |
| 5 | 0.3 | 1 |

#### Worked case 0: action_scale = 0.05

This case keeps the nominal configuration except for action_scale=0.05. The full input is {"action_scale": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| content identity changed | 1 |
| changed field count | 1 |
| action scale | 0.05 |
| scale ratio to baseline | 0.33333333 |

1. Baseline fields are {'model': 'sha256:model_example', 'policy': 'sha256:policy_example', 'calibration': 'calibration_r1', 'seed': 7, 'control_period': 0.02, 'action_scale': 0.15}.

2. Change action_scale to 0.05; changed fields are ['action_scale'].

3. Baseline canonical manifest hash is b3ffecbc531968289a1458991e696fb02a5890cfcec06fe38f7b3c688db3d93d.

4. Candidate canonical manifest hash is d92cea4610c05499c458db26ae8e692d0c46c79f06d10c2530d1698ff1414c35.

5. Reordering dictionary insertion order preserves the canonical hash, verified by assertion.

#### Worked case 1: action_scale = 0.1

This case keeps the nominal configuration except for action_scale=0.1. The full input is {"action_scale": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| content identity changed | 1 |
| changed field count | 1 |
| action scale | 0.1 |
| scale ratio to baseline | 0.66666667 |

1. Baseline fields are {'model': 'sha256:model_example', 'policy': 'sha256:policy_example', 'calibration': 'calibration_r1', 'seed': 7, 'control_period': 0.02, 'action_scale': 0.15}.

2. Change action_scale to 0.1; changed fields are ['action_scale'].

3. Baseline canonical manifest hash is b3ffecbc531968289a1458991e696fb02a5890cfcec06fe38f7b3c688db3d93d.

4. Candidate canonical manifest hash is e7250d2ab441055d5893d940a042266adda063850cc944a393a2d74dd54abf8c.

5. Reordering dictionary insertion order preserves the canonical hash, verified by assertion.

#### Worked case 2: action_scale = 0.15

This case keeps the nominal configuration except for action_scale=0.15. The full input is {"action_scale": 0.15}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| content identity changed | 0 |
| changed field count | 0 |
| action scale | 0.15 |
| scale ratio to baseline | 1 |

1. Baseline fields are {'model': 'sha256:model_example', 'policy': 'sha256:policy_example', 'calibration': 'calibration_r1', 'seed': 7, 'control_period': 0.02, 'action_scale': 0.15}.

2. Change action_scale to 0.15; changed fields are [].

3. Baseline canonical manifest hash is b3ffecbc531968289a1458991e696fb02a5890cfcec06fe38f7b3c688db3d93d.

4. Candidate canonical manifest hash is b3ffecbc531968289a1458991e696fb02a5890cfcec06fe38f7b3c688db3d93d.

5. Reordering dictionary insertion order preserves the canonical hash, verified by assertion.

#### Worked case 3: action_scale = 0.2

This case keeps the nominal configuration except for action_scale=0.2. The full input is {"action_scale": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| content identity changed | 1 |
| changed field count | 1 |
| action scale | 0.2 |
| scale ratio to baseline | 1.33333333 |

1. Baseline fields are {'model': 'sha256:model_example', 'policy': 'sha256:policy_example', 'calibration': 'calibration_r1', 'seed': 7, 'control_period': 0.02, 'action_scale': 0.15}.

2. Change action_scale to 0.2; changed fields are ['action_scale'].

3. Baseline canonical manifest hash is b3ffecbc531968289a1458991e696fb02a5890cfcec06fe38f7b3c688db3d93d.

4. Candidate canonical manifest hash is 0a5cd509dcf3fae033998f9f3586297bf17339f56f376b1905b93239ee9f1de0.

5. Reordering dictionary insertion order preserves the canonical hash, verified by assertion.

#### Worked case 4: action_scale = 0.25

This case keeps the nominal configuration except for action_scale=0.25. The full input is {"action_scale": 0.25}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| content identity changed | 1 |
| changed field count | 1 |
| action scale | 0.25 |
| scale ratio to baseline | 1.66666667 |

1. Baseline fields are {'model': 'sha256:model_example', 'policy': 'sha256:policy_example', 'calibration': 'calibration_r1', 'seed': 7, 'control_period': 0.02, 'action_scale': 0.15}.

2. Change action_scale to 0.25; changed fields are ['action_scale'].

3. Baseline canonical manifest hash is b3ffecbc531968289a1458991e696fb02a5890cfcec06fe38f7b3c688db3d93d.

4. Candidate canonical manifest hash is db7d39a86bf237b483c39e3f66dae19308764904e79becb4947b4ed888db5f38.

5. Reordering dictionary insertion order preserves the canonical hash, verified by assertion.

#### Worked case 5: action_scale = 0.3

This case keeps the nominal configuration except for action_scale=0.3. The full input is {"action_scale": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| content identity changed | 1 |
| changed field count | 1 |
| action scale | 0.3 |
| scale ratio to baseline | 2 |

1. Baseline fields are {'model': 'sha256:model_example', 'policy': 'sha256:policy_example', 'calibration': 'calibration_r1', 'seed': 7, 'control_period': 0.02, 'action_scale': 0.15}.

2. Change action_scale to 0.3; changed fields are ['action_scale'].

3. Baseline canonical manifest hash is b3ffecbc531968289a1458991e696fb02a5890cfcec06fe38f7b3c688db3d93d.

4. Candidate canonical manifest hash is 1ed29eb5869766785dd5c359085a7b513fea7defddeda163fcaf5c090e8516a4.

5. Reordering dictionary insertion order preserves the canonical hash, verified by assertion.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The model/policy hash strings are explicit fictional labels in this unit exercise; a real manifest must hash actual file bytes.

A hash detects content changes but does not prove provenance, authenticity, compatibility or safety.

### K. Failure modes and troubleshooting

Hashing a path instead of file bytes; forgetting calibration/normalizer artifacts; accepting an unchanged source commit as proof of unchanged behavior.

### L. Practical exercises and extension tasks

1. Build a manifest from actual supplied lab files.

2. Include the resolved package lock and model commit.

3. Verify a release bundle before allowing offline replay or activation.

### M. Connection to the Asimov research platform

Physical deployment records need exact model, firmware, calibration and policy identities plus a documented rollback bundle.

### N. Completion record

Record your chosen case, predicted trend, measured content_identity_changed, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 69, Fault injection, diagnostic coverage and remaining blind spots. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 69 - Fault injection, diagnostic coverage and remaining blind spots

### A. The engineering question

A protection claim should name the faults considered and the evidence for detecting and responding to them.

### B. Concepts and mathematical model

Injecting a convenient subset of faults can produce a misleading coverage percentage. Some failures are independent, some share causes, and some defeat both the controller and monitor. This laboratory builds a synthetic fault campaign with known detection probabilities to show the difference between observed detection, fault prevalence weighting and untested categories. The numbers are teaching probabilities, not measured reliability data.

observed coverage=detected/injected; weighted residual probability=sum(fault_weight*(1-detection_probability)) under stated assumptions.

### C. Real-world meaning and limits

Actual protective systems need hazard-specific design and independent evidence; this campaign is a method exercise only.

### D. Architecture and data flow

Configuration (sensor_fault_detection) -> numerical model -> observed_detection_fraction, expected_weighted_detection, expected_undetected_fraction -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

sensor_fault_detection is an assumed probability for a synthetic sensor-bias fault; other campaign parameters remain fixed.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| sensor_fault_detection | 0.5 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/69_failure_modes.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only sensor_fault_detection changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/69_failure_modes.py --case 0

.venv-book/bin/python expanded_lab/modules/69_failure_modes.py --case 3

.venv-book/bin/python expanded_lab/run.py failure_modes --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/69_failure_modes.py

### H. Walkthrough and design decisions

Report per-category injections as well as aggregate coverage. A frequent easy-to-detect fault can dominate the aggregate while a serious blind spot remains.

### I. Expected behavior and six worked cases

The controlled variable is sensor_fault_detection. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/69_failure_modes.png

Figure L69. observed detection fraction as sensor_fault_detection changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | sensor_fault_detection | observed detection fraction |
|---|---|---|
| 0 | 0 | 0.575 |
| 1 | 0.25 | 0.6485 |
| 2 | 0.5 | 0.715 |
| 3 | 0.75 | 0.7945 |
| 4 | 0.9 | 0.8435 |
| 5 | 0.99 | 0.87 |

#### Worked case 0: sensor_fault_detection = 0

This case keeps the nominal configuration except for sensor_fault_detection=0. The full input is {"sensor_fault_detection": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed detection fraction | 0.575 |
| expected weighted detection | 0.575 |
| expected undetected fraction | 0.425 |
| undetected fault count | 850 |
| sensor bias detection assumption | 0 |

1. Inject 2000 synthetic faults with category counts {'stale': 568, 'range': 410, 'sensor_bias': 598, 'power_loss': 424}.

2. Assumed category detection probabilities are [0.99, 0.99, 0.0, 0.4].

3. Weighted expected detection is 0.575000.

4. The seeded campaign observes detection fraction 0.575000.

5. Expected residual undetected fraction is 0.425000 under the chosen artificial mixture.

#### Worked case 1: sensor_fault_detection = 0.25

This case keeps the nominal configuration except for sensor_fault_detection=0.25. The full input is {"sensor_fault_detection": 0.25}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed detection fraction | 0.6485 |
| expected weighted detection | 0.65 |
| expected undetected fraction | 0.35 |
| undetected fault count | 703 |
| sensor bias detection assumption | 0.25 |

1. Inject 2000 synthetic faults with category counts {'stale': 568, 'range': 410, 'sensor_bias': 598, 'power_loss': 424}.

2. Assumed category detection probabilities are [0.99, 0.99, 0.25, 0.4].

3. Weighted expected detection is 0.650000.

4. The seeded campaign observes detection fraction 0.648500.

5. Expected residual undetected fraction is 0.350000 under the chosen artificial mixture.

#### Worked case 2: sensor_fault_detection = 0.5

This case keeps the nominal configuration except for sensor_fault_detection=0.5. The full input is {"sensor_fault_detection": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed detection fraction | 0.715 |
| expected weighted detection | 0.725 |
| expected undetected fraction | 0.275 |
| undetected fault count | 570 |
| sensor bias detection assumption | 0.5 |

1. Inject 2000 synthetic faults with category counts {'stale': 568, 'range': 410, 'sensor_bias': 598, 'power_loss': 424}.

2. Assumed category detection probabilities are [0.99, 0.99, 0.5, 0.4].

3. Weighted expected detection is 0.725000.

4. The seeded campaign observes detection fraction 0.715000.

5. Expected residual undetected fraction is 0.275000 under the chosen artificial mixture.

#### Worked case 3: sensor_fault_detection = 0.75

This case keeps the nominal configuration except for sensor_fault_detection=0.75. The full input is {"sensor_fault_detection": 0.75}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed detection fraction | 0.7945 |
| expected weighted detection | 0.8 |
| expected undetected fraction | 0.2 |
| undetected fault count | 411 |
| sensor bias detection assumption | 0.75 |

1. Inject 2000 synthetic faults with category counts {'stale': 568, 'range': 410, 'sensor_bias': 598, 'power_loss': 424}.

2. Assumed category detection probabilities are [0.99, 0.99, 0.75, 0.4].

3. Weighted expected detection is 0.800000.

4. The seeded campaign observes detection fraction 0.794500.

5. Expected residual undetected fraction is 0.200000 under the chosen artificial mixture.

#### Worked case 4: sensor_fault_detection = 0.9

This case keeps the nominal configuration except for sensor_fault_detection=0.9. The full input is {"sensor_fault_detection": 0.9}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed detection fraction | 0.8435 |
| expected weighted detection | 0.845 |
| expected undetected fraction | 0.155 |
| undetected fault count | 313 |
| sensor bias detection assumption | 0.9 |

1. Inject 2000 synthetic faults with category counts {'stale': 568, 'range': 410, 'sensor_bias': 598, 'power_loss': 424}.

2. Assumed category detection probabilities are [0.99, 0.99, 0.9, 0.4].

3. Weighted expected detection is 0.845000.

4. The seeded campaign observes detection fraction 0.843500.

5. Expected residual undetected fraction is 0.155000 under the chosen artificial mixture.

#### Worked case 5: sensor_fault_detection = 0.99

This case keeps the nominal configuration except for sensor_fault_detection=0.99. The full input is {"sensor_fault_detection": 0.99}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed detection fraction | 0.87 |
| expected weighted detection | 0.872 |
| expected undetected fraction | 0.128 |
| undetected fault count | 260 |
| sensor bias detection assumption | 0.99 |

1. Inject 2000 synthetic faults with category counts {'stale': 568, 'range': 410, 'sensor_bias': 598, 'power_loss': 424}.

2. Assumed category detection probabilities are [0.99, 0.99, 0.99, 0.4].

3. Weighted expected detection is 0.872000.

4. The seeded campaign observes detection fraction 0.870000.

5. Expected residual undetected fraction is 0.128000 under the chosen artificial mixture.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The category mixture and detection probabilities are invented experiment inputs and cannot establish a physical safety integrity level.

Detection alone is incomplete: the protective response, common-cause failures and consequences must also be evaluated.

### K. Failure modes and troubleshooting

Equating detection with prevention; claiming reliability from invented fault weights; ignoring a common power or software failure affecting both monitor and controller.

### L. Practical exercises and extension tasks

1. Calculate coverage per fault category with confidence intervals.

2. Inject a common-cause monitor failure.

3. Add response-time and physical-outcome checks to the campaign definition.

### M. Connection to the Asimov research platform

Actual protective systems need hazard-specific design and independent evidence; this campaign is a method exercise only.

### N. Completion record

Record your chosen case, predicted trend, measured observed_detection_fraction, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 70, An integrated synthetic joint with perception, gating and fault recovery. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 70 - An integrated synthetic joint with perception, gating and fault recovery

### A. The engineering question

The final numerical capstone combines a simple observation, a bounded skill request, a feedback controller, telemetry and a latched fault.

### B. Concepts and mathematical model

It remains a fictional one-axis plant, so every equation and state transition is inspectable. The point is to test the complete chain and demonstrate that a fault blocks further motion authority. A physical backend is intentionally absent. Transfer to the supported Asimov simulation is the next integration exercise; transfer to hardware requires its separate commissioning evidence.

plant: I*q_ddot=u-b*q_dot; skill target is bounded; stale command age latches fault; latched state disables new actuation in the synthetic plant.

### C. Real-world meaning and limits

Reuse the architecture and tests, not the synthetic plant parameters or zero-torque stop assumption, when building a physical demonstration.

### D. Architecture and data flow

Configuration (dropout_start) -> numerical model -> final_position_rad, peak_applied_torque_Nm, tracking_rmse_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

dropout_start is the time in seconds when synthetic command refresh ends; five seconds means no dropout during the four-second run.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| dropout_start | 2 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/70_capstone.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only dropout_start changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/70_capstone.py --case 0

.venv-book/bin/python expanded_lab/modules/70_capstone.py --case 3

.venv-book/bin/python expanded_lab/run.py capstone --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/70_capstone.py

### H. Walkthrough and design decisions

The state machine owns actuation permission, while the controller computes a limited command only in EXECUTE. The plant continues evolving after a fault, exposing why disabling output is not the same as freezing mechanics.

### I. Expected behavior and six worked cases

The controlled variable is dropout_start. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/70_capstone.png

Figure L70. final position rad as dropout_start changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | dropout_start | final position rad |
|---|---|---|
| 0 | 0.5 | 0.03950397 |
| 1 | 1 | 0.09063787 |
| 2 | 1.5 | 0.10140148 |
| 3 | 2 | 0.06055133 |
| 4 | 3 | -0.00205178 |
| 5 | 5 | 2.0539015e-06 |

#### Worked case 0: dropout_start = 0.5

This case keeps the nominal configuration except for dropout_start=0.5. The full input is {"dropout_start": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final position rad | 0.03950397 |
| peak applied torque Nm | 0.02219542 |
| tracking rmse rad | 0.0366836 |
| fault latched | 1 |
| fault time s | 0.6 |

1. The synthetic object observation enables only a predefined 0.1 rad peak supported-style gesture.

2. Command refresh stops at t=0.5 s; timeout is 0.1 s.

3. A stale command latches FAULT and removes torque authority in this unloaded numerical plant.

4. Final state is FAULT; fault time is 0.6.

5. Peak torque is 0.022195 Nm; final position is 0.039504 rad and RMSE is 0.036684 rad.

#### Worked case 1: dropout_start = 1

This case keeps the nominal configuration except for dropout_start=1. The full input is {"dropout_start": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final position rad | 0.09063787 |
| peak applied torque Nm | 0.0226765 |
| tracking rmse rad | 0.05663015 |
| fault latched | 1 |
| fault time s | 1.098 |

1. The synthetic object observation enables only a predefined 0.1 rad peak supported-style gesture.

2. Command refresh stops at t=1 s; timeout is 0.1 s.

3. A stale command latches FAULT and removes torque authority in this unloaded numerical plant.

4. Final state is FAULT; fault time is 1.098.

5. Peak torque is 0.022677 Nm; final position is 0.090638 rad and RMSE is 0.056630 rad.

#### Worked case 2: dropout_start = 1.5

This case keeps the nominal configuration except for dropout_start=1.5. The full input is {"dropout_start": 1.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final position rad | 0.10140148 |
| peak applied torque Nm | 0.0226765 |
| tracking rmse rad | 0.06385488 |
| fault latched | 1 |
| fault time s | 1.598 |

1. The synthetic object observation enables only a predefined 0.1 rad peak supported-style gesture.

2. Command refresh stops at t=1.5 s; timeout is 0.1 s.

3. A stale command latches FAULT and removes torque authority in this unloaded numerical plant.

4. Final state is FAULT; fault time is 1.598.

5. Peak torque is 0.022677 Nm; final position is 0.101401 rad and RMSE is 0.063855 rad.

#### Worked case 3: dropout_start = 2

This case keeps the nominal configuration except for dropout_start=2. The full input is {"dropout_start": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final position rad | 0.06055133 |
| peak applied torque Nm | 0.0226765 |
| tracking rmse rad | 0.03767868 |
| fault latched | 1 |
| fault time s | 2.1 |

1. The synthetic object observation enables only a predefined 0.1 rad peak supported-style gesture.

2. Command refresh stops at t=2 s; timeout is 0.1 s.

3. A stale command latches FAULT and removes torque authority in this unloaded numerical plant.

4. Final state is FAULT; fault time is 2.1.

5. Peak torque is 0.022677 Nm; final position is 0.060551 rad and RMSE is 0.037679 rad.

#### Worked case 4: dropout_start = 3

This case keeps the nominal configuration except for dropout_start=3. The full input is {"dropout_start": 3.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final position rad | -0.00205178 |
| peak applied torque Nm | 0.02271077 |
| tracking rmse rad | 0.01074721 |
| fault latched | 1 |
| fault time s | 3.1 |

1. The synthetic object observation enables only a predefined 0.1 rad peak supported-style gesture.

2. Command refresh stops at t=3 s; timeout is 0.1 s.

3. A stale command latches FAULT and removes torque authority in this unloaded numerical plant.

4. Final state is FAULT; fault time is 3.1.

5. Peak torque is 0.022711 Nm; final position is -0.002052 rad and RMSE is 0.010747 rad.

#### Worked case 5: dropout_start = 5

This case keeps the nominal configuration except for dropout_start=5. The full input is {"dropout_start": 5.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| final position rad | 2.0539015e-06 |
| peak applied torque Nm | 0.02271077 |
| tracking rmse rad | 0.01072771 |
| fault latched | 0 |
| fault time s | -1 |

1. The synthetic object observation enables only a predefined 0.1 rad peak supported-style gesture.

2. Command refresh stops at t=5 s; timeout is 0.1 s.

3. A stale command latches FAULT and removes torque authority in this unloaded numerical plant.

4. Final state is EXECUTE; fault time is None.

5. Peak torque is 0.022711 Nm; final position is 0.000002 rad and RMSE is 0.010728 rad.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Zero torque after a fault is suitable only for this explicitly unloaded damped synthetic plant; a loaded physical robot needs a reviewed support/stop strategy.

No automatic healthy-message transition leaves the fault state, and no physical bus is opened.

### K. Failure modes and troubleshooting

Assuming a stopped software loop stops physical motion; evaluating only the no-fault case; declaring completion without measured feedback.

### L. Practical exercises and extension tasks

1. Add feedback-based completion and a separate CANCEL state.

2. Replay the same target into the supported Asimov simulator.

3. Inject nonfinite observations and reversed encoder direction, then verify rejection and diagnostic evidence.

### M. Connection to the Asimov research platform

Reuse the architecture and tests, not the synthetic plant parameters or zero-torque stop assumption, when building a physical demonstration.

### N. Completion record

Record your chosen case, predicted trend, measured final_position_rad, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Return to the supported Asimov perception-to-gesture project with the quantitative checks from these laboratories. Release only the capabilities supported by actual simulation and commissioning evidence.
