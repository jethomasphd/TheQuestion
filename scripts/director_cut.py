"""Reproducible editorial review cut. Never a release-gate bypass.

The review legend is burned into every frame. Public-release rendering remains
the responsibility of render.py and its shared, fail-closed release gate.
"""
from pathlib import Path
import argparse, concurrent.futures, csv, hashlib, json, math, os, re, shutil, subprocess, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from core import ROOT, load, release_errors

R=ROOT; W=R/'work/production'; G=R/'assets/generated'; S=R/'assets/source'
F=shutil.which('ffmpeg') or 'C:/ffmpeg/ffmpeg-2025-04-14-git-3b2a9410ef-full_build/bin/ffmpeg.exe'
P=str(Path(F).with_name('ffprobe.exe' if os.name=='nt' else 'ffprobe'))
FPS=24; SPEED=.94
IVORY=(238,230,215); AMBER=(194,155,99); MUTED=(169,169,162)
def run(cmd):
 p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True,encoding='utf8',errors='replace')
 if p.returncode:raise RuntimeError(p.stderr[-6500:])
 return p.stdout
def ff(*a):return run([F,'-hide_banner','-loglevel','error','-y',*a])
def probe(p):return json.loads(run([P,'-v','error','-show_format','-show_streams','-of','json',p]))
def dur(p):return float(probe(p)['format']['duration'])
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf8')
def quant(t):return math.ceil(t*FPS)/FPS
def font(n,serif=False):
 f=ImageFont.truetype(str(R/'assets/design/fonts'/('EBGaramond.ttf' if serif else 'Manrope.ttf')),n)
 if not serif:f.set_variation_by_axes([450])
 return f
def lines(draw,text,f,width):
 out=[]
 for para in text.split('\n'):
  line=''
  for word in para.split():
   n=(line+' '+word).strip()
   if draw.textlength(n,font=f)>width and line:out.append(line);line=word
   else:line=n
  out.append(line)
 return out
def block(draw,text,xy,size,width,fill=IVORY,serif=False,center=False):
 f=font(size,serif);x,y=xy
 for line in lines(draw,text,f,width):
  draw.text((x+(width-draw.textlength(line,font=f))/2 if center else x,y),line,font=f,fill=fill)
  y+=size*1.16
 return y

