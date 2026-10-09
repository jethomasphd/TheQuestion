"""Inspect locally supplied authorized media; never download or grant clearance."""
import argparse
from core import ROOT,local,probe,sha,write_json,load

def main():
    p=argparse.ArgumentParser();p.add_argument('path');p.add_argument('--source-id',required=True);p.add_argument('--authorization',required=True);a=p.parse_args()
    ids={s['source_id'] for s in load()['sources']}
    if a.source_id not in ids:p.error('Unknown source ID')
    media=local(ROOT,a.path);evidence=local(ROOT,a.authorization)
    info=probe(media)
    write_json(ROOT/'outputs/reports/ingest'/f'{a.source_id}.json',{'source_id':a.source_id,'media_path':media.relative_to(ROOT).as_posix(),'sha256':sha(media),'authorization_path':evidence.relative_to(ROOT).as_posix(),'authorization_sha256':sha(evidence),'probe':info,'verification_status':'unverified','rights_status':'unknown','publish_approved':False})
    print('Probe receipt written. No verification, clearance or publication approval granted.')

if __name__=='__main__':main()
