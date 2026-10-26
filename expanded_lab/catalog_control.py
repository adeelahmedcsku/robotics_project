from catalog import add
add('pd_control','Second-order joint dynamics and PD tuning',
'''Feedback gains set a closed-loop dynamic behavior, not merely a preference for stronger correction. For a single inertia with viscous damping, proportional feedback adds stiffness and derivative feedback adds damping. Natural frequency and damping ratio connect these gains to response speed and overshoot. The same numerical gains behave differently when inertia changes. This experiment integrates an ideal one-axis joint with a small target step and reports error and overshoot rather than judging the response by appearance.''',
'I*q_ddot + (b+Kd)*q_dot + Kp*q = Kp*q_target; omega_n=sqrt(Kp/I); zeta=(b+Kd)/(2*sqrt(Kp*I)).',
r'''
def experiment(p):
    I,kp,kd=p['inertia'],p['kp'],p['kd'];b=.1;dt=.001
    target=.1;q=0.;v=0.;positions=[]
    for _ in range(3000):
        torque=kp*(target-q)-kd*v
        acceleration=(torque-b*v)/I
        v+=dt*acceleration;q+=dt*v;positions.append(q)
    positions=np.array(positions)
    wn=np.sqrt(kp/I);zeta=(b+kd)/(2*np.sqrt(kp*I))
    overshoot=max(0.,positions.max()-target)/target
    metrics=dict(natural_frequency_rad_s=wn,damping_ratio=zeta,
        overshoot_fraction=overshoot,final_error_rad=target-q,
        trajectory_rmse_rad=np.sqrt(np.mean((positions-target)**2)))
    derivation=[f'Joint inertia is {I:g} kg*m^2; Kp={kp:g} Nm/rad; Kd={kd:g} Nm*s/rad.',
        f'The implied natural frequency is {wn:.6f} rad/s and damping ratio is {zeta:.6f}.',
        'Apply a 0.1 rad target and integrate semi-implicitly at 1 ms for three seconds.',
        f'Peak position is {positions.max():.6f} rad, producing overshoot fraction {overshoot:.6f}.',
        f'Final tracking error is {target-q:.8f} rad; trajectory RMSE is {metrics["trajectory_rmse_rad"]:.6f} rad.']
    notes=[('This model is underdamped.' if zeta<1 else 'This model is critically damped or overdamped.'),
           'There is no torque saturation, delay, gravity or contact in this identification-friendly reference.']
    return metrics,derivation,notes
''',dict(inertia=.08,kp=20.,kd=2.),'kd',[.1,.5,1.,2.,4.,8.],
'inertia is output-axis kg*m^2; kp is Nm/rad; kd is Nm*s/rad; physical viscous damping is fixed at 0.1 Nm*s/rad.',
'The velocity update precedes the position update, giving semi-implicit integration. Compare simulated overshoot with the damping classification; then vary inertia to see why gains are model dependent.',
'Increasing Kp to compensate for torque saturation; differentiating a noisy setpoint instead of defining derivative action carefully.',
['Double inertia and recover the original natural frequency and damping ratio.','Add a torque cap and compare the linear prediction to the actual response.','Measure settling within a predeclared error band.'],
'Physical gain changes require identified inertia, sensor noise, delay and a guarded test envelope; theoretical tuning is only a starting point.')

