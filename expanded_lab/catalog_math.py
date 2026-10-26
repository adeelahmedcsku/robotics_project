from catalog import add
add('units','Units, dimensional reasoning and motor-speed conversion',
'''A number without a unit is an incomplete interface. Radians are dimensionless in dimensional analysis, but treating an angle as interchangeable with a count or degree is a software error. Start from the quantity you want, write the conversion chain, and cancel the units before calculating. A gearbox changes both angular speed and available torque; it does not create power. Efficiency represents loss, while a gear ratio represents an ideal geometric relationship. This experiment keeps input and output shaft quantities separate and exposes why an RPM value cannot be sent straight to a radians-per-second controller.''',
'omega_motor = RPM*2*pi/60; omega_joint = omega_motor/G; tau_joint = eta*G*tau_motor; P = tau*omega.',
r'''
def experiment(p):
    rpm, ratio = p['rpm'], p['ratio']
    torque, efficiency = p['motor_torque'], p['efficiency']
    assert rpm > 0 and ratio > 0 and 0 < efficiency <= 1
    motor_speed = rpm*2*np.pi/60
    joint_speed = motor_speed/ratio
    joint_torque = torque*ratio*efficiency
    input_power = torque*motor_speed
    output_power = joint_torque*joint_speed
    recovered_rpm = joint_speed*ratio*60/(2*np.pi)
    assert abs(recovered_rpm-rpm) < 1e-9
    metrics = dict(joint_speed_rad_s=joint_speed,
                   joint_torque_Nm=joint_torque,
                   input_power_W=input_power,
                   output_power_W=output_power,
                   loss_W=input_power-output_power)
    derivation = [
        f'Motor speed: {rpm:g} rev/min times 2*pi/60 = {motor_speed:.6f} rad/s.',
        f'Divide by ratio {ratio:g}: output speed = {joint_speed:.6f} rad/s.',
        f'Multiply input torque {torque:g} Nm by ratio and efficiency: {joint_torque:.6f} Nm.',
        f'Input mechanical power = {input_power:.6f} W; output = {output_power:.6f} W.',
        f'The difference, {input_power-output_power:.6f} W, is modeled mechanical loss.'
    ]
    notes = [f'The ideal power ratio is reduced to {efficiency:.3f}; a torque increase does not imply a power increase.',
             'This constant-efficiency model excludes speed-dependent loss, driver current and thermal limits.']
    return metrics, derivation, notes
''',dict(rpm=1200.,ratio=36.,motor_torque=.3,efficiency=.8),'ratio',[6.,12.,25.,36.,50.,100.],
'RPM is motor-shaft speed; ratio is motor revolutions per output revolution; motor_torque is shaft Nm; efficiency is a fraction.',
'Trace the speed conversion first, then the torque relation, then check power. The recovered RPM assertion is a round-trip invariant; it catches a conversion direction error that a plausible-looking output torque would not.',
'Confusing motor current with output torque; forgetting 60 seconds per minute; using peak torque as a continuous operating point.',
['Hold output speed constant while increasing ratio: calculate the required motor speed.','Set efficiency to one and prove input/output mechanical power agree.','Introduce a 5% torque-constant error and propagate it to output torque.'],
'Confirm whether a vendor encoder reports motor-shaft or output-shaft position before applying a ratio. Actual Asimov actuator settings must come from its confirmed release.')

