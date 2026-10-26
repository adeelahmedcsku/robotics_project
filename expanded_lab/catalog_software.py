from catalog import add
add('message_contracts','Typed joint-command contracts and rejection accounting',
'''A valid JSON object is not necessarily a valid robot command. A command contract must constrain joint names and order, vector length, numeric finiteness, units, range, sequence and age. Validation should occur before a command enters the controller's active state. Rejection counters make faults observable without turning malformed requests into motor motion. This experiment defines a small typed-like schema and injects different kinds of failures into a deterministic message stream.''',
'accept = schema_ok and finite and limits_ok and sequence_new and 0<=age<=max_age.',
r'''
def valid(message,now,last_sequence):
    names=['joint_a','joint_b']
    if message.get('names')!=names:return False,'names'
    q=np.asarray(message.get('position',[]),dtype=float)
    if q.shape!=(2,):return False,'shape'
    if not np.isfinite(q).all():return False,'nonfinite'
    if np.any(abs(q)>.5):return False,'range'
    if message['sequence']<=last_sequence:return False,'sequence'
    age=now-message['sent']
    if not 0<=age<=.1:return False,'age'
    return True,'accepted'

def experiment(p):
    rng=np.random.default_rng(47);n=1000;last=-1;counts={}
    corrupt=p['invalid_fraction']
    for i in range(n):
        now=i*.02
        msg=dict(names=['joint_a','joint_b'],position=[.1,-.1],sequence=i,sent=now-.01)
        if rng.random()<corrupt:
            kind=i%4
            if kind==0:msg['names']=['joint_b','joint_a']
            if kind==1:msg['position']=[float('nan'),0.]
            if kind==2:msg['sent']=now-.2
            if kind==3:msg['position']=[2.,0.]
        ok,reason=valid(msg,now,last);counts[reason]=counts.get(reason,0)+1
        if ok:last=i
    accepted=counts.get('accepted',0)
    metrics=dict(accepted_count=accepted,rejected_count=n-accepted,
        rejection_fraction=(n-accepted)/n,last_accepted_sequence=last)
    derivation=[f'Generate {n} commands at 50 Hz with corruption probability {corrupt:g}.',
        'Corrupt name order, numeric finiteness, age or range in alternating injected cases.',
        'Validate the entire candidate before updating last accepted sequence.',
        f'Accepted {accepted} messages; rejected {n-accepted}.',
        f'Rejection reasons are {counts}.']
    notes=['Rejected messages do not update the accepted sequence or active target in this contract example.',
           'A production parser must also handle missing keys, malicious payload sizes, schema versions and transport authentication.']
    return metrics,derivation,notes
''',dict(invalid_fraction=.1),'invalid_fraction',[0.,.01,.05,.1,.25,.5],
'invalid_fraction is the probability of an injected synthetic schema/age/range fault, not a measured network error rate.',
'Validation is side-effect free until success is known. The experiment records rejected categories and accepted sequence progression, illustrating observability around a strict boundary.',
'Coercing missing targets to zero; partially applying a vector before all fields pass; accepting reordered names because lengths match.',
['Add explicit schema version and unit fields.','Test duplicate and out-of-order sequences.','Apply an input-size limit before allocating a vector.'],
'Physical command validation must use the commissioned joint/motor mapping and remain subordinate to local watchdogs and isolation.')