add('antiwindup','Integral action, saturation and anti-windup',
'''Integral action accumulates persistent error and can compensate an unknown constant disturbance. When an actuator saturates, continued integration stores a demand that the plant cannot realize. After the target changes, this stored integral can keep the output saturated in the wrong direction. Conditional integration is a simple anti-windup method: integrate only when unsaturated or when the error would move the demand back toward the permitted range. The experiment explicitly compares the same plant with and without this logic.''',
'u_raw=Kp*e+Ki*integral-Kd*v; u=clip(u_raw); integrate if unsaturated or e*(u_raw-u)<=0.',
r'''
def simulate(cap,anti):
    q=v=integral=0.;dt=.002;history=[];saturated=0
    for k in range(2000):
        target=.5 if k<500 else 0.
        error=target-q
        raw=12*error+10*integral-2*v
        u=np.clip(raw,-cap,cap)
        if not anti or abs(raw)<=cap or error*(raw-u)<=0:
            integral+=dt*error
        v+=dt*(u-.2*v)/.2;q+=dt*v
        history.append(q);saturated+=abs(raw)>cap
    return np.array(history),integral,saturated/2000

def experiment(p):
    cap=p['torque_cap'];plain,ip,sp=simulate(cap,False)
    protected,ia,sa=simulate(cap,True)
    metrics=dict(plain_final_error_rad=abs(plain[-1]),
        protected_final_error_rad=abs(protected[-1]),
        plain_integral=ip,protected_integral=ia,
        plain_saturation_fraction=sp,protected_saturation_fraction=sa)
    derivation=[f'Use symmetric actuator limit +/-{cap:g} Nm.',
        'Request 0.5 rad for one second, then return the target to zero.',
        f'Without anti-windup, saturation fraction is {sp:.6f} and final integral is {ip:.6f}.',
        f'Conditional integration gives saturation fraction {sa:.6f} and integral {ia:.6f}.',
        f'Final absolute errors are {abs(plain[-1]):.6f} and {abs(protected[-1]):.6f} rad respectively.']
    notes=['Anti-windup improves consistency with actuator authority but does not guarantee every transient metric improves.',
           'Integral state must also be handled explicitly when changing modes, resetting faults or switching controllers.']
    return metrics,derivation,notes
''',dict(torque_cap=1.),'torque_cap',[.1,.25,.5,1.,2.,5.],
'torque_cap is the symmetric teaching actuator limit in Nm; plant inertia is 0.2 kg*m^2 and timestep is 2 ms.',
'The paired simulations share target, gains and plant. Only the integral update rule changes, making the comparison causal. Inspect the return-to-zero segment rather than only the initial rise.',
'Clamping the output while leaving integral unbounded; resetting integral unexpectedly during a loaded transition; claiming one example proves all PID tuning.',
['Add back-calculation anti-windup and compare with conditional integration.','Apply a constant load and examine steady-state error.','Define a bumpless transfer from PD to PID.'],
'Integral action can command sustained physical torque; thermal and fault behavior must be part of its design.')

add('minimum_jerk','Minimum-jerk trajectories and duration constraints',
'''A position step implies unbounded ideal velocity and acceleration. A fifth-order minimum-jerk interpolation has zero endpoint velocity and acceleration, making it a useful smooth reference for a point-to-point move. Smoothness does not establish feasibility: shortening the duration increases velocity, acceleration and jerk by different powers. This laboratory computes those quantities analytically and compares them with finite sampled values so a trajectory can be rejected before being sent to a controller.''',
's=10*r^3-15*r^4+6*r^5; q=q0+delta*s; q_dot=delta*s_prime/T; q_ddot=delta*s_second/T^2.',
r'''
def experiment(p):
    T,delta=p['duration'],p['excursion'];r=np.linspace(0,1,1001)
    s=10*r**3-15*r**4+6*r**5
    ds=30*r**2-60*r**3+30*r**4
    dds=60*r-180*r**2+120*r**3
    ddds=60-360*r+360*r**2
    q=delta*s;v=delta*ds/T;a=delta*dds/T**2;j=delta*ddds/T**3
    assert np.isclose(q[0],0) and np.isclose(q[-1],delta)
    assert np.allclose(v[[0,-1]],0) and np.allclose(a[[0,-1]],0)
    metrics=dict(peak_speed_rad_s=np.max(abs(v)),
        peak_acceleration_rad_s2=np.max(abs(a)),peak_jerk_rad_s3=np.max(abs(j)),
        final_position_rad=q[-1],speed_limit_margin_rad_s=.5-np.max(abs(v)))
    derivation=[f'Move through delta={delta:g} rad over duration T={T:g} s.',
        'Evaluate the polynomial and its first three derivatives at 1001 normalized positions.',
        f'Peak speed is {np.max(abs(v)):.6f} rad/s.',
        f'Peak acceleration is {np.max(abs(a)):.6f} rad/s^2; peak jerk is {np.max(abs(j)):.6f} rad/s^3.',
        f'Against an illustrative 0.5 rad/s speed envelope, margin is {metrics["speed_limit_margin_rad_s"]:.6f} rad/s.']
    notes=['The speed envelope is a teaching assumption and must not be substituted for a released actuator limit.',
           'Zero endpoint velocity and acceleration do not ensure the controller can supply the required intermediate torque.']
    return metrics,derivation,notes
''',dict(duration=2.,excursion=.4),'duration',[.25,.5,1.,2.,3.,5.],
'duration is seconds; excursion is output-joint radians. The interpolation starts from zero relative displacement.',
'Use normalized time to separate trajectory shape from duration. The endpoint assertions check boundary conditions, while derivative scaling exposes why a fast smooth move can still be infeasible.',
'Checking position limits but not derivatives; differentiating noisy numerical samples when analytic derivatives are available; ignoring start velocity.',
['Derive a minimum duration from a chosen speed limit.','Check an acceleration limit and choose the stricter duration.','Generalize to nonzero initial velocity using a boundary-value polynomial.'],
'Physical trajectories need torque, collision, cable and thermal feasibility in addition to smooth kinematic references.')

