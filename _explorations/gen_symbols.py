import numpy as np, math, importlib.util
from skimage import measure, filters
import pathlib; S=str(pathlib.Path(__file__).parent)+'/'
spec=importlib.util.spec_from_file_location('g',S+'gen_logos.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
OUT=S+'round2/sym/'; import os; os.makedirs(OUT,exist_ok=True)
N=420
def grid():
    y,x=np.mgrid[0:N,0:N]; return (x/(N-1))*2-1,(y/(N-1))*2-1
def cpaths(Z,level,minlen=8,step=2):
    sc=200/(N-1); out=[]
    for c in measure.find_contours(Z,level):
        if len(c)<minlen: continue
        p=c[::step]; d='M'+' L'.join(f'{q[1]*sc:.1f},{q[0]*sc:.1f}' for q in p)
        if np.allclose(c[0],c[-1]): d+='Z'
        out.append(d)
    return out
CEN=[(-.36,-.36),(.36,-.36),(-.36,.36),(.36,.36)]

def sand_field(kind):
    X,Y=grid()
    if kind=='rings':   # four rings in sand: the Quad, drawn by sound
        th=np.arctan2(Y,X); F=np.full_like(X,9.)
        for i,(cx,cy) in enumerate(CEN):
            a=np.arctan2(Y-cy,X-cx); r=.43*(1+.035*np.sin(3*a+i)+.02*np.sin(5*a+2*i))
            F=np.minimum(F,np.abs(np.hypot(X-cx,Y-cy)-r))
        return F,0.022
    if kind=='plate':   # Chladni mode with four nodes
        u=(X+1)/2; v=(Y+1)/2; Z=np.cos(2*np.pi*u)*np.cos(6*np.pi*v)-np.cos(6*np.pi*u)*np.cos(2*np.pi*v)
        return np.abs(Z),0.07
def sand(kind,col,dots=7000,seed=4,rmax=.97):
    r=np.random.default_rng(seed); F,s=sand_field(kind); out=[]; t=0
    while len(out)<dots and t<900000:
        t+=1; x,y=r.uniform(-1,1,2)
        if x*x+y*y>rmax: continue
        i=int((y+1)/2*(N-1)); j=int((x+1)/2*(N-1))
        if r.random()<math.exp(-F[i,j]/s): out.append((x,y))
    return ''.join(f'<circle cx="{(x+1)*100:.1f}" cy="{(y+1)*100:.1f}" r="{r.uniform(.5,1.3):.2f}" fill="{col}"/>' for x,y in out)

def peaks(col,sw=2.3,levels=7):
    X,Y=grid(); Z=np.zeros_like(X)
    for (cx,cy),a,s in zip(CEN,[1,.9,.95,1.06],[.2,.19,.21,.2]):
        Z+=a*np.exp(-((X-cx*1.02)**2+(Y-cy*1.02)**2)/(2*s*s))
    Z+=.04*np.sin(X*6+1.1)*np.cos(Y*5-.3)+.025*np.sin(X*11+Y*7)
    out=[]
    for L in np.linspace(.16,.98,levels): out+=cpaths(Z,L)
    return ''.join(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>' for d in out)

def cells(col):
    X,Y=grid(); R=np.hypot(X,Y); a=np.arctan2(Y,X)
    D=np.stack([np.hypot(X-cx,Y-cy) for cx,cy in CEN]); lab=D.argmin(0)
    inside=R<.9+.025*np.sin(5*a+.7)
    out=''
    for i in range(4):
        m=filters.gaussian(((lab==i)&inside).astype(float),sigma=14)
        for d in cpaths(m,.62): out+=f'<path d="{d}" fill="{col}"/>'
    return out

def pen(col):
    out=''; r=np.random.default_rng(21)
    for i,(cx,cy) in enumerate(CEN):
        T=np.linspace(0,2*np.pi*1.08,500)+r.uniform(0,6)
        rad=.41*(1+.045*np.sin(3*T+i)+.025*np.sin(5*T+2*i))
        P=np.stack([(cx+rad*np.cos(T)),(cy+rad*np.sin(T))],1)*94+100
        d=np.gradient(P,axis=0); n=np.stack([-d[:,1],d[:,0]],1); n/=np.linalg.norm(n,axis=1,keepdims=True)
        u=np.linspace(0,1,len(T)); w=(3.2+2.6*np.sin(T*1+i)**2)*np.minimum(1,u*14)**.5*np.minimum(1,(1-u)*10)**.7+.6
        poly=np.concatenate([P+n*w[:,None]/2,(P-n*w[:,None]/2)[::-1]])
        out+='<path d="M'+' L'.join(f'{a:.1f},{b:.1f}' for a,b in poly[::2])+f'Z" fill="{col}"/>'
    return out

SYMS={'sand-rings':lambda c:sand('rings',c),'sand-plate':lambda c:sand('plate',c,dots=6500),'peaks':peaks,'cells':cells,'pen':pen}
def sym_svg(k,col,bg=None):
    b=f'<rect width="200" height="200" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{b}{SYMS[k](col)}</svg>'

# lockups
def stamp_sym(k,ink,acc,bg=None):
    """SD / symbol / ME in the stamp frame"""
    d1,w1=g.text('BigShouldersDisplay[wght].ttf','SD',112,{'wght':900},track=-10,x=30,y=112)
    d3,w3=g.text('BigShouldersDisplay[wght].ttf','ME',112,{'wght':900},track=-10,x=30,y=112+96*2)
    W=max(w1,w3); sz=min(W*.96,100)
    sym=f'<g transform="translate({30+(W-sz)/2:.1f},{119:.1f}) scale({sz/200:.3f})">{SYMS[k](acc)}</g>'
    b=f'<rect width="{60+W:.0f}" height="346" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {60+W:.0f} 346">{b}<rect x="12" y="12" width="{36+W:.0f}" height="322" fill="none" stroke="{ink}" stroke-width="3"/><path d="{d1}" fill="{ink}"/>{sym}<path d="{d3}" fill="{ink}"/></svg>'
def horiz(k,ink,acc,bg=None):
    d,w=g.text('BigShouldersDisplay[wght].ttf','SD88ME',118,{'wght':900},track=0,x=150,y=118)
    b=f'<rect width="{150+w+24:.0f}" height="150" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {150+w+24:.0f} 150">{b}<g transform="translate(12,12) scale(.63)">{SYMS[k](acc)}</g><path d="{d}" fill="{ink}"/></svg>'
def seal(k,ink,acc,bg=None):
    R=118; cx=cy=150; s='SD88ME · CIRCUIT-TRUE INSTRUMENTS · MADE FOR LONG NIGHTS · '
    runs=g.glyph_runs('BigShouldersDisplay[wght].ttf',s,21,{'wght':800},track=60)
    total=sum(a for _,a in runs); scale=(2*math.pi*R)/total; ang=-math.pi/2; out=[]
    for d,a in runs:
        x=cx+R*math.cos(ang); y=cy+R*math.sin(ang)
        out.append(f'<path d="{d}" fill="{ink}" transform="translate({x:.2f},{y:.2f}) rotate({math.degrees(ang)+90:.2f}) scale({scale:.3f},1)"/>'); ang+=a*scale/R
    b=f'<rect width="300" height="300" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">{b}<circle cx="150" cy="150" r="141" fill="none" stroke="{ink}" stroke-width="2"/><circle cx="150" cy="150" r="{R-30}" fill="none" stroke="{ink}" stroke-width="1.5"/>{"".join(out)}<g transform="translate(70,70) scale(.8)">{SYMS[k](acc)}</g></svg>'

pal={'light':('#1B1726','#1B1726','#EFEAE3'),'dark':('#EFE7DA','#EFE7DA','#1F1A2C')}
import sys
for k in SYMS:
    for pn,(ink,acc,bg) in pal.items():
        open(f'{OUT}{k}-{pn}.svg','w').write(sym_svg(k,acc))
    open(f'{OUT}{k}-stamp.svg','w').write(stamp_sym(k,'#1B1726','#1B1726'))
    open(f'{OUT}{k}-stamp-org.svg','w').write(stamp_sym(k,'#1B1726','#1B1726','#F04E23'))
    open(f'{OUT}{k}-horiz-dark.svg','w').write(horiz(k,'#EFE7DA','#EFE7DA'))
    open(f'{OUT}{k}-seal-dark.svg','w').write(seal(k,'#EFE7DA','#EFE7DA'))
print('ok')

# theme assets
open(OUT+'sand-rings-horiz-ink.svg','w').write(horiz('sand-rings','#16161D','#16161D'))
open(OUT+'peaks-horiz-rose.svg','w').write(horiz('peaks','#F1E8DA','#F2A3C6'))
open(OUT+'pen-seal-cream.svg','w').write(seal('pen','#FFF6EC','#FFF6EC'))
open(OUT+'pen-horiz-cream.svg','w').write(horiz('pen','#FFF6EC','#FFF6EC'))
open(OUT+'sand-rings-seal-ink.svg','w').write(seal('sand-rings','#16161D','#16161D'))
open(OUT+'peaks-seal-dark.svg','w').write(seal('peaks','#F1E8DA','#F2A3C6'))
