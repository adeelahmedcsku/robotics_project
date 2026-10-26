from catalog import add
add('encoder','Encoder counts, quantization, wrapping and velocity estimates',
'''An encoder converts position into a finite representation. Quantization error may be small for position but large after numerical differentiation, especially when the sample period is short. Wrapped single-turn angles also create artificial jumps at the boundary unless unwrapped consistently. This experiment produces a smooth known trajectory, quantizes it to counts, reconstructs angle and estimates velocity. Ground truth allows position and derivative error to be separated.''',
'count=round(angle/(2*pi)*resolution); angle_hat=count*2*pi/resolution; velocity_hat=delta(angle_unwrapped)/dt.',
r'''
def experiment(p):
    resolution=int(p['counts']);dt=.002;t=np.arange(0,2,dt)
    truth=3.1+.4*np.sin(2*np.pi*.5*t)
    wrapped=(truth+np.pi)%(2*np.pi)-np.pi
    counts=np.round(wrapped/(2*np.pi)*resolution)
    measured=counts*2*np.pi/resolution
    unwrapped=np.unwrap(measured)
    unwrapped+=truth[0]-unwrapped[0]
    velocity=np.gradient(unwrapped,dt)
    exact=.4*np.pi*np.cos(np.pi*t)
    metrics=dict(quantization_step_rad=2*np.pi/resolution,
        position_rmse_rad=np.sqrt(np.mean((unwrapped-truth)**2)),
        velocity_rmse_rad_s=np.sqrt(np.mean((velocity-exact)**2)),
        raw_wrap_jump_rad=np.max(abs(np.diff(measured))))
    derivation=[f'Encoder resolution is {resolution} counts per revolution.',
        f'One count represents {2*np.pi/resolution:.8f} rad.',
        'Generate a trajectory crossing the +/-pi wrapping boundary and quantize it.',
        f'After unwrap and initial alignment, position RMSE is {metrics["position_rmse_rad"]:.8f} rad.',
        f'Differentiating at 2 ms gives velocity RMSE {metrics["velocity_rmse_rad_s"]:.6f} rad/s.']
    notes=['The initial alignment removes an arbitrary integer-turn offset but is not an absolute-zero calibration.',
           'Higher numerical differentiation rate does not create additional encoder position information.']
    return metrics,derivation,notes
''',dict(counts=4096),'counts',[256,512,1024,4096,16384,65536],
'counts is the assumed effective output counts per revolution; the teaching sample interval is 2 ms.',
'Quantize the wrapped measurement before unwrapping, then compare position and differentiated velocity separately. The raw jump metric makes a wrapping bug visible even when the angle trace looks periodic.',
'Applying unwrap after differentiation; assuming nominal encoder bit depth equals effective output accuracy; losing multi-turn reference across reboot.',
['Add a missed-sample gap and use actual timestamps in differentiation.','Compare a short-window slope fit with a two-point difference.','Model a motor-side encoder through a gearbox and add backlash.'],
'Confirm encoder placement, count scaling, wrap convention and absolute-reference persistence for the exact actuator firmware.')

