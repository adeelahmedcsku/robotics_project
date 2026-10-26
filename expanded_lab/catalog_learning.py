from catalog import add
add('discounted_return','Markov decision processes and discounted reward',
'''A reward function expresses what training should favor, but its meaning depends on episode duration, timestep and discounting. Reward per step can change when policy rate changes even if physical behavior stays identical. Discounted return weights near-term and distant outcomes differently. This laboratory compares a short immediate reward with a delayed larger reward and calculates the effective discount horizon. It is a reasoning tool for reward design, not an argument that one discount factor is universally correct.''',
'G_t=sum(gamma^k*r[t+k]); continuous-time discount gamma=exp(-dt/tau); horizon scale approx 1/(1-gamma) steps.',
r'''
def experiment(p):
    gamma=p['gamma'];dt=.02
    immediate=np.zeros(100);delayed=np.zeros(100)
    immediate[0]=1.;delayed[50]=3.
    weights=gamma**np.arange(100)
    a=float(weights@immediate);b=float(weights@delayed)
    horizon=1/(1-gamma)
    tau=-dt/np.log(gamma)
    metrics=dict(immediate_return=a,delayed_return=b,
        delayed_preference_margin=b-a,effective_horizon_steps=horizon,
        continuous_time_scale_s=tau)
    derivation=[f'Choose gamma={gamma:g} at control period {dt:g} s.',
        'One candidate receives reward 1 now; the other receives reward 3 after 50 steps.',
        f'Immediate return is {a:.6f}; delayed return is 3*gamma^50={b:.6f}.',
        f'The geometric horizon scale is {horizon:.6f} steps.',
        f'The matching exponential time constant is {tau:.6f} s.']
    notes=[('The delayed outcome is preferred under this discount.' if b>a else
            'The immediate outcome is preferred despite the larger undiscounted delayed reward.'),
           'Episode termination, reward scaling and physical-time interpretation remain part of the task specification.']
    return metrics,derivation,notes
''',dict(gamma=.99),'gamma',[.9,.95,.97,.98,.99,.995],
'gamma is a dimensionless per-policy-step discount strictly between zero and one; the teaching policy step is 20 ms.',
'The sparse reward sequences isolate discount preference from action dynamics. Mapping gamma to seconds prevents accidental task changes when control frequency changes.',
'Comparing returns across different timesteps without rescaling; rewarding survival while ignoring command tracking; hiding terminal rewards in long episodes.',
['Keep a fixed discount time constant while changing policy period.','Add per-second energy cost and discretize it consistently.','Construct a reward-hacking example with a safe-looking but unproductive action.'],
'Physical task success must be evaluated directly; training return alone does not establish useful robot behavior.')

