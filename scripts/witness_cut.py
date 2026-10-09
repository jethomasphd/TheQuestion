"""Speaker-led editorial review assembly; no generated media or narration.

Uses measured source windows, constant-gain dialogue, brief identifiers, and
the shared release-gate report. This command never grants publication approval.
"""
from pathlib import Path
import argparse, concurrent.futures, copy, csv, json, re, subprocess, textwrap
from PIL import Image, ImageDraw, ImageOps
from director_cut import R,S,F,FPS,font,block,ff,probe,dur,sha,write,quant,concat,speech_filter,SPEAKERS
from core import load,release_errors

W=R/'work/reedit'; ALIGN=W/'transcripts'
VOICES=copy.deepcopy(SPEAKERS)
VOICES['collins_live']=dict(name='Francis Collins',role='Physician and geneticist',event='The Veritas Forum · Caltech',date='2009',url='https://www.youtube.com/watch?v=HaEQyNeaFZs',primary='https://www.youtube.com/watch?v=HaEQyNeaFZs',kind='explicit_jesus_testimony',rights='legal_review_required',owner='The Veritas Forum / recording producer',note='Official Veritas upload describes this as Caltech 2009. Upload date 2016 is not the event date. Actual on-camera lecture; replaces the animated BioLogos source.')
VOICES['king']['note']='Authentic 1968 sermon audio. The separately dated 1963 photograph is by Rowland Scherman, USIA, National Archives 542069. Photograph does not depict this sermon. Recording rights remain unresolved.'
PHOTO=dict(path='assets/source/king_1963.jpg',date='28 AUG 1963',credit='Rowland Scherman / USIA / National Archives',identifier='542069',url='https://unwritten-record.blogs.archives.gov/2013/08/30/images-of-the-week-august-30-2013/',rights='U.S. government photograph; source and credit documented')

def get_plan(cut='master'):
    cfg=json.loads((R/'data/witness_edit.json').read_text(encoding='utf8'))
    rows=copy.deepcopy(cfg[cut]);t=0
    for i,s in enumerate(rows):
        # Input decisions are frame-aligned decimal seconds. Round off their
        # representation noise rather than adding an accidental extra frame.
        s['duration']=round((s['source_out']-s['source_in'] if s['kind']=='archive' else s['duration'])*FPS)/FPS
        s.update(id=f'{cut}_{i:02}',start=round(t,6));t+=s['duration']
    validate(rows,cut)
    return rows

def validate(rows,cut):
    expected={'master':(420,540),'trailer':(90,90),'vertical':(60,60)}[cut]
    total=sum(s['duration'] for s in rows)
    if not expected[0]-.01<=total<=expected[1]+.01:raise ValueError(f'{cut}: invalid duration {total}')
    for s in rows:
        if s['kind'] not in ('archive','title','black','ending','credits'):raise ValueError('Non-archival scene is not allowed')
        if s['kind']=='archive':
            if s['source'] not in VOICES:raise ValueError('Unknown voice')
            if not 0<=s['source_in']<s['source_out']:raise ValueError('Invalid source window')
            if cut=='master' and s['source_out']-s['source_in']<30:raise ValueError('Master must preserve sustained passages')

def source_path(s):return S/(s['source']+('.webm' if s['source']=='king' else '.mp4'))

def graphics(s,w,h):
    vertical=h>w
    tag=Image.new('RGBA',(w,h));d=ImageDraw.Draw(tag)
    txt='REVIEW CUT · RIGHTS PENDING';f=font(16 if not vertical else 19)
    tw=d.textlength(txt,font=f);x=w-tw-32
    d.rounded_rectangle((x-12,22,w-20,57),radius=3,fill=(0,0,0,110))
    d.text((x,28),txt,font=f,fill=(230,230,224,215))
    tp=W/(s['id']+'_tag.png');tag.save(tp)
    lower=Image.new('RGBA',(w,h));d=ImageDraw.Draw(lower)
    if s['kind']=='archive' and s['source']!='king':
        v=VOICES[s['source']];y=h-220 if not vertical else 1220
        for j in range(205):d.line((0,y-20+j,w,y-20+j),fill=(0,0,0,int(160*min(1,j/45))))
        block(d,v['name'],(66,y+30),44 if not vertical else 48,w-132,serif=True)
        block(d,v['event']+'  /  '+v['date'],(68,y+91),22 if not vertical else 26,w-136,fill=(222,220,210))
    lp=W/(s['id']+'_lower.png');lower.save(lp)
    return tp,lp

