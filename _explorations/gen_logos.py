import math, os, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import pathlib; HERE=pathlib.Path(__file__).parent; F=str(HERE/'fonts')+'/'  # put the Google Fonts .ttf files here
OUT=str(HERE/'logos')+'/'
_cache={}
def font(fn):
    if fn not in _cache:
        data=open(F+fn,'rb').read(); _cache[fn]=(TTFont(F+fn),hb.Font(hb.Face(data)))
    return _cache[fn]
def text(fn,s,size,axes=None,track=0,x=0,y=0,feat=None):
    """return (path d, advance width) with baseline at y, starting at x; size in px; track in em/1000"""
    tt,hf=font(fn); upem=tt['head'].unitsPerEm
    if axes: hf.set_variations(axes)
    buf=hb.Buffer(); buf.add_str(s); buf.guess_segment_properties(); hb.shape(hf,buf,feat or {})
    gs=tt.getGlyphSet(location=axes) if axes else tt.getGlyphSet(); order=tt.getGlyphOrder()
    sc=size/upem; pen=SVGPathPen(gs); cx=0
    for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
        g=order[info.codepoint]
        tp=TransformPen(pen,(sc,0,0,-sc,x+(cx+pos.x_offset)*sc,y-pos.y_offset*sc))
        gs[g].draw(tp); cx+=pos.x_advance+track*upem/1000
    return pen.getCommands(), (cx-track*upem/1000)*sc
def glyph_runs(fn,s,size,axes=None,track=0):
    """per-glyph (d at origin, advance) for text on a path"""
    tt,hf=font(fn); upem=tt['head'].unitsPerEm
    if axes: hf.set_variations(axes)
    buf=hb.Buffer(); buf.add_str(s); buf.guess_segment_properties(); hb.shape(hf,buf,{})
    gs=tt.getGlyphSet(location=axes) if axes else tt.getGlyphSet(); order=tt.getGlyphOrder(); sc=size/upem; out=[]
    for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
        pen=SVGPathPen(gs); gs[order[info.codepoint]].draw(TransformPen(pen,(sc,0,0,-sc,0,0)))
        out.append((pen.getCommands(),(pos.x_advance+track*upem/1000)*sc))
    return out
def svg(w,h,body,bg=None,label=''):
    b=f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="sd88me{label}">{b}{body}</svg>'
def save(name,s): open(OUT+name+'.svg','w').write(s)

INK_D='#F1E8DA'; INK_L='#1B1726'
logos={}

# 1 QUAD: 2x2 rings = "88" seen from above; Syne wordmark
def quad(cx,cy,r,col,sw):
    d=r*0.62; return ''.join(f'<circle cx="{cx+dx:.2f}" cy="{cy+dy:.2f}" r="{r:.2f}" fill="none" stroke="{col}" stroke-width="{sw}"/>' for dx in(-d,d) for dy in(-d,d))
def L1(ink,acc,bg=None):
    d,w=text('Syne[wght].ttf','sd88me',120,{'wght':700},track=-25,x=170,y=118)
    return svg(170+w+20,160,quad(76,80,34,acc,7)+f'<path d="{d}" fill="{ink}"/>',bg)
logos['quad']=('Quad','Four rings in a square: two 8s seen from above. Syne Bold. Reads as hardware (a pad grid, a speaker) and as sacred geometry.',L1,'#1F1A2C','#C9E27F')
def M1(ink,acc,bg): return svg(160,160,quad(80,80,34,acc,8),bg)

# 2 MODEL: panel lettering, like a hardware model badge
def L2(ink,acc,bg=None):
    d,w=text('Michroma-Regular.ttf','SD·88·ME',72,track=60,x=40,y=96)
    d2,w2=text('MartianMono[wdth,wght].ttf','CIRCUIT-TRUE INSTRUMENTS',15,{'wght':400,'wdth':100},track=260,x=42,y=136)
    W=40+w+40
    return svg(W,170,f'<path d="{d}" fill="{ink}"/><rect x="40" y="112" width="{w:.1f}" height="2.5" fill="{acc}"/><path d="{d2}" fill="{ink}" fill-opacity=".6"/>',bg)
logos['model']=('Model number','Set like the silkscreen on a synth panel: wide Michroma caps, a coloured rule, a spec line underneath. The most “engineered” option.',L2,'#E9E7E2','#E8552B')

# 3 MATRIX: custom 5x7 dot-matrix glyphs, lit and unlit dots
G={'s':["00000","00000","01111","10000","01110","00001","11110"],
   'd':["00001","00001","01101","10011","10001","10011","01101"],
   '8':["01110","10001","10001","01110","10001","10001","01110"],
   'm':["00000","00000","11010","10101","10101","10101","10101"],
   'e':["00000","00000","01110","10001","11111","10000","01110"]}
def L3(ink,acc,bg=None):
    p=13; r=4.6; x0=30; y0=30; out=[]
    for i,ch in enumerate('sd88me'):
        for ry,row in enumerate(G[ch]):
            for rx,v in enumerate(row):
                cx=x0+(i*6+rx)*p; cy=y0+ry*p
                col=(acc if ch=='8' else ink) if v=='1' else ink
                op=1 if v=='1' else .1
                out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" fill-opacity="{op}"/>')
    W=x0*2+(6*6-1)*p; return svg(W,y0*2+6*p,''.join(out),bg)
logos['matrix']=('Matrix','Drawn on a 5×7 dot grid like the LCDs and LED readouts on your plugins. The 8s light up. Technical and a little playful.',L3,'#17141F','#FFB23F')

