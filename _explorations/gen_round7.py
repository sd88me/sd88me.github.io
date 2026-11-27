import numpy as np, math, importlib.util
import pathlib; S=str(pathlib.Path(__file__).parent)+'/'
def load(n,p):
    spec=importlib.util.spec_from_file_location(n,S+p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
r4=load('r4','gen_round4.py'); g=r4.g; s2=r4.s2
OUT=S+'round7/sym/'
CEN=[(-.36,-.36),(.36,-.36),(-.36,.36),(.36,.36)]
def ring_paths(col,w,grain=0.0,seed=3,n=360):
    """four slightly uneven rings as filled bands (w = band width in 200-unit box); grain roughens the edges"""
    rng=np.random.default_rng(seed); out=''
    for i,(cx,cy) in enumerate(CEN):
        T=np.linspace(0,2*np.pi,n,endpoint=False)
        r=.43*(1+.035*np.sin(3*T+i)+.02*np.sin(5*T+2*i))*94
        jo=grain*rng.normal(0,1,n); ji=grain*rng.normal(0,1,n)
        jo=np.convolve(np.r_[jo[-2:],jo,jo[:2]],np.ones(5)/5,'valid'); ji=np.convolve(np.r_[ji[-2:],ji,ji[:2]],np.ones(5)/5,'valid')
        ro=r+w/2+jo; ri=r-w/2+ji
        X=100+cx*94; Y=100+cy*94
        po=' L'.join(f'{X+a*math.cos(t):.1f},{Y+a*math.sin(t):.1f}' for a,t in zip(ro,T))
        pi=' L'.join(f'{X+a*math.cos(t):.1f},{Y+a*math.sin(t):.1f}' for a,t in zip(ri[::-1],T[::-1]))
        out+=f'<path fill-rule="evenodd" d="M{po}Z M{pi}Z" fill="{col}"/>'
    return out
def sand_dense(col,dots,spread,seed=4):
    rng=np.random.default_rng(seed); out=[]
    while len(out)<dots:
        i=rng.integers(4); cx,cy=CEN[i]; t=rng.uniform(0,2*np.pi)
        r=.43*(1+.035*math.sin(3*t+i)+.02*math.sin(5*t+2*i))+rng.normal(0,spread)
        out.append((cx+r*math.cos(t),cy+r*math.sin(t)))
    return ''.join(f'<circle cx="{(x+1)*100:.1f}" cy="{(y+1)*100:.1f}" r="{rng.uniform(.6,1.5):.2f}" fill="{col}"/>' for x,y in out)
LAD={'l':lambda c:sand_dense(c,7000,.022),
     'm':lambda c:sand_dense(c,5200,.012,seed=7),
     's':lambda c:ring_paths(c,15,grain=1.1),
     'xs':lambda c:ring_paths(c,21,grain=0.6)}
svg=lambda body,vb='0 0 200 200':f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>'
for k,f in LAD.items():
    for cn,c in [('ink','#16161D'),('cream','#F2EEE6')]:
        open(f'{OUT}rings-{k}-{cn}.svg','w').write(svg(f(c)))
# lockups (Big Shoulders Display 900, as in the round-2 Cymatic logo; stem-matched band width)
fn,ax,trk='BigShouldersDisplay[wght].ttf',{'wght':900},0
st,cap=r4.stem(fn,ax,100)
for variant,mh in [('',1.22),('-big',1.3)]:
    mark_h=cap*mh; scale=mark_h/200; band=st/scale*.86; gap=cap*.3
    for cn,ink in [('ink','#16161D'),('cream','#F2EEE6')]:
        d,w=g.text(fn,'SD88ME',100,ax,track=trk,x=mark_h+gap,y=(mark_h+cap)/2)
        W=mark_h+gap+w
        open(f'{OUT}lock{variant}-{cn}.svg','w').write(svg(f'<g transform="scale({scale:.4f})">{ring_paths(ink,band,grain=.9)}</g><path d="{d}" fill="{ink}"/>',f'-2 -2 {W+4:.1f} {mark_h+4:.1f}'))
# icons and favicons
for cn,bg,fg in [('ink','#16161D','#F2EEE6'),('blue','#2B33E8','#FFFFFF'),('orange','#FF5A1A','#16161D'),('stone','#E9E7E1','#16161D')]:
    open(f'{OUT}icon-{cn}.svg','w').write(svg(f'<rect width="200" height="200" rx="44" fill="{bg}"/><g transform="translate(26,26) scale(.74)">{ring_paths(fg,17,grain=1)}</g>'))
    open(f'{OUT}fav-{cn}.svg','w').write(svg(f'<rect width="200" height="200" rx="40" fill="{bg}"/><g transform="translate(14,14) scale(.86)">{ring_paths(fg,24,grain=.4)}</g>'))
# stamp with small rings
def stamp(ink,acc,bg):
    d1,w1=g.text('BigShouldersDisplay[wght].ttf','SD',112,{'wght':900},track=-10,x=30,y=112)
    d3,w3=g.text('BigShouldersDisplay[wght].ttf','ME',112,{'wght':900},track=-10,x=30,y=304)
    W=max(w1,w3); sz=min(W*.96,100)
    return svg(f'<rect width="{60+W:.0f}" height="346" fill="{bg}"/><rect x="12" y="12" width="{36+W:.0f}" height="322" fill="none" stroke="{ink}" stroke-width="3"/><path d="{d1}" fill="{ink}"/><g transform="translate({30+(W-sz)/2:.1f},119) scale({sz/200:.3f})">{ring_paths(acc,16,grain=1)}</g><path d="{d3}" fill="{ink}"/>',f'0 0 {60+W:.0f} 346')
open(OUT+'stamp-orange.svg','w').write(stamp('#16161D','#16161D','#FF5A1A'))
open(OUT+'stamp-blue.svg','w').write(stamp('#FFFFFF','#FFFFFF','#2B33E8'))
open(OUT+'seal-ink.svg','w').write(s2.seal('sand-rings','#F2EEE6','#F2EEE6','#16161D'))
print('stem',round(st,1),'cap',round(cap,1))
