import argparse
from core import load,validate,release_errors,fingerprint,write_json,ROOT

def main():
    p=argparse.ArgumentParser();p.add_argument('--release',action='store_true');p.add_argument('--fingerprint',action='store_true');a=p.parse_args();db=load()
    errors=release_errors(db) if a.release else validate(db)
    write_json(ROOT/'outputs/reports/validation.json',{'release_check':a.release,'passed':not errors,'errors':errors})
    if a.fingerprint:print(fingerprint(db)['input_sha256'])
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    print('Validation passed')

if __name__=='__main__':main()