add('gae','Temporal-difference residuals, GAE and episode boundaries',
'''An advantage estimate compares an action's outcome with the value baseline for its state. Generalized Advantage Estimation combines temporal-difference residuals over multiple horizons, trading variance against sensitivity to value errors. Episode boundaries matter: a true terminal state differs from an externally imposed time limit that still has continuation value. This laboratory computes the backward recurrence explicitly and exposes the effect of the lambda parameter while holding rewards and values fixed.''',
'delta_t=r_t+gamma*V_next-V_t; A_t=delta_t+gamma*lambda*A_next, with valid terminal/continuation masks.',
r'''
def experiment(p):
    gamma=.99;lam=p['gae_lambda']
    rewards=np.array([.2,.1,-.1,.3,1.])
    values=np.array([.4,.45,.3,.5,.6,0.])
    terminal=np.array([False,False,False,False,True])
    advantage=np.zeros(5);carry=0.;residual=[]
    for t in reversed(range(5)):
        continuation=0. if terminal[t] else 1.
        delta=rewards[t]+gamma*values[t+1]*continuation-values[t]
        carry=delta+gamma*lam*continuation*carry
        advantage[t]=carry;residual.append(delta)
    returns=advantage+values[:-1]
    metrics=dict(initial_advantage=advantage[0],final_advantage=advantage[-1],
        advantage_std=np.std(advantage),initial_value_target=returns[0],
        mean_advantage=np.mean(advantage))
    derivation=[f'Use rewards {rewards.tolist()} and value predictions {values.tolist()}.',
        f'The last transition is truly terminal; gamma={gamma:g}, lambda={lam:g}.',
        f'Backward TD residuals in chronological order are {list(reversed(residual))}.',
        f'The resulting advantage vector is {advantage.tolist()}.',
        f'Value targets A+V are {returns.tolist()}.']
    notes=['A time-limit truncation may retain a bootstrap value while still preventing recurrence into the next reset episode.',
           'Correct masking needs separate termination and rollout-boundary semantics; one generic done flag can hide a bug.']
    return metrics,derivation,notes
''',dict(gae_lambda=.95),'gae_lambda',[0.,.25,.5,.75,.95,1.],
'gae_lambda is the dimensionless trace parameter; rewards, value predictions and one terminal boundary are fixed.',
'Run the recurrence backward and retain intermediate deltas so every term can be checked by hand. Lambda zero reduces to one-step TD residuals; lambda one includes the longest available trace.',
'Bootstrapping a true terminal as if it continued; propagating advantages across reset episodes; normalizing advantages without checking their construction.',
['Replace the final terminal with a time-limit truncation and nonzero final value.','Calculate the lambda-zero and lambda-one results manually.','Inject a value bias and compare its effect across lambda values.'],
'Correct learning plumbing is essential before expensive humanoid rollouts; masking bugs can invalidate apparently successful training.')

add('ppo_clipping','PPO clipping, advantage signs and surrogate objectives',
'''PPO's clipped surrogate is a constrained-update heuristic, not a direct clipping of the motor command. The probability ratio measures how the new policy changes likelihood of sampled actions. Whether clipping limits the objective depends on both the ratio and the advantage sign. A common implementation mistake is to apply the same intuitive rule to positive and negative advantages without evaluating the minimum. This laboratory computes both branches on a fixed batch so the behavior is inspectable.''',
'L=min(ratio*A,clip(ratio,1-epsilon,1+epsilon)*A); policy loss=-mean(L).',
r'''
def experiment(p):
    epsilon=p['clip_epsilon']
    ratios=np.array([.5,.8,.95,1.,1.05,1.2,1.5])
    advantage=np.array([-1.,-.5,1.,-.2,.5,1.,-1.])
    raw=ratios*advantage
    clipped=np.clip(ratios,1-epsilon,1+epsilon)*advantage
    objective=np.minimum(raw,clipped)
    active=np.abs(raw-objective)>1e-12
    metrics=dict(policy_loss=-np.mean(objective),unclipped_loss=-np.mean(raw),
        objective_changed_fraction=np.mean(active),
        ratio_outside_clip_fraction=np.mean((ratios<1-epsilon)|(ratios>1+epsilon)),
        minimum_sample_objective=np.min(objective))
    derivation=[f'Probability ratios are {ratios.tolist()}.',
        f'Advantages are {advantage.tolist()}; clipping epsilon is {epsilon:g}.',
        f'Unclipped sample objectives are {raw.tolist()}.',
        f'Apply the minimum with the clipped branch to obtain {objective.tolist()}.',
        f'Negative mean objective gives policy loss {metrics["policy_loss"]:.6f}.']
    notes=['Ratio outside the clip interval is not identical to a changed surrogate contribution; advantage sign matters.',
           'This calculation omits value loss, entropy bonus, optimizer behavior and rollout collection.']
    return metrics,derivation,notes
''',dict(clip_epsilon=.2),'clip_epsilon',[.05,.1,.15,.2,.3,.4],
'clip_epsilon is the dimensionless probability-ratio interval half-width; the sampled ratios and advantages are fixed.',
'Calculate raw and clipped products before taking their elementwise minimum. Inspect one positive-advantage and one negative-advantage sample by hand to verify the sign logic.',
'Confusing policy-ratio clipping with action limits; maximizing a loss written for minimization; interpreting clipping as a physical safety constraint.',
['Plot surrogate objective versus ratio for both advantage signs.','Add an entropy term and inspect its separate contribution.','Compare approximate KL diagnostics with the ratio distribution.'],
'Policy optimization constraints do not replace bounded action scaling, runtime supervision or physical commissioning.')