def still(s,w,h):
    im=Image.new('RGB',(w,h),(8,10,11));d=ImageDraw.Draw(im)
    if s['kind']=='archive':
        # Preserve the portrait's aspect ratio. No invented movement or lip-sync.
        photo=Image.open(S/'king_1963.jpg').convert('RGB')
        ph=ImageOps.contain(photo,(980,1080),Image.Resampling.LANCZOS)
        im.paste(ph,(w-ph.width,(h-ph.height)//2));d=ImageDraw.Draw(im)
        block(d,'MARTIN LUTHER\nKING JR.',(95,324),71,860,serif=True)
        d.line((98,538,390,538),fill=(173,144,103),width=2)
        block(d,'The Drum Major Instinct',(98,581),31,790,serif=True)
        block(d,'Ebenezer Baptist Church\n4 February 1968 · Archival audio',(98,634),23,790,fill=(182,184,181))
        block(d,'PHOTOGRAPH: 28 AUGUST 1963\nRowland Scherman / USIA / National Archives',(98,949),17,790,fill=(152,155,151))
    elif s['kind']=='title':
        block(d,'THE QUESTION\nTHAT REMAINS',(100,340 if w>h else 710),104 if w>h else 78,w-200,serif=True,center=True)
        block(d,'A FILM IN THEIR OWN WORDS',(100,668 if w>h else 1040),23,w-200,fill=(184,162,123),center=True)
    elif s['kind']=='ending':
        y=410 if w>h else 750
        block(d,'“But who do you say\nthat I am?”',(90,y),78 if w>h else 68,w-180,serif=True,center=True)
        block(d,'Mark 8:29a · World English Bible Classic',(90,y+227),22,w-180,fill=(180,181,173),center=True)
    elif s['kind']=='credits':
        block(d,'THE QUESTION THAT REMAINS',(100,205),57,w-200,serif=True,center=True)
        txt='Bono / Gay Byrne · Francis Collins · Stephen Fry\nJim Carrey · Stephen Curry · Martin Luther King Jr.\n\nRecordings: RTÉ · The Veritas Forum · Homeboy Industries\nNBA / event broadcaster · The King sermon archive via IBW21\n\nKing photograph: Rowland Scherman / USIA / National Archives\nSource dates identify separate events. No endorsement is implied.\n\nEditorial screening copy · Public release rights pending'
        block(d,txt,(110,347),25,w-220,fill=(186,188,182),center=True)
    p=W/(s['id']+'_still.png');im.save(p);return p

def render_scene(s,dest,w,h):
    if dest.exists():return
    d=s['duration'];tp,lp=graphics(s,w,h)
    moving=s['kind']=='archive' and s['source']!='king'
    if moving:
        args=['-ss',str(s['source_in']),'-i',source_path(s)]
        vf=f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=0x080a0b,setsar=1,fps={FPS},setpts=PTS-STARTPTS'
        if h>w:
            # The portrait excerpt is one steady Carrey shot. Reframe the
            # actual source around his face; never stretch or reconstruct it.
            vf=f'crop=ih*9/16:ih:iw*.52-ow/2:0,scale={w}:{h},setsar=1,fps={FPS},setpts=PTS-STARTPTS'
        audio='0:a'
    else:
        args=['-loop','1','-framerate',str(FPS),'-i',still(s,w,h)]
        vf=f'fps={FPS},setsar=1,setpts=PTS-STARTPTS';audio='3:a'
    args+=['-loop','1','-framerate',str(FPS),'-i',tp,'-loop','1','-framerate',str(FPS),'-i',lp]
    if not moving:
        if s['kind']=='archive':args+=['-ss',str(s['source_in']),'-i',source_path(s)]
        else:args+=['-f','lavfi','-i','anullsrc=r=48000:cl=stereo']
    af=speech_filter(source_path(s),s['source_in'],d,'archive') if s['kind']=='archive' else f'atrim=duration={d},asetpts=N/SR/TB'
    filt=f"[0:v]{vf}[base];[base][1:v]overlay=shortest=1[tag];[tag][2:v]overlay=shortest=1:enable='lt(t,9)',format=yuv420p[v];[{audio}]{af}[a]"
    ff(*args,'-filter_complex_threads','2','-filter_complex',filt,'-map','[v]','-map','[a]','-t',str(d),'-c:v','libx264','-preset','fast','-crf','18','-threads','4','-c:a','pcm_s16le','-ar','48000',dest)
    print('RENDERED',s['id'],d,flush=True)

def caption_cues(rows):
    cues=[]
    corrections=json.loads((R/'data/witness_caption_corrections.json').read_text(encoding='utf8'))
    for s in rows:
        if s['kind']!='archive':continue
        path=ALIGN/(s['source']+'.json');data=json.loads(path.read_text(encoding='utf8'))
        start,end=s['source_in'],s['source_out']
        words=[dict(w) for seg in data for w in seg['words'] if w['end']>start+.015 and w['start']<end-.015]
        for change in corrections.get(s['source'],[]):
            if 'from' in change:
                words=[w for w in words if not change['from']-.005<=w['start']<change['to']-.005]
                words.append(dict(start=change['from'],end=change['to'],word=change['text']))
            else:
                for i,w in enumerate(words[:-1]):
                    if change['after']<=w['start']<=change['before'] and w['word'].strip()==change['find'] and words[i+1]['word'].strip()==change['require_next']:w['word']=change['text']
        words.sort(key=lambda w:w['start'])
        words=[w for w in words if w['end']>start+.015 and w['start']<end-.015]
        group=[]
        def flush():
            if not group:return
            a=max(start,group[0]['start'])-start+s['start'];b=min(end,group[-1]['end'])-start+s['start']
            if b>a:cues.append([a,b,' '.join(w['word'].strip() for w in group)])
            group.clear()
        for word in words:
            if group and (len(' '.join(w['word'] for w in group))+len(word['word'])>76 or word['end']-group[0]['start']>5 or word['start']-group[-1]['end']>.8):flush()
            group.append(word)
            if word['word'].rstrip().endswith(('.','?','!',';')) and len(group)>2:flush()
        flush()
    return cues

def timecode(t,sep=','):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02}{sep}{ms:03}'

def captions(rows,out):
    cues=caption_cues(rows)
    out.with_suffix('.srt').write_text('\n\n'.join(f'{i+1}\n{timecode(a)} --> {timecode(b)}\n'+textwrap.fill(t,44) for i,(a,b,t) in enumerate(cues))+'\n',encoding='utf8')
    out.with_suffix('.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{timecode(a,".")} --> {timecode(b,".")}\n'+textwrap.fill(t,44) for a,b,t in cues)+'\n',encoding='utf8')
    write(out.with_suffix('.captions.json'),cues)