add('gyro_bias','Gyroscope bias calibration and attitude drift',
'''A small gyro bias integrates into a large orientation error. Averaging a stationary segment can estimate a constant offset, but temperature drift or motion during calibration violates that assumption. Measurement noise and bias uncertainty affect integrated orientation differently. The experiment estimates bias from a known stationary period, then compares raw and corrected integration against a known angular motion. It separates the calibration samples from the evaluation interval.''',
'omega_measured=omega_true+bias+noise; bias_hat=mean(stationary samples); angle=sum((omega_measured-bias_hat)*dt).',
r'''
def experiment(p):
    rng=np.random.default_rng(23);dt=.01;T=10.;n=int(T/dt)
    calibration=int(p['calibration_seconds']/dt)
    calibration=max(2,calibration)
    bias=.015;sigma=.01
    stationary=bias+rng.normal(0,sigma,calibration)
    estimated=stationary.mean()
    truth=.2*np.ones(n);measured=truth+bias+rng.normal(0,sigma,n)
    raw=np.cumsum(measured)*dt;corrected=np.cumsum(measured-estimated)*dt
    expected=np.cumsum(truth)*dt
    metrics=dict(estimated_bias_rad_s=estimated,bias_error_rad_s=estimated-bias,
        raw_final_angle_error_rad=raw[-1]-expected[-1],
        corrected_final_angle_error_rad=corrected[-1]-expected[-1],
        corrected_angle_rmse_rad=np.sqrt(np.mean((corrected-expected)**2)))
    derivation=[f'Collect {calibration} stationary samples at 100 Hz.',
        f'True injected bias is {bias:g} rad/s; estimated bias is {estimated:.8f} rad/s.',
        f'Integrate a 0.2 rad/s motion for {T:g} s.',
        f'Raw final attitude error is {raw[-1]-expected[-1]:.8f} rad.',
        f'After bias correction, final error is {corrected[-1]-expected[-1]:.8f} rad.']
    notes=['This calibration assumes zero true angular velocity and constant bias during both intervals.',
           'Longer averaging reduces random estimation error but cannot remove a temperature-dependent bias change.']
    return metrics,derivation,notes
''',dict(calibration_seconds=2.),'calibration_seconds',[.1,.25,.5,1.,2.,5.],
'calibration_seconds is the stationary averaging duration; injected gyro bias and noise are in radians per second.',
'Use separate random samples for calibration and motion. Integrating the same noisy calibration record as evaluation would conceal the actual generalization problem.',
'Calibrating while the robot vibrates or moves; forgetting sensor-to-body rotation; subtracting degrees-per-second bias from radian data.',
['Introduce a slow temperature-dependent bias ramp.','Repeat across several seeds and quantify calibration variability.','Reject calibration intervals with excessive measured variance.'],
'Physical IMU calibration requires a known stationary fixture and documented temperature/mounting conditions.')

add('complementary','Complementary attitude filtering and acceleration contamination',
'''A gyroscope tracks rapid angular changes but drifts. An accelerometer can provide a gravity-direction reference when other acceleration is small, but cannot distinguish gravity from arbitrary linear acceleration by itself. A complementary filter blends integrated gyro attitude with a slower accelerometer estimate. The blend controls the response to bias and contamination. This scalar roll example makes those competing effects visible before a three-dimensional estimator is introduced.''',
'roll_pred=roll_prev+gyro*dt; roll_next=alpha*roll_pred+(1-alpha)*roll_acc; alpha=tau/(tau+dt).',
r'''
def experiment(p):
    rng=np.random.default_rng(29);dt=.01;t=np.arange(0,8,dt)
    truth=.15*np.sin(2*np.pi*.3*t)
    rate=.15*2*np.pi*.3*np.cos(2*np.pi*.3*t)
    gyro=rate+.01+rng.normal(0,.005,len(t))
    accel_angle=truth+rng.normal(0,.02,len(t))
    accel_angle[(t>3)&(t<4)]+=.15
    tau=p['time_constant'];alpha=tau/(tau+dt)
    estimate=0.;history=[]
    for g,a in zip(gyro,accel_angle):
        estimate=alpha*(estimate+g*dt)+(1-alpha)*a
        history.append(estimate)
    error=np.array(history)-truth
    clean=(t<3)|(t>5)
    metrics=dict(alpha=alpha,total_rmse_rad=np.sqrt(np.mean(error**2)),
        clean_rmse_rad=np.sqrt(np.mean(error[clean]**2)),
        contamination_peak_error_rad=np.max(abs(error[(t>3)&(t<4)])),
        final_error_rad=error[-1])
    derivation=[f'Time constant {tau:g} s with dt=0.01 s gives alpha={alpha:.8f}.',
        'True roll is a 0.15 rad, 0.3 Hz sinusoid; gyro bias is 0.01 rad/s.',
        'Contaminate the accelerometer roll proxy by +0.15 rad between three and four seconds.',
        f'Whole-record RMSE is {metrics["total_rmse_rad"]:.6f} rad; clean-segment RMSE is {metrics["clean_rmse_rad"]:.6f} rad.',
        f'Peak error during contamination is {metrics["contamination_peak_error_rad"]:.6f} rad.']
    notes=['The synthetic accelerometer-angle disturbance represents a limitation of gravity-based attitude correction during motion.',
           'A production estimator needs measurement validity checks and a consistent three-dimensional orientation representation.']
    return metrics,derivation,notes
''',dict(time_constant=.5),'time_constant',[.05,.1,.25,.5,1.,2.],
'time_constant is seconds; alpha is derived from it and the fixed 10 ms sample interval.',
'Compare clean and contaminated segments separately instead of rewarding a filter for one aggregate metric. Fast accelerometer correction reduces bias drift but follows false gravity cues more strongly.',
'Treating accelerometer-derived roll as ground truth while accelerating; tuning alpha without regard to sampling period.',
['Gate accelerometer correction when acceleration norm deviates from the stationary reference.','Estimate gyro bias as an additional state.','Compare a fixed alpha with a fixed time constant under changed sampling rate.'],
'IMU correction assumptions must be tested in supported stationary, moving and contact-transition conditions.')