add('queue_age','Message queues, delivery policy and stale-command risk',
'''A reliable queue can preserve every message while delivering commands too late to be useful. A latest-value stream favors freshness but intentionally discards intermediate samples. Those are different tradeoffs for telemetry, trajectories and events. This experiment simulates a producer faster than its consumer and compares FIFO delivery with replacing pending state by the newest sample. It illustrates queue-age behavior without pretending to implement all DDS QoS semantics.''',
'age_at_use = consumer_time - production_time; FIFO preserves history; latest-value keeps at most one pending state.',
r'''
def experiment(p):
    producer_dt=.01;consumer_dt=p['consumer_period']
    production=np.arange(0,5,producer_dt)
    consumption=np.arange(0,5,consumer_dt)
    fifo=[];latest=[];queue=[];index=0;dropped=0
    for now in consumption:
        arrivals=[]
        while index<len(production) and production[index]<=now+1e-12:
            arrivals.append(production[index]);index+=1
        queue.extend(arrivals)
        if queue:fifo.append(now-queue.pop(0))
        available=production[production<=now+1e-12]
        if len(available):latest.append(now-available[-1])
        dropped+=max(0,len(arrivals)-1)
    metrics=dict(fifo_mean_age_s=np.mean(fifo),fifo_max_age_s=np.max(fifo),
        latest_mean_age_s=np.mean(latest),latest_max_age_s=np.max(latest),
        fifo_backlog_count=len(queue),replaced_arrivals_count=dropped)
    derivation=[f'The producer emits state every {producer_dt:g} s.',
        f'The consumer processes one item every {consumer_dt:g} s.',
        f'FIFO retains {len(queue)} pending messages after the five-second run.',
        f'FIFO maximum age is {np.max(fifo):.6f} s; latest-value maximum age is {np.max(latest):.6f} s.',
        f'Latest-value replacement intentionally skips at least {dropped} intermediate arrivals in this schedule.']
    notes=['A trajectory is not always replaceable by its last point; choose semantics appropriate to the command type.',
           'The simulation concerns queue policy only and does not reproduce packet loss, DDS discovery or actual ROS middleware timing.']
    return metrics,derivation,notes
''',dict(consumer_period=.02),'consumer_period',[.005,.01,.015,.02,.05,.1],
'consumer_period is seconds; producer period is fixed at 10 ms and experiment duration is five seconds.',
'Compute age at consumption, not at arrival. The FIFO backlog exposes overload that can be hidden by successful delivery acknowledgments.',
'Choosing reliable delivery as a substitute for deadlines; using deep queues for current-state commands; dropping events that require ordered processing.',
['Add a bounded FIFO depth and count dropped old messages.','Reject messages older than a declared deadline.','Model a buffered trajectory separately from a replaceable velocity target.'],
'ROS QoS configuration must be paired with application-level age checks and control-specific command semantics.')

add('lifecycle','Lifecycle activation, preconditions and fault latching',
'''A robot process should not become motion-capable merely because it started. Configuration, inactive readiness, active control, fault handling and shutdown are distinct states. A fault should normally require a deliberate recovery path rather than disappear when a healthy packet arrives. This laboratory implements a small supervisor state machine and injects failed preconditions, making activation authority explicit and testable.''',
'configure: unconfigured->inactive; activate requires all readiness flags; fault: active->fault; recovery never directly resumes active motion.',
r'''
def transition(state,event,ready):
    if event=='shutdown':return 'finalized'
    if event=='fault' and state=='active':return 'fault'
    if state=='unconfigured' and event=='configure':return 'inactive'
    if state=='inactive' and event=='activate' and all(ready.values()):return 'active'
    if state=='active' and event=='deactivate':return 'inactive'
    if state=='fault' and event=='reset':return 'inactive'
    return state

def experiment(p):
    rng=np.random.default_rng(53);trials=200;activations=0;blocked=0
    faults=0;unsafe_resume=0
    for _ in range(trials):
        ready={k:rng.random()>=p['failed_readiness_probability']
               for k in ['calibration','limits','feedback','support']}
        state=transition('unconfigured','configure',ready)
        state=transition(state,'activate',ready)
        if state=='active':
            activations+=1;state=transition(state,'fault',ready);faults+=1
            state=transition(state,'healthy_packet',ready)
            unsafe_resume+=state=='active'
        else:blocked+=1
    assert unsafe_resume==0
    metrics=dict(activation_count=activations,blocked_count=blocked,
        fault_count=faults,automatic_resume_count=unsafe_resume,
        activation_fraction=activations/trials)
    derivation=[f'Run {trials} readiness trials with per-flag failure probability {p["failed_readiness_probability"]:g}.',
        'Configuration moves the supervisor to inactive; activation checks all four readiness flags.',
        f'Activate {activations} trials and block {blocked}.',
        f'Inject a fault into every active trial, then deliver a healthy packet.',
        f'Automatic active resumption count is {unsafe_resume}; the assertion requires zero.']
    notes=['Readiness flags represent evidence that must exist outside this synthetic state machine.',
           'A reset returns to inactive; a new reviewed activation is required before motion can resume.']
    return metrics,derivation,notes
''',dict(failed_readiness_probability=.1),'failed_readiness_probability',[0.,.01,.05,.1,.2,.5],
'failed_readiness_probability controls independent simulated readiness flags; it is not an estimated physical reliability rate.',
'Keep transition logic separate from side effects such as enabling a drive. Test forbidden transitions as carefully as the happy path.',
'Treating ROS node startup as hardware readiness; clearing a latched fault on fresh data; assuming a software state verifies physical isolation.',
['Add explicit evidence IDs to each readiness flag.','Enumerate every state/event pair and test allowed transitions.','Model emergency isolation separately from software inactive state.'],
'Commissioning records, local embedded protection and independent stop behavior must support the activation decision.')