SPEAKERS={
 'reagan':dict(name='Ronald Reagan',role='U.S. president',event='Christmas radio address',date='24 DEC 1983',url='https://www.youtube.com/watch?v=GT6xEAGA_nE',primary='https://www.reaganlibrary.gov/archives/speech/radio-address-nation-christmas',kind='christological_argument',rights='public_domain_verified',owner='U.S. government / Reagan Library',note='Official Reagan Library upload identifies NARA record 74614571; use and access unrestricted.'),
 'collins':dict(name='Francis Collins',role='Geneticist',event='A Testimony · BioLogos',date='2020',url='https://www.youtube.com/watch?v=ncMbufrVyMQ',primary='https://biologos.org/resources/francis-collins-a-testimony',kind='explicit_jesus_testimony',rights='legal_review_required',owner='BioLogos / recording producer',note='Official producer animation accompanying Collins’s authentic recorded testimony. This is not live action footage of his remembered experiences.'),
 'fry':dict(name='Stephen Fry',role='Actor and writer',event='The Meaning of Life · RTÉ',date='2015',url='https://www.youtube.com/watch?v=-suvkwNYSQo',primary='https://www.rte.ie/archives/2020/0201/1110624-stephen-fry-the-meaning-of-life/',kind='critical_questioning',rights='legal_review_required',owner='RTÉ',note='Official RTÉ excerpt. Interviewer asks a hypothetical encounter with God. Fry objects to suffering; he is not responding to the other people in this film.'),
 'carrey':dict(name='Jim Carrey',role='Actor',event='Homeboy Industries',date='2017',url='https://www.youtube.com/watch?v=MzyaQ0H5D74',primary='https://www.youtube.com/watch?v=MzyaQ0H5D74',kind='christian_ethics',rights='legal_review_required',owner='Homeboy Industries / recording producer',note='Official Homeboy upload. Addresses suffering, resentment, grace and forgiveness. No conversion claim. Year only: exact speech date is not independently settled.'),
 'bono':dict(name='Bono',role='Musician',event='The Meaning of Life · RTÉ',date='2013',url='https://www.youtube.com/watch?v=OZnsgvmTJmo',primary='https://www.rte.ie/entertainment/2013/0618/457284-nothing-off-limits-in-bono-interview-gay-byrne/',kind='explicit_jesus_testimony',rights='legal_review_required',owner='RTÉ',note='Full interview carried by a third-party uploader. Gay Byrne’s question and Bono’s answers retained together. Broadcaster master and rights remain outstanding.'),
 'curry':dict(name='Stephen Curry',role='Basketball player',event='NBA Most Valuable Player speech',date='2015',url='https://www.youtube.com/watch?v=fvJl02AziO0',primary='https://www.nba.com/warriors/videos/stephen-currys-2015-nba-mvp-campaign-was-special',kind='explicit_jesus_testimony',rights='legal_review_required',owner='NBA / event broadcaster',note='Full speech reposted by House Of Hoops. Source matched visually to 2015 MVP event. Broadcaster master and rights remain outstanding.'),
 'king':dict(name='Martin Luther King Jr.',role='Minister and civil rights leader',event='The Drum Major Instinct · Ebenezer Baptist Church',date='4 FEB 1968',url='https://www.youtube.com/watch?v=Mefbog-b4-4',primary='https://kinginstitute.stanford.edu/drum-major-instinct',kind='christian_ethics',rights='legal_review_required',owner='King Estate / recording rights holder',note='IBW21 full sermon audio, matched to Stanford transcript. Archival audio is presented with original typography, never simulated speaking footage. Estate permission not established.'),
 'obama':dict(name='Barack Obama',role='U.S. president',event='Easter Prayer Breakfast',date='7 APR 2015',url='https://www.youtube.com/watch?v=Kw8iLnIbVDo',primary='https://obamawhitehouse.archives.gov/photos-and-video/video/2015/04/07/president-and-vice-president-speak-easter-prayer-breakfast/',kind='christian_ethics',rights='public_domain_verified',owner='U.S. government / White House',note='Official archive explicitly labels the 11:22 video Public Domain. Two discontinuous passages are visibly separated by a dated transition card.'),
}
EXCERPTS={
 'reagan':(67.35,98.3), 'collins':(178.10,184.16), 'fry':(26.40,31.54),
 'carrey':(185.40,193.85),'bono':(2363.73,2368.48),'curry':(24.80,33.60),
 'king':(1792.56,1802.55),'obama':(552.65,585.1),'obama_end':(649.65,662.05)
}

def plan(script):
 scenes=[]
 def add(kind,d,**kw):scenes.append(dict(kind=kind,duration=quant(d),**kw))
 def card(title,subtitle='',d=5,chapter='',bg='window'):add('card',d,title=title,subtitle=subtitle,chapter=chapter,bg=bg)
 def narr(name,bgs):add('narration',dur(G/('narr_'+name+'.mp3'))/SPEED+2.8,narration=name,backgrounds=bgs,text=script[name])
 def clip(name):
  a,b=EXCERPTS[name];add('archive',b-a,source=name.split('_')[0],excerpt=name,source_in=a,source_out=b)
  add('breath',2,bg={'reagan':'threshold','collins':'knowledge','fry':'water','carrey':'service','bono':'window','curry':'victory','king':'service','obama':'service','obama_end':'window'}[name])
 add('black',3)
 narr('opening',['threshold','victory'])
 card('THE QUESTION\nTHAT REMAINS','A film about achievement, faith, doubt, and service',8,'', 'threshold')
 card('Power','What can authority answer?',5,'01','threshold')
 narr('power_in',['still_reagan']);clip('reagan');narr('power_out',['threshold'])
 card('Knowledge','A question thought closed',5,'02','knowledge')
 narr('knowledge_in',['knowledge','still_collins']);clip('collins');narr('knowledge_out',['window'])
 card('The wound','The objection deserves to be heard',5,'03','water')
 narr('doubt_in',['still_fry']);clip('fry');add('black',3);narr('doubt_out',['water','threshold'])
 card('Forgiveness','What do we do with suffering?',5,'04','service')
 narr('art_in',['service','still_carrey']);clip('carrey');narr('art_out',['threshold','still_bono']);clip('bono')
 card('Victory','What remains when the score is gone?',5,'05','victory')
 narr('victory_in',['victory','still_curry']);clip('curry');narr('victory_out',['victory','threshold'])
 card('The reversal','Greatness through service',5,'06','service')
 narr('reversal_in',['window','service']);clip('king');narr('reversal_out',['service','still_obama']);clip('obama')
 card('Later in the same address','Easter Prayer Breakfast · 7 April 2015',3,'','window');clip('obama_end')
 narr('ending',['service','water','window'])
 card('“But who do you say\nthat I am?”','Mark 8:29a · World English Bible Classic\nJesus addressing his disciples; an excerpt from the verse.',14,'','black')
 card('THE QUESTION REMAINS.','',8,'','black')
 add('credits',20,title='The voices / the question',subtitle='')
 t=0
 for i,s in enumerate(scenes):s.update(id=f'{i:03}',start=round(t,6));t+=s['duration']
 if not 420<=t<=540:raise ValueError(f'Main cut outside 7–9 minutes: {t}')
 return scenes