add('gaussian_policy','Gaussian policies, action limits and saturation probability',
'''A stochastic continuous policy often samples from a Gaussian distribution before applying environment bounds. Large standard deviation can create many clipped actions, changing the action distribution seen by the plant. A bounded tanh transformation has different density mathematics from simple clipping. This laboratory quantifies clipping frequency and variance reduction for a one-dimensional Gaussian policy. It also calculates Gaussian entropy so exploration magnitude has an interpretable scale.''',
'a_raw~Normal(mu,sigma^2); a=clip(a_raw,-1,1); entropy=0.5*log(2*pi*e*sigma^2).',
r'''
def experiment(p):
    rng=np.random.default_rng(67);mu=p['mean'];sigma=p['std']
    raw=rng.normal(mu,sigma,20000);bounded=np.clip(raw,-1,1)
    entropy=.5*np.log(2*np.pi*np.e*sigma*sigma)
    metrics=dict(clipped_fraction=np.mean(abs(raw)>1),raw_mean=np.mean(raw),
        bounded_mean=np.mean(bounded),raw_std=np.std(raw),bounded_std=np.std(bounded),
        gaussian_entropy_nats=entropy)
    derivation=[f'Sample 20,000 actions from mean {mu:g} and standard deviation {sigma:g}.',
        f'Unbounded Gaussian entropy is {entropy:.6f} nats.',
        f'Clip to [-1,1]; clipped fraction is {metrics["clipped_fraction"]:.6f}.',
        f'Raw sample standard deviation is {np.std(raw):.6f}; bounded standard deviation is {np.std(bounded):.6f}.',
        f'Bounded mean is {np.mean(bounded):.6f}, which can shift when clipping is asymmetric around the policy mean.']
    notes=['The entropy formula describes the unbounded Gaussian, not the clipped mixed distribution.',
           'A tanh-squashed policy requires a change-of-variables correction when computing log probabilities.']
    return metrics,derivation,notes
''',dict(mean=.2,std=.5),'std',[.05,.1,.2,.5,1.,2.],
'mean and std are normalized action units before the environment action scale and joint limits.',
'Compare raw and applied distributions rather than logging only the sampled Gaussian parameters. A high clipped fraction can make exploration look numerically broad while applied actions concentrate at limits.',
'Using raw Gaussian entropy as the applied distribution entropy; omitting export-time clipping; changing action scaling without retraining/evaluation.',
['Repeat with policy mean near an action boundary.','Compare clipping with tanh transformation histograms.','Propagate normalized actions into an actual simulated torque envelope.'],
'Physical inference generally uses deterministic policy evaluation plus explicit bounded action processing validated against training semantics.')