add('kalman_scalar','Scalar Kalman filtering and covariance interpretation',
'''A Kalman filter combines a prediction with a measurement according to their modeled uncertainty. The gain is not an arbitrary smoothing coefficient: it emerges from predicted state variance and measurement variance. If those variances are wrong, the numerical covariance can look precise while the estimate is biased or overconfident. This scalar random-walk model provides a complete update cycle and a direct comparison between empirical error and reported uncertainty.''',
'P_pred=P+Q; K=P_pred/(P_pred+R); x=x_pred+K*(z-x_pred); P=(1-K)^2*P_pred+K^2*R.',
r'''
def experiment(p):
    rng=np.random.default_rng(31);n=500;Q=.0001;true_R=.01
    truth=np.cumsum(rng.normal(0,np.sqrt(Q),n))
    measurements=truth+rng.normal(0,np.sqrt(true_R),n)
    x=0.;P=1.;errors=[];variances=[];gains=[]
    assumed_R=p['assumed_measurement_variance']
    for z,actual in zip(measurements,truth):
        prediction=P+Q;K=prediction/(prediction+assumed_R)
        x+=K*(z-x)
        P=(1-K)**2*prediction+K*K*assumed_R
        errors.append(x-actual);variances.append(P);gains.append(K)
    errors=np.array(errors);variances=np.array(variances)
    metrics=dict(estimate_rmse=np.sqrt(np.mean(errors**2)),
        reported_std=np.sqrt(np.mean(variances)),final_gain=gains[-1],
        empirical_two_sigma_coverage=np.mean(abs(errors)<=2*np.sqrt(variances)))
    derivation=[f'True process variance per step is {Q:g}; true measurement variance is {true_R:g}.',
        f'The filter assumes measurement variance {assumed_R:g}.',
        'Predict variance, calculate gain, correct state, then use Joseph-form scalar covariance update.',
        f'Empirical RMSE is {metrics["estimate_rmse"]:.6f}; reported RMS standard deviation is {metrics["reported_std"]:.6f}.',
        f'Two-sigma empirical coverage is {metrics["empirical_two_sigma_coverage"]:.6f}.']
    notes=['Coverage is a diagnostic under this synthetic model, not a universal confidence guarantee.',
           'Underestimating measurement variance can increase trust in noisy data and make the reported covariance overconfident.']
    return metrics,derivation,notes
''',dict(assumed_measurement_variance=.01),'assumed_measurement_variance',[.0001,.001,.005,.01,.05,.1],
'assumed_measurement_variance is squared measurement units; process variance and actual measurement noise stay fixed.',
'The Joseph covariance form retains nonnegativity more robustly than a careless subtractive implementation. Compare uncertainty calibration as well as state error.',
'Using standard deviation where variance is required; confusing measurement residual with state error; assuming diagonal covariance means physical independence.',
['Change actual noise without changing filter assumptions.','Add a constant measurement bias and inspect covariance failure.','Compute normalized innovations and test their scale.'],
'Robot estimators require a physically defensible process model and measurement covariances based on actual sensing conditions.')

