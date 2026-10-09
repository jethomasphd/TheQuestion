"""Shared validation, content fingerprinting and fail-closed release gate."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CLASSES = ['explicit_jesus_testimony','christological_argument','christian_ethics','general_faith','critical_questioning','context_only']
VERIFIED = ['unverified','source_confirmed','transcript_verified','context_verified']
RIGHTS = ['unknown','permission_requested','cleared','public_domain_verified','legal_review_required','rejected']

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+'\n', encoding='utf-8')

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def local(root, value):
    if not value: raise ValueError('Required local file path is missing')
    path = (Path(root)/value).resolve()
    if not path.is_relative_to(Path(root).resolve()): raise ValueError('Path escapes repository: '+str(value))
    if not path.is_file(): raise ValueError('File is missing: '+str(value))
    return path

def binary(name):
    configured = os.environ.get(name.upper())
    found = configured or shutil.which(name)
    if not found: raise RuntimeError(f'{name} is required: install FFmpeg or set {name.upper()} to the executable path')
    return found

def run(args):
    p = subprocess.run([str(x) for x in args], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode: raise RuntimeError(p.stderr[-6000:] or p.stdout[-6000:])
    return p.stdout

def probe(path):
    return json.loads(run([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',path]))

def load(root=ROOT):
    return {key: read(Path(root)/'data'/f'{key}.json') for key in ['sources','clips','rights','timeline','approvals']}

def validate(db, root=ROOT):
    errors=[]
    for key,value in db.items():
        schema=read(Path(root)/'data/schemas'/f'{key}.schema.json')
        errors += [f'{key}: {e.json_path}: {e.message}' for e in Draft202012Validator(schema).iter_errors(value)]
    if errors: return errors
    for key,field in [('sources','source_id'),('clips','clip_id'),('rights','asset_id')]:
        ids=[v[field] for v in db[key]]
        if len(ids)!=len(set(ids)): errors.append(f'{key}: duplicate identifiers')
    sources={x['source_id']:x for x in db['sources']}
    clips={x['clip_id']:x for x in db['clips']}
    rights={x['asset_id']:x for x in db['rights']}
    for c in db['clips']:
        if c['source_id'] not in sources: errors.append(c['clip_id']+': missing source')
        if c['asset_id'] not in rights: errors.append(c['clip_id']+': missing rights')
        a,b=c['source_in_ms'],c['source_out_ms']
        if (a is None)!=(b is None) or (a is not None and (a<0 or b<=a)): errors.append(c['clip_id']+': invalid clip bounds')
        dur=sources.get(c['source_id'],{}).get('duration_ms')
        if dur is not None and b is not None and b>dur: errors.append(c['clip_id']+': excerpt exceeds source duration')
        from captions import validate_cues
        if a is not None and b is not None: errors += [c['clip_id']+': '+e for e in validate_cues(c['caption_cues'],b-a)]
    for name,cut in db['timeline']['cuts'].items():
        cursor=0; ids=set()
        for s in cut['segments']:
            if s['segment_id'] in ids: errors.append(name+': duplicate segment')
            ids.add(s['segment_id'])
            if s['start_ms']!=cursor: errors.append(name+': gap or overlap at '+s['segment_id'])
            cursor+=s['duration_ms']
            if s['duration_ms']*db['timeline']['fps']%1000: errors.append(name+': duration off frame grid')
            if any(x not in rights for x in s['asset_ids']): errors.append(name+': missing asset declaration')
            if 'DESIGN' not in s['asset_ids'] or 'FONTS' not in s['asset_ids']: errors.append(name+': design/font provenance missing')
            if s['clip_id'] and s['clip_id'] not in clips: errors.append(name+': missing clip')
            if s['kind'] in ['clip','placeholder'] and not s['clip_id']: errors.append(name+': archival segment needs clip reference')
            if s['kind']=='clip' and s['clip_id'] in clips:
                c=clips[s['clip_id']]
                if c['source_in_ms'] is None or c['source_out_ms']-c['source_in_ms'] != s['duration_ms']: errors.append(name+': clip/segment duration mismatch')
            if s['kind']=='quote' and s['quote_asset_id'] not in s['asset_ids']: errors.append(name+': quote has no rights asset')
            if s['kind']!='quote' and s['quote_asset_id'] is not None: errors.append(name+': hidden quotation asset')
        if cursor!=cut['duration_ms']: errors.append(name+': duration differs from declared total')
    return errors

def fingerprint(db,root=ROOT):
    """Stable across machines: no clock, absolute paths or output artifacts."""
    files={}
    for folder in ['scripts','data/schemas','assets/design']:
        for p in sorted((Path(root)/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc': files[p.relative_to(root).as_posix()]=sha(p)
    for c in db['clips']:
        if c['media_path']:
            try: files[c['media_path']]=sha(local(root,c['media_path']))
            except ValueError: files[c['media_path']]='MISSING'
    for r in db['rights']:
        for field in ['evidence_path','media_path']:
            if r[field]:
                try: files[r[field]]=sha(local(root,r[field]))
                except ValueError: files[r[field]]='MISSING'
    for c in db['clips']:
        for field in ['context_review_path','acquisition_evidence_path']:
            if c[field]:
                try: files[c[field]]=sha(local(root,c[field]))
                except ValueError: files[c[field]]='MISSING'
    body={'metadata':{k:v for k,v in db.items() if k!='approvals'},'files':files}
    digest=hashlib.sha256(json.dumps(body,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    return {'input_sha256':digest, **body}

def usable_clip(c,db,root=ROOT,clearance=False):
    errors=[]; prefix=c['clip_id']+': '
    if c['verification_status']!='context_verified': errors.append(prefix+'recording, transcript and context not verified')
    for field in ['source_sha256','verbatim_transcript','context_before','context_after','reviewer','context_review_path','acquisition_evidence_path']:
        if not c[field]: errors.append(prefix+field+' missing')
    if c['source_in_ms'] is None or c['source_out_ms'] is None: errors.append(prefix+'source timecodes missing')
    if not c['caption_cues']:errors.append(prefix+'reviewed speech captions missing')
    elif ' '.join(' '.join(x['text'].split()) for x in c['caption_cues'])!=' '.join((c['verbatim_transcript'] or '').split()):errors.append(prefix+'caption text differs from verified transcript')
    for field in ['media_path','context_review_path','acquisition_evidence_path']:
        try:
            p=local(root,c[field])
            if field=='media_path' and sha(p)!=c['source_sha256']: errors.append(prefix+'media checksum mismatch')
        except ValueError as e: errors.append(prefix+str(e))
    source=next((s for s in db['sources'] if s['source_id']==c['source_id']),{})
    for field in ['original_producer','original_master_url','event_date','width','height','fps','duration_ms']:
        if not source.get(field): errors.append(prefix+'source '+field+' missing')
    r=next((r for r in db['rights'] if r['asset_id']==c['asset_id']),{})
    if clearance and r.get('status') not in ['cleared','public_domain_verified']: errors.append(prefix+'not cleared')
    return errors

def release_errors(db,root=ROOT):
    errors=validate(db,root)
    if errors: return errors
    clips={c['clip_id']:c for c in db['clips']}; rights={r['asset_id']:r for r in db['rights']}
    used=set(); used_clips=set()
    for cut in db['timeline']['cuts'].values():
        for s in cut['segments']:
            used.update(s['asset_ids'])
            if s['kind']=='placeholder': errors.append(s['segment_id']+': missing archival footage')
            if s['clip_id']: used_clips.add(s['clip_id']); used.add(clips[s['clip_id']]['asset_id'])
    for cid in sorted(used_clips):
        c=clips[cid]; errors+=usable_clip(c,db,root,True)
        if not c['publish_approved']: errors.append(cid+': human clip approval missing')
        if c['media_path']:
            try:
                info=probe(local(root,c['media_path'])); actual=float(info['format']['duration'])*1000
                if c['source_out_ms'] is None or c['source_out_ms']>actual+1: errors.append(cid+': clip exceeds actual media duration')
                source=next(x for x in db['sources'] if x['source_id']==c['source_id'])
                video=next(x for x in info['streams'] if x['codec_type']=='video')
                num,den=map(int,video['avg_frame_rate'].split('/'))
                if source['width']!=video['width'] or source['height']!=video['height'] or source['fps'] is None or abs(source['fps']-num/den)>.01 or source['duration_ms'] is None or abs(source['duration_ms']-actual)>50:errors.append(cid+': declared metadata differs from actual master')
            except (ValueError,RuntimeError,KeyError) as e: errors.append(cid+': media probe failed: '+str(e))
    for asset_id in sorted(used):
        r=rights[asset_id]
        if r['status'] not in ['cleared','public_domain_verified']: errors.append(asset_id+': rights not cleared')
        if not r['reviewer'] or not r['context_approved'] or not r['publish_approved']: errors.append(asset_id+': human asset review missing')
        if not r['rights_owner']: errors.append(asset_id+': rights owner missing')
        try:
            if sha(local(root,r['evidence_path']))!=r['evidence_sha256']: errors.append(asset_id+': evidence hash mismatch')
        except ValueError as e: errors.append(asset_id+': '+str(e))
        if r['media_path']:
            try:
                if sha(local(root,r['media_path']))!=r['media_sha256']: errors.append(asset_id+': asset hash mismatch')
            except ValueError as e: errors.append(asset_id+': '+str(e))
    a=db['approvals']; expected=fingerprint(db,root)['input_sha256']
    if not a['publication_approved'] or a['approver_role']!='human' or not a['approver'] or not a['approved_at']: errors.append('Explicit human publication approval missing')
    if a['input_sha256']!=expected: errors.append('Human approval is not bound to this exact edit, media, evidence and renderer')
    required=['title','paper_edit','interpretations','scripture_translation','credits','final_cut','captions','listening','audio_measurements','visual_qc']
    if not all(a['checks'].get(k) is True for k in required): errors.append('Human release checklist incomplete')
    try: local(root,a['evidence_path'])
    except ValueError as e: errors.append('Publication approval: '+str(e))
    return sorted(set(errors))

def assert_valid(db,root=ROOT,release=False):
    errors=release_errors(db,root) if release else validate(db,root)
    if errors: raise ValueError('\n'.join(errors))

def tc(ms):
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