def overlay(scene,path,w,h):
 vertical=h>w;im=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(im);sc=w/1920 if not vertical else w/1080
 mx=int((110 if not vertical else 78)*sc)
 if not vertical:
  d.rectangle((0,0,w,129),fill=(4,6,8,255));d.rectangle((0,h-130,w,h),fill=(4,6,8,255))
 tag='REVIEW CUT · RIGHTS PENDING';tagf=font(int(19*sc));tw=d.textlength(tag,font=tagf)
 d.text((w-mx-tw,42 if not vertical else 77),tag,font=tagf,fill=(177,174,163,255))
 kind=scene['kind'];bg=scene.get('bg','');is_sym=kind in ('card','breath') and bg not in ('black','') or kind=='narration'
 if is_sym:
  txt='AI-GENERATED SYMBOLIC IMAGERY' if not str(bg).startswith('still_') else 'ARCHIVAL STILL'
  if kind=='narration':txt='NARRATION · SYMBOLIC IMAGERY / ARCHIVAL STILLS'
  d.text((mx,42 if not vertical else 113),txt,font=font(int(17*sc)),fill=(*MUTED,255))
 if kind=='archive':
  who=SPEAKERS[scene['source']];y=h-121 if not vertical else h-460
  block(d,who['name'],(mx,y),int(33*sc),w-mx*2,serif=True)
  block(d,who['role']+'  /  '+who['event']+'  /  '+who['date'],(mx,y+43*sc),int(18*sc),w-mx*2,fill=MUTED)
  label='ARCHIVAL AUDIO' if scene['source']=='king' else 'ARCHIVAL RECORDING'
  d.text((mx,42),label,font=font(18),fill=(*AMBER,255))
  if scene['source']=='king':
   d.line((w*.25,h*.40,w*.75,h*.40),fill=(87,69,46,255),width=2)
   block(d,'Everybody can be great,\nbecause everybody can serve.',(mx,h*.43),72,w-mx*2,serif=True,center=True)
   block(d,'THE DRUM MAJOR INSTINCT · 1968',(mx,h*.65),21,w-mx*2,fill=AMBER,center=True)
 if kind=='card':
  d.rectangle((0,130 if not vertical else 0,w,h-130 if not vertical else h),fill=(3,5,7,75))
  y=h*.30
  if scene.get('chapter'):block(d,scene['chapter'],(mx,y),26,w-mx*2,fill=AMBER);y+=65
  size=100 if not vertical else 87
  if len(scene['title'])>36:size=85 if not vertical else 76
  y=block(d,scene['title'],(mx,y),size,w-mx*2,serif=True)+38
  block(d,scene.get('subtitle',''),(mx,y),25 if not vertical else 30,w-mx*2,fill=MUTED)
 if kind=='credits':
  y=h*.18
  y=block(d,'THE QUESTION THAT REMAINS',(mx,y),59,w-mx*2,serif=True)+34
  text='Archival voices\nRonald Reagan · Francis Collins · Stephen Fry · Jim Carrey\nBono / Gay Byrne · Stephen Curry · Martin Luther King Jr. · Barack Obama\n\nOriginal narration, symbolic imagery and instrumental score\nCreated with AI tools for this film · Historical voices are authentic recordings\n\nSource credits and editorial ledger accompany this screening copy.\nNo endorsement by any speaker, broadcaster, or institution is implied.\n\nDIRECTOR’S REVIEW CUT · 2026 · PUBLIC RELEASE CLEARANCE PENDING'
  block(d,text,(mx,y),24,w-mx*2,fill=MUTED)
 im.save(path)