add('vectors','Vectors, projections and joint-axis torque',
'''A force vector contains both magnitude and direction. The moment about an origin is r cross F, where r points from that origin to the point of application. A joint only responds to the component of that moment along its rotation axis. This explains why the same external force can produce different joint torques at different poses. A projection is meaningful only when both vectors are expressed in the same coordinate frame and the axis is normalized. In this laboratory the changing lever length is geometric; it is not an actuator specification.''',
'moment = r cross F; tau_axis = axis dot moment; F_parallel = axis*(axis dot F).',
r'''
def experiment(p):
    length, force = p['length'], p['force']
    angle = np.deg2rad(p['angle_deg'])
    r = np.array([length, 0., 0.])
    F = force*np.array([np.cos(angle), np.sin(angle), 0.])
    axis = np.array([0., 0., 1.])
    moment = np.cross(r, F)
    torque = float(axis@moment)
    perpendicular = force*np.sin(angle)
    assert np.isclose(torque, length*perpendicular)
    metrics = dict(axis_torque_Nm=torque,
                   force_perpendicular_N=perpendicular,
                   force_magnitude_N=float(np.linalg.norm(F)),
                   lever_m=length)
    derivation = [
        f'Force components in the chosen frame: Fx={F[0]:.6f} N, Fy={F[1]:.6f} N.',
        f'The lever is ({length:.6f}, 0, 0) m, so only Fy contributes to the z moment.',
        f'r cross F gives Mz={moment[2]:.6f} Nm.',
        f'Projection onto the unit z axis gives torque {torque:.6f} Nm.'
    ]
    notes = [f'The effective perpendicular force is {perpendicular:.6f} N, rather than the full {force:g} N.',
             'Changing origin changes moment; changing coordinates consistently does not change its physical meaning.']
    return metrics, derivation, notes
''',dict(length=.2,force=50.,angle_deg=60.),'angle_deg',[0.,15.,30.,45.,60.,90.],
'length is the lever in meters; force is Newtons; angle_deg is the angle from the lever toward the applied force.',
'Cross-product order determines sign. The scalar check against length times perpendicular force gives a separate geometric verification. Negative angles are a useful extension because the sign should reverse.',
'Using an unnormalized axis; swapping r cross F with F cross r; adding vectors from world and body coordinates.',
['Rotate r and F by the same rotation and verify the transformed moment.','Reverse the force and verify torque sign reversal.','Find the force angle that produces half the maximum joint moment.'],
'A limb load must be transformed into each joint frame along the chain; this is the foundation of Jacobian-transpose force mapping.')

add('rotations','Rotation matrices and the Rodrigues formula',
'''A valid rotation preserves lengths and angles. Its columns form an orthonormal right-handed basis. The Rodrigues formula constructs a rotation from a unit axis and an angle using the skew-symmetric cross-product matrix. This is more informative than memorizing three unrelated Euler-angle matrices because it makes the axis explicit. Rotation composition is generally noncommutative: rotating about x and then z differs from rotating about z and then x. Numerical checks should test orthogonality and determinant, not only whether a transformed vector looks plausible.''',
'R = I + sin(theta)*K + (1-cos(theta))*K*K, where K*v = axis cross v.',
r'''
def experiment(p):
    theta = np.deg2rad(p['angle_deg'])
    axis = np.array([1., 2., 3.]); axis /= np.linalg.norm(axis)
    x,y,z = axis
    K = np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])
    R = np.eye(3)+np.sin(theta)*K+(1-np.cos(theta))*(K@K)
    v = np.array([.3,-.2,.5]); rotated = R@v
    ortho = np.linalg.norm(R.T@R-np.eye(3))
    det = np.linalg.det(R)
    roundtrip = np.linalg.norm(R.T@rotated-v)
    assert ortho < 1e-12 and abs(det-1) < 1e-12
    metrics = dict(rotated_x_m=rotated[0],rotated_y_m=rotated[1],
                   rotated_z_m=rotated[2],orthogonality_error=ortho,
                   roundtrip_error_m=roundtrip)
    derivation = [
        f'Normalize axis (1,2,3) to {axis.tolist()}.',
        f'Convert {p["angle_deg"]:g} degrees to {theta:.6f} radians.',
        f'Assemble the skew matrix and evaluate Rodrigues; determinant is {det:.12f}.',
        f'R times (0.3,-0.2,0.5) gives {rotated.tolist()} meters.',
        f'Transpose the rotation to recover the original vector; residual is {roundtrip:.3e} m.'
    ]
    notes = ['A determinant near one does not alone guarantee orthogonality; both tests are retained.',
             'The chosen axis and vector are teaching geometry, unrelated to an unverified motor mounting.']
    return metrics, derivation, notes
''',dict(angle_deg=45.),'angle_deg',[0.,15.,45.,90.,135.,180.],
'angle_deg is a right-handed active rotation about the normalized axis (1,2,3). Input and output vectors use one fixed basis.',
'The skew matrix encodes the cross product. The quadratic term leaves the component along the axis unchanged while rotating the perpendicular component. Transpose is the inverse only after the rotation validity checks pass.',
'Treating a reflection with determinant -1 as a rotation; transposing only one factor in a composed transformation.',
['Verify the axis vector is unchanged by its own rotation.','Compare x-then-z and z-then-x rotations.','Add a small matrix perturbation and observe which validity test detects it.'],
'IMU-to-pelvis and camera-to-head rotations must be calibrated and tested with physical reference orientations.')