add('timing_schedule','Multi-rate controllers, policy decimation and sample age',
'''Robotics stacks use several update rates. Fast actuator feedback, slower policy inference and still slower telemetry can coexist if their interfaces specify sample-and-hold behavior and allowed age. Confusing a decimated display rate with the feedback rate can degrade control silently. This laboratory schedules deterministic physics, control, policy and logging events from one integer tick counter, avoiding floating-point modulo tests on accumulated time.''',
'event at tick k when k mod decimation=0; period=base_dt*decimation; held-action age=(k-last_policy_tick)*base_dt.',
r'''
def experiment(p):
    dt=.001;n=5000;decimation=int(p['policy_decimation'])
    last_policy=0;ages=[];counts=dict(physics=0,control=0,policy=0,telemetry=0)
    for tick in range(n):
        counts['physics']+=1
        if tick%2==0:counts['control']+=1
        if tick%decimation==0:
            last_policy=tick;counts['policy']+=1
        if tick%100==0:counts['telemetry']+=1
        ages.append((tick-last_policy)*dt)
    metrics=dict(policy_rate_Hz=1/(dt*decimation),
        maximum_held_action_age_s=max(ages),mean_held_action_age_s=np.mean(ages),
        control_updates=counts['control'],policy_updates=counts['policy'],
        telemetry_updates=counts['telemetry'])
    derivation=[f'Use {n} base ticks at {dt:g} s per tick.',
        f'Control runs every two ticks; policy runs every {decimation} ticks; telemetry every 100.',
        f'The policy rate is {1/(dt*decimation):.6f} Hz.',
        f'The oldest held policy action reaches {max(ages):.6f} s before replacement.',
        f'Event counts are {counts}.']
    notes=['This schedule is logical simulation time and assumes every computation completes before its deadline.',
           'Wall-time execution still needs measured compute/transport budgets and an overrun response.']
    return metrics,derivation,notes
''',dict(policy_decimation=20),'policy_decimation',[2,5,10,20,50,100],
'policy_decimation is an integer base-tick count; base step is 1 ms, control step 2 ms and telemetry step 100 ms.',
'Integer scheduling makes rate relationships reproducible. Track action age explicitly so the consumer can enforce a contract even when the producer rate changes.',
'Using accumulated float time modulo a period; assuming nominal loop rates equal measured wall rates; forgetting action holds during missed inference.',
['Add an inference-overrun event and specify the held-action timeout.','Reschedule a 60 Hz camera on a 1 kHz tick using a fractional accumulator.','Record every producer/consumer sample age in a replay trace.'],
'The physical controller must distinguish simulation clock, device sample clock and monotonic deadline clock.')