def make_stills():
 for name,(a,b) in EXCERPTS.items():
  source=name.split('_')[0]
  if source=='king':continue
  p=W/f'still_{source}.jpg'
  if not p.exists():ff('-ss',str((a+b)/2),'-i',S/(source+'.mp4'),'-frames:v','1','-q:v','2',p)

def render_bg(bg,dest,duration,w,h,variant=0):
 vh=h if h>w else 820;y=0 if h>w else 130
 if bg=='black':
  ff('-f','lavfi','-i',f'color=c=0x040608:s={w}x{h}:r=24','-t',str(duration),'-an','-c:v','libx264','-preset','fast','-crf','20','-threads','4',dest);return
 still=bg.startswith('still_')
 src=W/(bg+'.jpg') if still else G/(bg+'.mp4')
 inputs=['-loop','1','-framerate','24','-i',src] if still else ['-i',src]
 if still:
  vf=f'scale={w-180}:{vh-30}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=0x040608,setsar=1,fps=24'
 else:
  vf=f'setpts={duration/10:.8f}*PTS,scale={w}:{vh}:force_original_aspect_ratio=increase,crop={w}:{vh},setsar=1,fps=24,pad={w}:{h}:0:{y}:color=0x040608'
 vf+=f',fade=t=in:st=0:d=0.35,fade=t=out:st={max(.1,duration-.4)}:d=0.4'
 ff(*inputs,'-vf',vf,'-t',str(duration),'-an','-c:v','libx264','-preset','fast','-crf','20','-threads','4','-pix_fmt','yuv420p',dest)

def concat(paths,out,video_only=False):
 listing=out.with_suffix('.concat.txt');listing.write_text('\n'.join("file '"+str(p.resolve()).replace('\\','/').replace("'","'\\''")+"'" for p in paths),encoding='utf8')
 ff('-f','concat','-safe','0','-i',listing,'-c','copy',out)

def speech_filter(src,start,d,kind):
 """Measure separately; constant gain avoids loudnorm look-ahead PTS gaps."""
 base='aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=65'
 if kind=='narration':base+=f',atempo={SPEED}'
 measure=[F,'-hide_banner','-ss',str(start),'-t',str(d if kind=='archive' else dur(src)),'-i',str(src),'-af',base+',loudnorm=I=-19:TP=-2:LRA=9:print_format=json','-vn','-f','null','-']
 p=subprocess.run(measure,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-3000:])
 stat=json.loads(re.findall(r'\{[^{}]+\}',p.stderr)[-1]);gain=min(-19-float(stat['input_i']),-2-float(stat['input_tp']))
 af=base+f',volume={gain:.6f}dB,asetpts=N/SR/TB'
 if kind=='narration':af+=',adelay=900|900'
 return af+f',apad,atrim=duration={d},afade=t=in:d=0.015,afade=t=out:st={d-.04}:d=0.04,aresample=48000:async=1:first_pts=0'

def render_scene(s,dest,w,h):
 if dest.exists():return
 d=s['duration'];base=W/(dest.stem+'_bg.mp4');ov=W/(dest.stem+'_overlay.png');overlay(s,ov,w,h)
 kind=s['kind'];inputs=[];audio=None
 if kind=='archive':
  src=S/(s['source']+('.webm' if s['source']=='king' else '.mp4'))
  audio=(src,s['source_in'])
  if s['source']=='king':render_bg('black',base,d,w,h)
  else:
   vh=h-260 if w>h else int(h*.45)
   vf=f'scale={w-100}:{vh}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=0x040608,setsar=1,fps=24'
   ff('-ss',str(s['source_in']),'-i',src,'-t',str(d),'-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','19','-threads','4',base)
 elif kind=='narration':
  bgs=s['backgrounds'];parts=[];left=round(d*FPS)
  for i,bg in enumerate(bgs):
   frames=left if i==len(bgs)-1 else round(d*FPS/len(bgs));left-=frames
   p=W/(dest.stem+f'_bg{i}.mp4');render_bg(bg,p,frames/FPS,w,h,i);parts.append(p)
  concat(parts,base,True);audio=(G/('narr_'+s['narration']+'.mp3'),0)
 else:render_bg(s.get('bg','black'),base,d,w,h)
 args=['-i',base,'-loop','1','-i',ov]
 if audio:args+=['-ss',str(audio[1]),'-i',audio[0]]
 else:args+=['-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000']
 af=speech_filter(audio[0],audio[1],d,kind) if audio else f'aresample=48000,aformat=channel_layouts=stereo,atrim=duration={d}'
 filt=f'[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v];[2:a]{af}[a]'
 ff(*args,'-filter_complex',filt,'-map','[v]','-map','[a]','-t',str(d),'-c:v','libx264','-preset','fast','-crf','19','-threads','4','-c:a','pcm_s16le','-ar','48000',dest)
 print('RENDERED',dest.stem,flush=True)

