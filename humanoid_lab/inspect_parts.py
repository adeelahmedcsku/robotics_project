# /data/Robotics_Project/humanoid_lab/inspect_parts.py
import csv
import sys

def inspect(path):
    failures=[]
    for row in csv.DictReader(open(path, newline='')):
        value=float(row['measured_mm'])
        lo, hi=float(row['min_mm']), float(row['max_mm'])
        if not lo <= value <= hi:
            failures.append(row['part']+':'+row['feature'])
    return failures

if __name__ == '__main__':
    failed=inspect(sys.argv[1])
    print('FAILED FEATURES:', failed)
    raise SystemExit(bool(failed))