add('can_budget','CAN bandwidth screening without invented motor commands',
'''A communication link has finite capacity, and payload bits are not the entire frame cost. Arbitration, framing, acknowledgment, inter-frame spacing, bit stuffing and retransmission consume time. This laboratory uses an explicit assumed worst-case frame length to screen a bus budget. It does not define motor packet semantics or resolve the Asimov bus assignment. The purpose is to reject implausible update-rate plans before implementing a transport.''',
'bus utilization = joints*frames_per_joint_per_cycle*cycle_rate*assumed_frame_bits/bitrate.',
r'''
def experiment(p):
    joints=int(p['joints']);rate=p['cycle_rate'];bits=p['frame_bits'];baud=p['bitrate']
    frames=joints*p['frames_per_joint']*rate
    demand=frames*bits;utilization=demand/baud
    frame_time=bits/baud
    cycle_wire=joints*p['frames_per_joint']*frame_time
    metrics=dict(frames_per_second=frames,required_bits_per_second=demand,
        utilization_fraction=utilization,one_frame_wire_time_us=frame_time*1e6,
        minimum_cycle_wire_time_ms=cycle_wire*1000)
    derivation=[f'Plan {joints} joints at {rate:g} cycles/s with {p["frames_per_joint"]:g} frames per joint per cycle.',
        f'Frame demand is {frames:.6f} per second.',
        f'Assume {bits:g} total wire bits per frame at {baud:g} bit/s.',
        f'Required wire throughput is {demand:.6f} bit/s and utilization is {utilization:.6f}.',
        f'The minimum cycle wire time is {cycle_wire*1000:.6f} ms before additional contention or error handling.']
    notes=[('The budget exceeds nominal bus capacity and is infeasible under these assumptions.' if utilization>1 else
            'Nominal capacity is not exceeded, but margin and worst-case latency still need analysis.'),
           'The assumed frame length is a teaching budget input; confirm the actual bus generation, protocol and traffic pattern.']
    return metrics,derivation,notes
''',dict(joints=6,cycle_rate=500.,frame_bits=135.,bitrate=1000000.,frames_per_joint=2.),'cycle_rate',[50.,100.,200.,300.,500.,1000.],
'joints is actuator count on one hypothetical segment; frame_bits is an explicit total-wire-length assumption; bitrate is bits/s.',
'Start from traffic semantics: one command plus one response gives a different budget from broadcast commands and asynchronous telemetry. Treat utilization above one as a mathematical impossibility, not a tuning issue.',
'Counting only the eight-byte payload; ignoring response traffic and retransmissions; assuming all published interfaces share one bus.',
['Allocate traffic across two confirmed independent buses and compare.','Add periodic diagnostic frames and reserved fault traffic.','Analyze worst-case response age under arbitration priorities.'],
'Obtain the exact actuator protocol and release-specific Asimov bus mapping before choosing bitrates or connecting a populated bus.')

add('packet_codec','A synthetic packet codec and corruption tests',
'''Binary protocols need an explicit wire contract: field order, byte order, numeric representation, version, length and integrity checks. A successful unpack operation does not prove the values are safe. This laboratory defines a fictional teaching packet carrying one target and sequence number, then corrupts random bytes to test CRC-based rejection. It is deliberately incompatible with real actuators and must never be transmitted to them.''',
'packet = magic + version + sequence + float target + CRC16(payload); validate length, magic, CRC, finiteness and range.',
r'''
import struct

def crc16(data):
    crc=0xffff
    for byte in data:
        crc^=byte<<8
        for _ in range(8):
            crc=((crc<<1)^0x1021)&0xffff if crc&0x8000 else (crc<<1)&0xffff
    return crc

def encode(sequence,target):
    payload=struct.pack('<2sBIf',b'ED',1,sequence,target)
    return payload+struct.pack('<H',crc16(payload))

def decode(packet):
    if len(packet)!=13:raise ValueError('length')
    payload,check=packet[:-2],struct.unpack('<H',packet[-2:])[0]
    if crc16(payload)!=check:raise ValueError('crc')
    magic,version,sequence,target=struct.unpack('<2sBIf',payload)
    if magic!=b'ED' or version!=1:raise ValueError('schema')
    if not np.isfinite(target) or abs(target)>.5:raise ValueError('target')
    return sequence,target

def experiment(p):
    rng=np.random.default_rng(59);rejected=0;n=500
    target=p['target'];base=encode(7,target)
    seq,recovered=decode(base)
    for _ in range(n):
        damaged=bytearray(base);index=int(rng.integers(0,len(base)))
        damaged[index]^=1<<int(rng.integers(0,8))
        try:decode(damaged)
        except ValueError:rejected+=1
    assert seq==7 and rejected==n
    metrics=dict(packet_bytes=len(base),target_roundtrip_error_rad=abs(recovered-target),
        single_bit_faults_rejected=rejected,rejection_fraction=rejected/n)
    derivation=[f'Encode sequence 7 and target {target:g} rad with explicit little-endian fields.',
        f'The complete fictional packet occupies {len(base)} bytes.',
        f'Float32 round-trip error is {abs(recovered-target):.9e} rad.',
        f'Inject {n} random single-bit corruptions across payload and checksum.',
        f'Reject {rejected} corrupted packets; no physical transport exists.']
    notes=['CRC detects accidental corruption; it is not authentication or a defense against a deliberate sender.',
           'This CRC and packet layout are teaching choices, not the CAN wire format or Asimov motor protocol.']
    return metrics,derivation,notes
''',dict(target=.1),'target',[-.4,-.1,0.,.1,.25,.4],
 'target is a fictional joint angle in radians; sequence, magic, version and CRC format are fixed by this exercise only.',
 'Separate codec integrity from application validity. Length and CRC are checked before interpreting fields; numerical range and schema checks occur after unpacking.',
 'Assuming a checksum authenticates a sender; relying on native byte order; sending an educational packet to real hardware.',
 ['Add a unit field and reject a mismatched unit.','Test truncated, appended and invalid-version packets.','Design replay protection independently of CRC.'],
 'Implement real motor encoding only from confirmed manufacturer protocol documentation, with inhibited-output tests and reviewed configuration.')

