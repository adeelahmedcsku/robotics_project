from catalog import add
add('center_mass','Link masses, payload shifts and center of mass',
'''Center of mass is an average weighted by mass, not by link count. A light component placed far from the body can shift the combined center substantially. Adding a payload also changes inertia and torque requirements, but COM alone describes only the first moment of mass. This experiment adds a point payload to a simple three-link assembly and calculates both the new COM and the gravity moment about an origin. All coordinates must share one frame; averaging body-local positions would produce a physically meaningless answer.''',
'c = sum(m_i*r_i)/sum(m_i); M_gravity = sum(r_i cross m_i*g).',
r'''
def experiment(p):
    masses=np.array([4.,2.,1.,p['payload_mass']])
    positions=np.array([[0.,0.,.4],[.1,0.,.3],[-.1,0.,.2],
                        [p['payload_x'],0.,.5]])
    total=masses.sum()
    com=(masses[:,None]*positions).sum(axis=0)/total
    forces=masses[:,None]*np.array([0.,0.,-9.81])
    moment=np.cross(positions,forces).sum(axis=0)
    expected=np.cross(com,total*np.array([0.,0.,-9.81]))
    assert np.allclose(moment,expected)
    metrics=dict(total_mass_kg=total,com_x_m=com[0],com_z_m=com[2],
                 gravity_pitch_moment_Nm=moment[1],weight_N=total*9.81)
    derivation=[f'Total mass is 4+2+1+{p["payload_mass"]:g} = {total:.6f} kg.',
        f'The payload lies at x={p["payload_x"]:g} m in the shared frame.',
        f'Sum mass times position, then divide by total: COM={com.tolist()} m.',
        f'Sum each gravity moment to obtain pitch moment {moment[1]:.6f} Nm.',
        'Applying total weight at the COM reproduces the same moment, providing an independent check.']
    notes=['This static point-mass model does not represent distributed inertia or dynamic contact stability.',
           f'The horizontal COM displacement from the origin is {com[0]:.6f} m; compare it with a measured support margin.']
    return metrics,derivation,notes
''',dict(payload_mass=1.,payload_x=.3),'payload_mass',[0.,.25,.5,1.,2.,4.],
'payload_mass is kilograms; payload_x is meters in the common origin frame. The other three masses are fixed teaching links.',
'Broadcast masses over vector positions, form gravity forces, and compare distributed moments with the equivalent resultant at COM. This verifies the coordinate and weighting conventions together.',
'Averaging local link coordinates; omitting batteries or cables from mass accounting; treating COM margin as a dynamic balance proof.',
['Move the payload laterally and recompute roll moment.','Estimate COM uncertainty for a 10 mm payload-position error.','Add a fifth link and verify the equivalent resultant identity.'],
'Weigh actual assemblies and measure their reference positions; CAD mass depends on assigned density and included components.')

