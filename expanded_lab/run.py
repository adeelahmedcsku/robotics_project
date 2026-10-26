"""Run one original numerical textbook experiment or validate the full catalog."""
import argparse
import json
from pathlib import Path
from catalog import load_catalog,evaluate

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('experiment',help='catalog key, list, or test_all')
    parser.add_argument('--case',type=int,default=-1)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();specs=load_catalog()
    if args.experiment=='list':
        for i,s in enumerate(specs,1):print(i,s['key'],s['title'])
        return
    selected=specs if args.experiment=='test_all' else [s for s in specs if s['key']==args.experiment]
    if not selected:parser.error('Unknown experiment; use list')
    results=[]
    for spec in selected:
        values=spec['values'] if args.experiment=='test_all' else [
            spec['values'][args.case] if args.case>=0 else spec['params'][spec['vary']]]
        for value in values:
            params=dict(spec['params']);params[spec['vary']]=value
            result=evaluate(spec,params)
            results.append(dict(key=spec['key'],parameters=params,**result))
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(results,indent=2))
    if args.experiment=='test_all':
        print(f'Executed {len(results)} finite-result cases across {len(selected)} experiments')
    else:print(json.dumps(results,indent=2))

if __name__=='__main__':main()
