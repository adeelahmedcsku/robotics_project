"""Original numerical experiments; teaching values are not hardware ratings."""
from pathlib import Path
import importlib
import json
import math
import numpy as np

SPECS=[]
def add(key, title, concept, equation, source, params, vary, values,
        parameter_notes, walkthrough, pitfalls, exercises, physical):
    SPECS.append(dict(key=key,title=title,concept=concept,equation=equation,
        source=source.strip()+'\n',params=params,vary=vary,values=values,
        parameter_notes=parameter_notes,walkthrough=walkthrough,pitfalls=pitfalls,
        exercises=exercises,physical=physical))

def load_catalog():
    if not SPECS:
        for name in ['catalog_math','catalog_mechanics','catalog_control',
                     'catalog_sensors','catalog_software','catalog_learning',
                     'catalog_hardware']:
            importlib.import_module(name)
    return SPECS

def evaluate(spec, params):
    namespace={'np':np,'math':math}
    exec(compile(spec['source'],spec['key']+'.py','exec'),namespace)
    metrics,derivation,notes=namespace['experiment'](dict(params))
    for key,value in metrics.items():
        if not np.isfinite(float(value)):
            raise AssertionError((spec['key'],key,value))
    return {'metrics':{k:float(v) for k,v in metrics.items()},
            'derivation':derivation,'notes':notes}