add('inertia','Inertia tensors and the parallel-axis theorem',
'''Mass describes resistance to translation. Inertia describes resistance to angular acceleration about a chosen axis and origin. Two assemblies with equal mass can require very different torque if their mass is distributed differently. The inertia tensor must be expressed in a named frame; moving the reference origin adds a parallel-axis term. Physical principal inertias are nonnegative and obey constraints that arbitrary matrix entries may violate. Here a uniform box is shifted away from an axis to make the geometric effect visible.''',
'I_box = m/12*diag(b^2+c^2,a^2+c^2,a^2+b^2); I_origin = I_com + m*((r dot r)*I-r*r.T).',
r'''
def experiment(p):
    m=p['mass'];a,b,c=.2,.1,.08
    r=np.array([p['offset'],.02,0.])
    Ic=m/12*np.diag([b*b+c*c,a*a+c*c,a*a+b*b])
    shift=m*((r@r)*np.eye(3)-np.outer(r,r))
    Io=Ic+shift
    principal=np.linalg.eigvalsh(Io)
    alpha=np.array([0.,0.,p['acceleration']])
    tau=Io@alpha
    assert np.all(principal>0) and np.allclose(Io,Io.T)
    metrics=dict(Izz_kg_m2=Io[2,2],minimum_principal_kg_m2=principal[0],
        torque_z_Nm=tau[2],offset_contribution_kg_m2=shift[2,2])
    derivation=[f'A uniform {m:g} kg box has COM Izz={Ic[2,2]:.8f} kg*m^2.',
        f'Shift the reference by {r.tolist()} m.',
        f'The parallel-axis contribution to Izz is {shift[2,2]:.8f} kg*m^2.',
        f'Total Izz is {Io[2,2]:.8f}; requested z acceleration is {alpha[2]:g} rad/s^2.',
        f'Ignoring other dynamics, required z torque is {tau[2]:.8f} Nm.']
    notes=['This acceleration-only torque excludes gravity, Coriolis terms, friction and transmission effects.',
           'An inertia tensor attached to the wrong origin can make a controller consistently wrong even when total mass is correct.']
    return metrics,derivation,notes
''',dict(mass=2.,offset=.1,acceleration=3.),'offset',[0.,.02,.05,.1,.2,.3],
'mass is kilograms; offset is the x displacement of COM from the target origin in meters; acceleration is rad/s^2.',
'The outer product creates both diagonal and off-diagonal terms. Eigenvalues check positive principal inertias; the torque calculation shows how placement affects actuation demand.',
'Using grams as kilograms; importing inertia in mm^2 units; moving inertia without transforming its frame; diagonalizing away real coupling.',
['Rotate the tensor by R*I*R.T and compare kinetic energy in both frames.','Double every box dimension and derive the inertia scaling at fixed mass.','Compare a point mass with a distributed box.'],
'Validate CAD inertia units, density assignments and reference frames before policy training or gravity compensation.')

add('angular_momentum','Angular momentum, kinetic energy and off-axis motion',
'''For rotation about a fixed principal axis, angular momentum and angular velocity are parallel. For a general rigid body they need not be. The inertia tensor maps angular velocity to angular momentum, and rotational kinetic energy is a quadratic form. This distinction matters when arms or torso motions redistribute whole-body angular momentum. Conservation arguments require the external moment assumptions to be explicit; contact forces and a support fixture can inject moments.''',
'L=I*omega; E_rot=0.5*omega.T*I*omega; tau=I*alpha+omega cross (I*omega).',
r'''
def experiment(p):
    I=np.diag([.08,.12,.2])
    omega=np.array([p['speed'],.7,.2])
    alpha=np.array([0.,.3,0.])
    momentum=I@omega
    energy=.5*omega@momentum
    gyroscopic=np.cross(omega,momentum)
    torque=I@alpha+gyroscopic
    cosine=(omega@momentum)/(np.linalg.norm(omega)*np.linalg.norm(momentum))
    angle=np.arccos(np.clip(cosine,-1,1))
    metrics=dict(kinetic_energy_J=energy,momentum_norm_kg_m2_s=np.linalg.norm(momentum),
        misalignment_rad=angle,gyroscopic_torque_Nm=np.linalg.norm(gyroscopic),
        required_torque_Nm=np.linalg.norm(torque))
    derivation=[f'Angular velocity is {omega.tolist()} rad/s.',
        f'Multiply by diagonal inertia to obtain L={momentum.tolist()} kg*m^2/s.',
        f'The quadratic energy is {energy:.6f} J.',
        f'Compute omega cross L: {gyroscopic.tolist()} Nm.',
        f'Include the acceleration term to obtain torque {torque.tolist()} Nm.']
    notes=[f'L and omega differ in direction by {angle:.6f} rad in this non-spherical body.',
           'The calculation assumes a rigid body about its COM with a consistently expressed inertia tensor.']
    return metrics,derivation,notes
''',dict(speed=1.),'speed',[.1,.3,.7,1.,2.,4.],
'speed is the x angular-velocity component in rad/s; the y and z components and inertia tensor are fixed.',
'Compute momentum before energy and gyroscopic torque so the directional coupling is visible. A spherical-inertia extension should eliminate the gyroscopic term for any omega.',
'Treating inertia as one scalar in a three-axis problem; omitting external moments when discussing conservation.',
['Set all diagonal inertias equal and verify L is parallel to omega.','Reverse omega and compare momentum, energy and gyroscopic torque.','Evaluate kinetic energy after a frame rotation.'],
'Whole-body controllers must account for angular momentum and contact wrench feasibility; a torso orientation target alone is incomplete.')