# 4 DUALITY: Bodoni roman + Cormorant italic 88
def L4(ink,acc,bg=None):
    d1,w1=text('BodoniModa[opsz,wght].ttf','sd',120,{'wght':500,'opsz':96},x=30,y=120)
    d2,w2=text('CormorantGaramond-Italic[wght].ttf','88',150,{'wght':500},track=-40,x=30+w1+4,y=120)
    d3,w3=text('BodoniModa[opsz,wght].ttf','me',120,{'wght':500,'opsz':96},x=30+w1+w2+10,y=120)
    return svg(30+w1+w2+w3+44,160,f'<path d="{d1}" fill="{ink}"/><path d="{d2}" fill="{acc}"/><path d="{d3}" fill="{ink}"/>',bg)
logos['duality']=('Duality','A precise high-contrast roman for the engineering, a soft italic 88 for the spirit. Editorial and quiet, like a record label from the art world.',L4,'#F2EEF0','#B0326E')

# 5 CIPHER: Major Mono Display + frequency ruler
def L5(ink,acc,bg=None):
    d,w=text('MajorMonoDisplay-Regular.ttf','sd88me',100,track=20,x=30,y=100)
    ticks=''.join(f'<rect x="{30+i*w/48:.1f}" y="122" width="1.6" height="{14 if i%8==0 else 7}" fill="{acc if i%8==0 else ink}" fill-opacity="{1 if i%8==0 else .45}"/>' for i in range(49))
    return svg(60+w,160,f'<path d="{d}" fill="{ink}"/>'+ticks,bg)
logos['cipher']=('Cipher','Major Mono Display, whose odd mixed-case letters read like a code. A tuning ruler underneath. The most mysterious option.',L5,'#101A1C','#7FE3D0')

# 6 STAMP: stacked condensed block
def L6(ink,acc,bg=None):
    out=[];W=0
    for i,t in enumerate(['SD','88','ME']):
        d,w=text('BigShouldersDisplay[wght].ttf',t,112,{'wght':900},track=-10,x=30,y=112+i*96)
        out.append(f'<path d="{d}" fill="{acc if t=="88" else ink}"/>'); W=max(W,w)
    return svg(60+W,346,f'<rect x="12" y="12" width="{36+W:.0f}" height="322" fill="none" stroke="{ink}" stroke-width="3"/>'+''.join(out),bg)
logos['stamp']=('Stamp','Stacked heavy condensed caps in a frame, like a techno label’s run-out stamp. Loud and confident. Works great on vinyl and merch.',L6,'#F04E23','#1B1726')

# 7 SEAL: text around a circle, quad in the middle
def L7(ink,acc,bg=None):
    R=118; cx=cy=150; s='SD88ME ✦ CIRCUIT-TRUE INSTRUMENTS ✦ MADE FOR LONG NIGHTS ✦ '
    runs=glyph_runs('Michroma-Regular.ttf',s.replace('✦','·'),15.5,track=120)
    total=sum(a for _,a in runs); scale=(2*math.pi*R)/total; ang=-math.pi/2; out=[]
    for d,a in runs:
        th=ang+(a*scale/2)/R
        x=cx+R*math.cos(ang); y=cy+R*math.sin(ang)
        out.append(f'<path d="{d}" fill="{ink}" transform="translate({x:.2f},{y:.2f}) rotate({math.degrees(ang)+90:.2f}) scale({scale:.3f},1)"/>')
        ang+=a*scale/R
    ring=f'<circle cx="{cx}" cy="{cy}" r="{R+18}" fill="none" stroke="{ink}" stroke-width="1.5"/><circle cx="{cx}" cy="{cy}" r="{R-26}" fill="none" stroke="{ink}" stroke-width="1.5"/>'
    return svg(300,300,ring+''.join(out)+quad(cx,cy,30,acc,6),bg)
logos['seal']=('Seal','A round badge: the Quad mark inside a ring of text. Not a main logo. For stickers, merch, installers and the back of the manual.',L7,'#2A2140','#F6D88E')

# 8 SOFT: Unbounded rounded wide, gradient 88
def L8(ink,acc,bg=None):
    d1,w1=text('Unbounded[wght].ttf','sd',110,{'wght':600},track=-30,x=24,y=118)
    d2,w2=text('Unbounded[wght].ttf','88',110,{'wght':600},track=-30,x=24+w1-3,y=118)
    d3,w3=text('Unbounded[wght].ttf','me',110,{'wght':600},track=-30,x=24+w1+w2-6,y=118)
    W=48+w1+w2+w3-6
    grad=f'<defs><linearGradient id="g8" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF8A5B"/><stop offset=".5" stop-color="#F2A3C6"/><stop offset="1" stop-color="#B69CFF"/></linearGradient></defs>'
    return svg(W,160,grad+f'<path d="{d1}" fill="{ink}"/><path d="{d2}" fill="url(#g8)"/><path d="{d3}" fill="{ink}"/>',bg)
logos['soft']=('Soft','Unbounded: rounded, wide and friendly, with a sunset gradient through the 88. The most playful and positive option, at home on a festival poster.',L8,'#1E1530','#F2A3C6')

import json
meta=[]
for k,(name,desc,fn,bg,acc) in logos.items():
    dark_bg=bg; light=bg in('#E9E7E2','#F2EEF0','#F04E23')
    ink=INK_L if light else INK_D
    save(f'{k}',fn(ink,acc,None)); save(f'{k}-tile',fn(ink,acc,bg))
    meta.append({'k':k,'name':name,'desc':desc,'bg':bg,'ink':ink,'acc':acc})
save('quad-mark',M1(INK_D,'#C9E27F','#1F1A2C'))
json.dump(meta,open(OUT+'meta.json','w'),indent=1)
print('done',len(meta))