add('kalman_velocity','Position and velocity estimation with intermittent measurements',
'''Velocity is often not measured directly or is too noisy to use after simple differentiation. A constant-velocity Kalman model estimates position and speed together while carrying uncertainty through missing observations. Prediction during a dropout should increase uncertainty; inventing a repeated fresh measurement would hide the lack of information. This laboratory removes a block of position measurements and measures estimation error during that interval.''',
'F=[[1,dt],[0,1]]; H=[1,0]; P_pred=F*P*F.T+Q; K=P_pred*H.T/(H*P_pred*H.T+R).',
r'''
def experiment(p):
    rng=np.random.default_rng(37);dt=.02;t=np.arange(0,6,dt)
    true_position=.2*t+.02*np.sin(t);true_velocity=.2+.02*np.cos(t)
    measurements=true_position+rng.normal(0,.01,len(t))
    F=np.array([[1.,dt],[0.,1.]]);H=np.array([[1.,0.]])
    Q=.01*np.array([[dt**4/4,dt**3/2],[dt**3/2,dt**2]])
    x=np.zeros(2);P=np.eye(2);errors=[];drop_errors=[]
    dropout=p['dropout_seconds'];end=2+dropout
    for i,z in enumerate(measurements):
        x=F@x;P=F@P@F.T+Q
        missing=2<=t[i]<end
        if not missing:
            S=float((H@P@H.T)[0,0]+.0001)
            K=P@H.T/S;x+=K[:,0]*(z-float((H@x)[0]))
            A=np.eye(2)-K@H;P=A@P@A.T+K*.0001@K.T
        error=x[1]-true_velocity[i];errors.append(error)
        if missing:drop_errors.append(error)
        assert np.linalg.eigvalsh(P).min()>-1e-10
    metrics=dict(velocity_rmse_m_s=np.sqrt(np.mean(np.array(errors)**2)),
        dropout_velocity_rmse_m_s=np.sqrt(np.mean(np.array(drop_errors)**2)) if drop_errors else 0.,
        final_velocity_m_s=x[1],final_position_std_m=np.sqrt(P[0,0]),
        final_velocity_std_m_s=np.sqrt(P[1,1]))
    derivation=[f'Use a two-state position/velocity model with dt={dt:g} s.',
        f'Drop measurements from t=2 s to t={end:g} s.',
        'Predict through missing samples without applying fabricated corrections.',
        f'Whole-run speed RMSE is {metrics["velocity_rmse_m_s"]:.6f} m/s.',
        f'Dropout speed RMSE is {metrics["dropout_velocity_rmse_m_s"]:.6f} m/s; final speed estimate is {x[1]:.6f} m/s.']
    notes=['The true motion contains a small acceleration that is not exactly constant velocity.',
           'The filter state and covariance are expressed in one dimension; full robot base estimation requires orientation and contact models.']
    return metrics,derivation,notes
''',dict(dropout_seconds=.5),'dropout_seconds',[0.,.1,.25,.5,1.,2.],
'dropout_seconds is the duration of missing position observations; measurement standard deviation is 0.01 m.',
'Prediction and correction are separate branches. Inspect covariance positive-semidefiniteness and avoid accidentally updating on stale copies during the dropout.',
'Labeling a held last measurement as newly sampled; measuring velocity truth in a different frame; omitting process noise during unmodeled acceleration.',
['Add timestamp jitter and rebuild F from actual intervals.','Inject a sensor jump and add an innovation gate.','Compare with differentiated noisy position.'],
'Contact-based velocity updates must be disabled or downweighted when the assumed foot slips or loses load.')