add('joint_loading','Gravity, acceleration and joint-load budgeting',
'''A motor must support gravity and accelerate the link while overcoming friction. Looking only at the static gravity torque can underestimate peaks; looking only at the peak actuator rating can overestimate continuous capability. This experiment combines a point payload and a uniform rod into an explicitly simple joint-load model. The result is useful for reasoning about sensitivity, but cannot replace a released mechanism model, bearing analysis or duty-cycle study.''',
'tau = (m_payload*g*l + m_rod*g*l/2)*cos(q) + (m_payload*l^2+m_rod*l^2/3)*q_ddot + tau_friction.',
r'''
def experiment(p):
    l,mp,mr=p['length'],p['payload'],p['rod_mass']
    q=np.deg2rad(p['angle_deg']);alpha=p['acceleration']
    gravity=(mp*9.81*l+mr*9.81*l/2)*np.cos(q)
    inertia=mp*l*l+mr*l*l/3
    dynamic=inertia*alpha
    friction=.3
    total=gravity+dynamic+friction
    metrics=dict(gravity_Nm=gravity,inertia_kg_m2=inertia,
        acceleration_Nm=dynamic,total_required_Nm=total,
        gravity_fraction=gravity/total)
    derivation=[f'Payload mass {mp:g} kg acts at {l:g} m; rod COM acts at {l/2:g} m.',
        f'At angle {p["angle_deg"]:g} degrees, gravity torque is {gravity:.6f} Nm.',
        f'Total modeled rotational inertia is {inertia:.6f} kg*m^2.',
        f'Acceleration {alpha:g} rad/s^2 adds {dynamic:.6f} Nm.',
        f'Add 0.3 Nm illustrative friction: total demand is {total:.6f} Nm.']
    notes=['The load budget separates assumptions so the dominant contribution can be identified.',
           'This one-axis model excludes impact, gear reflected inertia, cable forces and multi-link coupling.']
    return metrics,derivation,notes
''',dict(length=.25,payload=2.,rod_mass=1.,angle_deg=20.,acceleration=3.),'acceleration',[0.,1.,2.,3.,6.,12.],
'length is meters; payload and rod_mass are kilograms; acceleration is output-axis rad/s^2; angle is measured from horizontal.',
'The rod and payload have different lever arms and inertia formulas. Keeping gravity and acceleration terms separate makes the result auditable and supports a duty-cycle calculation later.',
'Using motor-shaft acceleration with output-axis inertia; applying a static margin to an impact; omitting the fixture reaction load.',
['Compare the horizontal and vertical configurations.','Double payload mass and identify linear terms.','Calculate a trajectory torque trace rather than one worst-looking pose.'],
'Use release-specific mass/inertia, measured friction and continuous motor envelopes before choosing a physical load.')

