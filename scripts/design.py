"""Original geometric title design. No historical imagery or simulated speech."""
import math
import urllib.request
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from core import ROOT,read,sha

IVORY=(237,229,212);AMBER=(187,142,84);MUTED=(152,154,149)

def fonts():
    manifest=read(ROOT/'assets/design/font_manifest.json')
    for f in manifest:
        p=ROOT/f['path']
        if not p.exists():
            p.parent.mkdir(parents=True,exist_ok=True)
            with urllib.request.urlopen(f['url'],timeout=60) as r: data=r.read()
            p.write_bytes(data)
        if sha(p)!=f['sha256']: raise ValueError('Font integrity check failed: '+str(p))
    return {f['path'].split('/')[-1].split('.')[0]:ROOT/f['path'] for f in manifest}

def wrap(text,font,width,draw):
    lines=[]
    for paragraph in text.split('\n'):
        line=''
        for word in paragraph.split():
            nxt=(line+' '+word).strip()
            if draw.textlength(nxt,font=font)>width and line: lines.append(line);line=word
            else: line=nxt
        lines.append(line)
    return lines

def block(draw,text,font,x,y,width,fill,leading=1.15,align='left'):
    lines=wrap(text,font,width,draw);step=round(font.size*leading)
    for line in lines:
        xx=x if align=='left' else x+(width-draw.textlength(line,font=font))/2
        draw.text((xx,y),line,font=font,fill=fill,stroke_width=0);y+=step
    return y

