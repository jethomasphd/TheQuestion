"""No bypass flag: every final export requires the same exact-input human gate."""
from core import ROOT,load,assert_valid
from render import render_cut
from build_timeline import reports
from qa_media import inspect

def main():
    db=load();assert_valid(db,release=True)
    out=ROOT/'outputs/final'
    jobs=[('master',2160),('master',1080),('trailer',1080),('vertical',1920)]
    for name,height in jobs:
        path=render_cut(db,name,out,'final',height)
        result=inspect(path,db['timeline']['cuts'][name]['duration_ms']/1000)
        if result['errors']:raise ValueError('Rendered media failed QA: '+str(result['errors']))
    reports(db,out,'final');print(out)

if __name__=='__main__':main()