add('observation_schema','Observation ordering, normalization and schema hashes',
'''A learned policy sees an ordered vector, not a collection of semantically labeled Python variables. Reordering two fields can produce plausible finite numbers and completely wrong actions. Normalization is also part of the policy interface and must be frozen for deployment. A schema hash can identify the ordered names and units, but only if the entire preprocessing contract is included. This laboratory demonstrates a silent ordering error and validates a canonical schema representation.''',
'z_i=(x_i-mean_i)/std_i; policy_input order is part of the model; hash=SHA256(canonical schema bytes).',
r'''
import hashlib
import json

def experiment(p):
    raw=np.array([.2,-.1,.5]);mean=np.array([0.,0.,.1]);std=np.array([.5,.5,.2])
    names=['elbow_rad','knee_rad','gyro_rad_s']
    normalized=(raw-mean)/std
    weights=np.array([.4,-.2,.1])
    baseline=float(weights@normalized)
    shifted=raw.copy();shifted[2]+=p['gyro_offset']
    correct=float(weights@((shifted-mean)/std))
    wrong=float(weights@((shifted[[2,1,0]]-mean)/std))
    schema=dict(names=names,mean=mean.tolist(),std=std.tolist(),dtype='float32')
    encoded=json.dumps(schema,sort_keys=True,separators=(',',':')).encode()
    digest=hashlib.sha256(encoded).hexdigest()
    metrics=dict(reference_action=baseline,correct_action=correct,
        reordered_action=wrong,reordering_action_error=abs(correct-wrong),
        normalized_gyro=(shifted[2]-mean[2])/std[2])
    derivation=[f'Ordered fields are {names}.',
        f'Means are {mean.tolist()} and standard deviations are {std.tolist()}.',
        f'Apply gyro offset {p["gyro_offset"]:g} rad/s and normalize in the declared order.',
        f'Correct action is {correct:.6f}; a silent field swap produces {wrong:.6f}.',
        f'Canonical schema SHA256 is {digest}.']
    notes=['A schema hash detects version mismatch only when both producer and consumer actually enforce it.',
           'Include clipping, frame conventions, history stacking and action scaling in a real deployment contract.']
    return metrics,derivation,notes
''',dict(gyro_offset=0.),'gyro_offset',[-.2,-.1,0.,.1,.2,.5],
'gyro_offset is an added angular-rate offset in rad/s; all normalized fields follow the explicitly named ordered schema.',
'The reference linear actor is deliberately simple so the action difference can be traced exactly to preprocessing. Canonical serialization avoids hashes changing with dictionary formatting alone.',
'Hashing unordered names without normalization; updating running statistics during evaluation; interpreting finite actions as evidence of correct semantics.',
['Add action scales and clipping to the schema hash.','Create a migration test for an added observation field.','Compare batched and single-observation preprocessing.'],
'Hardware estimators must supply the same units, frames, order, timing and normalization used in policy training.')

