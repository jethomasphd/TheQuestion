"""Accessible on-screen text for animatics; reviewed speech cues for archive."""
from pathlib import Path
from core import tc

def validate_cues(cues,duration_ms):
    errors=[];last=0
    for c in cues:
        if not isinstance(c.get('start_ms'),int) or not isinstance(c.get('end_ms'),int):
            errors.append('Caption timing must be integer milliseconds');continue
        if not (last<=c['start_ms']<c['end_ms']<=duration_ms): errors.append('Caption overlap, reversed range or out of bounds')
        if not c.get('text','').strip(): errors.append('Empty caption')
        last=c['end_ms']
    return errors

def cues_for(cut,db,mode='animatic'):
    clips={x['clip_id']:x for x in db['clips']};result=[]
    for s in cut['segments']:
        start=s['start_ms'];end=start+s['duration_ms']
        if s['kind']=='clip' and mode!='animatic':
            c=clips[s['clip_id']]
            for cue in c['caption_cues']:
                result.append({'start_ms':start+cue['start_ms'],'end_ms':start+cue['end_ms'],'text':cue['text']})
        else:
            label='[Missing archival footage — no recorded speech]\n' if s['kind'] in ['clip','placeholder'] else ''
            text=label+'\n'.join(x for x in [s['title'],s['body']] if x)
            if not text: text='[Intentional silence]'
            result.append({'start_ms':start,'end_ms':end,'text':text})
    errors=validate_cues(result,cut['duration_ms'])
    if errors: raise ValueError('\n'.join(errors))
    return result

def export(cut,db,out,stem='captions_en',mode='animatic'):
    cues=cues_for(cut,db,mode);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    srt=[];vtt=['WEBVTT\n']
    for n,c in enumerate(cues,1):
        a,b=tc(c['start_ms']),tc(c['end_ms'])
        srt.append(f'{n}\n{a.replace(".",",")} --> {b.replace(".",",")}\n{c["text"]}\n')
        vtt.append(f'{a} --> {b}\n{c["text"]}\n')
    (out/f'{stem}.srt').write_text('\n'.join(srt),encoding='utf-8')
    (out/f'{stem}.vtt').write_text('\n'.join(vtt),encoding='utf-8')
    return cues
