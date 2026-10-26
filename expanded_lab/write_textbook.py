"""Build the worked-laboratory manuscript from executed numerical cases."""
from pathlib import Path
import json
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from catalog import load_catalog,evaluate

ROOT=Path('/data/Robotics_Project')
SOURCES=ROOT/'textbook_source';MODULES=ROOT/'expanded_lab/modules'
MODULES.mkdir(exist_ok=True)
SPECS=load_catalog()
GROUPS=[
('10_mathematics.md','Part VI - Mathematical foundations in depth',
'''The following ten laboratories develop the language used by every later robot component: units, vectors, rotations, transforms, derivatives, fitting, numerical integration, uncertainty and sampling. Work through the derivations before running the code. A number should carry its unit and frame all the way from a sensor through an algorithm into a log. The examples are intentionally small enough to calculate by hand and large enough to expose errors that disappear in a trivial zero-pose test.'''),
('20_mechanics.md','Part VII - Mechanics, kinematics and contact',
'''A geometric model becomes an engineering model only when its mass, inertia, load paths and contact assumptions are explicit. These laboratories move from mass aggregation through rotation and transmission effects to inverse kinematics and support feasibility. They use simple idealized bodies to isolate one phenomenon at a time. The complete humanoid model combines these phenomena; its apparent complexity is a reason to validate each component relationship first, not a reason to skip the equations.'''),
('30_feedback.md','Part VIII - Feedback, trajectories and actuator constraints',
'''A command generator, feedback law and actuator are different components. A smooth trajectory can exceed torque authority; a stable ideal controller can become unstable with delay; a motor that meets a peak load can overheat over repeated cycles. The laboratories below keep these boundaries explicit and measure the tradeoffs. Treat every numerical value as an exercise input until it has been replaced by an identified or verified physical parameter.'''),
('40_estimation.md','Part IX - Sensors, geometry and state estimation',
'''State estimation is a disciplined explanation of what noisy, delayed measurements say about the robot. It requires units, coordinate frames, clock models and validity conditions. These laboratories make quantization, bias, acceleration contamination, measurement dropout, calibration geometry and slipping-contact assumptions visible. Each estimator is compared with known synthetic truth, allowing a precise diagnosis before the same method is tested against physical reference measurements.'''),
('50_interfaces.md','Part X - Software interfaces, timing and supervisory control',
'''Your software-engineering experience is directly useful here, but physical control gives ordinary interface bugs greater consequences. Message ordering, queue age, activation state, packet interpretation and preprocessing versions must be explicit. These laboratories test contracts with deliberate faults and expose the limits of software-only evidence. The fictional wire format is never a motor protocol; no chapter opens a CAN bus or enables a physical actuator.'''),
('60_learning.md','Part XI - Learning algorithms, evaluation and embodied skills',
'''Before training a difficult humanoid behavior, verify the mathematics of rewards, returns, policy updates, action processing and evaluation. Small deterministic examples are faster to diagnose than a million-step rollout. The learning laboratories connect algorithmic definitions with the deployed observation/action interface, then connect perception evidence to an allowlisted skill. A reward curve, detector confidence or successful API call cannot substitute for measured task completion.'''),
('70_engineering.md','Part XII - Physical engineering, evidence and integration',
'''These laboratories develop procurement arithmetic, fit variation, load screening, electrical energy reasoning, bidirectional calibration and evidence management. Their values are fictional teaching inputs unless the earlier source register explicitly identifies a verified fact. They support better questions and better experiments; they do not approve a fabricated structure, power system or complete robot. The final synthetic capstone integrates the same authority boundaries used by the practical Asimov simulation.''')]

UNITS={'dt':'seconds','duration':'seconds','ratio':'dimensionless motor/output ratio',
 'rpm':'motor revolutions per minute','motor_torque':'Nm','efficiency':'fraction',
 'length':'meters','force':'Newtons','angle_deg':'degrees','offset':'meters',
 'epsilon':'radian perturbation','noise':'measurement standard deviation',
 'samples':'count','span':'radians','decay_rate':'inverse seconds',
 'rate':'rad/s','seed':'integer random seed','angle_noise':'radians',
 'sample_rate':'Hertz','signal_frequency':'Hertz','payload_mass':'kilograms',
 'payload_x':'meters','mass':'kilograms','acceleration':'SI acceleration in the chapter equation',
 'speed':'angular speed in the chapter equation','inertia':'kg*m^2','kp':'Nm/rad','kd':'Nm*s/rad',
 'torque_cap':'Nm','excursion':'radians','delay':'seconds','deceleration':'rad/s^2',
 'loss_power':'Watts','thermal_resistance':'K/W','thermal_capacity':'J/K'}

