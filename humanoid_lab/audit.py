"""Procurement completeness and recorded commissioning gate checker."""
import argparse
import csv
import json
from pathlib import Path
from model import ROOT

def budget(path):
    rows = list(csv.DictReader(Path(path).open()))
    verified = 0.; unknown=[]
    for row in rows:
        if row['verified_eur']:
            verified += float(row['quantity'])*float(row['verified_eur'])
        else:
            unknown.append(row['component'])
    return dict(known_subtotal_eur=round(verified, 2),
                unquoted=unknown, approved=False,
                reason='Incomplete quotes' if unknown else 'Requires compatibility review')

def commissioning(path):
    report = json.loads(Path(path).read_text())
    required = ['mechanical_inspection', 'polarity', 'protective_devices',
                'support_rig', 'emergency_isolation', 'watchdog',
                'encoder_direction', 'limits', 'thermal', 'rollback']
    failed = [x for x in required if report.get(x) != 'PASS']
    return dict(go=not failed, failed=failed,
                note='Record review only; not independent physical verification')

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('mode', choices=['budget', 'commission'])
    p.add_argument('path'); args = p.parse_args()
    print(json.dumps(budget(args.path) if args.mode == 'budget'
                     else commissioning(args.path), indent=2))