add('replay','Offline replay, action parity and fault localization',
'''Replay separates policy inference from the physical plant so interface changes can be investigated without motion. A useful replay artifact includes ordered observations, timestamps, policy version, preprocessing state and expected actions. Comparing only a single zero input misses errors that appear in the operating distribution. This experiment uses a deterministic nonlinear actor and injects a preprocessing scale mismatch, then reports action disagreement over a dataset rather than one sample.''',
'action=tanh(W*observation+b); parity metrics include maximum absolute error, RMSE and threshold-exceedance fraction.',
r'''
def experiment(p):
    rng=np.random.default_rng(61);obs=rng.normal(0,1,(1000,4))
    W=np.array([[.2,-.1,.3,.4],[-.3,.2,.1,-.2]])
    bias=np.array([.05,-.02])
    reference=np.tanh(obs@W.T+bias)
    migrated=obs.copy();migrated[:,2]*=p['scale_error_factor']
    candidate=np.tanh(migrated@W.T+bias)
    difference=candidate-reference
    per_sample=np.max(abs(difference),axis=1)
    metrics=dict(action_rmse=np.sqrt(np.mean(difference**2)),
        maximum_absolute_action_error=np.max(abs(difference)),
        mismatch_fraction=np.mean(per_sample>1e-5),
        mean_action_magnitude=np.mean(abs(reference)))
    derivation=['Generate 1000 four-dimensional observations from a fixed seeded distribution.',
        f'The candidate preprocessing multiplies field 2 by {p["scale_error_factor"]:g}.',
        'Run the same tanh actor for reference and candidate pipelines.',
        f'Action RMSE is {metrics["action_rmse"]:.8f}; maximum disagreement is {metrics["maximum_absolute_action_error"]:.8f}.',
        f'Fraction exceeding 1e-5 action error is {metrics["mismatch_fraction"]:.6f}.']
    notes=['The replay distribution is synthetic; physical logs and edge cases must be included before deployment.',
           'Exact inference parity does not validate the policy behavior or the physical actuator mapping.']
    return metrics,derivation,notes
''',dict(scale_error_factor=1.),'scale_error_factor',[.5,.9,.99,1.,1.01,1.1],
'scale_error_factor multiplies one candidate observation channel; one is the intentionally matching baseline.',
'Keep the actor identical while changing only preprocessing. Dataset-level metrics locate the regression before any controller or hardware backend is involved.',
'Testing only zero observations; comparing unclipped exported actions with clipped framework outputs; using unrelated normalization checkpoints.',
['Add timestamp-based observation history and replay it exactly.','Compare float32 and float64 inference tolerances.','Inject a joint-name permutation and identify the affected action channels.'],
'Replay is a required intermediate step, but still must be followed by inhibited-output and supported physical validation.')

