"""Package a built director review cut with 4K canvas and captioned promos."""
from director_cut import *
import html
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--skip-4k',action='store_true');a=p.parse_args();OUT=a.output.resolve()
for ext in ['srt','vtt']:shutil.copy2(OUT/('master_1080p.'+ext),OUT/('captions_en.'+ext))
if not a.skip_4k:
 ff('-i',OUT/'master_1080p.mp4','-map','0:v','-map','0:a','-map','0:s?','-vf','scale=3840:2160:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','20','-threads','8','-c:a','copy','-c:s','copy','-movflags','+faststart',OUT/'master_4k.mp4')
def astime(t):
 cs=round(t*100);hh,cs=divmod(cs,360000);mm,cs=divmod(cs,6000);ss,cs=divmod(cs,100);return f'{hh}:{mm:02}:{ss:02}.{cs:02}'
for name,w,h in [('trailer_90s',1920,1080),('vertical_60s',1080,1920)]:
 cues=json.loads((OUT/(name+'.json')).read_text(encoding='utf8'));ap=W/(name+'.ass');v=h>w
 style=f'''[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Manrope,{44 if v else 37},&H00E9E4DA,&H00E9E4DA,&H00110F0C,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,{80 if v else 160},{80 if v else 160},{260 if v else 170},1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
'''
 for a,b,t in cues:
  t='\\N'.join(textwrap.wrap(t,36 if v else 62));style+=f'Dialogue: 0,{astime(a)},{astime(b)},Default,,0,0,0,,{t}\n'
 ap.write_text(style,encoding='utf8')
 esc=lambda p:str(p.resolve()).replace('\\','/').replace(':','\\:')
 dest=OUT/(name+'_captioned.mp4')
 ff('-i',OUT/(name+'.mp4'),'-vf',f"ass=filename='{esc(ap)}':fontsdir='{esc(R/'assets/design/fonts')}'",'-map','0:v','-map','0:a','-c:v','libx264','-preset','fast','-crf','20','-threads','6','-c:a','copy','-movflags','+faststart',dest)
 dest.replace(OUT/(name+'.mp4'));print('CAPTIONED',name,flush=True)
ff('-ss','31','-i',OUT/'master_1080p.mp4','-frames:v','1','-q:v','2',OUT/'poster.jpg')
scenes=json.loads((OUT/'timeline.json').read_text(encoding='utf8'));chapters=[s for s in scenes if s.get('chapter')]
buttons=''.join(f'<button onclick="seek({s["start"]})"><b>{int(s["start"]//60)}:{int(s["start"]%60):02}</b> {html.escape(s["title"])}</button>' for s in chapters)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Question That Remains</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#070a0b;color:#ece4d6;font:16px/1.6 system-ui,sans-serif}main{max-width:1260px;margin:auto;padding:42px 28px}small{color:#c39c69;letter-spacing:.17em}h1{font:clamp(38px,5vw,70px)/1.07 Georgia,serif;max-width:900px;margin:24px 0}p{color:#b7b9b4;max-width:900px}video{display:block;width:100%;max-height:75vh;background:#000;border:1px solid #292d2c;margin-top:24px}nav{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0}button,a{color:#e8dfce}button{font:inherit;cursor:pointer;background:#121718;border:1px solid #39413e;border-radius:4px;padding:10px 15px}button:hover,button.active{border-color:#c49b66;background:#28251e}b{color:#c6a570;margin-right:8px}footer{margin-top:42px;padding-top:22px;border-top:1px solid #333b37;font-size:13px}a{margin-right:18px}#chapters{margin:22px 0}
</style><main><small>A DOCUMENTARY ESSAY · DIRECTOR’S REVIEW CUT</small><h1>The Question<br>That Remains</h1><p>Power. Knowledge. Suffering. Forgiveness. Victory. Service.<br>Eight authentic archival voices, original narration, and an invitation to examine a life.</p><nav><button class="active" onclick="selectCut('master_1080p','film',this)">Film · 8:48</button><button onclick="selectCut('trailer_90s','trailer',this)">Trailer · 90 seconds</button><button onclick="selectCut('vertical_60s','vertical',this)">Vertical · 60 seconds</button></nav><video id="screen" controls playsinline preload="metadata" poster="poster.jpg"><source src="master_1080p.mp4" type="video/mp4"><track kind="captions" src="master_1080p.vtt" srclang="en" label="English"></video><div id="chapters">CHAPTER_BUTTONS</div><p id="note">English captions are available through the player’s CC control. Historical recordings keep their original proportions. Symbolic imagery and the narrator are identified as AI-generated.</p><footer><p>The editorial film is assembled. This screening copy retains its review legend while third-party rights and human listening review remain open. The 4K version is a delivery upscale of the 1080p composition.</p><a href="master_4k.mp4">4K download</a><a href="transcript.md">Transcript</a><a href="sources_and_credits.md">Sources & credits</a><a href="editorial_report.md">Editorial report</a></footer></main><script>
const player=document.getElementById('screen');function selectCut(name,kind,button){player.pause();player.src=name+'.mp4';player.querySelectorAll('track').forEach(t=>t.remove());if(kind==='film'){const t=document.createElement('track');t.kind='captions';t.src=name+'.vtt';t.srclang='en';t.label='English';player.appendChild(t)}document.querySelectorAll('nav button').forEach(b=>b.classList.remove('active'));button.classList.add('active');document.getElementById('chapters').style.display=kind==='film'?'block':'none';document.getElementById('note').textContent=kind==='film'?'English captions are available through the player’s CC control. Historical recordings keep their original proportions.':'This short cut includes visible English captions.';player.load()}function seek(t){if(!player.src.includes('master_1080p'))selectCut('master_1080p','film',document.querySelector('nav button'));player.currentTime=t;player.play()}
</script></html>'''.replace('CHAPTER_BUTTONS',buttons)
vtt=(OUT/'master_1080p.vtt').read_text(encoding='utf8')
js="const captionURL=URL.createObjectURL(new Blob(["+json.dumps(vtt)+"],{type:'text/vtt'}));player.querySelector('track').src=captionURL;"
page=page.replace("const player=document.getElementById('screen');","const player=document.getElementById('screen');"+js).replace("t.src=name+'.vtt';","t.src=captionURL;")
(OUT/'Screening.html').write_text(page,encoding='utf8')
print('SCREENING PACKAGE READY',flush=True)
