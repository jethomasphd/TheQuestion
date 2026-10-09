from pathlib import Path
import sys,copy,shutil,uuid
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from core import ROOT,load,sha,fingerprint

def fixture():
    base=(ROOT/'work/test-fixtures').resolve();base.mkdir(parents=True,exist_ok=True)
    root=base/uuid.uuid4().hex;root.mkdir()
    class Workspace:
        def cleanup(self):
            target=root.resolve()
            if target.parent!=base:raise ValueError('Refusing cleanup outside test workspace')
            shutil.rmtree(target)
    temp=Workspace()
    shutil.copytree(ROOT/'data/schemas',root/'data/schemas')
    (root/'scripts').mkdir();(root/'assets/design').mkdir(parents=True)
    (root/'scripts/render.py').write_text('# Test-only renderer fixture',encoding='utf-8')
    evidence=root/'evidence.txt';evidence.write_text('Synthetic test attestation. Not a real license or approval.',encoding='utf-8')
    db=load();c=copy.deepcopy(db['clips'][0]);s=copy.deepcopy(db['sources'][0])
    media=root/'test.bin';media.write_bytes(b'TEST ONLY: not historical media')
    s.update(original_producer='Synthetic fixture',original_master_url='https://example.invalid/test',width=640,height=360,fps=24,duration_ms=2000,event_date='2000-01-01')
    c.update(media_path='test.bin',source_sha256=sha(media),source_in_ms=0,source_out_ms=1000,verbatim_transcript='Test words.',context_before='Source begins here: no preceding audio exists.',context_after='Synthetic test context.',verification_status='context_verified',reviewer='Test human fixture',context_review_path='evidence.txt',acquisition_evidence_path='evidence.txt',publish_approved=True,caption_cues=[{'start_ms':0,'end_ms':1000,'text':'Test words.'}])
    r=copy.deepcopy(db['rights'][0]);r.update(status='cleared',rights_owner='Synthetic fixture',evidence_path='evidence.txt',evidence_sha256=sha(evidence),reviewer='Test human fixture',context_approved=True,publish_approved=True)
    db['sources']=[s];db['clips']=[c];db['rights']=[r]
    for aid in ['DESIGN','FONTS']:
        n=copy.deepcopy(r);n.update(asset_id=aid,kind='original_design' if aid=='DESIGN' else 'font');db['rights'].append(n)
    seg=copy.deepcopy(db['timeline']['cuts']['master']['segments'][7]);seg.update(segment_id='TEST',start_ms=0,duration_ms=1000,kind='clip',clip_id=c['clip_id'],asset_ids=['DESIGN','FONTS'])
    for cut in db['timeline']['cuts'].values():cut.update(duration_ms=1000,segments=[copy.deepcopy(seg)])
    a=db['approvals'];a.update(publication_approved=True,approver_role='human',approver='Synthetic test approver',approved_at='2000-01-01',evidence_path='evidence.txt',checks={k:True for k in a['checks']})
    a['input_sha256']=fingerprint(db,root)['input_sha256']
    return temp,root,db

PROBE={'format':{'duration':'2'},'streams':[{'codec_type':'video','width':640,'height':360,'avg_frame_rate':'24/1'}]}