def make_captions(scenes,out):
 cues=[]
 for s in scenes:
  if s['kind'] not in ('archive','narration'):continue
  name=s['source'] if s['kind']=='archive' else 'narr_'+s['narration']
  transcript=R/'work/transcripts'/(name+'.json')
  if s['kind']=='archive':
   refined=R/'work/transcripts/excerpts'/(s['excerpt']+'.json')
   if refined.exists():transcript=refined
  data=json.loads(transcript.read_text(encoding='utf8'))
  st=s.get('source_in',0);en=s.get('source_out',1e9)
  words=[dict(x) for seg in data for x in seg['words'] if x['end']>st+.02 and x['start']<en-.02]
  for x in words:
   if name=='king' and x['word'].strip().lower() in ('say','save'):x['word']=' serve.'
   if name=='obama' and x['word'].strip()=='looked?':x['word']=' loved?'
   if name=='reagan' and 95<=x['start']<98 and x['word'].strip()=='is':x['word']=' as'
   if name=='carrey' and x['word'].strip()=='You':x['word']=" You've"
   if name.startswith('narr_'):
    x['word']=x['word'].replace('Frye','Fry').replace("Who's",'Whose')
    if name=='narr_doubt_in' and x['word'].strip()=='has':x['word']=' is'
    if name=='narr_knowledge_in' and x['word'].strip()=='remained':x['word']=' remain'
  if name=='bono':
   # Low-volume replies verified against the supplied full-program captions.
   words=[{'start':2363.83,'end':2366.21,'word':'When you pray then, you pray to Jesus?'},
          {'start':2366.27,'end':2366.85,'word':'Yes.'},
          {'start':2367.17,'end':2367.74,'word':'The risen Jesus?'},
          {'start':2367.74,'end':2368.40,'word':'Yes.'}]
  group=[]
  def flush():
   if not group:return
   a=max(st,group[0]['start']);b=min(en,group[-1]['end']);txt=' '.join(x['word'].strip() for x in group)
   if s['kind']=='narration':a=a/SPEED+.9;b=b/SPEED+.9
   else:a-=st;b-=st
   a+=s['start'];b+=s['start']
   if b>a:cues.append([a,b,txt])
   group.clear()
  for x in words:
   if group and (sum(len(q['word']) for q in group)+len(x['word'])>70 or x['end']-group[0]['start']>5.2):flush()
   group.append(x)
   if x['word'].rstrip().endswith(('.','?','!',';')) and len(group)>=3:flush()
  flush()
 def tc(t,sep=','):
  ms=round(t*1000);hh,ms=divmod(ms,3600000);mm,ms=divmod(ms,60000);ss,ms=divmod(ms,1000);return f'{hh:02}:{mm:02}:{ss:02}{sep}{ms:03}'
 out.with_suffix('.srt').write_text('\n\n'.join(f'{i+1}\n{tc(a)} --> {tc(b)}\n'+textwrap.fill(t,48) for i,(a,b,t) in enumerate(cues))+'\n',encoding='utf8')
 out.with_suffix('.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{tc(a,".")} --> {tc(b,".")}\n'+textwrap.fill(t,48) for a,b,t in cues)+'\n',encoding='utf8')
 write(out.with_suffix('.json'),cues)