add('quaternions','Unit quaternions, sign equivalence and incremental attitude',
'''Quaternions avoid the coordinate singularities of a three-angle parameterization, but they introduce a unit constraint and a component-order convention. A quaternion and its negative represent the same physical rotation. Comparing their components with ordinary Euclidean distance can therefore report a large difference for identical attitudes. For constant angular velocity, an exact axis-angle increment can be composed each timestep. This is a simple reference against which to test a differential integrator and normalization policy.''',
'q_increment = [cos(|omega|*dt/2), axis*sin(|omega|*dt/2)]; q_next = q*q_increment; angular error = 2*acos(|q1 dot q2|).',
r'''
def multiply(a,b):
    aw,ax,ay,az=a; bw,bx,by,bz=b
    return np.array([aw*bw-ax*bx-ay*by-az*bz,
        aw*bx+ax*bw+ay*bz-az*by,
        aw*by-ax*bz+ay*bw+az*bx,
        aw*bz+ax*by-ay*bx+az*bw])

def experiment(p):
    dt, duration, rate = p['dt'], p['duration'], p['rate']
    n = round(duration/dt); actual=n*dt
    inc=np.array([np.cos(rate*dt/2),0.,0.,np.sin(rate*dt/2)])
    q=np.array([1.,0.,0.,0.])
    for _ in range(n):
        q=multiply(q,inc);q/=np.linalg.norm(q)
    exact=np.array([np.cos(rate*actual/2),0.,0.,np.sin(rate*actual/2)])
    error=2*np.arccos(np.clip(abs(q@exact),0,1))
    same=2*np.arccos(np.clip(abs(q@(-q)),0,1))
    assert np.isclose(np.linalg.norm(q),1)
    metrics=dict(final_w=q[0],final_z=q[3],angle_error_rad=error,
                 sign_equivalence_error_rad=same,actual_duration_s=actual)
    derivation=[f'One increment rotates {rate*dt:.6f} rad about local z.',
        f'Apply {n} increments, giving actual duration {actual:.6f} s.',
        f'The final scalar-first quaternion is {q.tolist()}.',
        f'Use the absolute dot product for sign-invariant error: {error:.9f} rad.',
        f'Compare q with -q using the same metric: {same:.9f} rad.']
    notes=['Constant-axis exact increments are a reference case, not a full noisy IMU estimator.',
           'Changing the multiplication side changes whether increments are interpreted in body or world coordinates.']
    return metrics,derivation,notes
''',dict(dt=.01,duration=2.,rate=.7),'dt',[.001,.002,.005,.01,.02,.05],
'dt and duration are seconds; rate is constant body-z angular speed in rad/s; quaternion order is w,x,y,z.',
'The Hamilton product is written explicitly so component order and multiplication side are inspectable. Normalizing after composition controls floating-point drift, while the exact solution supplies an independent check.',
'Comparing q and -q directly; passing scalar-first values into an API expecting scalar-last; integrating degrees per second as radians.',
['Replace exact increments by first-order quaternion integration and compare timestep sensitivity.','Alternate x and y angular increments and examine composition order.','Test conversion to ROS scalar-last message ordering and back.'],
'Real gyro integration needs calibrated axes, bias estimation, timestamp handling and external correction for drift.')