def finish(joined,out):
    p=subprocess.run([F,'-hide_banner','-i',str(joined),'-af','loudnorm=I=-16:TP=-1.7:LRA=11:print_format=json','-vn','-f','null','-'],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-2000:])
    stat=json.loads(re.findall(r'\{[^{}]+\}',p.stderr)[-1]);write(out.with_suffix('.loudness-input.json'),stat)
    af='loudnorm=I=-16:TP=-1.7:LRA=11:linear=true:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset},aresample=48000:async=1:first_pts=0'.format(**stat)
    ff('-i',joined,'-i',out.with_suffix('.srt'),'-map','0:v','-map','0:a','-map','1:0','-c:v','copy','-af',af,'-c:a','aac','-b:a','256k','-ac','2','-ar','48000','-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata','title=The Question That Remains — In Their Own Words','-movflags','+faststart',out)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--cut',choices=['master','trailer','vertical'],default='master');p.add_argument('--plan-only',action='store_true');a=p.parse_args()
    W.mkdir(parents=True,exist_ok=True);a.output.mkdir(parents=True,exist_ok=True)
    rows=get_plan(a.cut);write(a.output/(a.cut+'_timeline.json'),rows)
    gate=release_errors(load(),R)
    write(a.output/'rights_report.json',dict(mode='speaker_led_editorial_review',public_release_ready=False,authorization='User authorized source acquisition and requested longer authentic speaker passages, replacing generated imagery and narration.',voices={k:VOICES[k] for k in ['bono','collins_live','fry','carrey','curry','king']},photograph=PHOTO,shared_release_gate_errors=gate,human_listening_review='pending'))
    print('PLANNED',a.cut,sum(s['duration'] for s in rows),flush=True)
    if a.plan_only:return
    dims=(1080,1920) if a.cut=='vertical' else (1920,1080)
    paths=[W/(s['id']+'.mkv') for s in rows]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda pair:render_scene(*pair,*dims),zip(rows,paths)))
    joined=W/(a.cut+'_joined.mkv');concat(paths,joined)
    name={'master':'TheQuestion_InTheirOwnWords_1080p','trailer':'TheQuestion_Trailer_90s','vertical':'TheQuestion_Vertical_60s'}[a.cut]
    out=a.output/(name+'.mp4');captions(rows,out);finish(joined,out)
    with (a.output/(a.cut+'_edit_decisions.csv')).open('w',newline='',encoding='utf8') as f:
        writer=csv.DictWriter(f,fieldnames=['id','start','duration','kind','source','source_in','source_out'],extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    if a.cut=='master':
        used=[source_path(s) for s in rows if s['kind']=='archive']+[S/'king_1963.jpg']
        write(a.output/'source_manifest.json',{str(p.relative_to(R)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in used})
    print('FINISHED',out,flush=True)

if __name__=='__main__':main()