add('rate_limits','Position envelopes, slew limits and stopping distance',
'''A position limit alone does not protect a joint already moving toward a stop. The controller also needs enough distance to decelerate within its available authority. A slew limiter bounds requested changes but can introduce tracking lag, while an emergency stop requires a separate physically reviewed outcome. This experiment applies a velocity-limited target and calculates an ideal stopping-distance screen including reaction delay. It is a planning calculation, not a certified stopping model.''',
'q_next=q_prev+clip(q_request-q_prev,+/-vmax*dt); d_stop=v*delay+v^2/(2*a_brake).',
r'''
def experiment(p):
    vmax,dt,delay=p['speed'],p['dt'],p['delay'];brake=p['deceleration']
    q=0.;request=.5;trace=[]
    for _ in range(500):
        q+=np.clip(request-q,-vmax*dt,vmax*dt);trace.append(q)
    stopping=vmax*delay+vmax*vmax/(2*brake)
    margin=.12-stopping
    metrics=dict(final_target_rad=q,ideal_stopping_distance_rad=stopping,
        remaining_travel_margin_rad=margin,per_update_step_rad=vmax*dt,
        time_to_target_s=request/vmax)
    derivation=[f'At vmax={vmax:g} rad/s and dt={dt:g} s, each target increment is capped at {vmax*dt:.6f} rad.',
        f'Reaction delay contributes {vmax*delay:.6f} rad of travel.',
        f'Ideal constant deceleration {brake:g} rad/s^2 contributes {vmax*vmax/(2*brake):.6f} rad.',
        f'Total screened stopping distance is {stopping:.6f} rad.',
        f'With 0.12 rad assumed remaining travel, margin is {margin:.6f} rad.']
    notes=[('The ideal calculation leaves positive travel margin.' if margin>=0 else
            'The ideal calculation already exceeds available travel; reduce speed or increase clearance before considering uncertainty.'),
           'Load, control delay, brake authority and power-loss behavior must be measured for a physical stopping claim.']
    return metrics,derivation,notes
''',dict(speed=.4,dt=.01,delay=.05,deceleration=2.),'speed',[.1,.2,.4,.6,.8,1.],
'speed is rad/s; dt and delay are seconds; deceleration is a positive assumed rad/s^2 magnitude.',
'Calculate reaction travel and braking travel separately. The target slew limiter governs requests, whereas actual velocity and stopping must be monitored from feedback.',
'Calling a setpoint limiter a measured speed limiter; assuming torque remains available after power isolation; ignoring gravity-assisted motion.',
['Propagate uncertainty in delay and deceleration to a conservative margin.','Add acceleration-limited setpoint generation.','Compare command motion and measured motion under saturation.'],
'Physical limits require independent sensing, conservative travel margins and a stop strategy compatible with the support rig.')