add('gear_backlash','Gear ratio, reflected inertia and backlash dead zones',
'''A gearbox changes the coordinate system between a motor and an output. Rotor inertia reflected to the output grows with the square of the velocity ratio, which can make a high-ratio transmission dynamically significant. Backlash is a lost-motion region during reversals, not a random measurement error. This laboratory combines an inertia calculation with a simple play operator that holds the output until the input crosses the slack boundary. It is deliberately a scalar transmission model, not an identified Asimov actuator.''',
'I_reflected = J_motor*G^2; backlash output remains inside input +/- half_gap until a boundary forces motion.',
r'''
def experiment(p):
    ratio=p['ratio'];J=p['rotor_inertia'];gap=p['backlash']
    t=np.linspace(0,4,1001);desired=.1*np.sin(2*np.pi*.5*t)
    actual=np.zeros_like(desired)
    for i in range(1,len(t)):
        previous=actual[i-1]
        actual[i]=np.clip(previous,desired[i]-gap/2,desired[i]+gap/2)
    error=desired-actual
    metrics=dict(reflected_inertia_kg_m2=J*ratio**2,
        tracking_rmse_rad=np.sqrt(np.mean(error**2)),
        peak_lost_motion_rad=np.max(np.abs(error)),
        transmitted_range_rad=np.ptp(actual))
    derivation=[f'Rotor inertia {J:.3e} kg*m^2 is reflected through ratio {ratio:g}.',
        f'Output-equivalent inertia is {J*ratio**2:.8f} kg*m^2.',
        f'The commanded output trajectory has 0.1 rad amplitude and 0.5 Hz frequency.',
        f'Apply a total backlash gap of {gap:.6f} rad with a stateful play operator.',
        f'The resulting RMSE is {np.sqrt(np.mean(error**2)):.6f} rad; peak error is {np.max(np.abs(error)):.6f} rad.']
    notes=['A stateful dead zone creates hysteresis; adding independent Gaussian noise would model a different phenomenon.',
           'The play model excludes stiffness, friction and load-dependent tooth contact.']
    return metrics,derivation,notes
''',dict(ratio=36.,rotor_inertia=2e-5,backlash=.01),'backlash',[0.,.002,.005,.01,.02,.04],
'ratio is motor/output speed ratio; rotor_inertia is motor-shaft kg*m^2; backlash is total output-coordinate gap in radians.',
'The output carries memory through previous, so reversal behavior differs from a stateless clipping function. The reflected inertia calculation is independent of the backlash trajectory and must not be conflated with it.',
'Double-applying gear ratio to an output encoder; assuming all tracking error is sensor noise; ignoring reversal direction.',
['Add a load direction and compare reversal behavior.','Sweep gear ratio separately and show its squared inertia dependence.','Fit backlash from a recorded slow bidirectional experiment.'],
'Actual transmission behavior requires measured reversals and verified encoder placement; do not copy the teaching gap into a physical controller.')

add('planar_ik','Closed-form two-link inverse kinematics and branch choice',
'''Inverse kinematics often has several solutions or no solution. A two-link planar arm makes those possibilities explicit: two elbow branches can reach the same point, while targets outside an annulus cannot be reached. Clipping an impossible cosine into [-1,1] without reporting the original violation hides reachability failure. Branch selection should preserve continuity and respect limits. This simple analytic model becomes a reference for numerical IK and for understanding why more joints do not eliminate ambiguity.''',
'cos(q2)=(x^2+y^2-l1^2-l2^2)/(2*l1*l2); q1=atan2(y,x)-atan2(l2*sin(q2),l1+l2*cos(q2)).',
r'''
def experiment(p):
    l1,l2=.3,.2;x,y=p['target_x'],p['target_y']
    cosine=(x*x+y*y-l1*l1-l2*l2)/(2*l1*l2)
    reachable=abs(cosine)<=1
    q2=np.arccos(np.clip(cosine,-1,1))
    q1=np.arctan2(y,x)-np.arctan2(l2*np.sin(q2),l1+l2*np.cos(q2))
    predicted=np.array([l1*np.cos(q1)+l2*np.cos(q1+q2),
                        l1*np.sin(q1)+l2*np.sin(q1+q2)])
    residual=np.linalg.norm(predicted-[x,y])
    metrics=dict(reachable=float(reachable),q1_rad=q1,q2_rad=q2,
        residual_m=residual,cosine_raw=cosine)
    derivation=[f'Target is ({x:g},{y:g}) m with link lengths {l1:g},{l2:g} m.',
        f'Compute the raw elbow cosine {cosine:.8f}; reachability is {reachable}.',
        f'The positive-elbow candidate is q2={q2:.8f} rad.',
        f'Compute shoulder correction to obtain q1={q1:.8f} rad.',
        f'Forward kinematics returns {predicted.tolist()} m, with residual {residual:.8f} m.']
    notes=[('The target is geometrically reachable; joint limits and collisions still require separate checks.' if reachable else
            'The clipped candidate is only a nearest-boundary diagnostic. It must not be returned as a successful IK solution.'),
           'Negating q2 and recomputing q1 gives the other elbow branch when the target is not singular.']
    return metrics,derivation,notes
''',dict(target_x=.35,target_y=.1),'target_x',[.05,.1,.2,.35,.48,.6],
'target_x and target_y are meters in a fixed planar base frame; q1 and q2 are relative joint angles.',
'Compute the reachability flag before clipping for numerical evaluation. The forward residual is an independent success metric, while branch continuity requires information from the previous pose.',
'Calling a clipped cosine a valid solution; mixing absolute and relative elbow angles; assuming endpoint reachability guarantees collision freedom.',
['Compute both branches and choose the closest to a previous joint state.','Add asymmetric joint limits and identify rejected branches.','Follow a Cartesian line through a near-singular pose and inspect continuity.'],
'The humanoid arm has more axes and geometry, but the same reachability, branch, limit and collision questions remain.')