def mix(scenes,joined,out):
 duration=sum(s['duration'] for s in scenes);score=W/(out.stem+'_score.wav')
 # Three independently generated compositions; crossfade their boundaries.
 ff('-i',G/'score1.mp3','-i',G/'score2.mp3','-i',G/'score3.mp3','-filter_complex',
    '[0:a]atrim=0:160,asetpts=PTS-STARTPTS[a];[1:a]atrim=0:150,asetpts=PTS-STARTPTS[b];[2:a]asetpts=PTS-STARTPTS[c];[a][b]acrossfade=d=8:c1=tri:c2=tri[ab];[ab][c]acrossfade=d=8:c1=tri:c2=tri,aresample=48000,loudnorm=I=-27:TP=-4:LRA=12[out]',
    '-map','[out]','-ar','48000','-c:a','pcm_s16le',score)
 last_voice=max(s['start']+s['duration'] for s in scenes if s['kind'] in ('archive','narration'))
 mixed=W/(out.stem+'_mix.wav')
 # Sidechain voice ducking and a deliberate silent scripture/closing hold.
 filters=f'[0:a]aresample=48000:async=1:first_pts=0,asplit=2[voice][key];[1:a]aresample=48000,apad,atrim=0:{duration},afade=t=in:st=3:d=7,afade=t=out:st={last_voice-5}:d=5[m];[m][key]sidechaincompress=threshold=0.018:ratio=7:attack=70:release=1000[duck];[voice][duck]amix=inputs=2:normalize=0,apad,atrim=0:{duration}[mix]'
 ff('-i',joined,'-i',score,'-filter_complex',filters,'-map','[mix]','-ar','48000','-c:a','pcm_s16le',mixed)
 # Measure, then apply linear loudness normalization to the entire program.
 p=subprocess.run([F,'-hide_banner','-i',str(mixed),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
 stat=json.loads(re.findall(r'\{[^{}]+\}',p.stderr)[-1]);write(out.with_suffix('.loudness-input.json'),stat)
 af='loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}'.format(**stat)
 ff('-i',joined,'-i',mixed,'-i',out.with_suffix('.srt'),'-map','0:v','-map','1:a','-map','2:0','-c:v','copy','-af',af,'-c:a','aac','-b:a','256k','-ar','48000','-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata','title=The Question That Remains — Director’s Review Cut','-movflags','+faststart',out)

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--plan-only',action='store_true');a=p.parse_args();W.mkdir(parents=True,exist_ok=True);a.output.mkdir(parents=True,exist_ok=True)
 script=json.loads((R/'data/director_narration.json').read_text(encoding='utf8'));scenes=plan(script)
 write(R/'data/director_timeline.json',scenes)
 # Record the shared gate result without forging approval or using final mode.
 gate=release_errors(load(),R);write(a.output/'rights_report.json',{'mode':'director_review_cut','public_release_ready':False,'authorization':'User: these are all public sources you have my approval, create a masterpiece','authorization_date':'2026-10-09','rights':SPEAKERS,'shared_release_gate_errors':gate,'human_listening_review':'pending','note':'Production is authorized. This is not a representation that third-party copyrights have been licensed.'})
 print('PLANNED',round(sum(s['duration'] for s in scenes),3),'seconds',len(scenes),'scenes',flush=True)
 if a.plan_only:return
 make_stills()
 dests=[W/('main_'+s['id']+'.mkv') for s in scenes]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda t:render_scene(*t),[(s,d,1920,1080) for s,d in zip(scenes,dests)]))
 joined=W/'director_joined.mkv';concat(dests,joined)
 out=a.output/'master_1080p.mp4';make_captions(scenes,out);mix(scenes,joined,out)
 with (a.output/'edit_decisions.csv').open('w',newline='',encoding='utf8') as f:
  fields=['id','start','duration','kind','source','source_in','source_out','narration'];cw=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');cw.writeheader();cw.writerows(scenes)
 write(a.output/'timeline.json',scenes)
 manifest={}
 for folder in [G,S]:
  for media in folder.iterdir():
   if media.suffix.lower() in ('.mp3','.mp4','.webm'):manifest[str(media.relative_to(R))]={'sha256':sha(media),'bytes':media.stat().st_size,'duration':dur(media)}
 write(a.output/'source_manifest.json',manifest)
 print('FINISHED',out,flush=True)
if __name__=='__main__':main()