add('pinhole','Camera intrinsics, projection and pixel-error sensitivity',
'''A camera converts spatial geometry into pixel measurements. Focal lengths are measured in pixels after calibration; principal point is the pixel location of the optical axis. Projection divides by depth, making near-zero or negative depth invalid for a simple visible-point model. Pixel error maps back into metric lateral error in proportion to depth. This laboratory computes a projection and an inverse reconstruction with known depth, making the missing-depth assumption explicit.''',
'u=fx*X/Z+cx; v=fy*Y/Z+cy; X=(u-cx)*Z/fx; lateral uncertainty approx Z*sigma_pixel/fx.',
r'''
def experiment(p):
    Z=p['depth'];fx,fy,cx,cy=400.,410.,320.,240.
    X,Y=.1,-.05;sigma=p['pixel_noise']
    assert Z>0
    u=fx*X/Z+cx;v=fy*Y/Z+cy
    reconstructed=np.array([(u-cx)*Z/fx,(v-cy)*Z/fy,Z])
    error=np.linalg.norm(reconstructed-[X,Y,Z])
    lateral=Z*sigma/fx
    metrics=dict(pixel_u=u,pixel_v=v,lateral_uncertainty_m=lateral,
        roundtrip_error_m=error,projection_scale_px_per_m=fx/Z)
    derivation=[f'Use fx={fx:g}, fy={fy:g}, cx={cx:g}, cy={cy:g} pixels.',
        f'Project point (0.1,-0.05,{Z:g}) m.',
        f'Pixel result is u={u:.6f}, v={v:.6f}.',
        f'Assuming exact known depth, inverse projection returns {reconstructed.tolist()} m.',
        f'Pixel noise sigma={sigma:g} px maps to lateral sigma approximately {lateral:.6f} m.']
    notes=['The inverse result requires known depth; a monocular pixel alone does not identify a metric 3-D point.',
           'Distortion, rolling shutter, calibration uncertainty and camera-to-body extrinsics are excluded here.']
    return metrics,derivation,notes
''',dict(depth=1.,pixel_noise=1.),'depth',[.2,.5,1.,2.,3.,5.],
'depth is positive optical-axis meters; pixel_noise is assumed image-coordinate standard deviation in pixels.',
'Perform a projection/inverse round trip before adding noise. The uncertainty scaling then isolates geometric depth sensitivity from calibration and detector accuracy.',
'Using image width as focal length without calibration; assuming Euclidean range equals optical-axis depth; mixing RGB camera and depth camera frames.',
['Propagate focal-length uncertainty in addition to pixel noise.','Add a calibrated camera-to-base transform.','Reject points behind the camera and near the projection singularity.'],
'The documented Asimov monocular camera does not by itself provide the known depth used in this numerical exercise.')

add('stereo_depth','Stereo depth, disparity uncertainty and range limits',
'''Stereo geometry can estimate depth from a calibrated baseline and image disparity. Small disparity at long range makes depth highly sensitive to pixel error. Thus a detector may identify an object reliably while its metric position is too uncertain for reaching. The first-order uncertainty calculation is informative near a well-behaved measurement, but poor disparity and outliers need explicit rejection. This is a generic optional sensor study, not a claim that the base Asimov includes stereo depth.''',
'Z=f*B/d; sigma_Z approx f*B*sigma_d/d^2; relative depth uncertainty=sigma_d/d.',
r'''
def experiment(p):
    Z=p['true_depth'];f,B=400.,.06;sigma=p['disparity_noise']
    disparity=f*B/Z
    std=f*B*sigma/disparity**2
    noisy_depth=f*B/(disparity+sigma)
    metrics=dict(disparity_px=disparity,depth_std_m=std,
        relative_depth_std=std/Z,one_sigma_positive_disparity_depth_m=noisy_depth,
        linearization_error_m=abs((Z-std)-noisy_depth))
    derivation=[f'Use focal length {f:g} px and calibrated baseline {B:g} m.',
        f'At true depth {Z:g} m, expected disparity is {disparity:.6f} px.',
        f'Disparity sigma={sigma:g} px propagates to sigma_Z={std:.6f} m.',
        f'A +1 sigma disparity perturbation gives exact depth {noisy_depth:.6f} m.',
        f'Compare the first-order prediction Z-sigma_Z; linearization discrepancy is {metrics["linearization_error_m"]:.6f} m.']
    notes=['Depth uncertainty grows quadratically with range in this fixed-camera approximation.',
           'When disparity approaches its uncertainty scale, Gaussian linearization and naive depth estimates become unreliable.']
    return metrics,derivation,notes
''',dict(true_depth=1.,disparity_noise=.5),'true_depth',[.3,.5,1.,2.,3.,5.],
'true_depth is meters; disparity_noise is pixels; baseline and focal length are fixed calibrated teaching values.',
'Compare exact perturbed geometry with a derivative-based approximation. This reveals where uncertainty propagation itself needs a nonlinear or robust treatment.',
'Assuming a precise-looking depth number has low uncertainty; ignoring rectification and synchronization; treating disparity outliers as ordinary noise.',
['Define a maximum permitted relative-depth uncertainty and calculate usable range.','Monte Carlo disparity noise and inspect the depth distribution.','Combine depth and camera-extrinsic uncertainty in base coordinates.'],
'Adding a depth sensor changes mounting, compute, power and calibration budgets and requires explicit compatibility verification.')

