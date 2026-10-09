"""Generate edit documents, provenance reports and review requests from metadata."""
import argparse,csv,json,platform,sys
from pathlib import Path
from core import ROOT,load,assert_valid,tc,write_json,release_errors,fingerprint,sha,binary,run

def reports(db,out,mode='animatic'):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    clips={c['clip_id']:c for c in db['clips']};sources={s['source_id']:s for s in db['sources']}
    paper=['# Timecoded paper edit\n','All edit times below are timeline reservations. Blank source times are unknown. No archival speech is simulated.\n','| Edit in–out | Movement | Image / text | Source / status |','|---|---|---|---|']
    transcript=['# Transcript\n','Preproduction text and editorial reservations; no archival speech.' if mode=='animatic' else 'Approved speech cues and on-screen editorial text.\n']
    edl=[]
    for name,cut in db['timeline']['cuts'].items():
        for s in cut['segments']:
            c=clips.get(s['clip_id']);label=s['title'].replace('\n',' / ') or '[Intentional silence]'
            if name=='master':
                paper.append(f'| {tc(s["start_ms"])}–{tc(s["start_ms"]+s["duration_ms"])} | {s["movement"]} | {label} | {c["source_id"]+"; "+c["verification_status"] if c else "original design / biblical question where labeled"} |')
            edl.append(dict(cut=name,segment_id=s['segment_id'],edit_in_ms=s['start_ms'],edit_out_ms=s['start_ms']+s['duration_ms'],kind=s['kind'],clip_id=s['clip_id'],source_id=c['source_id'] if c else '',source_in_ms=c['source_in_ms'] if c else '',source_out_ms=c['source_out_ms'] if c else '',media_sha256=c['source_sha256'] if c else '',claim_class=c['claim_class'] if c else ''))
    from captions import cues_for
    for cue in cues_for(db['timeline']['cuts']['master'],db,mode):transcript.append(f'## {tc(cue["start_ms"])}\n\n{cue["text"]}\n')
    (ROOT/'docs/paper_edit.md').write_text('\n'.join(paper)+'\n',encoding='utf-8')
    (out/'transcript.md').write_text('\n'.join(transcript),encoding='utf-8')
    intro='Preproduction animatic. Named people are research candidates, not participating cast or endorsers. No archival recordings appear. Original design and editorial text prepared in this repository. Music and speech: none.' if mode=='animatic' else 'Archival credits follow the exact source ledger and rights evidence. Appearance does not imply participation or endorsement. Original geometric design and editorial text prepared in this repository; no score is used.'
    credits=['# Sources and credits\n',intro+'\n','Typefaces: EB Garamond and Manrope, SIL Open Font License 1.1; source and checksums in assets/design/font_manifest.json.\n','Scripture: Mark 8:29a, World English Bible Classic. [Text](https://ebible.org/eng-web/MRK08.htm); [public-domain statement](https://ebible.org/details.php?id=eng-web).\n']
    used={c['source_id'] for c in clips.values() if any(s['clip_id']==c['clip_id'] for cut in db['timeline']['cuts'].values() for s in cut['segments'])}
    for sid in sorted(used):
        s=sources[sid];credits.append(f'- {s["speaker"]}: [{s["event"]}]({s["source_url"]}). {s["research_notes"]}')
    (out/'sources_and_credits.md').write_text('\n'.join(credits)+'\n',encoding='utf-8')
    with (out/'edit_decisions.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(edl[0]));w.writeheader();w.writerows(edl)
    blockers=release_errors(db)
    write_json(out/'rights_report.json',{'release_allowed':not blockers,'blockers':blockers,'assets':db['rights']})
    manifest=fingerprint(db)
    manifest['toolchain']={'python':platform.python_version(),'platform':platform.platform(),'ffmpeg':run([binary('ffmpeg'),'-version']).splitlines()[0]}
    manifest['output_sha256']={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!='build_manifest.json'}
    manifest['mode']=mode
    write_json(out/'build_manifest.json',manifest)

def review_packets(db):
    folder=ROOT/'outputs/reports/review';folder.mkdir(parents=True,exist_ok=True)
    for c in db['clips']:
        a,b=c['source_in_ms'],c['source_out_ms']
        interval={'in_ms':max(0,a-30000),'out_ms':b+30000} if a is not None and b is not None else None
        write_json(folder/f'{c["clip_id"]}.json',{'clip':c,'requested_context_interval':interval,'instructions':'Review actual authorized master, exact words and at least 30 seconds each side if available. Document source-boundary limitations. Complete context review and independent human rights decision. ASR never grants verification.','approval':None})
    return folder

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['research','verify']);a=p.parse_args();db=load();assert_valid(db)
    out=ROOT/'outputs/reports';reports(db,out)
    if a.command=='verify':print(review_packets(db))
    print(out)

if __name__=='__main__':main()