add('transforms','Homogeneous transforms and frame-chain round trips',
'''A rigid transform combines a rotation and translation without losing the frame relationship between them. The notation T_AB means coordinates expressed in B are converted to A. Adjacent frame labels cancel during composition: T_AB*T_BC gives T_AC. This mnemonic is safer than deciding matrix multiplication order from visual intuition. Points carry translation; direction vectors do not. A transform inverse uses the transposed rotation and a rotated negative translation, not simply negating the position column.''',
'T_AB = [[R_AB,p_AB],[0,1]]; T_AC = T_AB*T_BC; T_BA = [[R_AB.T,-R_AB.T*p_AB],[0,1]].',
r'''
def transform(angle,translation):
    c,s=np.cos(angle),np.sin(angle)
    T=np.eye(4);T[:3,:3]=[[c,-s,0],[s,c,0],[0,0,1]]
    T[:3,3]=translation
    return T

def experiment(p):
    a=np.deg2rad(p['angle_deg'])
    T_ab=transform(a,[.1,.2,.3])
    T_bc=transform(-.3,[p['offset'],0.,.05])
    T_ac=T_ab@T_bc
    point=np.array([.2,.1,0.,1.])
    world=T_ac@point
    R,t=T_ac[:3,:3],T_ac[:3,3]
    inverse=np.eye(4);inverse[:3,:3]=R.T;inverse[:3,3]=-R.T@t
    recovered=inverse@world
    error=np.linalg.norm(recovered-point)
    direct=T_ab@(T_bc@point)
    assert np.allclose(world,direct) and error<1e-12
    metrics=dict(point_x_m=world[0],point_y_m=world[1],point_z_m=world[2],
                 roundtrip_error_m=error,translation_norm_m=np.linalg.norm(t))
    derivation=[f'T_BC translation is ({p["offset"]:.6f},0,0.05) m.',
        f'T_AB rotates by {a:.6f} rad before adding its translation.',
        f'Compose T_AC; the resulting translation is {t.tolist()} m.',
        f'Point (0.2,0.1,0) in C becomes {world[:3].tolist()} in A.',
        f'Apply the analytic inverse; recovery error is {error:.3e} m.']
    notes=['The point result includes both translations in the correct rotated directions.',
           'A direction encoded with homogeneous last element zero would ignore translation.']
    return metrics,derivation,notes
''',dict(angle_deg=45.,offset=.15),'angle_deg',[0.,15.,30.,45.,60.,90.],
'angle_deg is the A-from-B active z rotation; offset is B-to-C origin displacement in meters.',
'Build each transform independently, compose in the frame-label order, and check both nested multiplication and inverse recovery. These two checks expose different classes of implementation error.',
'Using -translation directly for the inverse; multiplying a three-vector by a 4x4 matrix; confusing a point with a direction.',
['Replace the point last coordinate with zero and explain the changed result.','Insert a head-to-camera transform and verify a four-frame chain.','Perturb camera translation by 5 mm and calculate world-position error.'],
'Camera-to-base transforms are reusable only after matching link definitions, mounting offsets and timestamps to the assembled robot.')

add('jacobian','Finite-difference Jacobians and derivative verification',
'''The Jacobian answers a local question: how much does an endpoint move for a small joint displacement? Analytic derivatives are efficient, but a sign or index error can hide inside plausible motion. Central finite differences provide a separate numerical check. The perturbation must be small enough to approximate a derivative but not so small that subtraction roundoff dominates. This laboratory compares the two methods at a nonsingular two-link pose and makes epsilon an experimental variable.''',
'J_ij = partial f_i/partial q_j; central difference = [f(q+epsilon*e_j)-f(q-epsilon*e_j)]/(2*epsilon).',
r'''
def fk(q):
    a,b=q
    return np.array([.3*np.cos(a)+.2*np.cos(a+b),
                     .3*np.sin(a)+.2*np.sin(a+b)])

def experiment(p):
    q=np.array([.4,-.7]);eps=p['epsilon']
    a,b=q
    J=np.array([[-.3*np.sin(a)-.2*np.sin(a+b),-.2*np.sin(a+b)],
                [.3*np.cos(a)+.2*np.cos(a+b),.2*np.cos(a+b)]])
    estimated=np.zeros((2,2))
    for j in range(2):
        delta=np.zeros(2);delta[j]=eps
        estimated[:,j]=(fk(q+delta)-fk(q-delta))/(2*eps)
    error=np.linalg.norm(estimated-J)
    velocity=J@np.array([.1,-.2])
    metrics=dict(derivative_error=error,velocity_x_m_s=velocity[0],
                 velocity_y_m_s=velocity[1],jacobian_condition=np.linalg.cond(J))
    derivation=[f'At joint pose {q.tolist()} rad, endpoint is {fk(q).tolist()} m.',
        f'Use symmetric perturbations of {eps:.3e} rad for each joint.',
        f'The analytic first column is {J[:,0].tolist()} m/rad.',
        f'The estimated first column is {estimated[:,0].tolist()} m/rad.',
        f'Full matrix residual norm is {error:.3e}; predicted endpoint velocity is {velocity.tolist()} m/s.']
    notes=['Reducing epsilon eventually makes floating-point cancellation important.',
           'Compare columns in the same frame and at the same configuration; otherwise the residual is not a derivative test.']
    return metrics,derivation,notes
''',dict(epsilon=1e-5),'epsilon',[1e-1,1e-2,1e-3,1e-5,1e-7,1e-9],
'epsilon is a central-difference joint perturbation in radians; lengths are 0.3 and 0.2 meters.',
'The two columns correspond to the two independent joint perturbations. Multiplying by a joint-rate vector produces a local Cartesian velocity, whose units provide another check on the derivative.',
'Reusing a mutable q array without restoring it; comparing degrees-based perturbations to radian derivatives; testing only at zero pose.',
['Repeat with forward differences and compare convergence order.','Check every column at ten seeded nonsingular poses.','Move near a stretched configuration and track conditioning separately from derivative accuracy.'],
'The same column test should validate the selected MuJoCo or hardware-model Jacobian before Cartesian controllers depend on it.')

