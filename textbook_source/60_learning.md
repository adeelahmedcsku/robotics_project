# Part XI - Learning algorithms, evaluation and embodied skills

Before training a difficult humanoid behavior, verify the mathematics of rewards, returns, policy updates, action processing and evaluation. Small deterministic examples are faster to diagnose than a million-step rollout. The learning laboratories connect algorithmic definitions with the deployed observation/action interface, then connect perception evidence to an allowlisted skill. A reward curve, detector confidence or successful API call cannot substitute for measured task completion.

## Laboratory 51 - Markov decision processes and discounted reward

### A. The engineering question

A reward function expresses what training should favor, but its meaning depends on episode duration, timestep and discounting.

### B. Concepts and mathematical model

Reward per step can change when policy rate changes even if physical behavior stays identical. Discounted return weights near-term and distant outcomes differently. This laboratory compares a short immediate reward with a delayed larger reward and calculates the effective discount horizon. It is a reasoning tool for reward design, not an argument that one discount factor is universally correct.

G_t=sum(gamma^k*r[t+k]); continuous-time discount gamma=exp(-dt/tau); horizon scale approx 1/(1-gamma) steps.

### C. Real-world meaning and limits

Physical task success must be evaluated directly; training return alone does not establish useful robot behavior.

### D. Architecture and data flow

Configuration (gamma) -> numerical model -> immediate_return, delayed_return, delayed_preference_margin -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

gamma is a dimensionless per-policy-step discount strictly between zero and one; the teaching policy step is 20 ms.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| gamma | 0.99 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/51_discounted_return.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only gamma changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/51_discounted_return.py --case 0

.venv-book/bin/python expanded_lab/modules/51_discounted_return.py --case 3

.venv-book/bin/python expanded_lab/run.py discounted_return --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/51_discounted_return.py

### H. Walkthrough and design decisions

The sparse reward sequences isolate discount preference from action dynamics. Mapping gamma to seconds prevents accidental task changes when control frequency changes.

### I. Expected behavior and six worked cases

The controlled variable is gamma. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/51_discounted_return.png

Figure L51. immediate return as gamma changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | gamma | immediate return |
|---|---|---|
| 0 | 0.9 | 1 |
| 1 | 0.95 | 1 |
| 2 | 0.97 | 1 |
| 3 | 0.98 | 1 |
| 4 | 0.99 | 1 |
| 5 | 0.995 | 1 |

#### Worked case 0: gamma = 0.9

This case keeps the nominal configuration except for gamma=0.9. The full input is {"gamma": 0.9}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| immediate return | 1 |
| delayed return | 0.01546133 |
| delayed preference margin | -0.98453867 |
| effective horizon steps | 10 |
| continuous time scale s | 0.18982443 |

1. Choose gamma=0.9 at control period 0.02 s.

2. One candidate receives reward 1 now; the other receives reward 3 after 50 steps.

3. Immediate return is 1.000000; delayed return is 3*gamma^50=0.015461.

4. The geometric horizon scale is 10.000000 steps.

5. The matching exponential time constant is 0.189824 s.

#### Worked case 1: gamma = 0.95

This case keeps the nominal configuration except for gamma=0.95. The full input is {"gamma": 0.95}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| immediate return | 1 |
| delayed return | 0.23083493 |
| delayed preference margin | -0.76916507 |
| effective horizon steps | 20 |
| continuous time scale s | 0.38991451 |

1. Choose gamma=0.95 at control period 0.02 s.

2. One candidate receives reward 1 now; the other receives reward 3 after 50 steps.

3. Immediate return is 1.000000; delayed return is 3*gamma^50=0.230835.

4. The geometric horizon scale is 20.000000 steps.

5. The matching exponential time constant is 0.389915 s.

#### Worked case 2: gamma = 0.97

This case keeps the nominal configuration except for gamma=0.97. The full input is {"gamma": 0.97}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| immediate return | 1 |
| delayed return | 0.65419613 |
| delayed preference margin | -0.34580387 |
| effective horizon steps | 33.33333333 |
| continuous time scale s | 0.6566159 |

1. Choose gamma=0.97 at control period 0.02 s.

2. One candidate receives reward 1 now; the other receives reward 3 after 50 steps.

3. Immediate return is 1.000000; delayed return is 3*gamma^50=0.654196.

4. The geometric horizon scale is 33.333333 steps.

5. The matching exponential time constant is 0.656616 s.

#### Worked case 3: gamma = 0.98

This case keeps the nominal configuration except for gamma=0.98. The full input is {"gamma": 0.98}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| immediate return | 1 |
| delayed return | 1.09250904 |
| delayed preference margin | 0.09250904 |
| effective horizon steps | 50 |
| continuous time scale s | 0.98996633 |

1. Choose gamma=0.98 at control period 0.02 s.

2. One candidate receives reward 1 now; the other receives reward 3 after 50 steps.

3. Immediate return is 1.000000; delayed return is 3*gamma^50=1.092509.

4. The geometric horizon scale is 50.000000 steps.

5. The matching exponential time constant is 0.989966 s.

The delayed outcome is preferred under this discount.

#### Worked case 4: gamma = 0.99

This case keeps the nominal configuration except for gamma=0.99. The full input is {"gamma": 0.99}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| immediate return | 1 |
| delayed return | 1.8150182 |
| delayed preference margin | 0.8150182 |
| effective horizon steps | 100 |
| continuous time scale s | 1.98998325 |

1. Choose gamma=0.99 at control period 0.02 s.

2. One candidate receives reward 1 now; the other receives reward 3 after 50 steps.

3. Immediate return is 1.000000; delayed return is 3*gamma^50=1.815018.

4. The geometric horizon scale is 100.000000 steps.

5. The matching exponential time constant is 1.989983 s.

The delayed outcome is preferred under this discount.

#### Worked case 5: gamma = 0.995

This case keeps the nominal configuration except for gamma=0.995. The full input is {"gamma": 0.995}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| immediate return | 1 |
| delayed return | 2.33493767 |
| delayed preference margin | 1.33493767 |
| effective horizon steps | 200 |
| continuous time scale s | 3.98999165 |

1. Choose gamma=0.995 at control period 0.02 s.

2. One candidate receives reward 1 now; the other receives reward 3 after 50 steps.

3. Immediate return is 1.000000; delayed return is 3*gamma^50=2.334938.

4. The geometric horizon scale is 200.000000 steps.

5. The matching exponential time constant is 3.989992 s.

The delayed outcome is preferred under this discount.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The immediate outcome is preferred despite the larger undiscounted delayed reward.

Episode termination, reward scaling and physical-time interpretation remain part of the task specification.

### K. Failure modes and troubleshooting

Comparing returns across different timesteps without rescaling; rewarding survival while ignoring command tracking; hiding terminal rewards in long episodes.

### L. Practical exercises and extension tasks

1. Keep a fixed discount time constant while changing policy period.

2. Add per-second energy cost and discretize it consistently.

3. Construct a reward-hacking example with a safe-looking but unproductive action.

### M. Connection to the Asimov research platform

Physical task success must be evaluated directly; training return alone does not establish useful robot behavior.

### N. Completion record

Record your chosen case, predicted trend, measured immediate_return, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 52, Temporal-difference residuals, GAE and episode boundaries. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 52 - Temporal-difference residuals, GAE and episode boundaries

### A. The engineering question

An advantage estimate compares an action's outcome with the value baseline for its state.

### B. Concepts and mathematical model

Generalized Advantage Estimation combines temporal-difference residuals over multiple horizons, trading variance against sensitivity to value errors. Episode boundaries matter: a true terminal state differs from an externally imposed time limit that still has continuation value. This laboratory computes the backward recurrence explicitly and exposes the effect of the lambda parameter while holding rewards and values fixed.

delta_t=r_t+gamma*V_next-V_t; A_t=delta_t+gamma*lambda*A_next, with valid terminal/continuation masks.

### C. Real-world meaning and limits

Correct learning plumbing is essential before expensive humanoid rollouts; masking bugs can invalidate apparently successful training.

### D. Architecture and data flow

Configuration (gae_lambda) -> numerical model -> initial_advantage, final_advantage, advantage_std -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

gae_lambda is the dimensionless trace parameter; rewards, value predictions and one terminal boundary are fixed.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| gae_lambda | 0.95 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/52_gae.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only gae_lambda changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/52_gae.py --case 0

.venv-book/bin/python expanded_lab/modules/52_gae.py --case 3

.venv-book/bin/python expanded_lab/run.py gae --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/52_gae.py

### H. Walkthrough and design decisions

Run the recurrence backward and retain intermediate deltas so every term can be checked by hand. Lambda zero reduces to one-step TD residuals; lambda one includes the longest available trace.

### I. Expected behavior and six worked cases

The controlled variable is gae_lambda. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/52_gae.png

Figure L52. initial advantage as gae_lambda changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | gae_lambda | initial advantage |
|---|---|---|
| 0 | 0 | 0.2455 |
| 1 | 0.25 | 0.24567618 |
| 2 | 0.5 | 0.3143445 |
| 3 | 0.75 | 0.54137891 |
| 4 | 0.95 | 0.92042199 |
| 5 | 1 | 1.05267571 |

#### Worked case 0: gae_lambda = 0

