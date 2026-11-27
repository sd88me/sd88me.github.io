import numpy as np, importlib.util, math
from skimage import measure
import pathlib; S=str(pathlib.Path(__file__).parent)+'/'
def load(n,p):
    spec=importlib.util.spec_from_file_location(n,S+p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
s2=load('s2','gen_symbols.py'); g=s2.g
OUT=S+'round4/sym/'
N=420
def field(noise=1.0,sep=1.02):
    y,x=np.mgrid[0:N,0:N]; X=(x/(N-1))*2-1; Y=(y/(N-1))*2-1; Z=np.zeros_like(X)
    for (cx,cy),a,s in zip([(-.36,-.36),(.36,-.36),(-.36,.36),(.36,.36)],[1,.9,.95,1.06],[.2,.19,.21,.2]):
        Z+=a*np.exp(-((X-cx*sep)**2+(Y-cy*sep)**2)/(2*s*s))
    Z+=noise*(.04*np.sin(X*6+1.1)*np.cos(Y*5-.3)+.025*np.sin(X*11+Y*7))
    return Z
def paths(Z,L):
    sc=200/(N-1); out=[]
    for c in measure.find_contours(Z,L):
        if len(c)<10: continue
        p=c[::3]; d='M'+' L'.join(f'{q[1]*sc:.1f},{q[0]*sc:.1f}' for q in p)
        if np.allclose(c[0],c[-1]): d+='Z'
        out.append(d)
    return out
def peaks_mark(col,sw,levels,noise=.6,dots=False,lo=.18,hi=.9):
    """optical-size Peaks: fewer, heavier contours as it gets smaller; optional solid summits"""
    Z=field(noise); body=''
    for L in np.linspace(lo,hi,levels):
        for d in paths(Z,L): body+=f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw:.2f}" stroke-linejoin="round"/>'
    if dots:
        for d in paths(Z,.97): body+=f'<path d="{d}" fill="{col}"/>'
    return body
def svg(body,vb='0 0 200 200'): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>'
# optical size ladder
LADDER={'xs':dict(sw=15,levels=2,noise=.4,lo=.2,hi=.62,dots=True),   # 16 px
        's': dict(sw=13,levels=2,noise=.4,lo=.16,hi=.74),            # 24-32 px  (the favicon you liked, heavier)
        'm': dict(sw=7, levels=4,noise=.6,lo=.17,hi=.86),            # 48-96 px
        'l': dict(sw=3.4,levels=7,noise=1,lo=.16,hi=.98)}            # hero / print
for k,a in LADDER.items():
    for cn,c in [('ink','#15201D'),('cream','#F4EEDF'),('green','#2F6B4F'),('orange','#E8642C')]:
        open(f'{OUT}peaks-{k}-{cn}.svg','w').write(svg(peaks_mark(c,**a)))
# app icon / favicon on tile
for cn,bg,fg in [('green','#2F6B4F','#F4EEDF'),('ink','#15201D','#F4EEDF'),('orange','#E8642C','#15201D'),('stone','#ECE9E2','#15201D')]:
    open(f'{OUT}icon-{cn}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" rx="44" fill="{bg}"/><g transform="translate(22,22) scale(.78)">{peaks_mark(fg,**LADDER["s"])}</g></svg>')
    open(f'{OUT}fav-{cn}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" rx="40" fill="{bg}"/><g transform="translate(16,16) scale(.84)">{peaks_mark(fg,**LADDER["xs"])}</g></svg>')

# caps wordmarks, stem-matched lockups
FONTS={
 'shoulders':('BigShouldersDisplay[wght].ttf',{'wght':800},40,'Big Shoulders 800'),
 'instrument':('InstrumentSans[wdth,wght].ttf',{'wght':600,'wdth':100},60,'Instrument Sans 600'),
 'mona':('MonaSans[wdth,wght].ttf',{'wght':650,'wdth':125},50,'Mona Sans Wide 650'),
 'syne':('Syne[wght].ttf',{'wght':700},30,'Syne 700'),
}
def stem(fn,axes,size):
    tt,_=g.font(fn); gs=tt.getGlyphSet(location=axes); from fontTools.pens.boundsPen import BoundsPen
    bp=BoundsPen(gs); gs[tt.getBestCmap()[ord('I')]].draw(bp); x0,y0,x1,y1=bp.bounds; up=tt['head'].unitsPerEm
    bh=BoundsPen(gs); gs[tt.getBestCmap()[ord('H')]].draw(bh); cap=bh.bounds[3]
    return (x1-x0)/up*size, cap/up*size
meta=[]
for k,(fn,ax,trk,label) in FONTS.items():
    size=100; st,cap=stem(fn,ax,size)
    mark_h=cap*1.42; scale=mark_h/200; sw_vb=st/scale*0.78   # match the letter stem, a touch lighter optically
    gap=cap*.42
    for cn,ink,acc in [('ink','#15201D','#15201D'),('cream','#F4EEDF','#F4EEDF'),('duo','#15201D','#2F6B4F')]:
        d,w=g.text(fn,'SD88ME',size,ax,track=trk,x=mark_h+gap,y=(mark_h+cap)/2)
        W=mark_h+gap+w; H=mark_h
        body=f'<g transform="scale({scale:.4f})">{peaks_mark(acc,sw_vb,2,noise=.4,lo=.16,hi=.74)}</g><path d="{d}" fill="{ink}"/>'
        open(f'{OUT}lock-{k}-{cn}.svg','w').write(svg(body,f'{-2} {-2} {W+4:.1f} {H+4:.1f}'))
        d2,w2=g.text(fn,'SD88ME',size,ax,track=trk,x=0,y=cap)
        open(f'{OUT}word-{k}-{cn}.svg','w').write(svg(f'<path d="{d2}" fill="{ink}"/>',f'0 -2 {w2:.1f} {cap+4:.1f}'))
    meta.append((k,label,round(st,1),round(sw_vb,1)))
# Stamp with the m-size peaks, Seal with l-size
def stamp(ink,acc,bg=None):
    d1,w1=g.text('BigShouldersDisplay[wght].ttf','SD',112,{'wght':900},track=-10,x=30,y=112)
    d3,w3=g.text('BigShouldersDisplay[wght].ttf','ME',112,{'wght':900},track=-10,x=30,y=304)
    W=max(w1,w3); sz=min(W*.96,100)
    b=f'<rect width="{60+W:.0f}" height="346" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {60+W:.0f} 346">{b}<rect x="12" y="12" width="{36+W:.0f}" height="322" fill="none" stroke="{ink}" stroke-width="3"/><path d="{d1}" fill="{ink}"/><g transform="translate({30+(W-sz)/2:.1f},119) scale({sz/200:.3f})">{peaks_mark(acc,**LADDER["s"])}</g><path d="{d3}" fill="{ink}"/></svg>'
open(OUT+'stamp-green.svg','w').write(stamp('#F4EEDF','#F4EEDF','#2F6B4F'))
open(OUT+'stamp-orange.svg','w').write(stamp('#15201D','#15201D','#E8642C'))
print(meta)