add('least_squares','Least-squares identification and residual diagnosis',
'''Many calibration tasks are linear in their unknown parameters even when the robot is complicated. A simple example estimates a sensor scale and offset from known references. Least squares chooses parameters minimizing squared residuals, but a small residual does not guarantee the experiment identified both parameters well. Excitation range determines conditioning. Noise, repeated references and validation data must be considered before accepting a fit.''',
'y = a*x+b+noise; theta_hat = argmin ||X*theta-y||^2; X=[x,1].',
r'''
def experiment(p):
    n=int(p['samples']);sigma=p['noise'];span=p['span']
    rng=np.random.default_rng(11)
    x=np.linspace(-span,span,n)
    X=np.column_stack([x,np.ones(n)])
    truth=np.array([1.04,.025])
    y=X@truth+rng.normal(0,sigma,n)
    estimate,_,_,_=np.linalg.lstsq(X,y,rcond=None)
    residual=y-X@estimate
    variance=float(residual@residual/(n-2))
    covariance=variance*np.linalg.inv(X.T@X)
    metrics=dict(scale_error=estimate[0]-truth[0],
                 offset_error_rad=estimate[1]-truth[1],
                 residual_rmse_rad=np.sqrt(np.mean(residual**2)),
                 design_condition=np.linalg.cond(X),
                 scale_std_estimate=np.sqrt(covariance[0,0]))
    derivation=[f'Collect {n} reference positions spanning [-{span:g},{span:g}] rad.',
        f'True scale and offset are {truth.tolist()}; inject noise sigma={sigma:g} rad.',
        f'Least-squares estimate is {estimate.tolist()}.',
        f'Residual degrees of freedom are {n-2}; variance estimate is {variance:.6e}.',
        f'The design matrix condition is {np.linalg.cond(X):.6f}; estimated scale uncertainty is {np.sqrt(covariance[0,0]):.6f}.']
    notes=[f'The identification range is {2*span:g} rad; narrowing it weakens scale estimation even if the offset remains observable.',
           'Covariance assumes the linear noise model and does not account for backlash, systematic reference error or temperature drift.']
    return metrics,derivation,notes
''',dict(samples=40,noise=.005,span=.5),'span',[.01,.025,.05,.1,.5,1.],
'samples is the number of references; noise is measurement standard deviation in radians; span is the symmetric excitation half-range.',
'Use lstsq rather than explicitly inverting the normal equations for the estimate. The covariance calculation is kept separate to inspect its assumptions. Compare parameter errors to the injected truth and residual magnitude.',
'Judging calibration only on training residuals; confusing standard deviation with a hard error bound; assuming repeated identical inputs identify scale.',
['Fit a separate held-out reference set and report prediction error.','Add a quadratic distortion and inspect residual versus position.','Change sample count and compare uncertainty to excitation range.'],
'Encoder zero, current-to-torque scale and camera calibration require trusted independent references and validation outside the fit data.')