This case keeps the nominal configuration except for gae_lambda=0. The full input is {"gae_lambda": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial advantage | 0.2455 |
| final advantage | 0.4 |
| advantage std | 0.17516381 |
| initial value target | 0.6455 |
| mean advantage | 0.2163 |

1. Use rewards [0.2, 0.1, -0.1, 0.3, 1.0] and value predictions [0.4, 0.45, 0.3, 0.5, 0.6, 0.0].

2. The last transition is truly terminal; gamma=0.99, lambda=0.

3. Backward TD residuals in chronological order are [np.float64(0.24549999999999994), np.float64(-0.05299999999999999), np.float64(0.09500000000000003), np.float64(0.3939999999999999), np.float64(0.4)].

4. The resulting advantage vector is [0.24549999999999994, -0.05299999999999999, 0.09500000000000003, 0.3939999999999999, 0.4].

5. Value targets A+V are [0.6455, 0.397, 0.395, 0.8939999999999999, 1.0].

#### Worked case 1: gae_lambda = 0.25

This case keeps the nominal configuration except for gae_lambda=0.25. The full input is {"gae_lambda": 0.25}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial advantage | 0.24567618 |
| final advantage | 0.4 |
| advantage std | 0.16884058 |
| initial value target | 0.64567618 |
| mean advantage | 0.2712811 |

1. Use rewards [0.2, 0.1, -0.1, 0.3, 1.0] and value predictions [0.4, 0.45, 0.3, 0.5, 0.6, 0.0].

2. The last transition is truly terminal; gamma=0.99, lambda=0.25.

3. Backward TD residuals in chronological order are [np.float64(0.24549999999999994), np.float64(-0.05299999999999999), np.float64(0.09500000000000003), np.float64(0.3939999999999999), np.float64(0.4)].

4. The resulting advantage vector is [0.24567617823437493, 0.0007118312500000099, 0.2170175, 0.4929999999999999, 0.4].

5. Value targets A+V are [0.645676178234375, 0.45071183125000003, 0.5170175, 0.9929999999999999, 1.0].

#### Worked case 2: gae_lambda = 0.5

This case keeps the nominal configuration except for gae_lambda=0.5. The full input is {"gae_lambda": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial advantage | 0.3143445 |
| final advantage | 0.4 |
| advantage std | 0.14620289 |
| initial value target | 0.7143445 |
| mean advantage | 0.36669286 |

1. Use rewards [0.2, 0.1, -0.1, 0.3, 1.0] and value predictions [0.4, 0.45, 0.3, 0.5, 0.6, 0.0].

2. The last transition is truly terminal; gamma=0.99, lambda=0.5.

3. Backward TD residuals in chronological order are [np.float64(0.24549999999999994), np.float64(-0.05299999999999999), np.float64(0.09500000000000003), np.float64(0.3939999999999999), np.float64(0.4)].

4. The resulting advantage vector is [0.31434450099999994, 0.13907979999999998, 0.38803999999999994, 0.5919999999999999, 0.4].

5. Value targets A+V are [0.714344501, 0.5890797999999999, 0.68804, 1.0919999999999999, 1.0].

#### Worked case 3: gae_lambda = 0.75

This case keeps the nominal configuration except for gae_lambda=0.75. The full input is {"gae_lambda": 0.75}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial advantage | 0.54137891 |
| final advantage | 0.4 |
| advantage std | 0.11516543 |
| initial value target | 0.94137891 |
| mean advantage | 0.52778731 |

1. Use rewards [0.2, 0.1, -0.1, 0.3, 1.0] and value predictions [0.4, 0.45, 0.3, 0.5, 0.6, 0.0].

2. The last transition is truly terminal; gamma=0.99, lambda=0.75.

3. Backward TD residuals in chronological order are [np.float64(0.24549999999999994), np.float64(-0.05299999999999999), np.float64(0.09500000000000003), np.float64(0.3939999999999999), np.float64(0.4)].

4. The resulting advantage vector is [0.5413789131718747, 0.3984901187499998, 0.6080674999999998, 0.6909999999999998, 0.4].

5. Value targets A+V are [0.9413789131718747, 0.8484901187499998, 0.9080674999999998, 1.1909999999999998, 1.0].

#### Worked case 4: gae_lambda = 0.95

This case keeps the nominal configuration except for gae_lambda=0.95. The full input is {"gae_lambda": 0.95}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial advantage | 0.92042199 |
| final advantage | 0.4 |
| advantage std | 0.17596429 |
| initial value target | 1.32042199 |
| mean advantage | 0.7255231 |

1. Use rewards [0.2, 0.1, -0.1, 0.3, 1.0] and value predictions [0.4, 0.45, 0.3, 0.5, 0.6, 0.0].

2. The last transition is truly terminal; gamma=0.99, lambda=0.95.

3. Backward TD residuals in chronological order are [np.float64(0.24549999999999994), np.float64(-0.05299999999999999), np.float64(0.09500000000000003), np.float64(0.3939999999999999), np.float64(0.4)].

4. The resulting advantage vector is [0.9204219867172749, 0.71762040055, 0.8193731, 0.7702, 0.4].

5. Value targets A+V are [1.320421986717275, 1.16762040055, 1.1193731, 1.2702, 1.0].

#### Worked case 5: gae_lambda = 1

This case keeps the nominal configuration except for gae_lambda=1. The full input is {"gae_lambda": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| initial advantage | 1.05267571 |
| final advantage | 0.4 |
| advantage std | 0.21414113 |
| initial value target | 1.45267571 |
| mean advantage | 0.78702094 |

1. Use rewards [0.2, 0.1, -0.1, 0.3, 1.0] and value predictions [0.4, 0.45, 0.3, 0.5, 0.6, 0.0].

2. The last transition is truly terminal; gamma=0.99, lambda=1.

3. Backward TD residuals in chronological order are [np.float64(0.24549999999999994), np.float64(-0.05299999999999999), np.float64(0.09500000000000003), np.float64(0.3939999999999999), np.float64(0.4)].

4. The resulting advantage vector is [1.05267571, 0.815329, 0.8771, 0.7899999999999999, 0.4].

5. Value targets A+V are [1.4526757099999998, 1.265329, 1.1771, 1.29, 1.0].

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

A time-limit truncation may retain a bootstrap value while still preventing recurrence into the next reset episode.

Correct masking needs separate termination and rollout-boundary semantics; one generic done flag can hide a bug.

### K. Failure modes and troubleshooting

Bootstrapping a true terminal as if it continued; propagating advantages across reset episodes; normalizing advantages without checking their construction.

### L. Practical exercises and extension tasks

1. Replace the final terminal with a time-limit truncation and nonzero final value.

2. Calculate the lambda-zero and lambda-one results manually.

3. Inject a value bias and compare its effect across lambda values.

### M. Connection to the Asimov research platform

Correct learning plumbing is essential before expensive humanoid rollouts; masking bugs can invalidate apparently successful training.

### N. Completion record

Record your chosen case, predicted trend, measured initial_advantage, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 53, PPO clipping, advantage signs and surrogate objectives. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 53 - PPO clipping, advantage signs and surrogate objectives

### A. The engineering question

PPO's clipped surrogate is a constrained-update heuristic, not a direct clipping of the motor command.

### B. Concepts and mathematical model

The probability ratio measures how the new policy changes likelihood of sampled actions. Whether clipping limits the objective depends on both the ratio and the advantage sign. A common implementation mistake is to apply the same intuitive rule to positive and negative advantages without evaluating the minimum. This laboratory computes both branches on a fixed batch so the behavior is inspectable.

L=min(ratio*A,clip(ratio,1-epsilon,1+epsilon)*A); policy loss=-mean(L).

### C. Real-world meaning and limits

Policy optimization constraints do not replace bounded action scaling, runtime supervision or physical commissioning.

### D. Architecture and data flow

Configuration (clip_epsilon) -> numerical model -> policy_loss, unclipped_loss, objective_changed_fraction -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

clip_epsilon is the dimensionless probability-ratio interval half-width; the sampled ratios and advantages are fixed.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| clip_epsilon | 0.2 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/53_ppo_clipping.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only clip_epsilon changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/53_ppo_clipping.py --case 0

.venv-book/bin/python expanded_lab/modules/53_ppo_clipping.py --case 3

.venv-book/bin/python expanded_lab/run.py ppo_clipping --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/53_ppo_clipping.py

### H. Walkthrough and design decisions

Calculate raw and clipped products before taking their elementwise minimum. Inspect one positive-advantage and one negative-advantage sample by hand to verify the sign logic.

### I. Expected behavior and six worked cases

The controlled variable is clip_epsilon. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/53_ppo_clipping.png

Figure L53. policy loss as clip_epsilon changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | clip_epsilon | policy loss |
|---|---|---|
| 0 | 0.05 | 0.08571429 |
| 1 | 0.1 | 0.06785714 |
| 2 | 0.15 | 0.05 |
| 3 | 0.2 | 0.03214286 |
| 4 | 0.3 | 0.01785714 |
| 5 | 0.4 | 0.00357143 |

#### Worked case 0: clip_epsilon = 0.05

This case keeps the nominal configuration except for clip_epsilon=0.05. The full input is {"clip_epsilon": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy loss | 0.08571429 |
| unclipped loss | -0.01071429 |
| objective changed fraction | 0.42857143 |
| ratio outside clip fraction | 0.57142857 |
| minimum sample objective | -1.5 |

1. Probability ratios are [0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 1.5].

2. Advantages are [-1.0, -0.5, 1.0, -0.2, 0.5, 1.0, -1.0]; clipping epsilon is 0.05.

3. Unclipped sample objectives are [-0.5, -0.4, 0.95, -0.2, 0.525, 1.2, -1.5].

4. Apply the minimum with the clipped branch to obtain [-0.95, -0.475, 0.95, -0.2, 0.525, 1.05, -1.5].

5. Negative mean objective gives policy loss 0.085714.

#### Worked case 1: clip_epsilon = 0.1

This case keeps the nominal configuration except for clip_epsilon=0.1. The full input is {"clip_epsilon": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy loss | 0.06785714 |
| unclipped loss | -0.01071429 |
| objective changed fraction | 0.42857143 |
| ratio outside clip fraction | 0.57142857 |
| minimum sample objective | -1.5 |

1. Probability ratios are [0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 1.5].

2. Advantages are [-1.0, -0.5, 1.0, -0.2, 0.5, 1.0, -1.0]; clipping epsilon is 0.1.

3. Unclipped sample objectives are [-0.5, -0.4, 0.95, -0.2, 0.525, 1.2, -1.5].

4. Apply the minimum with the clipped branch to obtain [-0.9, -0.45, 0.95, -0.2, 0.525, 1.1, -1.5].

5. Negative mean objective gives policy loss 0.067857.

#### Worked case 2: clip_epsilon = 0.15

This case keeps the nominal configuration except for clip_epsilon=0.15. The full input is {"clip_epsilon": 0.15}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy loss | 0.05 |
| unclipped loss | -0.01071429 |
| objective changed fraction | 0.42857143 |
| ratio outside clip fraction | 0.57142857 |
| minimum sample objective | -1.5 |

1. Probability ratios are [0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 1.5].

2. Advantages are [-1.0, -0.5, 1.0, -0.2, 0.5, 1.0, -1.0]; clipping epsilon is 0.15.

3. Unclipped sample objectives are [-0.5, -0.4, 0.95, -0.2, 0.525, 1.2, -1.5].

4. Apply the minimum with the clipped branch to obtain [-0.85, -0.425, 0.95, -0.2, 0.525, 1.15, -1.5].

5. Negative mean objective gives policy loss 0.050000.

#### Worked case 3: clip_epsilon = 0.2

This case keeps the nominal configuration except for clip_epsilon=0.2. The full input is {"clip_epsilon": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy loss | 0.03214286 |
| unclipped loss | -0.01071429 |
| objective changed fraction | 0.14285714 |
| ratio outside clip fraction | 0.28571429 |
| minimum sample objective | -1.5 |

1. Probability ratios are [0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 1.5].

2. Advantages are [-1.0, -0.5, 1.0, -0.2, 0.5, 1.0, -1.0]; clipping epsilon is 0.2.

3. Unclipped sample objectives are [-0.5, -0.4, 0.95, -0.2, 0.525, 1.2, -1.5].

4. Apply the minimum with the clipped branch to obtain [-0.8, -0.4, 0.95, -0.2, 0.525, 1.2, -1.5].

5. Negative mean objective gives policy loss 0.032143.

#### Worked case 4: clip_epsilon = 0.3

This case keeps the nominal configuration except for clip_epsilon=0.3. The full input is {"clip_epsilon": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy loss | 0.01785714 |
| unclipped loss | -0.01071429 |
| objective changed fraction | 0.14285714 |
| ratio outside clip fraction | 0.28571429 |
| minimum sample objective | -1.5 |

1. Probability ratios are [0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 1.5].

2. Advantages are [-1.0, -0.5, 1.0, -0.2, 0.5, 1.0, -1.0]; clipping epsilon is 0.3.

3. Unclipped sample objectives are [-0.5, -0.4, 0.95, -0.2, 0.525, 1.2, -1.5].

4. Apply the minimum with the clipped branch to obtain [-0.7, -0.4, 0.95, -0.2, 0.525, 1.2, -1.5].

5. Negative mean objective gives policy loss 0.017857.

#### Worked case 5: clip_epsilon = 0.4

This case keeps the nominal configuration except for clip_epsilon=0.4. The full input is {"clip_epsilon": 0.4}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| policy loss | 0.00357143 |
| unclipped loss | -0.01071429 |
| objective changed fraction | 0.14285714 |
| ratio outside clip fraction | 0.28571429 |
| minimum sample objective | -1.5 |

1. Probability ratios are [0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 1.5].

2. Advantages are [-1.0, -0.5, 1.0, -0.2, 0.5, 1.0, -1.0]; clipping epsilon is 0.4.

3. Unclipped sample objectives are [-0.5, -0.4, 0.95, -0.2, 0.525, 1.2, -1.5].

4. Apply the minimum with the clipped branch to obtain [-0.6, -0.4, 0.95, -0.2, 0.525, 1.2, -1.5].

5. Negative mean objective gives policy loss 0.003571.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Ratio outside the clip interval is not identical to a changed surrogate contribution; advantage sign matters.

This calculation omits value loss, entropy bonus, optimizer behavior and rollout collection.

### K. Failure modes and troubleshooting

Confusing policy-ratio clipping with action limits; maximizing a loss written for minimization; interpreting clipping as a physical safety constraint.

### L. Practical exercises and extension tasks

1. Plot surrogate objective versus ratio for both advantage signs.

2. Add an entropy term and inspect its separate contribution.

3. Compare approximate KL diagnostics with the ratio distribution.

### M. Connection to the Asimov research platform

Policy optimization constraints do not replace bounded action scaling, runtime supervision or physical commissioning.

### N. Completion record

Record your chosen case, predicted trend, measured policy_loss, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 54, Gaussian policies, action limits and saturation probability. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 54 - Gaussian policies, action limits and saturation probability

### A. The engineering question

A stochastic continuous policy often samples from a Gaussian distribution before applying environment bounds.

### B. Concepts and mathematical model

Large standard deviation can create many clipped actions, changing the action distribution seen by the plant. A bounded tanh transformation has different density mathematics from simple clipping. This laboratory quantifies clipping frequency and variance reduction for a one-dimensional Gaussian policy. It also calculates Gaussian entropy so exploration magnitude has an interpretable scale.

a_raw~Normal(mu,sigma^2); a=clip(a_raw,-1,1); entropy=0.5*log(2*pi*e*sigma^2).

### C. Real-world meaning and limits

Physical inference generally uses deterministic policy evaluation plus explicit bounded action processing validated against training semantics.

### D. Architecture and data flow

Configuration (mean, std) -> numerical model -> clipped_fraction, raw_mean, bounded_mean -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

mean and std are normalized action units before the environment action scale and joint limits.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| mean | 0.2 | Defined by the explicit chapter model and parameter contract |
| std | 0.5 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/54_gaussian_policy.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only std changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/54_gaussian_policy.py --case 0

.venv-book/bin/python expanded_lab/modules/54_gaussian_policy.py --case 3

.venv-book/bin/python expanded_lab/run.py gaussian_policy --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/54_gaussian_policy.py

### H. Walkthrough and design decisions

Compare raw and applied distributions rather than logging only the sampled Gaussian parameters. A high clipped fraction can make exploration look numerically broad while applied actions concentrate at limits.

### I. Expected behavior and six worked cases

The controlled variable is std. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/54_gaussian_policy.png

Figure L54. clipped fraction as std changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | std | clipped fraction |
|---|---|---|
| 0 | 0.05 | 0 |
| 1 | 0.1 | 0 |
| 2 | 0.2 | 0.00005 |
| 3 | 0.5 | 0.0623 |
| 4 | 1 | 0.3254 |
| 5 | 2 | 0.61905 |

#### Worked case 0: std = 0.05

This case keeps the nominal configuration except for std=0.05. The full input is {"mean": 0.2, "std": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| clipped fraction | 0 |
| raw mean | 0.2001035 |
| bounded mean | 0.2001035 |
| raw std | 0.04973828 |
| bounded std | 0.04973828 |
| gaussian entropy nats | -1.57679374 |

1. Sample 20,000 actions from mean 0.2 and standard deviation 0.05.

2. Unbounded Gaussian entropy is -1.576794 nats.

3. Clip to [-1,1]; clipped fraction is 0.000000.

4. Raw sample standard deviation is 0.049738; bounded standard deviation is 0.049738.

5. Bounded mean is 0.200104, which can shift when clipping is asymmetric around the policy mean.

#### Worked case 1: std = 0.1

This case keeps the nominal configuration except for std=0.1. The full input is {"mean": 0.2, "std": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| clipped fraction | 0 |
| raw mean | 0.200207 |
| bounded mean | 0.200207 |
| raw std | 0.09947656 |
| bounded std | 0.09947656 |
| gaussian entropy nats | -0.88364656 |

1. Sample 20,000 actions from mean 0.2 and standard deviation 0.1.

2. Unbounded Gaussian entropy is -0.883647 nats.

3. Clip to [-1,1]; clipped fraction is 0.000000.

4. Raw sample standard deviation is 0.099477; bounded standard deviation is 0.099477.

5. Bounded mean is 0.200207, which can shift when clipping is asymmetric around the policy mean.

#### Worked case 2: std = 0.2

This case keeps the nominal configuration except for std=0.2. The full input is {"mean": 0.2, "std": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| clipped fraction | 0.00005 |
| raw mean | 0.200414 |
| bounded mean | 0.20041272 |
| raw std | 0.19895312 |
| bounded std | 0.19894788 |
| gaussian entropy nats | -0.19049938 |

1. Sample 20,000 actions from mean 0.2 and standard deviation 0.2.

2. Unbounded Gaussian entropy is -0.190499 nats.

3. Clip to [-1,1]; clipped fraction is 0.000050.

4. Raw sample standard deviation is 0.198953; bounded standard deviation is 0.198948.

5. Bounded mean is 0.200413, which can shift when clipping is asymmetric around the policy mean.

#### Worked case 3: std = 0.5

This case keeps the nominal configuration except for std=0.5. The full input is {"mean": 0.2, "std": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| clipped fraction | 0.0623 |
| raw mean | 0.201035 |
| bounded mean | 0.19079612 |
| raw std | 0.4973828 |
| bounded std | 0.47122932 |
| gaussian entropy nats | 0.72579135 |

1. Sample 20,000 actions from mean 0.2 and standard deviation 0.5.

2. Unbounded Gaussian entropy is 0.725791 nats.

3. Clip to [-1,1]; clipped fraction is 0.062300.

4. Raw sample standard deviation is 0.497383; bounded standard deviation is 0.471229.

5. Bounded mean is 0.190796, which can shift when clipping is asymmetric around the policy mean.

#### Worked case 4: std = 1

This case keeps the nominal configuration except for std=1. The full input is {"mean": 0.2, "std": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| clipped fraction | 0.3254 |
| raw mean | 0.20207 |
| bounded mean | 0.13974087 |
| raw std | 0.9947656 |
| bounded std | 0.70848934 |
| gaussian entropy nats | 1.41893853 |

1. Sample 20,000 actions from mean 0.2 and standard deviation 1.

2. Unbounded Gaussian entropy is 1.418939 nats.

3. Clip to [-1,1]; clipped fraction is 0.325400.

4. Raw sample standard deviation is 0.994766; bounded standard deviation is 0.708489.

5. Bounded mean is 0.139741, which can shift when clipping is asymmetric around the policy mean.

#### Worked case 5: std = 2

This case keeps the nominal configuration except for std=2. The full input is {"mean": 0.2, "std": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| clipped fraction | 0.61905 |
| raw mean | 0.20414 |
| bounded mean | 0.0792849 |
| raw std | 1.98953121 |
| bounded std | 0.85736778 |
| gaussian entropy nats | 2.11208571 |

1. Sample 20,000 actions from mean 0.2 and standard deviation 2.

2. Unbounded Gaussian entropy is 2.112086 nats.

3. Clip to [-1,1]; clipped fraction is 0.619050.

4. Raw sample standard deviation is 1.989531; bounded standard deviation is 0.857368.

5. Bounded mean is 0.079285, which can shift when clipping is asymmetric around the policy mean.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The entropy formula describes the unbounded Gaussian, not the clipped mixed distribution.

A tanh-squashed policy requires a change-of-variables correction when computing log probabilities.

### K. Failure modes and troubleshooting

Using raw Gaussian entropy as the applied distribution entropy; omitting export-time clipping; changing action scaling without retraining/evaluation.

### L. Practical exercises and extension tasks

1. Repeat with policy mean near an action boundary.

2. Compare clipping with tanh transformation histograms.

3. Propagate normalized actions into an actual simulated torque envelope.

### M. Connection to the Asimov research platform

Physical inference generally uses deterministic policy evaluation plus explicit bounded action processing validated against training semantics.

### N. Completion record

Record your chosen case, predicted trend, measured clipped_fraction, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 55, Streaming normalization, numerical stability and evaluation leakage. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 55 - Streaming normalization, numerical stability and evaluation leakage

### A. The engineering question

Policies often require normalized observations.

### B. Concepts and mathematical model

Streaming mean and variance can be estimated without retaining every sample, but evaluation must normally freeze the training statistics. Updating them on test observations changes the policy input distribution and leaks information across the evaluation boundary. This laboratory uses Welford's stable recurrence and compares a frozen training normalizer with a normalizer incorrectly refitted after a distribution shift.

n+=1; delta=x-mean; mean+=delta/n; M2+=delta*(x-mean); variance=M2/(n-1).

### C. Real-world meaning and limits

Hardware observation normalization must match the validated training/replay pipeline, including clipping and missing-data treatment.

### D. Architecture and data flow

Configuration (test_shift) -> numerical model -> training_mean, training_variance, frozen_test_mean -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

test_shift is the mean offset of the held-out synthetic observation distribution in raw channel units.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| test_shift | 1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/55_running_statistics.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only test_shift changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/55_running_statistics.py --case 0

.venv-book/bin/python expanded_lab/modules/55_running_statistics.py --case 3

.venv-book/bin/python expanded_lab/run.py running_statistics --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/55_running_statistics.py

### H. Walkthrough and design decisions

Verify the streaming calculation against a batch reference, then freeze it. Separate numerical correctness of the estimator from the experimental policy of when it is allowed to update.

### I. Expected behavior and six worked cases

The controlled variable is test_shift. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/55_running_statistics.png

Figure L55. training mean as test_shift changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | test_shift | training mean |
|---|---|---|
| 0 | 0 | -0.01085555 |
| 1 | 0.2 | -0.01085555 |
| 2 | 0.5 | -0.01085555 |
| 3 | 1 | -0.01085555 |
| 4 | 2 | -0.01085555 |
| 5 | 4 | -0.01085555 |

#### Worked case 0: test_shift = 0

This case keeps the nominal configuration except for test_shift=0. The full input is {"test_shift": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| training mean | -0.01085555 |
| training variance | 0.94154387 |
| frozen test mean | 0.01337223 |
| leaked test mean | 0.01108065 |
| mean normalized disagreement | 0.00501517 |

1. Estimate training statistics with 5,000 seeded samples using Welford updates.

2. The held-out distribution has mean shift 0.

3. Frozen normalizer produces test mean 0.013372.

4. Updating statistics with evaluation data changes the test mean to 0.011081.

5. Mean per-sample normalized disagreement is 0.005015.

#### Worked case 1: test_shift = 0.2

This case keeps the nominal configuration except for test_shift=0.2. The full input is {"test_shift": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| training mean | -0.01085555 |
| training variance | 0.94154387 |
| frozen test mean | 0.21948728 |
| leaked test mean | 0.18127759 |
| mean normalized disagreement | 0.0382097 |

1. Estimate training statistics with 5,000 seeded samples using Welford updates.

2. The held-out distribution has mean shift 0.2.

3. Frozen normalizer produces test mean 0.219487.

4. Updating statistics with evaluation data changes the test mean to 0.181278.

5. Mean per-sample normalized disagreement is 0.038210.

#### Worked case 2: test_shift = 0.5

This case keeps the nominal configuration except for test_shift=0.5. The full input is {"test_shift": 0.5}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| training mean | -0.01085555 |
| training variance | 0.94154387 |
| frozen test mean | 0.52865986 |
| leaked test mean | 0.42989609 |
| mean normalized disagreement | 0.09876378 |

1. Estimate training statistics with 5,000 seeded samples using Welford updates.

2. The held-out distribution has mean shift 0.5.

3. Frozen normalizer produces test mean 0.528660.

4. Updating statistics with evaluation data changes the test mean to 0.429896.

5. Mean per-sample normalized disagreement is 0.098764.

#### Worked case 3: test_shift = 1

This case keeps the nominal configuration except for test_shift=1. The full input is {"test_shift": 1.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| training mean | -0.01085555 |
| training variance | 0.94154387 |
| frozen test mean | 1.0439475 |
| leaked test mean | 0.80677996 |
| mean normalized disagreement | 0.23716754 |

1. Estimate training statistics with 5,000 seeded samples using Welford updates.

2. The held-out distribution has mean shift 1.

3. Frozen normalizer produces test mean 1.043947.

4. Updating statistics with evaluation data changes the test mean to 0.806780.

5. Mean per-sample normalized disagreement is 0.237168.

#### Worked case 4: test_shift = 2

This case keeps the nominal configuration except for test_shift=2. The full input is {"test_shift": 2.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| training mean | -0.01085555 |
| training variance | 0.94154387 |
| frozen test mean | 2.07452277 |
| leaked test mean | 1.36280645 |
| mean normalized disagreement | 0.71171632 |

1. Estimate training statistics with 5,000 seeded samples using Welford updates.

2. The held-out distribution has mean shift 2.

3. Frozen normalizer produces test mean 2.074523.

4. Updating statistics with evaluation data changes the test mean to 1.362806.

5. Mean per-sample normalized disagreement is 0.711716.

#### Worked case 5: test_shift = 4

This case keeps the nominal configuration except for test_shift=4. The full input is {"test_shift": 4.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| training mean | -0.01085555 |
| training variance | 0.94154387 |
| frozen test mean | 4.13567331 |
| leaked test mean | 1.87257638 |
| mean normalized disagreement | 2.26309693 |

1. Estimate training statistics with 5,000 seeded samples using Welford updates.

2. The held-out distribution has mean shift 4.

3. Frozen normalizer produces test mean 4.135673.

4. Updating statistics with evaluation data changes the test mean to 1.872576.

5. Mean per-sample normalized disagreement is 2.263097.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

A shifted test mean can be useful evidence of distribution shift; normalizing it away may hide the problem.

Explicit online adaptation can be legitimate, but it is a different deployed algorithm requiring separate validation.

### K. Failure modes and troubleshooting

Updating statistics during final evaluation; resetting normalizers when loading a policy; confusing population and sample variance conventions.

### L. Practical exercises and extension tasks

1. Extend Welford to vector observations.

2. Merge statistics from two independent training workers.

3. Store normalizer parameters and schema hash with a policy checkpoint.

### M. Connection to the Asimov research platform

Hardware observation normalization must match the validated training/replay pipeline, including clipping and missing-data treatment.

### N. Completion record

Record your chosen case, predicted trend, measured training_mean, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 56, Domain randomization, correlations and feasible parameter sets. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 56 - Domain randomization, correlations and feasible parameter sets

### A. The engineering question

Randomization should represent plausible physical variation.

### B. Concepts and mathematical model

Sampling every parameter independently can produce impossible combinations, such as mass and inertia that no real assembly could have. Correlated randomization can preserve relationships while exploring uncertainty. This laboratory samples a density scale and length scale, deriving mass and rod inertia consistently, then compares it with independent inertia sampling. It illustrates why wider randomization is not automatically better.

For fixed cross-section with length scale sL and density scale srho: m=m0*srho*sL; I=m*(L0*sL)^2/3.

### C. Real-world meaning and limits

Sim-to-real ranges should reflect measured actuator strength, delays, contact surfaces, calibration error and expected operating conditions.

### D. Architecture and data flow

Configuration (range_fraction) -> numerical model -> mass_std_kg, consistent_inertia_std_kg_m2, mass_inertia_correlation -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

range_fraction is the symmetric fractional range of density and length scales; nominal rod mass is 2 kg and length 0.3 m.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| range_fraction | 0.1 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/56_domain_randomization.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only range_fraction changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/56_domain_randomization.py --case 0

.venv-book/bin/python expanded_lab/modules/56_domain_randomization.py --case 3

.venv-book/bin/python expanded_lab/run.py domain_randomization --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/56_domain_randomization.py

### H. Walkthrough and design decisions

Generate latent physical variations first, then derive dependent parameters. Compare statistical coverage with physical consistency rather than judging samples only by marginal ranges.

### I. Expected behavior and six worked cases

The controlled variable is range_fraction. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/56_domain_randomization.png

Figure L56. mass std kg as range_fraction changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | range_fraction | mass std kg |
|---|---|---|
| 0 | 0.01 | 0.01623354 |
| 1 | 0.025 | 0.04058687 |
| 2 | 0.05 | 0.08119077 |
| 3 | 0.1 | 0.16250174 |
| 4 | 0.2 | 0.32589935 |
| 5 | 0.3 | 0.49101698 |

#### Worked case 0: range_fraction = 0.01

This case keeps the nominal configuration except for range_fraction=0.01. The full input is {"range_fraction": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mass std kg | 0.01623354 |
| consistent inertia std kg m2 | 0.001094 |
| mass inertia correlation | 0.8919605 |
| independent implied length rmse m | 0.00286993 |
| maximum consistent inertia kg m2 | 0.06242462 |

1. Sample density and length scales within +/-1 percent.

2. Derive mass and inertia from the same physical dimensions rather than unrelated ranges.

3. Mass standard deviation is 0.016234 kg and inertia standard deviation is 0.001094 kg*m^2.

4. Mass/inertia sample correlation is 0.891960.

5. Independent inertia sampling implies a rod-length RMSE of 0.002870 m relative to the actual sampled length.

#### Worked case 1: range_fraction = 0.025

This case keeps the nominal configuration except for range_fraction=0.025. The full input is {"range_fraction": 0.025}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mass std kg | 0.04058687 |
| consistent inertia std kg m2 | 0.00273593 |
| mass inertia correlation | 0.89198415 |
| independent implied length rmse m | 0.00717536 |
| maximum consistent inertia kg m2 | 0.06619842 |

1. Sample density and length scales within +/-2.5 percent.

2. Derive mass and inertia from the same physical dimensions rather than unrelated ranges.

3. Mass standard deviation is 0.040587 kg and inertia standard deviation is 0.002736 kg*m^2.

4. Mass/inertia sample correlation is 0.891984.

5. Independent inertia sampling implies a rod-length RMSE of 0.007175 m relative to the actual sampled length.

#### Worked case 2: range_fraction = 0.05

This case keeps the nominal configuration except for range_fraction=0.05. The full input is {"range_fraction": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mass std kg | 0.08119077 |
| consistent inertia std kg m2 | 0.00547789 |
| mass inertia correlation | 0.89204348 |
| independent implied length rmse m | 0.01435604 |
| maximum consistent inertia kg m2 | 0.07286513 |

1. Sample density and length scales within +/-5 percent.

2. Derive mass and inertia from the same physical dimensions rather than unrelated ranges.

3. Mass standard deviation is 0.081191 kg and inertia standard deviation is 0.005478 kg*m^2.

4. Mass/inertia sample correlation is 0.892043.

5. Independent inertia sampling implies a rod-length RMSE of 0.014356 m relative to the actual sampled length.

#### Worked case 3: range_fraction = 0.1

This case keeps the nominal configuration except for range_fraction=0.1. The full input is {"range_fraction": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mass std kg | 0.16250174 |
| consistent inertia std kg m2 | 0.01100211 |
| mass inertia correlation | 0.89223425 |
| independent implied length rmse m | 0.02875988 |
| maximum consistent inertia kg m2 | 0.08769602 |

1. Sample density and length scales within +/-10 percent.

2. Derive mass and inertia from the same physical dimensions rather than unrelated ranges.

3. Mass standard deviation is 0.162502 kg and inertia standard deviation is 0.011002 kg*m^2.

4. Mass/inertia sample correlation is 0.892234.

5. Independent inertia sampling implies a rod-length RMSE of 0.028760 m relative to the actual sampled length.

#### Worked case 4: range_fraction = 0.2

This case keeps the nominal configuration except for range_fraction=0.2. The full input is {"range_fraction": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mass std kg | 0.32589935 |
| consistent inertia std kg m2 | 0.02236775 |
| mass inertia correlation | 0.89287222 |
| independent implied length rmse m | 0.05793277 |
| maximum consistent inertia kg m2 | 0.12402677 |

1. Sample density and length scales within +/-20 percent.

2. Derive mass and inertia from the same physical dimensions rather than unrelated ranges.

3. Mass standard deviation is 0.325899 kg and inertia standard deviation is 0.022368 kg*m^2.

4. Mass/inertia sample correlation is 0.892872.

5. Independent inertia sampling implies a rod-length RMSE of 0.057933 m relative to the actual sampled length.

#### Worked case 5: range_fraction = 0.3

This case keeps the nominal configuration except for range_fraction=0.3. The full input is {"range_fraction": 0.3}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| mass std kg | 0.49101698 |
| consistent inertia std kg m2 | 0.03445635 |
| mass inertia correlation | 0.89376348 |
| independent implied length rmse m | 0.08801483 |
| maximum consistent inertia kg m2 | 0.17062402 |

1. Sample density and length scales within +/-30 percent.

2. Derive mass and inertia from the same physical dimensions rather than unrelated ranges.

3. Mass standard deviation is 0.491017 kg and inertia standard deviation is 0.034456 kg*m^2.

4. Mass/inertia sample correlation is 0.893763.

5. Independent inertia sampling implies a rod-length RMSE of 0.088015 m relative to the actual sampled length.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

The chosen manufacturing model is still simplified; real uncertainty may arise from payload, assembly and calibration rather than density changes.

Randomization ranges need identification evidence and held-out evaluation, not just an intuition that more variation is safer.

### K. Failure modes and troubleshooting

Sampling nonphysical inertias; randomizing unobservable ground truth instead of measurements; choosing ranges after looking at final test performance.

### L. Practical exercises and extension tasks

1. Add a discrete payload mode instead of scaling every link.

2. Correlate friction with temperature in a measured way.

3. Separate training randomization and held-out stress conditions.

### M. Connection to the Asimov research platform

Sim-to-real ranges should reflect measured actuator strength, delays, contact surfaces, calibration error and expected operating conditions.

### N. Completion record

Record your chosen case, predicted trend, measured mass_std_kg, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 57, Fall rates, confidence intervals and finite evidence. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 57 - Fall rates, confidence intervals and finite evidence

### A. The engineering question

A controller that does not fall in a small number of trials has not demonstrated zero failure probability.

### B. Concepts and mathematical model

Report the number of trials, condition distribution, training seeds and observed failures. A confidence interval quantifies sampling uncertainty under assumptions about independent comparable trials; it does not cover untested terrain or correlated hardware faults. This laboratory calculates a Wilson binomial interval and an exact one-sided upper bound for the special zero-failure case.

Wilson center=(p_hat+z^2/(2n))/(1+z^2/n); zero-failure one-sided upper bound=1-alpha^(1/n).

### C. Real-world meaning and limits

Physical risk assessment requires broader evidence than binomial simulation fall counts, including consequences and independent protection.

### D. Architecture and data flow

Configuration (trials, observed_fraction) -> numerical model -> observed_failure_fraction, wilson_lower, wilson_upper -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

trials is the independent comparable evaluation count; observed_fraction is converted to an integer failure count and reported exactly.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| trials | 100 | Defined by the explicit chapter model and parameter contract |
| observed_fraction | 0.02 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/57_evaluation_intervals.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only trials changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/57_evaluation_intervals.py --case 0

.venv-book/bin/python expanded_lab/modules/57_evaluation_intervals.py --case 3

.venv-book/bin/python expanded_lab/run.py evaluation_intervals --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/57_evaluation_intervals.py

### H. Walkthrough and design decisions

Retain integer failures and trials before computing a fraction. The interval width and zero-failure bound make the limits of a small demonstration explicit.

### I. Expected behavior and six worked cases

The controlled variable is trials. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/57_evaluation_intervals.png

Figure L57. observed failure fraction as trials changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | trials | observed failure fraction |
|---|---|---|
| 0 | 10 | 0 |
| 1 | 20 | 0 |
| 2 | 50 | 0.02 |
| 3 | 100 | 0.02 |
| 4 | 500 | 0.02 |
| 5 | 1000 | 0.02 |

#### Worked case 0: trials = 10

This case keeps the nominal configuration except for trials=10. The full input is {"observed_fraction": 0.02, "trials": 10}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed failure fraction | 0 |
| wilson lower | 0 |
| wilson upper | 0.2775328 |
| zero failure upper if applicable | 0.25886555 |
| observed failures | 0 |

1. Use 10 trials and 0 observed failures.

2. Observed fraction is 0.00000000.

3. The 95% Wilson interval is [0.00000000,0.27753280].

4. If all 10 trials had zero failures, a one-sided 95% upper bound would be 0.25886555.

5. The zero-failure formula solves (1-p)^n=0.05 under the binomial independent-trial assumption.

#### Worked case 1: trials = 20

This case keeps the nominal configuration except for trials=20. The full input is {"observed_fraction": 0.02, "trials": 20}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed failure fraction | 0 |
| wilson lower | 0 |
| wilson upper | 0.16112516 |
| zero failure upper if applicable | 0.13910834 |
| observed failures | 0 |

1. Use 20 trials and 0 observed failures.

2. Observed fraction is 0.00000000.

3. The 95% Wilson interval is [0.00000000,0.16112516].

4. If all 20 trials had zero failures, a one-sided 95% upper bound would be 0.13910834.

5. The zero-failure formula solves (1-p)^n=0.05 under the binomial independent-trial assumption.

#### Worked case 2: trials = 50

This case keeps the nominal configuration except for trials=50. The full input is {"observed_fraction": 0.02, "trials": 50}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed failure fraction | 0.02 |
| wilson lower | 0.00353926 |
| wilson upper | 0.10495444 |
| zero failure upper if applicable | 0.05815508 |
| observed failures | 1 |

1. Use 50 trials and 1 observed failures.

2. Observed fraction is 0.02000000.

3. The 95% Wilson interval is [0.00353926,0.10495444].

4. If all 50 trials had zero failures, a one-sided 95% upper bound would be 0.05815508.

5. The zero-failure formula solves (1-p)^n=0.05 under the binomial independent-trial assumption.

#### Worked case 3: trials = 100

This case keeps the nominal configuration except for trials=100. The full input is {"observed_fraction": 0.02, "trials": 100}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed failure fraction | 0.02 |
| wilson lower | 0.00550197 |
| wilson upper | 0.07001179 |
| zero failure upper if applicable | 0.02951305 |
| observed failures | 2 |

1. Use 100 trials and 2 observed failures.

2. Observed fraction is 0.02000000.

3. The 95% Wilson interval is [0.00550197,0.07001179].

4. If all 100 trials had zero failures, a one-sided 95% upper bound would be 0.02951305.

5. The zero-failure formula solves (1-p)^n=0.05 under the binomial independent-trial assumption.

#### Worked case 4: trials = 500

This case keeps the nominal configuration except for trials=500. The full input is {"observed_fraction": 0.02, "trials": 500}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed failure fraction | 0.02 |
| wilson lower | 0.01089918 |
| wilson upper | 0.03642018 |
| zero failure upper if applicable | 0.00597355 |
| observed failures | 10 |

1. Use 500 trials and 10 observed failures.

2. Observed fraction is 0.02000000.

3. The 95% Wilson interval is [0.01089918,0.03642018].

4. If all 500 trials had zero failures, a one-sided 95% upper bound would be 0.00597355.

5. The zero-failure formula solves (1-p)^n=0.05 under the binomial independent-trial assumption.

#### Worked case 5: trials = 1000

This case keeps the nominal configuration except for trials=1000. The full input is {"observed_fraction": 0.02, "trials": 1000}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| observed failure fraction | 0.02 |
| wilson lower | 0.01298368 |
| wilson upper | 0.03069001 |
| zero failure upper if applicable | 0.00299125 |
| observed failures | 20 |

1. Use 1000 trials and 20 observed failures.

2. Observed fraction is 0.02000000.

3. The 95% Wilson interval is [0.01298368,0.03069001].

4. If all 1000 trials had zero failures, a one-sided 95% upper bound would be 0.00299125.

5. The zero-failure formula solves (1-p)^n=0.05 under the binomial independent-trial assumption.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Changing the terrain, disturbance distribution or controller release changes the population to which these intervals apply.

Repeated trials with shared initialization or correlated faults may provide less information than the independent model assumes.

### K. Failure modes and troubleshooting

Reporting only percentage without denominator; combining unlike test conditions into one reassuring score; treating simulated trials as physical reliability evidence.

### L. Practical exercises and extension tasks

1. Calculate trials required to bound zero-failure probability below a chosen level.

2. Report intervals separately by terrain and training seed.

3. Model correlated failures and compare effective evidence.

### M. Connection to the Asimov research platform

Physical risk assessment requires broader evidence than binomial simulation fall counts, including consequences and independent protection.

### N. Completion record

Record your chosen case, predicted trend, measured observed_failure_fraction, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 58, Gait phase metrics, contact slip and energy accounting. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 58 - Gait phase metrics, contact slip and energy accounting

### A. The engineering question

A walking evaluation needs more than distance traveled.

### B. Concepts and mathematical model

A falling robot can move far, a dragging foot can track velocity, and a low net-energy number can hide large power peaks. Contact-conditioned slip should exclude swing motion. This laboratory synthesizes a walking-like trace with known command, stance masks and controlled slip, then computes tracking, path distance, positive mechanical work and contact slip. It demonstrates metric definitions without claiming a trained gait.

distance=sum(||delta xy||); tracking_RMSE=sqrt(mean((v-v_cmd)^2)); slip_RMS uses stance samples only; positive work=integral(max(P,0) dt).

### C. Real-world meaning and limits

Use measured/estimated world-frame foot motion and contact load confidence when evaluating a real gait.

### D. Architecture and data flow

Configuration (stance_slip) -> numerical model -> distance_m, velocity_rmse_m_s, stance_slip_rms_m_s -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

stance_slip is synthetic loaded-foot world speed in m/s; stance mask is known truth for the metric test.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| stance_slip | 0.01 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/58_gait_evaluation.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only stance_slip changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/58_gait_evaluation.py --case 0

.venv-book/bin/python expanded_lab/modules/58_gait_evaluation.py --case 3

.venv-book/bin/python expanded_lab/run.py gait_evaluation --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/58_gait_evaluation.py

### H. Walkthrough and design decisions

The all-phase foot-speed metric is deliberately included as a counterexample: it mainly measures swing, not unwanted slip. Contact confidence should accompany real metric reports.

### I. Expected behavior and six worked cases

The controlled variable is stance_slip. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/58_gait_evaluation.png

Figure L58. distance m as stance_slip changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | stance_slip | distance m |
|---|---|---|
| 0 | 0 | 1.998 |
| 1 | 0.002 | 1.998 |
| 2 | 0.005 | 1.998 |
| 3 | 0.01 | 1.998 |
| 4 | 0.03 | 1.998 |
| 5 | 0.1 | 1.998 |

#### Worked case 0: stance_slip = 0

This case keeps the nominal configuration except for stance_slip=0. The full input is {"stance_slip": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| distance m | 1.998 |
| velocity rmse m s | 0.01414214 |
| stance slip rms m s | 0 |
| all phase foot speed rms m s | 0.1466101 |
| positive mechanical work J | 119.88251162 |
| stance fraction | 0.602 |

1. Create a ten-second synthetic trajectory commanded at 0.2 m/s.

2. Loaded-stance foot speed is 0 m/s; swing motion is excluded from the slip metric.

3. Distance is 1.998000 m and velocity RMSE is 0.014142 m/s.

4. Stance-only slip RMS is 0.000000 m/s while all-phase RMS is 0.146610 m/s.

5. Positive mechanical work is 119.882512 J.

#### Worked case 1: stance_slip = 0.002

This case keeps the nominal configuration except for stance_slip=0.002. The full input is {"stance_slip": 0.002}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| distance m | 1.998 |
| velocity rmse m s | 0.01414214 |
| stance slip rms m s | 0.002 |
| all phase foot speed rms m s | 0.14661831 |
| positive mechanical work J | 119.88251162 |
| stance fraction | 0.602 |

1. Create a ten-second synthetic trajectory commanded at 0.2 m/s.

2. Loaded-stance foot speed is 0.002 m/s; swing motion is excluded from the slip metric.

3. Distance is 1.998000 m and velocity RMSE is 0.014142 m/s.

4. Stance-only slip RMS is 0.002000 m/s while all-phase RMS is 0.146618 m/s.

5. Positive mechanical work is 119.882512 J.

#### Worked case 2: stance_slip = 0.005

This case keeps the nominal configuration except for stance_slip=0.005. The full input is {"stance_slip": 0.005}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| distance m | 1.998 |
| velocity rmse m s | 0.01414214 |
| stance slip rms m s | 0.005 |
| all phase foot speed rms m s | 0.14666141 |
| positive mechanical work J | 119.88251162 |
| stance fraction | 0.602 |

1. Create a ten-second synthetic trajectory commanded at 0.2 m/s.

2. Loaded-stance foot speed is 0.005 m/s; swing motion is excluded from the slip metric.

3. Distance is 1.998000 m and velocity RMSE is 0.014142 m/s.

4. Stance-only slip RMS is 0.005000 m/s while all-phase RMS is 0.146661 m/s.

5. Positive mechanical work is 119.882512 J.

#### Worked case 3: stance_slip = 0.01

This case keeps the nominal configuration except for stance_slip=0.01. The full input is {"stance_slip": 0.01}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| distance m | 1.998 |
| velocity rmse m s | 0.01414214 |
| stance slip rms m s | 0.01 |
| all phase foot speed rms m s | 0.14681526 |
| positive mechanical work J | 119.88251162 |
| stance fraction | 0.602 |

1. Create a ten-second synthetic trajectory commanded at 0.2 m/s.

2. Loaded-stance foot speed is 0.01 m/s; swing motion is excluded from the slip metric.

3. Distance is 1.998000 m and velocity RMSE is 0.014142 m/s.

4. Stance-only slip RMS is 0.010000 m/s while all-phase RMS is 0.146815 m/s.

5. Positive mechanical work is 119.882512 J.

#### Worked case 4: stance_slip = 0.03

This case keeps the nominal configuration except for stance_slip=0.03. The full input is {"stance_slip": 0.03}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| distance m | 1.998 |
| velocity rmse m s | 0.01414214 |
| stance slip rms m s | 0.03 |
| all phase foot speed rms m s | 0.14844635 |
| positive mechanical work J | 119.88251162 |
| stance fraction | 0.602 |

1. Create a ten-second synthetic trajectory commanded at 0.2 m/s.

2. Loaded-stance foot speed is 0.03 m/s; swing motion is excluded from the slip metric.

3. Distance is 1.998000 m and velocity RMSE is 0.014142 m/s.

4. Stance-only slip RMS is 0.030000 m/s while all-phase RMS is 0.148446 m/s.

5. Positive mechanical work is 119.882512 J.

#### Worked case 5: stance_slip = 0.1

This case keeps the nominal configuration except for stance_slip=0.1. The full input is {"stance_slip": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| distance m | 1.998 |
| velocity rmse m s | 0.01414214 |
| stance slip rms m s | 0.1 |
| all phase foot speed rms m s | 0.16587501 |
| positive mechanical work J | 119.88251162 |
| stance fraction | 0.602 |

1. Create a ten-second synthetic trajectory commanded at 0.2 m/s.

2. Loaded-stance foot speed is 0.1 m/s; swing motion is excluded from the slip metric.

3. Distance is 1.998000 m and velocity RMSE is 0.014142 m/s.

4. Stance-only slip RMS is 0.100000 m/s while all-phase RMS is 0.165875 m/s.

5. Positive mechanical work is 119.882512 J.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

These traces are synthetic metric fixtures, not walking results from the Asimov model.

Mechanical work is not battery energy; physical electrical measurements require voltage/current timing and regeneration accounting.

### K. Failure modes and troubleshooting

Including swing speed in foot slip; integrating commanded velocity instead of measured motion; omitting falls from a distance score.

### L. Practical exercises and extension tasks

1. Add a fall event and report survival time separately from distance.

2. Include commanded yaw-rate tracking.

3. Use uncertain contact labels and quantify metric sensitivity.

### M. Connection to the Asimov research platform

Use measured/estimated world-frame foot motion and contact load confidence when evaluating a real gait.

### N. Completion record

Record your chosen case, predicted trend, measured distance_m, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 59, Color segmentation, false positives and image-space evidence. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 59 - Color segmentation, false positives and image-space evidence

### A. The engineering question

A controlled color target is useful for testing the perception-to-behavior path before adding a learned detector.

### B. Concepts and mathematical model

Thresholding is sensitive to illumination, distractors, sensor noise and object size. Pixel area is not physical area unless camera geometry and depth are known. This experiment creates a labeled synthetic RGB-like image, adds noise and measures precision, recall and centroid error for a simple green-excess threshold. It provides a ground-truth test fixture, not a benchmark of real camera performance.

mask=(G-R>threshold) and (G-B>threshold); precision=TP/(TP+FP); recall=TP/(TP+FN).

### C. Real-world meaning and limits

Physical perception must carry timestamps, calibration identity, uncertainty and an explicit no-detection result into the skill supervisor.

### D. Architecture and data flow

Configuration (noise_std) -> numerical model -> precision, recall, centroid_error_px -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

noise_std is synthetic per-channel intensity noise on a 0-255 scale; images are teaching arrays, not captured hardware frames.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| noise_std | 10 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/59_image_segmentation.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only noise_std changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/59_image_segmentation.py --case 0

.venv-book/bin/python expanded_lab/modules/59_image_segmentation.py --case 3

.venv-book/bin/python expanded_lab/run.py image_segmentation --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/59_image_segmentation.py

### H. Walkthrough and design decisions

Ground-truth masks make precision and recall calculable. Evaluate centroid localization separately from pixel classification because a small false-positive region far away can shift the target estimate.

### I. Expected behavior and six worked cases

The controlled variable is noise_std. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/59_image_segmentation.png

Figure L59. precision as noise_std changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | noise_std | precision |
|---|---|---|
| 0 | 0 | 1 |
| 1 | 5 | 0.98901099 |
| 2 | 10 | 0.94637224 |
| 3 | 20 | 0.9010101 |
| 4 | 30 | 0.72687986 |
| 5 | 50 | 0.37038988 |

#### Worked case 0: noise_std = 0

This case keeps the nominal configuration except for noise_std=0. The full input is {"noise_std": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| precision | 1 |
| recall | 1 |
| centroid error px | 0 |
| predicted area px | 900 |
| false positive pixels | 0 |

1. Place a 30x30 pixel bright-green target and a dimmer green distractor in a 160x120 image.

2. Add pixel-channel noise sigma=0.

3. Threshold green excess over red and blue by 70 intensity units.

4. Count TP=900, FP=0, FN=0; precision=1.000000, recall=1.000000.

5. The predicted-mask centroid differs from the target center by 0.000000 pixels.

#### Worked case 1: noise_std = 5

This case keeps the nominal configuration except for noise_std=5. The full input is {"noise_std": 5.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| precision | 0.98901099 |
| recall | 1 |
| centroid error px | 1.01671693 |
| predicted area px | 910 |
| false positive pixels | 10 |

1. Place a 30x30 pixel bright-green target and a dimmer green distractor in a 160x120 image.

2. Add pixel-channel noise sigma=5.

3. Threshold green excess over red and blue by 70 intensity units.

4. Count TP=900, FP=10, FN=0; precision=0.989011, recall=1.000000.

5. The predicted-mask centroid differs from the target center by 1.016717 pixels.

#### Worked case 2: noise_std = 10

This case keeps the nominal configuration except for noise_std=10. The full input is {"noise_std": 10.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| precision | 0.94637224 |
| recall | 1 |
| centroid error px | 4.96058189 |
| predicted area px | 951 |
| false positive pixels | 51 |

1. Place a 30x30 pixel bright-green target and a dimmer green distractor in a 160x120 image.

2. Add pixel-channel noise sigma=10.

3. Threshold green excess over red and blue by 70 intensity units.

4. Count TP=900, FP=51, FN=0; precision=0.946372, recall=1.000000.

5. The predicted-mask centroid differs from the target center by 4.960582 pixels.

#### Worked case 3: noise_std = 20

This case keeps the nominal configuration except for noise_std=20. The full input is {"noise_std": 20.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| precision | 0.9010101 |
| recall | 0.99111111 |
| centroid error px | 8.2329377 |
| predicted area px | 990 |
| false positive pixels | 98 |

1. Place a 30x30 pixel bright-green target and a dimmer green distractor in a 160x120 image.

2. Add pixel-channel noise sigma=20.

3. Threshold green excess over red and blue by 70 intensity units.

4. Count TP=892, FP=98, FN=8; precision=0.901010, recall=0.991111.

5. The predicted-mask centroid differs from the target center by 8.232938 pixels.

#### Worked case 4: noise_std = 30

This case keeps the nominal configuration except for noise_std=30. The full input is {"noise_std": 30.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| precision | 0.72687986 |
| recall | 0.93444444 |
| centroid error px | 12.78969139 |
| predicted area px | 1157 |
| false positive pixels | 316 |

1. Place a 30x30 pixel bright-green target and a dimmer green distractor in a 160x120 image.

2. Add pixel-channel noise sigma=30.

3. Threshold green excess over red and blue by 70 intensity units.

4. Count TP=841, FP=316, FN=59; precision=0.726880, recall=0.934444.

5. The predicted-mask centroid differs from the target center by 12.789691 pixels.

#### Worked case 5: noise_std = 50

This case keeps the nominal configuration except for noise_std=50. The full input is {"noise_std": 50.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| precision | 0.37038988 |
| recall | 0.78111111 |
| centroid error px | 19.47774569 |
| predicted area px | 1898 |
| false positive pixels | 1195 |

1. Place a 30x30 pixel bright-green target and a dimmer green distractor in a 160x120 image.

2. Add pixel-channel noise sigma=50.

3. Threshold green excess over red and blue by 70 intensity units.

4. Count TP=703, FP=1195, FN=197; precision=0.370390, recall=0.781111.

5. The predicted-mask centroid differs from the target center by 19.477746 pixels.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

All foreground pixels are pooled, so distractors can shift the centroid; connected-component selection is an important extension.

No depth or metric reach target is inferred from this mask.

### K. Failure modes and troubleshooting

Calling color classification object recognition; ignoring distractors; converting pixel coordinates directly into joint targets without calibration.

### L. Practical exercises and extension tasks

1. Add connected-component filtering and compare centroid error.

2. Vary illumination independently of sensor noise.

3. Build a real-image held-out dataset under declared lighting.

### M. Connection to the Asimov research platform

Physical perception must carry timestamps, calibration identity, uncertainty and an explicit no-detection result into the skill supervisor.

### N. Completion record

Record your chosen case, predicted trend, measured precision, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 60, Allowlisted skills, bounded parameters and behavior outcomes. Keep the present result as a reference fixture for diagnosing changes in the larger stack.

## Laboratory 60 - Allowlisted skills, bounded parameters and behavior outcomes

### A. The engineering question

High-level instruction following should select a validated capability rather than generate arbitrary low-level actuation.

### B. Concepts and mathematical model

A skill request needs a fixed name, a bounded parameter schema, preconditions and a timeout. Invalid requests should produce a clear rejection without partially applying motion. This experiment defines a small supported-gesture library and evaluates malformed, stale and over-limit planner requests. It isolates the task-selection boundary from both language-model implementation and physical transport.

approved_skill = allowlist[name] and parameters_in_bounds and readiness and fresh_request; execution requires feedback-based completion.

### C. Real-world meaning and limits

A physical skill library must expose only commissioned capabilities and keep local limits, watchdogs and independent stop authority in control.

### D. Architecture and data flow

Configuration (amplitude) -> numerical model -> approved_requests, rejected_requests, requested_amplitude_rad -> assertions and experiment record.

### E. Prerequisites and parameter contract

Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; it has no simulator, ROS or physical-transport dependency. The complete module is printed below and saved at the specified path. A fixed seed is part of the experiment where randomness is present.

amplitude is a requested supported-joint excursion in radians; the 0.1 rad limit is an educational schema choice.

| Parameter | Nominal value | Interpretation |
|---|---|---|
| amplitude | 0.05 | Defined by the explicit chapter model and parameter contract |

### F. Implementation and experiment protocol

1. Read the model equation and identify which assumptions separate it from the physical robot.

2. Open /data/Robotics_Project/expanded_lab/modules/60_skill_planner.py and locate the experiment function before running it.

3. Run case 0, then case 3 and case 5. Only amplitude changes in the published study.

4. Predict the direction of change in the first metric before comparing with the worked solutions.

5. Re-run the complete six-case study and preserve results with the source and environment identity.

```bash

cd /data/Robotics_Project

.venv-book/bin/python expanded_lab/modules/60_skill_planner.py --case 0

.venv-book/bin/python expanded_lab/modules/60_skill_planner.py --case 3

.venv-book/bin/python expanded_lab/run.py skill_planner --case 5

```

The supplied .venv-book was used to prepare the numerical results. On another machine, use your own Lesson 0 environment instead of assuming that directory has been copied or is portable.

### G. Complete executable implementation

!code expanded_lab/modules/60_skill_planner.py

### H. Walkthrough and design decisions

Separate request approval from execution and completion. The unknown-skill test proves the planner cannot introduce a new actuation capability by naming it.

### I. Expected behavior and six worked cases

The controlled variable is amplitude. All other parameters stay at their declared nominal values. The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.

!image expanded_lab/results/60_skill_planner.png

Figure L60. approved requests as amplitude changes. Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.

| Case | amplitude | approved requests |
|---|---|---|
| 0 | -0.05 | 1 |
| 1 | 0 | 2 |
| 2 | 0.025 | 2 |
| 3 | 0.05 | 2 |
| 4 | 0.1 | 2 |
| 5 | 0.2 | 1 |

#### Worked case 0: amplitude = -0.05

This case keeps the nominal configuration except for amplitude=-0.05. The full input is {"amplitude": -0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| approved requests | 1 |
| rejected requests | 3 |
| requested amplitude rad | -0.05 |
| primary request approved | 0 |
| inactive request approved | 0 |

1. The planner requests supported_wave amplitude -0.05 rad.

2. The allowlist contains observe and supported_wave only.

3. Decisions for normal, unknown, stale and observation requests are [(False, 'amplitude'), (False, 'unknown_skill'), (False, 'stale'), (True, 'approved')].

4. Approved 1 requests and rejected 3.

5. The same request with readiness false is rejected as not_ready.

#### Worked case 1: amplitude = 0

This case keeps the nominal configuration except for amplitude=0. The full input is {"amplitude": 0.0}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| approved requests | 2 |
| rejected requests | 2 |
| requested amplitude rad | 0 |
| primary request approved | 1 |
| inactive request approved | 0 |

1. The planner requests supported_wave amplitude 0 rad.

2. The allowlist contains observe and supported_wave only.

3. Decisions for normal, unknown, stale and observation requests are [(True, 'approved'), (False, 'unknown_skill'), (False, 'stale'), (True, 'approved')].

4. Approved 2 requests and rejected 2.

5. The same request with readiness false is rejected as not_ready.

#### Worked case 2: amplitude = 0.025

This case keeps the nominal configuration except for amplitude=0.025. The full input is {"amplitude": 0.025}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| approved requests | 2 |
| rejected requests | 2 |
| requested amplitude rad | 0.025 |
| primary request approved | 1 |
| inactive request approved | 0 |

1. The planner requests supported_wave amplitude 0.025 rad.

2. The allowlist contains observe and supported_wave only.

3. Decisions for normal, unknown, stale and observation requests are [(True, 'approved'), (False, 'unknown_skill'), (False, 'stale'), (True, 'approved')].

4. Approved 2 requests and rejected 2.

5. The same request with readiness false is rejected as not_ready.

#### Worked case 3: amplitude = 0.05

This case keeps the nominal configuration except for amplitude=0.05. The full input is {"amplitude": 0.05}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| approved requests | 2 |
| rejected requests | 2 |
| requested amplitude rad | 0.05 |
| primary request approved | 1 |
| inactive request approved | 0 |

1. The planner requests supported_wave amplitude 0.05 rad.

2. The allowlist contains observe and supported_wave only.

3. Decisions for normal, unknown, stale and observation requests are [(True, 'approved'), (False, 'unknown_skill'), (False, 'stale'), (True, 'approved')].

4. Approved 2 requests and rejected 2.

5. The same request with readiness false is rejected as not_ready.

#### Worked case 4: amplitude = 0.1

This case keeps the nominal configuration except for amplitude=0.1. The full input is {"amplitude": 0.1}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| approved requests | 2 |
| rejected requests | 2 |
| requested amplitude rad | 0.1 |
| primary request approved | 1 |
| inactive request approved | 0 |

1. The planner requests supported_wave amplitude 0.1 rad.

2. The allowlist contains observe and supported_wave only.

3. Decisions for normal, unknown, stale and observation requests are [(True, 'approved'), (False, 'unknown_skill'), (False, 'stale'), (True, 'approved')].

4. Approved 2 requests and rejected 2.

5. The same request with readiness false is rejected as not_ready.

#### Worked case 5: amplitude = 0.2

This case keeps the nominal configuration except for amplitude=0.2. The full input is {"amplitude": 0.2}. Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.

| Computed quantity | Numerical result |
|---|---|
| approved requests | 1 |
| rejected requests | 3 |
| requested amplitude rad | 0.2 |
| primary request approved | 0 |
| inactive request approved | 0 |

1. The planner requests supported_wave amplitude 0.2 rad.

2. The allowlist contains observe and supported_wave only.

3. Decisions for normal, unknown, stale and observation requests are [(False, 'amplitude'), (False, 'unknown_skill'), (False, 'stale'), (True, 'approved')].

4. Approved 1 requests and rejected 3.

5. The same request with readiness false is rejected as not_ready.

### J. Validation and independent reasoning

All six published configurations were executed with finite numerical results. Assertions in the module check the stated identities or state-machine invariants where applicable. Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.

Approval is permission to start a bounded skill; it is not proof the physical task completed.

The executor still needs cancellation, tracking checks, timeout and a reviewed stop response.

### K. Failure modes and troubleshooting

Accepting arbitrary code from a planner; confusing language confidence with readiness; considering a successful API call a completed physical task.

### L. Practical exercises and extension tasks

1. Add strict unknown-field rejection and a schema version.

2. Define feedback-based success for the supported gesture.

3. Inject observation disappearance between approval and execution.

### M. Connection to the Asimov research platform

A physical skill library must expose only commissioned capabilities and keep local limits, watchdogs and independent stop authority in control.

### N. Completion record

Record your chosen case, predicted trend, measured approved_requests, the largest discrepancy from the worked result, and the explanation for that discrepancy. Preserve the code revision, environment identity and raw JSON. For a hardware connection, name the measurement or verified document that would replace each teaching assumption before use.

### O. Next laboratory connection

Continue with Laboratory 61, Landed cost, VAT, contingency and scope decisions. Keep the present result as a reference fixture for diagnosing changes in the larger stack.