add('gravity_identification','Gravity compensation and model-mismatch torque',
'''Gravity compensation predicts load torque from configuration and feeds it forward so feedback need not create all supporting effort through error. A biased mass or lever estimate creates a pose-dependent residual. This is different from a constant encoder offset or viscous friction. The experiment synthesizes static measurements over a range of angles and estimates the gravity coefficient from a cosine basis. It then quantifies the residual if the controller uses an incorrect payload mass.''',
'gravity torque = A*cos(q); A=m*g*l; A_hat=(cos(q).T*y)/(cos(q).T*cos(q)).',
r'''
def experiment(p):
    true_mass=2.;model_mass=p['model_mass'];length=.25
    angles=np.linspace(-1.,1.,41);basis=np.cos(angles)
    true= true_mass*9.81*length*basis
    assumed=model_mass*9.81*length*basis
    rng=np.random.default_rng(3);measured=true+rng.normal(0,.03,len(angles))
    coefficient=float(basis@measured/(basis@basis))
    fitted=coefficient*basis
    metrics=dict(feedforward_rmse_Nm=np.sqrt(np.mean((true-assumed)**2)),
        peak_residual_Nm=np.max(abs(true-assumed)),
        identified_mass_kg=coefficient/(9.81*length),
        fit_residual_rmse_Nm=np.sqrt(np.mean((measured-fitted)**2)))
    derivation=[f'The true static gravity coefficient is {true_mass*9.81*length:.6f} Nm.',
        f'The assumed model uses mass {model_mass:g} kg and coefficient {model_mass*9.81*length:.6f} Nm.',
        'Generate static samples over -1 to +1 rad with 0.03 Nm standard-deviation noise.',
        f'Project measurements onto cos(q), obtaining A_hat={coefficient:.6f} Nm.',
        f'The inferred mass is {metrics["identified_mass_kg"]:.6f} kg; feedforward mismatch RMSE is {metrics["feedforward_rmse_Nm"]:.6f} Nm.']
    notes=['The cosine model assumes a known angle convention, lever and negligible dynamic/friction torque during the measurement.',
           'A good gravity fit does not identify inertia, backlash or transient motor limits.']
    return metrics,derivation,notes
''',dict(model_mass=1.8),'model_mass',[1.,1.5,1.8,2.,2.2,2.5],
'model_mass is the controller payload estimate in kilograms; true teaching mass is 2 kg at a 0.25 m lever.',
'The identification uses independent synthetic measurements rather than fitting the controller prediction. Report fit residual and feedforward-model residual separately; they answer different questions.',
'Using moving samples as static gravity data; absorbing encoder-zero error into an incorrect mass estimate; ignoring multi-link coupling.',
['Add a constant torque bias and fit both cosine and offset terms.','Introduce a small angle-zero error and inspect residual structure.','Compare fit and validation angle ranges.'],
'Actual gravity compensation requires verified model conventions and low-energy measurements with load support.')

add('motor_envelope','Torque-speed envelopes and trajectory feasibility',
'''An actuator does not provide its maximum torque at every speed. Electrical voltage, current limits, losses and thermal constraints shape a feasible envelope. A simple linear torque-speed model is useful for screening and for understanding why a trajectory can become infeasible as speed rises. It is not a substitute for a vendor curve. Here the torque demand is fixed while speed varies, making reserve and mechanical power easy to compare.''',
'tau_available=tau_stall*max(0,1-|omega|/omega_no_load); reserve=tau_available-|tau_required|.',
r'''
def experiment(p):
    omega=p['speed'];stall=p['stall_torque'];free=p['no_load_speed']
    required=p['required_torque']
    available=stall*max(0.,1-abs(omega)/free)
    reserve=available-abs(required)
    metrics=dict(available_torque_Nm=available,reserve_Nm=reserve,
        required_mechanical_power_W=required*omega,
        envelope_power_W=available*abs(omega),feasible=float(reserve>=0))
    derivation=[f'The teaching envelope has zero-speed torque {stall:g} Nm and no-load speed {free:g} rad/s.',
        f'At speed {omega:g} rad/s the linear speed factor is {max(0,1-abs(omega)/free):.6f}.',
        f'Available torque is {available:.6f} Nm while demand is {required:g} Nm.',
        f'Reserve is {reserve:.6f} Nm; feasibility flag is {reserve>=0}.',
        f'Demanded mechanical power is {required*omega:.6f} W.']
    notes=['The illustrative envelope is instantaneous and excludes continuous thermal derating and regenerative quadrants.',
           'A positive reserve is only one constraint; position, load path, current and thermal checks remain separate.']
    return metrics,derivation,notes
''',dict(speed=2.,stall_torque=10.,no_load_speed=8.,required_torque=4.),'speed',[0.,1.,2.,4.,6.,8.],
'speed is output rad/s; stall_torque and required_torque are Nm; no_load_speed is the assumed output speed at negligible torque.',
'Separate the model of available authority from the load demand. The feasibility flag is derived from the reserve rather than from whether the numerical simulator keeps running.',
'Treating stall torque as continuous; mixing motor-shaft and output-shaft speed; extrapolating a linear toy curve beyond the data range.',
['Evaluate an entire minimum-jerk torque/speed trajectory against the envelope.','Add a voltage-dependent no-load speed.','Separate motoring and regenerative operation.'],
'Use measured or manufacturer-supplied actuator curves, firmware current limits and duty-cycle constraints for actual motors.')