add('integration','Discrete integration and numerical stability',
'''A stable continuous equation can become unstable after a poor discretization. The scalar decay equation is simple enough to solve exactly, making it a useful laboratory for numerical reasoning. Explicit Euler predicts the next state from the current derivative. Implicit Euler evaluates the derivative at the next state and solves the resulting equation. Smaller timesteps reduce error but increase computation; choosing them blindly can conceal a model or controller problem.''',
'x_dot=-k*x; exact x(t)=x0*exp(-k*t); explicit x_next=(1-k*dt)*x; implicit x_next=x/(1+k*dt).',
r'''
def experiment(p):
    dt,k,T=p['dt'],p['decay_rate'],p['duration']
    n=max(1,round(T/dt));actual=n*dt
    explicit=1.;implicit=1.
    for _ in range(n):
        explicit*=1-k*dt
        implicit/=1+k*dt
    exact=np.exp(-k*actual)
    factor=abs(1-k*dt)
    metrics=dict(explicit_final=explicit,implicit_final=implicit,
        exact_final=exact,explicit_abs_error=abs(explicit-exact),
        implicit_abs_error=abs(implicit-exact),explicit_amplification=factor)
    derivation=[f'Choose dt={dt:g} s and decay rate k={k:g} per second.',
        f'Advance {n} steps to actual time {actual:.6f} s.',
        f'Explicit one-step multiplier is {1-k*dt:.6f}; its magnitude is {factor:.6f}.',
        f'Exact final value is {exact:.8f}; explicit gives {explicit:.8f}.',
        f'Implicit final value is {implicit:.8f}; compare absolute errors in the table.']
    notes=[('The explicit recurrence is stable for this scalar decay.' if factor<1 else
            'The explicit recurrence is on or outside its stability boundary; reducing dt changes the numerical problem.'),
           'Implicit stability does not mean high accuracy; a heavily damped numerical result can still be wrong.']
    return metrics,derivation,notes
''',dict(dt=.02,decay_rate=10.,duration=1.),'dt',[.005,.01,.02,.05,.1,.25],
'dt is seconds; decay_rate is inverse seconds; duration is desired integration horizon. Actual duration is an integer number of steps.',
'Track the recurrence multiplier before the final state. The exact exponential allows an accuracy comparison independent of either integrator. A negative explicit multiplier alternates sign even when the continuous solution does not.',
'Equating absence of NaNs with accuracy; changing dt without scaling controller updates; comparing runs with different actual horizons.',
['Find the explicit stability boundary analytically and confirm it numerically.','Compare equal actual horizons for non-dividing timesteps.','Apply the same methodology to a mass-spring system.'],
'A MuJoCo timestep, controller period and policy period are separate choices; document their relationship and validate contact/controller behavior together.')

add('uncertainty','Monte Carlo uncertainty propagation and repeatability',
'''A nominal calculation hides variability. Monte Carlo propagation samples uncertain inputs, evaluates the same physical relationship repeatedly, and summarizes the output distribution. It is useful when several uncertainties combine nonlinearly, but its answer is only as credible as the input distributions and correlations. A fixed seed makes an experiment repeatable; multiple independent seeds are needed to assess sampling variability rather than overfit a convenient random realization.''',
'tau = m*g*l*cos(theta); sample uncertain m, l and theta; summarize mean, standard deviation and quantiles.',
r'''
def experiment(p):
    rng=np.random.default_rng(int(p['seed']))
    n=int(p['samples']);sigma=p['angle_noise']
    mass=rng.normal(2.,.04,n)
    length=rng.normal(.25,.002,n)
    angle=rng.normal(.6,sigma,n)
    torque=mass*9.81*length*np.cos(angle)
    nominal=2*9.81*.25*np.cos(.6)
    low,high=np.quantile(torque,[.025,.975])
    metrics=dict(mean_torque_Nm=np.mean(torque),std_torque_Nm=np.std(torque,ddof=1),
        lower_quantile_Nm=low,upper_quantile_Nm=high,nominal_torque_Nm=nominal)
    derivation=[f'Draw {n} samples with generator seed {int(p["seed"])}.',
        f'Mass sigma is 0.04 kg, lever sigma is 0.002 m, angle sigma is {sigma:g} rad.',
        f'Evaluate gravity torque for each sample; nominal value is {nominal:.6f} Nm.',
        f'Sample mean is {np.mean(torque):.6f} Nm and sample standard deviation is {np.std(torque,ddof=1):.6f} Nm.',
        f'Central empirical 95% interval is [{low:.6f},{high:.6f}] Nm.']
    notes=['These quantiles describe the assumed population, not a confidence interval for the sample mean.',
           'Independent Gaussian inputs are a declared teaching assumption; shared calibration errors can create correlations.']
    return metrics,derivation,notes
''',dict(seed=17,samples=5000,angle_noise=.02),'angle_noise',[.001,.005,.01,.02,.05,.1],
'seed identifies a pseudorandom stream; samples controls numerical sample count; angle_noise is standard deviation in radians.',
'Generate uncertain quantities first, then evaluate the same torque equation vectorially. Compare the nonlinear mean with the nominal prediction. Distinguish the distribution width from the standard error of a mean estimate.',
'Calling a percentile interval a guarantee; assuming independent errors without evidence; selecting a seed because it gives an attractive answer.',
['Compare repeated seeds at 100 and 10,000 samples.','Correlate mass and lever length and inspect the output spread.','Use a bounded distribution for angle and compare tail behavior.'],
'Use measured calibration and manufacturing variation to justify randomization ranges rather than arbitrary broad noise.')