add('damped_ik','Singular values and damped least-squares motion',
'''Near a kinematic singularity, an inverse Jacobian can demand enormous joint changes to achieve a small endpoint motion. Damped least squares trades exact Cartesian tracking for bounded numerical sensitivity. Singular values reveal which directions are poorly controllable. Damping is not a safety proof: a bounded numerical update can still violate a joint limit or collision constraint. This laboratory exposes the tradeoff with a nearly stretched two-link arm.''',
'dq = J.T*(J*J.T+lambda^2*I)^-1*error; J=U*S*V.T; directional gain=s/(s^2+lambda^2).',
r'''
def experiment(p):
    q1=.2;q2=p['elbow'];lam=p['damping']
    J=np.array([[-.3*np.sin(q1)-.2*np.sin(q1+q2),-.2*np.sin(q1+q2)],
                [.3*np.cos(q1)+.2*np.cos(q1+q2),.2*np.cos(q1+q2)]])
    error=np.array([.01,0.])
    singular=np.linalg.svd(J,compute_uv=False)
    dq=J.T@np.linalg.solve(J@J.T+lam*lam*np.eye(2),error)
    predicted=J@dq
    metrics=dict(min_singular_value=singular[-1],joint_step_norm_rad=np.linalg.norm(dq),
        predicted_residual_m=np.linalg.norm(error-predicted),
        max_joint_step_rad=np.max(np.abs(dq)))
    derivation=[f'Use pose q1={q1:g}, q2={q2:g} rad and Cartesian request {error.tolist()} m.',
        f'The Jacobian singular values are {singular.tolist()}.',
        f'Choose damping lambda={lam:g} and solve the regularized 2x2 system.',
        f'The joint update is {dq.tolist()} rad.',
        f'Linearized achieved displacement is {predicted.tolist()} m; residual is {np.linalg.norm(error-predicted):.8f} m.']
    notes=['The linearized prediction is only valid for sufficiently small joint updates; recompute nonlinear FK after each iteration.',
           'A larger damping value can improve numerical behavior while deliberately leaving more task error.']
    return metrics,derivation,notes
''',dict(elbow=.03,damping=.01),'damping',[.0001,.001,.005,.01,.03,.1],
'elbow is the relative second-joint angle in radians; damping is the regularization scale in the selected Jacobian units.',
'Inspect singular values before choosing damping. Compare joint-step magnitude and residual together; selecting the smallest residual alone rewards unreasonable motion near singularity.',
'Inverting J directly near rank loss; comparing damping values across differently scaled translation/orientation tasks without unit normalization.',
['Sweep elbow angle toward zero while holding damping fixed.','Cap joint increments and recompute the actual nonlinear displacement.','Add a secondary posture task in the null space of a redundant arm.'],
'Use conservative increment, velocity and collision checks around the numerical solver; hardware compliance changes the achieved endpoint.')