add('delay_control','Feedback delay, sample-and-hold and tracking degradation',
'''A controller acts on information from the past. Even if each packet is delivered reliably, delayed position feedback changes the phase of the loop and can create oscillation. Sample-and-hold output adds another timing effect. This experiment stores a queue of previous states and makes the feedback delay explicit in samples. The plant and gains remain fixed, so changes in error can be attributed to the delay model rather than a simultaneous retuning.''',
'u[k]=Kp*(reference-q[k-d])-Kd*v[k-d]; delay_seconds=d*dt.',
r'''
def experiment(p):
    dt=.001;delay=p['delay'];d=max(0,round(delay/dt))
    q=v=0.;states=[(0.,0.)]*(d+1);errors=[];torques=[]
    for k in range(3000):
        t=k*dt;target=.1*np.sin(2*np.pi*.5*t)
        oldq,oldv=states[max(0,len(states)-1-d)]
        u=np.clip(20*(target-oldq)-2*oldv,-3,3)
        v+=dt*(u-.1*v)/.08;q+=dt*v
        states.append((q,v));errors.append(target-q);torques.append(u)
    errors=np.array(errors);torques=np.array(torques)
    metrics=dict(actual_delay_s=d*dt,tracking_rmse_rad=np.sqrt(np.mean(errors**2)),
        peak_error_rad=np.max(abs(errors)),saturation_fraction=np.mean(abs(torques)>=2.999))
    derivation=[f'Request delay {delay:g} s; rounding to 1 ms samples gives {d} delayed samples.',
        'The reference is a 0.1 rad, 0.5 Hz sinusoid; gains remain Kp=20 and Kd=2.',
        'Use delayed position and velocity but the current reference to calculate torque.',
        f'After three seconds, RMSE is {np.sqrt(np.mean(errors**2)):.6f} rad.',
        f'Peak error is {np.max(abs(errors)):.6f} rad and saturation fraction is {metrics["saturation_fraction"]:.6f}.']
    notes=['The chosen delay is deterministic; real transport also has jitter, dropouts and timestamp uncertainty.',
           'A simulator with immediate state access can substantially overestimate the usable gain margin.']
    return metrics,derivation,notes
''',dict(delay=.01),'delay',[0.,.002,.005,.01,.02,.05],
'delay is seconds of feedback age; plant integration is 1 ms and torque limit is an illustrative 3 Nm.',
'The state history implements delay without altering the integration timestep. Inspect the actual rounded delay because requested values may not be exactly representable in samples.',
'Ignoring packet age because delivery is reliable; compensating delay with unvalidated gain increases; comparing different reference timing conventions.',
['Add bounded seeded jitter to the feedback index.','Drop a burst of feedback samples and define a watchdog response.','Compare delayed feedback with predicted current state.'],
'Physical timing measurements must include sensing, transport, scheduling and actuator application, not only network round-trip time.')