add('signals','Sampling, aliasing and the difference between signal and display rate',
'''Sampling converts a continuous-time signal into discrete observations. Different underlying frequencies can produce the same sampled sequence, so a plot can look smooth and still misrepresent motion. The Nyquist condition is a minimum for reconstructing a band-limited signal; real sensors require anti-alias filtering and margin. Display decimation is separate from measurement sampling and should never reduce the feedback rate accidentally.''',
'x[n]=sin(2*pi*f*n/fs); aliased frequency = abs((f+fs/2) mod fs - fs/2).',
r'''
def experiment(p):
    fs,frequency,T=p['sample_rate'],p['signal_frequency'],p['duration']
    n=max(4,int(fs*T));t=np.arange(n)/fs
    x=np.sin(2*np.pi*frequency*t)
    alias=abs((frequency+fs/2)%fs-fs/2)
    spectrum=np.abs(np.fft.rfft(x))
    frequencies=np.fft.rfftfreq(n,1/fs)
    peak=float(frequencies[np.argmax(spectrum)])
    metrics=dict(nyquist_Hz=fs/2,alias_Hz=alias,fft_peak_Hz=peak,
        samples=n,sampled_rms=float(np.sqrt(np.mean(x*x))))
    derivation=[f'Sample a {frequency:g} Hz sinusoid at {fs:g} samples per second.',
        f'The sample interval is {1/fs:.6f} s and Nyquist frequency is {fs/2:.6f} Hz.',
        f'The analytical alias frequency is {alias:.6f} Hz.',
        f'An {n}-sample FFT resolves bins spaced {fs/n:.6f} Hz; peak bin is {peak:.6f} Hz.',
        f'Sampled RMS is {np.sqrt(np.mean(x*x)):.6f}; exact coincidences can produce misleading zeros.']
    notes=[('Signal lies below Nyquist, but practical reconstruction still needs filtering assumptions.' if frequency<fs/2 else
            'The original signal cannot be uniquely recovered from these samples without extra information.'),
           'FFT leakage depends on record duration and windowing; a peak bin alone is not a precision frequency estimate.']
    return metrics,derivation,notes
''',dict(sample_rate=100.,signal_frequency=35.,duration=2.),'sample_rate',[20.,40.,60.,80.,100.,200.],
'sample_rate and signal_frequency are Hertz; duration is seconds. Samples begin at zero phase in this controlled example.',
'Calculate the expected alias independently before looking at the FFT. The frequency-bin calculation prevents overclaiming resolution from a short record. Consider anti-alias filtering before a physical sampling boundary.',
'Inferring physical oscillation frequency from a low-rate dashboard; reducing sample rate without filtering; trusting a line drawn between sparse points.',
['Change sinusoid phase and inspect exact-coincidence cases.','Compare a two-second and ten-second FFT record.','Design a display decimator while preserving the original controller samples.'],
'High-frequency encoder/IMU motion and low-rate network telemetry serve different purposes; the dashboard is not a control sensor.')