add('support_polygon','Support polygons, center of pressure and load transfer',
'''A support polygon is determined by active contact geometry, not by a drawing of where the feet might be. Contact loads determine the center of pressure, while COM projection provides a static load-feasibility clue under restrictive assumptions. An unloaded foot should not enlarge the support region. This laboratory uses two point contact resultants to show how vertical load redistribution moves COP and how a horizontal COM shift consumes a chosen geometric margin.''',
'COP_x=sum(Fz_i*x_i)/sum(Fz_i); signed margin=min(x-xmin,xmax-x); Fz_i must be nonnegative for unilateral contact.',
r'''
def experiment(p):
    left=p['left_load'];right=1-left;weight=p['mass']*9.81
    assert 0<=left<=1
    positions=np.array([-.1,.1]);forces=weight*np.array([left,right])
    cop=float(forces@positions/forces.sum())
    com=p['com_x'];margin=min(com+.14,.14-com)
    moment=weight*(com-cop)
    metrics=dict(cop_x_m=cop,com_margin_m=margin,left_force_N=forces[0],
                 right_force_N=forces[1],unbalanced_pitch_moment_Nm=moment)
    derivation=[f'Total vertical load is {weight:.6f} N.',
        f'Left fraction {left:g} gives forces {forces.tolist()} N at x=-0.1,+0.1 m.',
        f'The weighted contact location is COP x={cop:.6f} m.',
        f'COM x={com:g} m has signed margin {margin:.6f} m inside the illustrative outer edges.',
        f'The gravity/COP moment difference is {moment:.6f} Nm.']
    notes=[('One contact resultant has zero load; do not treat both point contacts as equally active support.' if min(left,right)==0 else
            'Both contact resultants are compressive in this static illustration.'),
           'The .14 m outer edges are teaching geometry; real support requires measured foot patches and contact state.']
    return metrics,derivation,notes
''',dict(left_load=.5,mass=10.,com_x=.02),'left_load',[0.,.1,.25,.5,.75,1.],
'left_load is the fraction of total vertical load; mass is kilograms; com_x is the COM projection in meters.',
'Compute COP from forces, not masses. The residual pitch moment is a useful sign check but does not model whole-body angular momentum or dynamic ground reaction.',
'Expanding the support hull with unloaded feet; confusing COP and COM; dividing by total contact force near zero.',
['Vary COM x and find the load split needed for zero pitch moment.','Replace point contacts with measured foot corners and compute a convex hull.','Simulate a lifting foot and update the active support set.'],
'Foot contact sensing may require estimation; simulation contact truth must not be silently substituted for unavailable hardware force sensors.')