add('telemetry_buffer','Ring buffers, bounded memory and time-window diagnostics',
'''Long-running robot processes cannot retain every high-rate sample in an unbounded Python list. A ring buffer bounds memory by overwriting old data, but that choice defines the available diagnostic horizon. Logging and visualization should consume copied snapshots without blocking the control loop. This laboratory implements a fixed-size numerical buffer and verifies wraparound, chronology and horizon as capacity changes.''',
'write_index=total_samples mod capacity; chronological snapshot starts at the oldest retained index after wrap.',
r'''
def experiment(p):
    capacity=int(p['capacity']);rate=500;n=5000
    buffer=np.zeros((capacity,3));count=0
    for i in range(n):
        t=i/rate;buffer[count%capacity]=[t,np.sin(t),np.cos(t)];count+=1
    retained=min(count,capacity)
    if count<=capacity:snapshot=buffer[:retained].copy()
    else:
        start=count%capacity
        snapshot=np.concatenate([buffer[start:],buffer[:start]]).copy()
    assert np.all(np.diff(snapshot[:,0])>0)
    expected_last=(n-1)/rate
    assert np.isclose(snapshot[-1,0],expected_last)
    horizon=snapshot[-1,0]-snapshot[0,0]
    metrics=dict(retained_samples=retained,horizon_s=horizon,
        allocated_bytes=buffer.nbytes,oldest_timestamp_s=snapshot[0,0],
        latest_timestamp_s=snapshot[-1,0])
    derivation=[f'Write {n} samples at {rate} Hz into capacity {capacity}.',
        f'The allocated numerical storage is {buffer.nbytes} bytes.',
        f'After wrapping, retain {retained} most recent samples.',
        f'Chronological snapshot runs from {snapshot[0,0]:.6f} to {snapshot[-1,0]:.6f} s.',
        f'The retained diagnostic horizon is {horizon:.6f} s.']
    notes=['Memory accounting covers the array payload, not interpreter, transport or rendering overhead.',
           'The example is single-threaded; concurrent producers/consumers require a reviewed synchronization or lock-free design.']
    return metrics,derivation,notes
''',dict(capacity=1000),'capacity',[100,250,500,1000,2000,5000],
'capacity is samples; three float64 columns store timestamp and two diagnostic signals at 500 Hz.',
'The wrap index and chronological view are separate concerns. Copying the returned snapshot prevents a plot from reading values while the producer overwrites them.',
'Unbounded logging in a control process; plotting mutable array views; assuming bounded storage guarantees nonblocking disk writes.',
['Add a consumer that decimates by timestamp rather than index.','Define a disk-writer queue with a bounded drop policy.','Measure control-loop impact of snapshot copies.'],
'Telemetry transport and rendering must remain outside the timing-critical actuator path and expose dropped-sample counts.')

add('fault_supervisor','Fault persistence, debounce and explicit re-arming',
'''A single transient threshold crossing may be noise, while a persistent violation may require a stop. Debounce trades false alarms against detection delay. After a real fault is latched, a return to normal measurements should not automatically re-enable motion. This laboratory injects both short spikes and a sustained thermal-like violation, then measures detection latency under different debounce durations. It distinguishes detection policy from the physical action that a real supervisor must execute.''',
'consecutive_bad+=1 while violation; latch when consecutive_bad>=N; latched state persists until an explicit validated reset.',
r'''
def experiment(p):
    dt=.01;t=np.arange(0,5,dt);signal=np.ones(len(t))*30.
    signal[50]=90.;signal[100:102]=90.;signal[t>=3]=90.
    required=max(1,round(p['debounce_seconds']/dt))
    count=0;latched=False;first=None;false_before=0
    for i,value in enumerate(signal):
        count=count+1 if value>70 else 0
        if count>=required and not latched:
            latched=True;first=t[i]
            false_before+=t[i]<3
    latency=-1. if first is None else first-3.
    metrics=dict(required_bad_samples=required,first_latch_time_s=-1 if first is None else first,
        detection_latency_from_sustained_fault_s=latency,
        false_latch_before_fault=false_before,latched_final=float(latched))
    derivation=[f'At 100 Hz, debounce duration {p["debounce_seconds"]:g} s becomes {required} consecutive samples.',
        'Inject a one-sample spike at 0.5 s and a two-sample spike at 1 s.',
        'At 3 s, begin a sustained threshold violation.',
        f'First latched fault occurs at {first} s; early false-latch count is {false_before}.',
        f'Relative to sustained-fault onset, reported latency is {latency:.6f} s; a negative value means an earlier spike already latched.']
    notes=['The temperature values and threshold are synthetic and do not specify a physical motor limit.',
           'Detection delay must be included in the reviewed response envelope; debouncing every fault category identically is inappropriate.']
    return metrics,derivation,notes
''',dict(debounce_seconds=.05),'debounce_seconds',[.01,.02,.03,.05,.1,.2],
'debounce_seconds is the required persistence duration at a fixed 10 ms measurement interval.',
'The fault latch changes only once, while the persistence counter can reset on healthy measurements. Early spikes deliberately expose the difference between nuisance rejection and delayed true detection.',
'Automatically clearing a fault on healthy data; debouncing an emergency input without design justification; ignoring total reaction travel during debounce.',
['Use different policies for stale feedback, overcurrent and thermal drift.','Add an explicit inactive reset state and prohibit direct active resumption.','Log the first triggering sample and pre-fault buffer.'],
'Physical fault responses depend on load support, stored energy and independent isolation; this numerical detector is not the protective system.')