add('thermal','First-order thermal models and duty-cycle limits',
'''Temperature accumulates the history of losses. A motor can satisfy an instantaneous torque requirement while exceeding its thermal capacity over a longer duty cycle. A first-order resistance-capacitance model represents thermal storage and heat flow to ambient. Its time constant explains why short successful tests cannot prove continuous capability. The parameters below are illustrative and deliberately separate electrical loss from the thermal model.''',
'C_th*T_dot=P_loss-(T-T_ambient)/R_th; steady rise=P_loss*R_th; time_constant=R_th*C_th.',
r'''
def experiment(p):
    power,R,C=p['loss_power'],p['thermal_resistance'],p['thermal_capacity']
    duration,ambient=p['duration'],25.
    rise=power*R*(1-np.exp(-duration/(R*C)))
    final=ambient+rise
    threshold=70.;steady=ambient+power*R
    if steady>threshold:
        crossing=-R*C*np.log(1-(threshold-ambient)/(power*R))
    else:
        crossing=-1.
    metrics=dict(final_temperature_C=final,steady_temperature_C=steady,
        time_constant_s=R*C,screening_margin_C=threshold-final,
        threshold_crossing_s=crossing)
    derivation=[f'Assume loss power {power:g} W, Rth={R:g} K/W and Cth={C:g} J/K.',
        f'The thermal time constant is {R*C:.6f} s.',
        f'After {duration:g} s, temperature rise is {rise:.6f} K above 25 C ambient.',
        f'Predicted final temperature is {final:.6f} C and steady temperature is {steady:.6f} C.',
        f'The 70 C teaching threshold crossing time is {crossing:.6f} s; -1 means no crossing in the ideal constant-loss model.']
    notes=['The 70 C threshold is an exercise parameter, not a motor or material rating.',
           'Actual winding, housing, drive and gearbox temperatures have different dynamics and measurement locations.']
    return metrics,derivation,notes
''',dict(loss_power=20.,thermal_resistance=2.,thermal_capacity=100.,duration=300.),'loss_power',[5.,10.,15.,20.,30.,40.],
'loss_power is Watts dissipated as heat; thermal_resistance is K/W; thermal_capacity is J/K; duration is seconds.',
'The analytical solution gives both transient and steady behavior. An unreachable threshold is encoded explicitly rather than confusing infinity with a safe physical guarantee.',
'Using mechanical output power as heat loss; trusting a housing sensor to represent winding temperature instantly; ignoring ambient and airflow.',
['Integrate a square-wave duty cycle numerically and compare average-loss approximations.','Fit Rth and Cth from a safe measured heating/cooling trace.','Repeat at a higher ambient temperature.'],
'Use manufacturer temperature limits and identified thermal behavior to design real derating and stop thresholds.')

add('energy_regen','Mechanical energy, electrical demand and regeneration',
'''Electrical supply design depends on energy flow as well as peak current. Motoring consumes electrical energy; decelerating or lowering a load may return energy to the bus. A bench supply that sources current may not safely sink it. Separating positive mechanical work, negative mechanical work, conversion losses and regenerated energy avoids the misleading assumption that average motor power describes every electrical condition.''',
'P_mech=tau*omega; P_elec=P_mech/eta for motoring, eta_regen*P_mech for regenerative operation; E=integral(P dt).',
r'''
def experiment(p):
    eta=p['efficiency'];regen=p['regen_efficiency'];T=4.
    t=np.linspace(0,T,2001);speed=2*np.sin(2*np.pi*t/T)
    torque=1.5*np.cos(2*np.pi*t/T)+.5
    mechanical=torque*speed
    electrical=np.where(mechanical>=0,mechanical/eta,mechanical*regen)
    positive=np.trapezoid(np.maximum(electrical,0),t)
    returned=-np.trapezoid(np.minimum(electrical,0),t)
    metrics=dict(energy_drawn_J=positive,energy_returned_J=returned,
        net_energy_J=positive-returned,peak_draw_W=max(electrical),
        peak_return_W=-min(electrical))
    derivation=['Generate a four-second signed torque and speed cycle.',
        f'Motoring efficiency is {eta:g}; regenerative efficiency is {regen:g}.',
        f'Convert positive and negative mechanical power using their respective efficiencies.',
        f'Integrate positive electrical power: {positive:.6f} J drawn.',
        f'Integrate negative electrical power: {returned:.6f} J returned; net is {positive-returned:.6f} J.']
    notes=['Negative mechanical power represents energy leaving the mechanical system; the electrical destination depends on the actual drive and power topology.',
           'A low net-energy cycle can still impose large instantaneous source and sink requirements.']
    return metrics,derivation,notes
''',dict(efficiency=.8,regen_efficiency=.5),'regen_efficiency',[0.,.2,.4,.6,.8,1.],
'efficiency is motoring mechanical/electrical power ratio; regen_efficiency is the fraction of negative mechanical energy returned electrically.',
'Use signed power before integrating and keep motoring and regeneration totals separate. Clipping all negative power to zero would conceal a supply design requirement.',
'Calculating battery current from average mechanical power alone; assuming every supply can absorb regeneration; ignoring driver protection behavior.',
['Estimate bus-capacitor voltage rise from returned energy.','Compare peak and average demand for the same cycle.','Add constant electronics power and recompute net energy.'],
'Regeneration handling must be approved for the actual supply, battery, drive and isolation scheme before a loaded actuator test.')