add('lipm','Linear inverted pendulum prediction and capture-point intuition',
'''The linear inverted pendulum model approximates horizontal COM motion at fixed height above a support plane. Its unstable mode explains why a small COM displacement can grow without corrective contact placement. The capture point combines position and velocity into a location associated with stopping the divergent motion under the model assumptions. It is useful intuition, but variable height, angular momentum, foot limits and impact dynamics can invalidate the simplified prediction.''',
'omega=sqrt(g/h); x_ddot=omega^2*(x-zmp); capture point xi=x+x_dot/omega.',
r'''
def experiment(p):
    h,T=p['height'],p['horizon'];w=np.sqrt(9.81/h)
    x0,v0,zmp=.02,.05,0.
    x=zmp+(x0-zmp)*np.cosh(w*T)+v0/w*np.sinh(w*T)
    v=(x0-zmp)*w*np.sinh(w*T)+v0*np.cosh(w*T)
    capture=x0+v0/w
    metrics=dict(natural_rate_per_s=w,final_com_x_m=x,final_speed_m_s=v,
        initial_capture_point_m=capture,divergent_growth_factor=np.exp(w*T))
    derivation=[f'At height {h:g} m, omega=sqrt(9.81/h)={w:.6f} per second.',
        f'Start at x0={x0:g} m and v0={v0:g} m/s with ZMP zero.',
        f'Over {T:g} s, the hyperbolic solution predicts x={x:.6f} m and v={v:.6f} m/s.',
        f'The initial capture-point coordinate is {capture:.6f} m.',
        f'The divergent mode multiplies by exp(omega*T)={np.exp(w*T):.6f}.']
    notes=['A fixed support point does not recover the displaced state in this open-loop model.',
           'A predicted capture point outside reachable/contact-feasible support is a warning, not an invitation to command an impossible step.']
    return metrics,derivation,notes
''',dict(height=.6,horizon=.3),'height',[.3,.4,.5,.6,.8,1.],
'height is fixed COM height in meters; horizon is seconds; the model assumes a constant planar ZMP.',
'The exact hyperbolic solution avoids confusing integration error with the physical instability of the approximation. Compare the growth factor across heights while keeping initial state fixed.',
'Treating the capture point as a complete gait planner; ignoring available foot motion and contact torque limits.',
['Set initial velocity so the divergent component cancels for a chosen support point.','Compare exact prediction with a numerical integrator.','Add a bounded ZMP choice and test feasibility against support edges.'],
'Validate fixed-height and contact assumptions before using LIPM predictions in an actual humanoid controller.')

add('friction_cone','Friction cones, slip feasibility and contact margins',
'''A contact can push but usually cannot pull, and its tangential force is limited by friction and normal load. This simple inequality couples balance and propulsion: reducing normal load reduces available horizontal force. A friction coefficient is not a universal property independent of surfaces, wear or contamination. This laboratory evaluates a requested horizontal acceleration under a Coulomb-friction approximation and distinguishes feasibility margin from a measured slip guarantee.''',
'||F_t|| <= mu*F_n; F_t_required=m*a; margin=mu*F_n-||F_t_required||.',
r'''
def experiment(p):
    mass,mu,acc=p['mass'],p['mu'],p['acceleration']
    normal=mass*9.81*p['supported_fraction']
    required=mass*acc
    capacity=mu*normal;margin=capacity-abs(required)
    angle=np.arctan(mu)
    utilization=abs(required)/capacity
    metrics=dict(normal_force_N=normal,tangential_required_N=required,
        friction_capacity_N=capacity,force_margin_N=margin,
        utilization=utilization,cone_half_angle_rad=angle)
    derivation=[f'The modeled normal force is {normal:.6f} N.',
        f'Acceleration {acc:g} m/s^2 requires horizontal force {required:.6f} N.',
        f'At mu={mu:g}, Coulomb capacity is {capacity:.6f} N.',
        f'Margin is {margin:.6f} N and utilization is {utilization:.6f}.',
        f'The friction-cone half angle is atan(mu)={angle:.6f} rad.']
    notes=[('The requested force is inside the modeled friction bound.' if margin>=0 else
            'The requested force exceeds the modeled friction capacity; a controller must reduce demand or change support.'),
           'This static feasibility check excludes torsional friction, impact, compliance and changing normal force.']
    return metrics,derivation,notes
''',dict(mass=10.,mu=.6,acceleration=2.,supported_fraction=1.),'mu',[.1,.2,.3,.4,.6,.8],
'mass is kilograms; mu is dimensionless assumed friction; acceleration is m/s^2; supported_fraction scales normal loading.',
'Calculate load before friction capacity and compare force magnitudes. Utilization makes conditions comparable, but remains conditional on the assumed normal force and coefficient.',
'Using visual foot contact as proof of load; making friction arbitrarily large to rescue a bad gait; ignoring unloading during stepping.',
['Reduce normal support fraction while keeping horizontal demand fixed.','Include a lateral acceleration and use the vector norm.','Estimate a conservative friction interval and evaluate worst-case feasibility.'],
'Real foot-ground interaction needs measurement across the intended surfaces and support states; simulation friction tuning is not certification.')