add('running_statistics','Streaming normalization, numerical stability and evaluation leakage',
'''Policies often require normalized observations. Streaming mean and variance can be estimated without retaining every sample, but evaluation must normally freeze the training statistics. Updating them on test observations changes the policy input distribution and leaks information across the evaluation boundary. This laboratory uses Welford's stable recurrence and compares a frozen training normalizer with a normalizer incorrectly refitted after a distribution shift.''',
'n+=1; delta=x-mean; mean+=delta/n; M2+=delta*(x-mean); variance=M2/(n-1).',
r'''
def welford(samples):
    n=0;mean=0.;M2=0.
    for value in samples:
        n+=1;delta=value-mean;mean+=delta/n;M2+=delta*(value-mean)
    return mean,M2/(n-1)

def experiment(p):
    rng=np.random.default_rng(71)
    training=rng.normal(0,1,5000);testing=rng.normal(p['test_shift'],1,1000)
    mean,var=welford(training)
    frozen=(testing-mean)/np.sqrt(var+1e-8)
    leaked_mean,leaked_var=welford(np.concatenate([training,testing]))
    leaked=(testing-leaked_mean)/np.sqrt(leaked_var+1e-8)
    assert np.isclose(mean,training.mean())
    assert np.isclose(var,np.var(training,ddof=1))
    metrics=dict(training_mean=mean,training_variance=var,
        frozen_test_mean=np.mean(frozen),leaked_test_mean=np.mean(leaked),
        mean_normalized_disagreement=np.mean(abs(frozen-leaked)))
    derivation=['Estimate training statistics with 5,000 seeded samples using Welford updates.',
        f'The held-out distribution has mean shift {p["test_shift"]:g}.',
        f'Frozen normalizer produces test mean {np.mean(frozen):.6f}.',
        f'Updating statistics with evaluation data changes the test mean to {np.mean(leaked):.6f}.',
        f'Mean per-sample normalized disagreement is {np.mean(abs(frozen-leaked)):.6f}.']
    notes=['A shifted test mean can be useful evidence of distribution shift; normalizing it away may hide the problem.',
           'Explicit online adaptation can be legitimate, but it is a different deployed algorithm requiring separate validation.']
    return metrics,derivation,notes
''',dict(test_shift=1.),'test_shift',[0.,.2,.5,1.,2.,4.],
'test_shift is the mean offset of the held-out synthetic observation distribution in raw channel units.',
'Verify the streaming calculation against a batch reference, then freeze it. Separate numerical correctness of the estimator from the experimental policy of when it is allowed to update.',
'Updating statistics during final evaluation; resetting normalizers when loading a policy; confusing population and sample variance conventions.',
['Extend Welford to vector observations.','Merge statistics from two independent training workers.','Store normalizer parameters and schema hash with a policy checkpoint.'],
'Hardware observation normalization must match the validated training/replay pipeline, including clipping and missing-data treatment.')

add('domain_randomization','Domain randomization, correlations and feasible parameter sets',
'''Randomization should represent plausible physical variation. Sampling every parameter independently can produce impossible combinations, such as mass and inertia that no real assembly could have. Correlated randomization can preserve relationships while exploring uncertainty. This laboratory samples a density scale and length scale, deriving mass and rod inertia consistently, then compares it with independent inertia sampling. It illustrates why wider randomization is not automatically better.''',
'For fixed cross-section with length scale sL and density scale srho: m=m0*srho*sL; I=m*(L0*sL)^2/3.',
r'''
def experiment(p):
    rng=np.random.default_rng(73);n=5000;width=p['range_fraction']
    density=rng.uniform(1-width,1+width,n)
    length_scale=rng.uniform(1-width,1+width,n)
    mass=2*density*length_scale;length=.3*length_scale
    consistent=mass*length**2/3
    independent=.06*rng.uniform(1-width,1+width,n)
    implied_length=np.sqrt(3*independent/mass)
    metrics=dict(mass_std_kg=np.std(mass),consistent_inertia_std_kg_m2=np.std(consistent),
        mass_inertia_correlation=np.corrcoef(mass,consistent)[0,1],
        independent_implied_length_rmse_m=np.sqrt(np.mean((implied_length-length)**2)),
        maximum_consistent_inertia_kg_m2=np.max(consistent))
    derivation=[f'Sample density and length scales within +/-{width*100:g} percent.',
        'Derive mass and inertia from the same physical dimensions rather than unrelated ranges.',
        f'Mass standard deviation is {np.std(mass):.6f} kg and inertia standard deviation is {np.std(consistent):.6f} kg*m^2.',
        f'Mass/inertia sample correlation is {metrics["mass_inertia_correlation"]:.6f}.',
        f'Independent inertia sampling implies a rod-length RMSE of {metrics["independent_implied_length_rmse_m"]:.6f} m relative to the actual sampled length.']
    notes=['The chosen manufacturing model is still simplified; real uncertainty may arise from payload, assembly and calibration rather than density changes.',
           'Randomization ranges need identification evidence and held-out evaluation, not just an intuition that more variation is safer.']
    return metrics,derivation,notes
''',dict(range_fraction=.1),'range_fraction',[.01,.025,.05,.1,.2,.3],
'range_fraction is the symmetric fractional range of density and length scales; nominal rod mass is 2 kg and length 0.3 m.',
'Generate latent physical variations first, then derive dependent parameters. Compare statistical coverage with physical consistency rather than judging samples only by marginal ranges.',
'Sampling nonphysical inertias; randomizing unobservable ground truth instead of measurements; choosing ranges after looking at final test performance.',
['Add a discrete payload mode instead of scaling every link.','Correlate friction with temperature in a measured way.','Separate training randomization and held-out stress conditions.'],
'Sim-to-real ranges should reflect measured actuator strength, delays, contact surfaces, calibration error and expected operating conditions.')