add('scheduler','Control deadlines, jitter and tail-latency budgets',
'''Average runtime is insufficient for a feedback deadline. Rare scheduling delays or long inference calls can age a command enough to matter physically. A timing budget should account for sensing, transport, estimation, control, inference and application. This experiment uses a seeded synthetic workload with occasional long delays to compare average and high-percentile completion times. It demonstrates a measurement method, not the timing performance of your laptop or a real-time operating system.''',
'completion = sensing+transport+compute+scheduler_jitter; deadline_miss = completion>period.',
r'''
def experiment(p):
    rng=np.random.default_rng(19);n=10000;period=p['period_ms']
    sensing=rng.uniform(.1,.3,n);transport=rng.uniform(.1,.4,n)
    compute=np.maximum(.05,rng.normal(.7,.12,n))
    jitter=rng.exponential(p['jitter_mean_ms'],n)
    rare=rng.random(n)<.005;jitter[rare]+=3.
    elapsed=sensing+transport+compute+jitter
    metrics=dict(mean_completion_ms=np.mean(elapsed),p99_completion_ms=np.quantile(elapsed,.99),
        max_completion_ms=np.max(elapsed),deadline_miss_fraction=np.mean(elapsed>period),
        minimum_observed_margin_ms=period-np.max(elapsed))
    derivation=[f'Generate {n} synthetic cycles with period {period:g} ms.',
        f'Exponential jitter mean is {p["jitter_mean_ms"]:g} ms, plus a 0.5% long-delay mechanism.',
        f'Mean completion is {np.mean(elapsed):.6f} ms.',
        f'The 99th percentile is {np.quantile(elapsed,.99):.6f} ms and worst observed is {np.max(elapsed):.6f} ms.',
        f'Missed-deadline fraction is {np.mean(elapsed>period):.6f}.']
    notes=['Worst observed latency is not a proven worst-case bound; finite sampling can miss rarer events.',
           'The random workload is pedagogical. Real timing claims require instrumented measurements under declared stress conditions.']
    return metrics,derivation,notes
''',dict(period_ms=2.,jitter_mean_ms=.1),'jitter_mean_ms',[.01,.05,.1,.2,.5,1.],
'period_ms is the target cycle deadline in milliseconds; jitter_mean_ms controls a synthetic scheduler-delay distribution.',
'Retain the entire latency distribution long enough to calculate misses and tails. The rare-delay mechanism explains why a reassuring mean can coexist with unacceptable behavior.',
'Calling Python timer intervals hard-real-time guarantees; measuring only warm unloaded inference; ignoring clock overhead and missed samples.',
['Add a separate inference task every tenth cycle and calculate the shared budget.','Compare a deadline watchdog with a packet-count watchdog.','Measure actual workload latency on the current workstation and replace the synthetic distribution.'],
'Use local embedded deadlines and independently tested stop authority where the physical control design requires them.')
