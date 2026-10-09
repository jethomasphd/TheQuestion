"""Package the speaker-led screening cut and optional conventional 4K upscale."""
from pathlib import Path
import argparse, html, json, textwrap
from witness_cut import R,W,VOICES,PHOTO,get_plan,ff,probe,sha,write,font,block
from PIL import Image,ImageDraw

def caption_shorts(out):
    receipt=out/'caption_burns.json';done=json.loads(receipt.read_text()) if receipt.exists() else {}
    for name,w,h in [('TheQuestion_Trailer_90s',1920,1080),('TheQuestion_Vertical_60s',1080,1920)]:
        target=out/(name+'.mp4')
        if not target.exists() or done.get(name)==sha(target):continue
        cues=json.loads((out/(name+'.captions.json')).read_text(encoding='utf8'));vertical=h>w
        ass=f'''[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Manrope,{46 if vertical else 38},&H00F0ECE5,&H00F0ECE5,&H00100C08,&H80000000,0,0,0,0,100,100,0,0,1,2.5,1,2,{70 if vertical else 150},{70 if vertical else 150},{280 if vertical else 85},1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
'''
        def clock(t):
            cs=round(t*100);hh,cs=divmod(cs,360000);mm,cs=divmod(cs,6000);ss,cs=divmod(cs,100)
            return f'{hh}:{mm:02}:{ss:02}.{cs:02}'
        for a,b,t in cues:
            text='\\N'.join(textwrap.wrap(t,35 if vertical else 62))
            ass+=f'Dialogue: 0,{clock(a)},{clock(b)},Default,,0,0,0,,{text}\n'
        ap=W/(name+'.ass');ap.write_text(ass,encoding='utf8')
        esc=lambda p:str(p.resolve()).replace('\\','/').replace(':','\\:')
        dest=out/(name+'_captioned.mp4')
        ff('-i',target,'-vf',f"ass=filename='{esc(ap)}':fontsdir='{esc(R/'assets/design/fonts')}'",'-map','0:v','-map','0:a','-c:v','libx264','-preset','fast','-crf','19','-threads','4','-c:a','copy','-movflags','+faststart',dest)
        dest.replace(target);done[name]=sha(target);write(receipt,done)
        print('CAPTIONED',name,flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--upscale',action='store_true');a=p.parse_args();out=a.output
    master=out/'TheQuestion_InTheirOwnWords_1080p.mp4';rows=get_plan()
    ff('-ss','45','-i',master,'-frames:v','1','-q:v','2',out/'poster.jpg')
    im=Image.open(out/'poster.jpg').convert('RGB');veil=Image.new('RGBA',im.size);d=ImageDraw.Draw(veil)
    for y in range(im.height):d.line((0,y,im.width,y),fill=(0,0,0,int(180*max(0,(y-350)/(im.height-350)))))
    im=Image.alpha_composite(im.convert('RGBA'),veil);d=ImageDraw.Draw(im)
    block(d,'THE QUESTION THAT REMAINS',(86,850),62,1748,serif=True)
    block(d,'IN THEIR OWN WORDS',(91,945),23,1740,fill=(232,222,202));im.convert('RGB').save(out/'poster.jpg',quality=93)
    voices=[VOICES[s['source']] for s in rows if s['kind']=='archive']
    credits=['# Sources — In Their Own Words','', 'Editorial screening copy. Third-party release permissions remain unresolved.','']
    for v in voices:credits.extend([f"## {v['name']} — {v['date']}",f"{v['event']}. {v['note']}",f"[Recording]({v['url']}) · [Source context]({v['primary']})",''])
    credits.extend(['## Archival photograph',f"{PHOTO['credit']}, {PHOTO['date']}. [Source]({PHOTO['url']}). Photograph and sermon are different events.",'','No generated narration, imagery or score appears in this edit. Source sound and speech are preserved at their recorded speed.'])
    (out/'source_credits.md').write_text('\n'.join(credits),encoding='utf8')
    chapter=''.join(f'<button data-time="{s["start"]:.3f}"><b>{int(s["start"])//60}:{int(s["start"])%60:02}</b> {html.escape(VOICES[s["source"]]["name"])}</button>' for s in rows if s['kind']=='archive')
    vtt=(out/'TheQuestion_InTheirOwnWords_1080p.vtt').read_text(encoding='utf8')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Question That Remains — In Their Own Words</title><style>*{box-sizing:border-box}body{margin:0;background:#090b0c;color:#efebe1;font:16px/1.6 system-ui,sans-serif}main{max-width:1280px;margin:auto;padding:36px 24px 64px}header{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-bottom:24px}h1{font:normal clamp(30px,4vw,54px)/1.1 Georgia,serif;margin:4px 0 0}.eyebrow{color:#c6aa7c;font-size:12px;letter-spacing:.18em;text-transform:uppercase}.duration{color:#aaa;font-size:14px;white-space:nowrap}video{width:100%;max-height:78vh;background:black;display:block}nav{display:flex;flex-wrap:wrap;gap:9px;margin:22px 0}button{background:#171b1d;border:1px solid #343a3d;color:#ece8dc;padding:11px 16px;border-radius:3px;cursor:pointer;font:inherit}button:hover,button:focus{border-color:#c6aa7c}button b{color:#b8a07b;margin-right:10px;font-size:13px}p{color:#aeb3b0;max-width:850px}a{color:#d4bc91}footer{border-top:1px solid #303537;margin-top:28px;padding-top:20px;font-size:13px}.links{display:flex;gap:24px;flex-wrap:wrap}</style><main><header><div><div class="eyebrow">In their own words</div><h1>The Question That Remains</h1></div><div class="duration">8:57 · Editorial screening</div></header><video id="film" controls preload="metadata" poster="poster.jpg"><source src="TheQuestion_InTheirOwnWords_1080p.mp4" type="video/mp4"><track id="subs" kind="subtitles" label="English" srclang="en"></video><nav aria-label="Film chapters">CHAPTERS</nav><p>Six sustained passages. Real voices, room sound, and the space to finish a thought.</p><div class="links"><a href="TheQuestion_Trailer_90s.mp4">90-second preview</a><a href="TheQuestion_Vertical_60s.mp4">60-second portrait cut</a><a href="source_credits.md">Sources and credits</a></div><footer>The King sequence uses 1968 sermon audio with a separately dated 1963 photograph. Public-release permissions remain pending. English captions are available through the player.</footer></main><script>const film=document.getElementById('film');document.getElementById('subs').src=URL.createObjectURL(new Blob([CAPTIONS],{type:'text/vtt'}));document.querySelectorAll('[data-time]').forEach(b=>b.onclick=()=>{film.currentTime=Number(b.dataset.time);film.play()});</script></html>'''
    page=page.replace('CHAPTERS',chapter).replace('CAPTIONS',json.dumps(vtt).replace('</','<\\/'))
    (out/'Watch.html').write_text(page,encoding='utf8')
    (out/'README.txt').write_text('THE QUESTION THAT REMAINS — IN THEIR OWN WORDS\n\nOpen Watch.html, or play TheQuestion_InTheirOwnWords_1080p.mp4 directly.\nThe main film is a new speaker-led edit, superseding the earlier generated-media version.\nNo generated narrator, imagery, or music. Six continuous passages at original speed.\nEnglish captions are embedded as an optional subtitle track and supplied separately.\nThe 90-second preview retains a whole interview exchange. The portrait cut is one continuous passage.\nKing is genuine sermon audio; the explicitly dated photograph is from another event.\nAny 4K version is a conventional upscale of this same edit.\n\nEditorial review copy; source credits and the rights report document pending public-release clearance.\n',encoding='utf8')
    caption_shorts(out)
    if a.upscale:
        target=out/'TheQuestion_InTheirOwnWords_4k.mp4'
        ff('-i',master,'-map','0:v','-map','0:a','-map','0:s?','-vf','scale=3840:2160:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','20','-threads','8','-c:a','copy','-c:s','copy','-movflags','+faststart','-metadata','comment=Conventional 4K canvas upscale; archive sources retain their original detail.',target)
        print('UPSCALED',target,flush=True)
    write(out/'delivery_manifest.json',{p.name:{'bytes':p.stat().st_size,'sha256':sha(p),'duration_seconds':float(probe(p)['format']['duration'])} for p in out.glob('*.mp4')})
    print('PACKAGED',out,flush=True)

if __name__=='__main__':main()