add('evaluation_intervals','Fall rates, confidence intervals and finite evidence',
'''A controller that does not fall in a small number of trials has not demonstrated zero failure probability. Report the number of trials, condition distribution, training seeds and observed failures. A confidence interval quantifies sampling uncertainty under assumptions about independent comparable trials; it does not cover untested terrain or correlated hardware faults. This laboratory calculates a Wilson binomial interval and an exact one-sided upper bound for the special zero-failure case.''',
'Wilson center=(p_hat+z^2/(2n))/(1+z^2/n); zero-failure one-sided upper bound=1-alpha^(1/n).',
r'''
def experiment(p):
    n=int(p['trials']);failures=int(round(n*p['observed_fraction']))
    phat=failures/n;z=1.959963984540054;denom=1+z*z/n
    center=(phat+z*z/(2*n))/denom
    half=z*np.sqrt(phat*(1-phat)/n+z*z/(4*n*n))/denom
    zero_upper=1-.05**(1/n)
    metrics=dict(observed_failure_fraction=phat,wilson_lower=max(0,center-half),
        wilson_upper=min(1,center+half),zero_failure_upper_if_applicable=zero_upper,
        observed_failures=failures)
    derivation=[f'Use {n} trials and {failures} observed failures.',
        f'Observed fraction is {phat:.8f}.',
        f'The 95% Wilson interval is [{max(0,center-half):.8f},{min(1,center+half):.8f}].',
        f'If all {n} trials had zero failures, a one-sided 95% upper bound would be {zero_upper:.8f}.',
        'The zero-failure formula solves (1-p)^n=0.05 under the binomial independent-trial assumption.']
    notes=['Changing the terrain, disturbance distribution or controller release changes the population to which these intervals apply.',
           'Repeated trials with shared initialization or correlated faults may provide less information than the independent model assumes.']
    return metrics,derivation,notes
''',dict(trials=100,observed_fraction=.02),'trials',[10,20,50,100,500,1000],
'trials is the independent comparable evaluation count; observed_fraction is converted to an integer failure count and reported exactly.',
'Retain integer failures and trials before computing a fraction. The interval width and zero-failure bound make the limits of a small demonstration explicit.',
'Reporting only percentage without denominator; combining unlike test conditions into one reassuring score; treating simulated trials as physical reliability evidence.',
['Calculate trials required to bound zero-failure probability below a chosen level.','Report intervals separately by terrain and training seed.','Model correlated failures and compare effective evidence.'],
'Physical risk assessment requires broader evidence than binomial simulation fall counts, including consequences and independent protection.')