def plate(s,w,h,path,mode='animatic'):
    vertical=h>w;scale=w/1920 if not vertical else w/1080
    # Render at delivery resolution; same mathematical texture on every build.
    yy,xx=np.mgrid[0:h,0:w];nx=xx/w;ny=yy/h
    glow=np.exp(-((nx-.76)**2/.10+(ny-.43)**2/.27))
    grain=np.random.default_rng(19).normal(0,.48,(h,w))
    arr=np.stack([10+10*glow+grain,13+9*glow+grain,16+5*glow+grain],axis=-1).clip(0,255).astype('uint8')
    im=Image.fromarray(arr);d=ImageDraw.Draw(im)
    fs=fonts();serif=lambda n:ImageFont.truetype(str(fs['EBGaramond']),max(10,round(n*scale)))
    def sans(n):
        font=ImageFont.truetype(str(fs['Manrope']),max(9,round(n*scale)))
        font.set_variation_by_axes([450])
        return font
    margin=round((90 if vertical else 120)*scale);edge=w-margin
    col=(45,42,34);fine=(63,54,39);motif=s['motif']
    # Geometric light forms are visibly abstract and never resemble archive.
    cx=w*.76 if not vertical else w*.65;cy=h*.44;unit=min(w,h)
    if motif in ['orbit','ripple','arena']:
        for i in range(7):
            radius=unit*(.12+i*.074)
            if motif=='arena':box=(cx-radius,cy-radius*.40,cx+radius,cy+radius*.40)
            else:box=(cx-radius,cy-radius,cx+radius,cy+radius)
            d.arc(box,19+i*13,285+i*6,fill=col if i%2 else fine,width=max(1,round(scale)))
        d.ellipse((cx-3*scale,cy-3*scale,cx+3*scale,cy+3*scale),fill=AMBER)
    elif motif in ['columns','steps']:
        for i in range(9):
            x=w*(.52+i*.055);top=h*(.20+(i*.044 if motif=='steps' else abs(i-4)*.025))
            d.line((x,top,x,h*.79),fill=fine if i==4 else col,width=max(1,round(2*scale)))
            d.line((x,top,x+w*.033,top),fill=col,width=max(1,round(scale)))
    elif motif=='light':
        d.line((w*.77,h*.15,w*.77,h*.77),fill=(89,68,43),width=max(1,round(2*scale)))
        d.line((w*.61,h*.66,w*.9,h*.66),fill=(53,46,35),width=max(1,round(scale)))
    elif motif=='void':
        im=Image.new('RGB',(w,h),(6,8,10));d=ImageDraw.Draw(im)
    top=round((132 if vertical else 65)*scale)
    label='PREPRODUCTION ANIMATIC / NOT FOR DISTRIBUTION' if mode=='animatic' else 'ROUGH CUT / NOT CLEARED FOR DISTRIBUTION'
    if mode!='final':
        block(d,label,sans(15 if vertical else 19),margin,top,w-2*margin,MUTED,1.25)
    if s['kind']=='silence':
        d.line((margin,h-margin,margin+60*scale,h-margin),fill=(55,48,36),width=max(1,round(scale)))
        im.save(path);return
    y=round(h*(.30 if vertical else .27))
    d.text((margin,y),s['movement'],font=sans(19 if vertical else 22),fill=AMBER);y+=round(60*scale)
    if s['kind'] in ['placeholder','clip']:
        d.text((margin,y),'ARCHIVAL RESERVATION',font=sans(16 if vertical else 20),fill=MUTED);y+=round(48*scale)
    size=76 if vertical else 104
    if s['kind']=='credits':size=55 if vertical else 69
    elif s['kind'] in ['placeholder','clip']:size=70 if vertical else 90
    elif s['kind']=='title':size=81 if vertical else 110
    maxwidth=w-2*margin if vertical else w*.78
    f=serif(size)
    # Bound text to safe area by reducing size for tall blocks.
    while len(wrap(s['title'],f,maxwidth,d))*f.size*1.06>h*.32 and size>40:
        size-=3;f=serif(size)
    y=block(d,s['title'],f,margin,y,maxwidth,IVORY,1.06)+round(35*scale)
    body_size=26 if vertical else 29
    if s['kind']=='credits':body_size=20 if vertical else 25
    y=block(d,s['body'],sans(body_size),margin,y,w-2*margin if vertical else w*.78,MUTED,1.55)
    bottom=h-round((280 if vertical else 155)*scale)
    if s['kind'] in ['placeholder','clip']:
        d.line((margin,bottom,edge,bottom),fill=(78,64,45),width=max(1,round(scale)))
        block(d,'FOOTAGE NOT ACQUIRED / NO RECORDED SPEECH',sans(15 if vertical else 18),margin,bottom+24*scale,w-2*margin,AMBER,1.25)
        block(d,s['citation'],sans(16 if vertical else 18),margin,bottom+62*scale,w-2*margin,MUTED,1.3)
    elif s['citation']:
        block(d,s['citation'],sans(16 if vertical else 19),margin,bottom+50*scale,w-2*margin,MUTED,1.3)
    if mode!='final':
        d.text((margin,h-round((160 if vertical else 56)*scale)),'THE QUESTION THAT REMAINS',font=sans(15 if vertical else 17),fill=(117,109,93))
        d.text((edge-round(90*scale),h-round((160 if vertical else 56)*scale)),s['segment_id'],font=sans(17),fill=(117,109,93))
    im.save(path)

def archive_overlay(s,w,h,path,mode):
    im=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(im);f=fonts();scale=w/1920
    d.rectangle((0,h*.78,w,h),fill=(0,0,0,170))
    block(d,s['title'],ImageFont.truetype(str(f['EBGaramond']),int(62*scale)),w*.06,h*.81,w*.86,(237,229,212),1.1)
    block(d,s['citation'],ImageFont.truetype(str(f['Manrope']),int(24*scale)),w*.06,h*.90,w*.86,(200,191,175),1.2)
    if mode!='final':
        d.rectangle((0,0,w,h*.06),fill=(0,0,0,190))
        d.text((w*.04,h*.012),'ROUGH CUT — NOT CLEARED FOR DISTRIBUTION',font=ImageFont.truetype(str(f['Manrope']),int(24*scale)),fill=(237,229,212))
    im.save(path)