add('resampling','Timestamps, interpolation and asynchronous sensor streams',
'''Sensors rarely produce measurements at identical times. Comparing an encoder sample at one instant with an IMU sample at another creates a synchronization error even if both values are individually accurate. Interpolation can align streams for analysis, but it needs timestamp validity and does not recover arbitrarily fast unseen motion. This laboratory samples a known signal with a clock offset and compares naive alignment with timestamp-aware interpolation.''',
'y_aligned(t_ref)=interpolate((t_sensor+offset,y_sensor),t_ref); error depends on signal slope, offset and sampling interval.',
r'''
def experiment(p):
    offset=p['offset'];fs=p['sample_rate'];frequency=2.
    reference_t=np.arange(.2,2.8,.005)
    sensor_t=np.arange(0,3,1/fs)
    measured=np.sin(2*np.pi*frequency*(sensor_t+offset))
    truth=np.sin(2*np.pi*frequency*reference_t)
    naive=np.interp(reference_t,sensor_t,measured)
    corrected=np.interp(reference_t,sensor_t+offset,measured)
    metrics=dict(naive_alignment_rmse=np.sqrt(np.mean((naive-truth)**2)),
        corrected_alignment_rmse=np.sqrt(np.mean((corrected-truth)**2)),
        nominal_phase_error_rad=2*np.pi*frequency*offset,
        sensor_interval_s=1/fs)
    derivation=[f'The signal is a 2 Hz sinusoid sampled at {fs:g} Hz.',
        f'Sensor timestamp offset is {offset:g} s, equivalent to phase {2*np.pi*frequency*offset:.6f} rad.',
        'Naive interpolation treats nominal sensor times as correct.',
        f'Naive RMSE is {metrics["naive_alignment_rmse"]:.6f}.',
        f'Adding the known offset before interpolation reduces RMSE to {metrics["corrected_alignment_rmse"]:.6f}.']
    notes=['Residual after offset correction includes interpolation error from finite sampling.',
           'An unknown or drifting clock offset requires estimation and validity limits; arrival time is not a substitute for sample time.']
    return metrics,derivation,notes
''',dict(offset=.01,sample_rate=100.),'offset',[0.,.001,.005,.01,.02,.05],
'offset is seconds added to the actual sampling instant; sample_rate is Hertz; reference timestamps remain independent.',
'The synthetic signal is evaluated at actual sensor instants so the offset has a precise meaning. Correcting timestamps rather than shifting values preserves the measurement model.',
'Interpolating across long dropouts; subtracting unsynchronized host clocks; using future samples in a real-time algorithm without accounting for latency.',
['Add linear clock drift and estimate it from matched events.','Mark interpolation across large gaps invalid.','Compare causal hold, linear interpolation and delayed smoothing.'],
'Time alignment affects state estimation, camera localization and replay; document the clock source of every recorded field.')

add('contact_hysteresis','Contact detection, thresholds and hysteresis',
'''A noisy force-like signal can chatter around a single contact threshold, repeatedly changing the controller's assumed support set. Hysteresis uses a higher entry threshold and lower exit threshold, creating memory that reduces switching. It also delays transitions and can miss weak contacts. Evaluate detection against labeled conditions, not merely a smoother-looking plot. This experiment uses synthetic contact loads with noise and reports false positives, false negatives and transition count.''',
'if not_contact and load>=enter: contact=True; if contact and load<=exit: contact=False; exit<enter.',
r'''
def experiment(p):
    rng=np.random.default_rng(41);t=np.arange(0,4,.01)
    truth=(t>=1)&(t<3);signal=np.where(truth,30.,0.)
    signal=signal+rng.normal(0,p['noise_std'],len(t))
    enter,exit=15.,5.;state=False;predicted=[]
    for value in signal:
        if not state and value>=enter:state=True
        elif state and value<=exit:state=False
        predicted.append(state)
    predicted=np.array(predicted)
    false_positive=np.mean(predicted[~truth]);false_negative=np.mean(~predicted[truth])
    switches=np.count_nonzero(predicted[1:]!=predicted[:-1])
    metrics=dict(false_positive_fraction=false_positive,false_negative_fraction=false_negative,
        transition_count=switches,accuracy=np.mean(predicted==truth),
        signal_noise_std_N=p['noise_std'])
    derivation=['The labeled contact interval is one to three seconds with mean load 30 N.',
        f'Add Gaussian noise with sigma={p["noise_std"]:g} N.',
        'Enter contact at 15 N and leave at 5 N using a stateful threshold.',
        f'False-positive fraction is {false_positive:.6f}; false-negative fraction is {false_negative:.6f}.',
        f'The detector made {switches} state transitions instead of the ideal two.']
    notes=['Thresholds are teaching values; a real detector must be calibrated for sensor range, preload, bias and contact dynamics.',
           'A stable contact flag does not prove no slip or a known contact wrench.']
    return metrics,derivation,notes
''',dict(noise_std=5.),'noise_std',[.5,2.,5.,8.,12.,20.],
'noise_std is Newtons of synthetic zero-mean noise; the true supported load is 30 N during the labeled interval.',
'The detector carries state between samples. Calculate errors separately inside and outside contact; an always-contact classifier can look acceptable if the dataset is imbalanced.',
'Treating a threshold flag as load measurement; choosing thresholds on the same trials used for final evaluation; ignoring sensor bias.',
['Compare with a single threshold and count chatter.','Add a minimum-duration debounce and measure latency.','Introduce slowly increasing preload and test failure behavior.'],
'If physical force sensors are absent, contact estimation needs a separately validated model and uncertainty treatment.')