def value(x):
    x=float(x)
    if x==0:return '0'
    if abs(x)>=100000 or abs(x)<.00001:return f'{x:.7e}'
    return f'{x:.8f}'.rstrip('0').rstrip('.')

def metric_label(key):return key.replace('_',' ')
def paragraph(text):return ' '.join(textwrap.dedent(text).strip().split())

def module_text(spec):
    return ('"""'+spec['title']+'. Numerical teaching experiment only."""\n'
        'import math\nimport json\nimport argparse\nimport numpy as np\n\n'+spec['source']+
        '\nif __name__ == "__main__":\n'
        '    parser = argparse.ArgumentParser()\n'
        '    parser.add_argument("--case", type=int, default=0, choices=range(6))\n'
        '    args = parser.parse_args()\n'
        f'    parameters = {spec["params"]!r}\n'
        f'    parameters[{spec["vary"]!r}] = {spec["values"]!r}[args.case]\n'
        '    metrics, derivation, notes = experiment(parameters)\n'
        '    result = dict(parameters=parameters,\n'
        '                  metrics={k: float(v) for k, v in metrics.items()},\n'
        '                  derivation=derivation, notes=notes)\n'
        '    print(json.dumps(result, indent=2))\n')

all_results=[];word_counts={}
for group_index,(filename,title,intro) in enumerate(GROUPS):
    chapters=SPECS[group_index*10:(group_index+1)*10]
    text=[f'# {title}',intro]
    for local,spec in enumerate(chapters):
        index=group_index*10+local+1
        module=MODULES/f'{index:02d}_{spec["key"]}.py'
        module.write_text(module_text(spec))
        cases=[]
        for case_index,sweep in enumerate(spec['values']):
            params=dict(spec['params']);params[spec['vary']]=sweep
            result=evaluate(spec,params)
            cases.append(dict(case=case_index,parameters=params,**result))
        all_results.append(dict(chapter=index,key=spec['key'],cases=cases))
        outfile=ROOT/f'expanded_lab/results/{index:02d}_{spec["key"]}.json'
        outfile.write_text(json.dumps(cases,indent=2))
        selected_metric=list(cases[0]['metrics'])[0]
        x=np.array(spec['values'],float)
        y=np.array([case['metrics'][selected_metric] for case in cases])
        fig,ax=plt.subplots(figsize=(6.5,3.4))
        ax.plot(x,y,'o-',color='#007e87',lw=1.8)
        ax.set_xlabel(spec['vary'].replace('_',' '))
        ax.set_ylabel(metric_label(selected_metric))
        ax.set_title(f'Laboratory {index}: controlled parameter study',fontsize=10)
        ax.grid(alpha=.25);fig.tight_layout()
        figure=ROOT/f'expanded_lab/results/{index:02d}_{spec["key"]}.png'
        fig.savefig(figure,dpi=160);plt.close(fig)
        first_sentence,_,rest=paragraph(spec['concept']).partition('. ')
        text += [f'## Laboratory {index} - {spec["title"]}',
            '### A. The engineering question',first_sentence+'.',
            '### B. Concepts and mathematical model',rest,
            spec['equation'],
            '### C. Real-world meaning and limits',spec['physical'],
            '### D. Architecture and data flow',
            f'Configuration ({", ".join(spec["params"])}) -> numerical model -> '
            f'{", ".join(list(cases[0]["metrics"])[:3])} -> assertions and experiment record.',
            '### E. Prerequisites and parameter contract',
            'Use the Python environment from Lesson 0. This laboratory needs NumPy and the standard library; '
            'it has no simulator, ROS or physical-transport dependency. The complete module is printed below '
            'and saved at the specified path. A fixed seed is part of the experiment where randomness is present.',
            spec['parameter_notes'],
            '| Parameter | Nominal value | Interpretation |','|---|---|---|']
        for key,v in spec['params'].items():
            text.append(f'| {key} | {value(v)} | {UNITS.get(key,"Defined by the explicit chapter model and parameter contract")} |')
        text += ['### F. Implementation and experiment protocol',
            f'1. Read the model equation and identify which assumptions separate it from the physical robot.',
            f'2. Open {module} and locate the experiment function before running it.',
            f'3. Run case 0, then case 3 and case 5. Only {spec["vary"]} changes in the published study.',
            '4. Predict the direction of change in the first metric before comparing with the worked solutions.',
            '5. Re-run the complete six-case study and preserve results with the source and environment identity.',
            '```bash',
            'cd /data/Robotics_Project',
            f'.venv-book/bin/python expanded_lab/modules/{module.name} --case 0',
            f'.venv-book/bin/python expanded_lab/modules/{module.name} --case 3',
            f'.venv-book/bin/python expanded_lab/run.py {spec["key"]} --case 5',
            '```',
            'The supplied .venv-book was used to prepare the numerical results. On another machine, use your '
            'own Lesson 0 environment instead of assuming that directory has been copied or is portable.',
            '### G. Complete executable implementation',
            f'!code {module.relative_to(ROOT)}',
            '### H. Walkthrough and design decisions',spec['walkthrough'],
            '### I. Expected behavior and six worked cases',
            f'The controlled variable is {spec["vary"]}. All other parameters stay at their declared nominal values. '
            'The following graph and table summarize the executed cases. Values are computed, not hand-entered estimates. '
            'Read the derivation for each case to distinguish a useful result from a numerically valid but physically inapplicable one.',
            f'!image {figure.relative_to(ROOT)}',
            f'Figure L{index}. {metric_label(selected_metric)} as {spec["vary"]} changes. '
            'Axes use the quantities and units defined in this laboratory, not undocumented hardware ratings.',
            f'| Case | {spec["vary"]} | {metric_label(selected_metric)} |',
            '|---|---|---|']
        for case in cases:
            text.append(f'| {case["case"]} | {value(case["parameters"][spec["vary"]])} | {value(case["metrics"][selected_metric])} |')
        for case in cases:
            v=case['parameters'][spec['vary']]
            text += [f'#### Worked case {case["case"]}: {spec["vary"]} = {value(v)}',
                f'This case keeps the nominal configuration except for {spec["vary"]}={value(v)}. '
                f'The full input is {json.dumps(case["parameters"],sort_keys=True)}. '
                'Follow the calculation in order, then compare all reported quantities rather than selecting one favorable metric.',
                '| Computed quantity | Numerical result |','|---|---|']
            for key,number in case['metrics'].items():
                text.append(f'| {metric_label(key)} | {value(number)} |')
            for j,line in enumerate(case['derivation'],1):text.append(f'{j}. {line}')
            # Include the result-dependent interpretation, but omit unchanged boilerplate notes.
            base_notes=cases[0]['notes']
            distinct=[note for note in case['notes'] if note not in base_notes]
            if distinct:text.extend(distinct)
        text += ['### J. Validation and independent reasoning',
            'All six published configurations were executed with finite numerical results. '
            'Assertions in the module check the stated identities or state-machine invariants where applicable. '
            'Finiteness is only a basic execution check; the independent reasoning below is the substantive part of validation.',
            *cases[0]['notes'],
            '### K. Failure modes and troubleshooting',spec['pitfalls'],
            '### L. Practical exercises and extension tasks']
        for j,exercise in enumerate(spec['exercises'],1):text.append(f'{j}. {exercise}')
        text += ['### M. Connection to the Asimov research platform',spec['physical'],
            '### N. Completion record',
            f'Record your chosen case, predicted trend, measured {selected_metric}, '
            'the largest discrepancy from the worked result, and the explanation for that discrepancy. '
            'Preserve the code revision, environment identity and raw JSON. For a hardware connection, '
            'name the measurement or verified document that would replace each teaching assumption before use.',
            '### O. Next laboratory connection']
        if index<len(SPECS):
            text.append(f'Continue with Laboratory {index+1}, {SPECS[index]["title"]}. '
                'Keep the present result as a reference fixture for diagnosing changes in the larger stack.')
        else:
            text.append('Return to the supported Asimov perception-to-gesture project with the quantitative checks from these laboratories. '
                'Release only the capabilities supported by actual simulation and commissioning evidence.')
    manuscript='\n\n'.join(text)+'\n'
    # Keep Markdown tables contiguous so the PDF renderer creates actual tables.
    manuscript=manuscript.replace('|\n\n|','|\n|')
    (SOURCES/filename).write_text(manuscript)
    word_counts[filename]=len(manuscript.split())
(ROOT/'expanded_lab/results/textbook_cases.json').write_text(json.dumps(all_results,indent=2))
print(json.dumps(dict(laboratories=len(SPECS),worked_cases=sum(len(x['cases']) for x in all_results),
    manuscript_words=word_counts,total_words=sum(word_counts.values())),indent=2))