add('gait_evaluation','Gait phase metrics, contact slip and energy accounting',
'''A walking evaluation needs more than distance traveled. A falling robot can move far, a dragging foot can track velocity, and a low net-energy number can hide large power peaks. Contact-conditioned slip should exclude swing motion. This laboratory synthesizes a walking-like trace with known command, stance masks and controlled slip, then computes tracking, path distance, positive mechanical work and contact slip. It demonstrates metric definitions without claiming a trained gait.''',
'distance=sum(||delta xy||); tracking_RMSE=sqrt(mean((v-v_cmd)^2)); slip_RMS uses stance samples only; positive work=integral(max(P,0) dt).',
r'''
def experiment(p):
    t=np.arange(0,10,.01);dt=.01;command=.2
    velocity=command+.02*np.sin(2*np.pi*.7*t)
    position=np.cumsum(velocity)*dt
    phase=(t%1.)<.6
    foot_speed=np.where(phase,p['stance_slip'],.3*np.sin(2*np.pi*t))
    power=12+8*np.sin(2*np.pi*t)
    distance=float(np.sum(abs(np.diff(position))))
    slip=np.sqrt(np.mean(foot_speed[phase]**2))
    metrics=dict(distance_m=distance,velocity_rmse_m_s=np.sqrt(np.mean((velocity-command)**2)),
        stance_slip_rms_m_s=slip,all_phase_foot_speed_rms_m_s=np.sqrt(np.mean(foot_speed**2)),
        positive_mechanical_work_J=np.trapezoid(np.maximum(power,0),t),
        stance_fraction=np.mean(phase))
    derivation=['Create a ten-second synthetic trajectory commanded at 0.2 m/s.',
        f'Loaded-stance foot speed is {p["stance_slip"]:g} m/s; swing motion is excluded from the slip metric.',
        f'Distance is {distance:.6f} m and velocity RMSE is {metrics["velocity_rmse_m_s"]:.6f} m/s.',
        f'Stance-only slip RMS is {slip:.6f} m/s while all-phase RMS is {metrics["all_phase_foot_speed_rms_m_s"]:.6f} m/s.',
        f'Positive mechanical work is {metrics["positive_mechanical_work_J"]:.6f} J.']
    notes=['These traces are synthetic metric fixtures, not walking results from the Asimov model.',
           'Mechanical work is not battery energy; physical electrical measurements require voltage/current timing and regeneration accounting.']
    return metrics,derivation,notes
''',dict(stance_slip=.01),'stance_slip',[0.,.002,.005,.01,.03,.1],
'stance_slip is synthetic loaded-foot world speed in m/s; stance mask is known truth for the metric test.',
'The all-phase foot-speed metric is deliberately included as a counterexample: it mainly measures swing, not unwanted slip. Contact confidence should accompany real metric reports.',
'Including swing speed in foot slip; integrating commanded velocity instead of measured motion; omitting falls from a distance score.',
['Add a fall event and report survival time separately from distance.','Include commanded yaw-rate tracking.','Use uncertain contact labels and quantify metric sensitivity.'],
'Use measured/estimated world-frame foot motion and contact load confidence when evaluating a real gait.')

add('image_segmentation','Color segmentation, false positives and image-space evidence',
'''A controlled color target is useful for testing the perception-to-behavior path before adding a learned detector. Thresholding is sensitive to illumination, distractors, sensor noise and object size. Pixel area is not physical area unless camera geometry and depth are known. This experiment creates a labeled synthetic RGB-like image, adds noise and measures precision, recall and centroid error for a simple green-excess threshold. It provides a ground-truth test fixture, not a benchmark of real camera performance.''',
'mask=(G-R>threshold) and (G-B>threshold); precision=TP/(TP+FP); recall=TP/(TP+FN).',
r'''
def experiment(p):
    rng=np.random.default_rng(79);h,w=120,160
    image=np.ones((h,w,3))*40;truth=np.zeros((h,w),bool)
    truth[40:70,90:120]=True;image[truth]=[30,180,30]
    image[10:30,10:30]=[40,100,40]
    noisy=np.clip(image+rng.normal(0,p['noise_std'],image.shape),0,255)
    mask=(noisy[:,:,1]-noisy[:,:,0]>70)&(noisy[:,:,1]-noisy[:,:,2]>70)
    tp=np.count_nonzero(mask&truth);fp=np.count_nonzero(mask&~truth)
    fn=np.count_nonzero(~mask&truth)
    ys,xs=np.where(mask)
    centroid_error=np.hypot(xs.mean()-104.5,ys.mean()-54.5) if len(xs) else 1000.
    metrics=dict(precision=tp/max(1,tp+fp),recall=tp/max(1,tp+fn),
        centroid_error_px=centroid_error,predicted_area_px=mask.sum(),
        false_positive_pixels=fp)
    derivation=['Place a 30x30 pixel bright-green target and a dimmer green distractor in a 160x120 image.',
        f'Add pixel-channel noise sigma={p["noise_std"]:g}.',
        'Threshold green excess over red and blue by 70 intensity units.',
        f'Count TP={tp}, FP={fp}, FN={fn}; precision={metrics["precision"]:.6f}, recall={metrics["recall"]:.6f}.',
        f'The predicted-mask centroid differs from the target center by {centroid_error:.6f} pixels.']
    notes=['All foreground pixels are pooled, so distractors can shift the centroid; connected-component selection is an important extension.',
           'No depth or metric reach target is inferred from this mask.']
    return metrics,derivation,notes
''',dict(noise_std=10.),'noise_std',[0.,5.,10.,20.,30.,50.],
'noise_std is synthetic per-channel intensity noise on a 0-255 scale; images are teaching arrays, not captured hardware frames.',
'Ground-truth masks make precision and recall calculable. Evaluate centroid localization separately from pixel classification because a small false-positive region far away can shift the target estimate.',
'Calling color classification object recognition; ignoring distractors; converting pixel coordinates directly into joint targets without calibration.',
['Add connected-component filtering and compare centroid error.','Vary illumination independently of sensor noise.','Build a real-image held-out dataset under declared lighting.'],
'Physical perception must carry timestamps, calibration identity, uncertainty and an explicit no-detection result into the skill supervisor.')