add('zero_velocity','Zero-velocity updates, foot constraints and slip bias',
'''A stationary contacting foot supplies a useful constraint on body motion. If the foot actually slips, enforcing zero velocity injects a biased pseudo-measurement into the estimator. This illustrates a broader sensor-fusion principle: a model-based constraint is only a valid measurement while its assumptions hold. The laboratory combines integrated acceleration with occasional zero-velocity corrections and then deliberately violates the stationary-contact assumption.''',
'v_pred=v_prev+a*dt; contact correction v_next=(1-K)*v_pred+K*v_contact_assumed.',
r'''
def experiment(p):
    rng=np.random.default_rng(43);dt=.01;t=np.arange(0,6,dt)
    slip=p['slip_speed'];truth=np.where(t<2,0.,np.where(t<4,slip,0.))
    acceleration=np.gradient(truth,dt)
    measured=acceleration+.02+rng.normal(0,.01,len(t))
    estimate=0.;raw=0.;errors=[];raw_errors=[]
    for i,a in enumerate(measured):
        raw+=a*dt;estimate+=a*dt
        assumed_contact=(i%20)==0
        if assumed_contact:estimate=.2*estimate
        errors.append(estimate-truth[i]);raw_errors.append(raw-truth[i])
    metrics=dict(constrained_rmse_m_s=np.sqrt(np.mean(np.array(errors)**2)),
        unconstrained_rmse_m_s=np.sqrt(np.mean(np.array(raw_errors)**2)),
        slip_interval_bias_m_s=np.mean(np.array(errors)[(t>=2)&(t<4)]),
        final_constrained_error_m_s=errors[-1])
    derivation=[f'The synthetic foot/body velocity is {slip:g} m/s during a two-second slip interval.',
        'Acceleration measurement includes +0.02 m/s^2 bias and 0.01 m/s^2 noise.',
        'Every 0.2 s, impose a strong zero-velocity pseudo-measurement regardless of actual slip.',
        f'Constrained RMSE is {metrics["constrained_rmse_m_s"]:.6f} m/s; unconstrained RMSE is {metrics["unconstrained_rmse_m_s"]:.6f} m/s.',
        f'Mean bias during slip is {metrics["slip_interval_bias_m_s"]:.6f} m/s.']
    notes=['Zero-velocity constraints can reduce drift in valid stationary intervals and create systematic error during slip.',
           'Use contact confidence, slip indicators and innovation checks rather than permanently enforcing the constraint.']
    return metrics,derivation,notes
''',dict(slip_speed=.05),'slip_speed',[0.,.01,.03,.05,.1,.2],
'slip_speed is meters per second during the deliberately invalid contact-constraint interval.',
'Run an unconstrained integrator beside the constrained estimate to expose the tradeoff. The contact assumption is intentionally wrong during slip, allowing a controlled failure analysis.',
'Using foot contact as proof of zero world velocity; confusing a kinematic constraint with an independent sensor; hiding bias in a low covariance.',
['Gate corrections using an independent slip detector.','Add a bias state and compare observability in stationary and moving intervals.','Evaluate both drift reduction and slip-induced bias.'],
'Physical base-velocity estimators must tolerate contact transitions and slipping surfaces before learned policies depend on them.')