add('skill_planner','Allowlisted skills, bounded parameters and behavior outcomes',
'''High-level instruction following should select a validated capability rather than generate arbitrary low-level actuation. A skill request needs a fixed name, a bounded parameter schema, preconditions and a timeout. Invalid requests should produce a clear rejection without partially applying motion. This experiment defines a small supported-gesture library and evaluates malformed, stale and over-limit planner requests. It isolates the task-selection boundary from both language-model implementation and physical transport.''',
'approved_skill = allowlist[name] and parameters_in_bounds and readiness and fresh_request; execution requires feedback-based completion.',
r'''
def approve(request,ready,now):
    if not ready:return False,'not_ready'
    if request.get('skill') not in ('observe','supported_wave'):return False,'unknown_skill'
    if not 0<=now-request.get('sent',-100)<=.5:return False,'stale'
    if request['skill']=='supported_wave':
        amplitude=request.get('amplitude')
        if not isinstance(amplitude,(int,float)) or not np.isfinite(amplitude):return False,'type'
        if not 0<=amplitude<=.1:return False,'amplitude'
    return True,'approved'

def experiment(p):
    amplitude=p['amplitude'];now=1.
    requests=[dict(skill='supported_wave',amplitude=amplitude,sent=.9),
        dict(skill='arbitrary_motor_code',amplitude=.01,sent=.9),
        dict(skill='supported_wave',amplitude=.05,sent=0.),
        dict(skill='observe',sent=.9)]
    decisions=[approve(r,True,now) for r in requests]
    approved=sum(x[0] for x in decisions)
    not_ready=approve(requests[0],False,now)
    assert not not_ready[0]
    metrics=dict(approved_requests=approved,rejected_requests=len(requests)-approved,
        requested_amplitude_rad=amplitude,primary_request_approved=float(decisions[0][0]),
        inactive_request_approved=float(not_ready[0]))
    derivation=[f'The planner requests supported_wave amplitude {amplitude:g} rad.',
        'The allowlist contains observe and supported_wave only.',
        f'Decisions for normal, unknown, stale and observation requests are {decisions}.',
        f'Approved {approved} requests and rejected {len(requests)-approved}.',
        f'The same request with readiness false is rejected as {not_ready[1]}.']
    notes=['Approval is permission to start a bounded skill; it is not proof the physical task completed.',
           'The executor still needs cancellation, tracking checks, timeout and a reviewed stop response.']
    return metrics,derivation,notes
''',dict(amplitude=.05),'amplitude',[-.05,0.,.025,.05,.1,.2],
'amplitude is a requested supported-joint excursion in radians; the 0.1 rad limit is an educational schema choice.',
'Separate request approval from execution and completion. The unknown-skill test proves the planner cannot introduce a new actuation capability by naming it.',
'Accepting arbitrary code from a planner; confusing language confidence with readiness; considering a successful API call a completed physical task.',
['Add strict unknown-field rejection and a schema version.','Define feedback-based success for the supported gesture.','Inject observation disappearance between approval and execution.'],
'A physical skill library must expose only commissioned capabilities and keep local limits, watchdogs and independent stop authority in control.')
