import numpy as np, math, importlib.util
import pathlib; S=str(pathlib.Path(__file__).parent)+'/'
def load(n,p):
    spec=importlib.util.spec_from_file_location(n,S+p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
r7=load('r7','gen_round7.py'); r4=r7.r4; g=r4.g
OUT=S+'round7/sym/'
FN,AX='BigShouldersDisplay[wght].ttf',{'wght':900}
SIZE=100
st,cap=r4.stem(FN,AX,SIZE)
def ring(cx,cy,rx,ry,w,col,grain=.5,i=0,seed=1,n=300):
    rng=np.random.default_rng(seed+i*7); T=np.linspace(0,2*np.pi,n,endpoint=False)
    k=1+.035*np.sin(3*T+i)+.02*np.sin(5*T+2*i)
    def sm(a): return np.convolve(np.r_[a[-2:],a,a[:2]],np.ones(5)/5,'valid')
    jo=sm(grain*rng.normal(0,1,n)); ji=sm(grain*rng.normal(0,1,n))
    ox=(rx*k+w/2+jo)*np.cos(T); oy=(ry*k+w/2+jo)*np.sin(T)
    ix=(rx*k-w/2+ji)*np.cos(T); iy=(ry*k-w/2+ji)*np.sin(T)
    po=' L'.join(f'{cx+a:.2f},{cy+b:.2f}' for a,b in zip(ox,oy)); pi=' L'.join(f'{cx+a:.2f},{cy+b:.2f}' for a,b in zip(ix[::-1],iy[::-1]))
    return f'<path fill-rule="evenodd" d="M{po}Z M{pi}Z" fill="{col}"/>'
def sand_ring(cx,cy,rx,ry,col,dots,spread,i=0,seed=5):
    rng=np.random.default_rng(seed+i); out=''
    for _ in range(dots):
        t=rng.uniform(0,2*np.pi); k=1+.035*math.sin(3*t+i)+.02*math.sin(5*t+2*i); e=rng.normal(0,spread)
        out+=f'<circle cx="{cx+(rx*k+e)*math.cos(t):.2f}" cy="{cy+(ry*k+e)*math.sin(t):.2f}" r="{rng.uniform(.35,.95):.2f}" fill="{col}"/>'
    return out
def word(kind,ink,acc=None):
    acc=acc or ink
    d1,w1=g.text(FN,'SD',SIZE,AX,track=0,x=0,y=cap)
    _,w88=g.text(FN,'88',SIZE,AX,track=0,x=0,y=cap)
    sp=SIZE*.06; x0=w1+sp; top=0; body=''
    band=st*.95
    if kind=='overlap':      # 2x2 overlapping, the Quad narrowed to the width of 88
        W=w88*1.04
        cs=[(x0+W*.27,cap*.27),(x0+W*.73,cap*.27),(x0+W*.27,cap*.73),(x0+W*.73,cap*.73)]
        for i,(cx,cy) in enumerate(cs): body+=ring(cx,cy,W*.27-band*.4,cap*.27-band*.4,band*.8,acc,i=i)
    elif kind=='stacked':    # two typographic 8s: a smaller top ring sitting on a bottom ring
        W=w88; colw=(W-sp*.6)/2; b=band*.9
        for c in range(2):
            cx=x0+colw/2+c*(colw+sp*.6)
            body+=ring(cx,cap*.245,colw/2*.86-b/2,cap*.245-b/2,b,acc,i=c*2)
            body+=ring(cx,cap*.73,colw/2-b/2,cap*.27-b/2,b,acc,i=c*2+1)
    elif kind=='sand':
        W=w88*1.04
        cs=[(x0+W*.27,cap*.27),(x0+W*.73,cap*.27),(x0+W*.27,cap*.73),(x0+W*.73,cap*.73)]
        for i,(cx,cy) in enumerate(cs): body+=sand_ring(cx,cy,W*.25,cap*.25,acc,800,1.4,i=i)
    x3=x0+W+sp
    d3,w3=g.text(FN,'ME',SIZE,AX,track=0,x=x3,y=cap)
    total=x3+w3
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-3 -4 {total+6:.1f} {cap+8:.1f}"><path d="{d1}" fill="{ink}"/>{body}<path d="{d3}" fill="{ink}"/></svg>'
for k in ['overlap','stacked','sand']:
    for cn,ink in [('ink','#16161D'),('cream','#F2EEE6')]:
        open(f'{OUT}w88-{k}-{cn}.svg','w').write(word(k,ink))
    open(f'{OUT}w88-{k}-blue.svg','w').write(word(k,'#16161D','#2B33E8'))
    open(f'{OUT}w88-{k}-orange.svg','w').write(word(k,'#16161D','#FF5A1A'))
    open(f'{OUT}w88-{k}-lime.svg','w').write(word(k,'#F2EEE6','#B6FF3B'))
print('ok', round(st,1), round(cap,1))

# ---- "dense core" sand: a solid rough core, grains thinning and shrinking outward ----
def dust_ring(cx,cy,rx,ry,col,core,dots,scale,i=0,seed=9,gmax=1.0):
    rng=np.random.default_rng(seed+i*13)
    out=ring(cx,cy,rx,ry,core,col,grain=core*.09,i=i,seed=seed)
    for _ in range(dots):
        t=rng.uniform(0,2*np.pi); k=1+.035*math.sin(3*t+i)+.02*math.sin(5*t+2*i)
        e=rng.laplace(0,scale); d=abs(e)
        rr=gmax*max(.18,1-d/(scale*5))*rng.uniform(.6,1.1)
        out+=f'<circle cx="{cx+(rx*k+e)*math.cos(t):.2f}" cy="{cy+(ry*k+e)*math.sin(t):.2f}" r="{rr:.2f}" fill="{col}"/>'
    return out
def word_dust(layout,ink,acc=None):
    acc=acc or ink
    d1,w1=g.text(FN,'SD',SIZE,AX,track=0,x=0,y=cap); _,w88=g.text(FN,'88',SIZE,AX,track=0,x=0,y=cap)
    sp=SIZE*.06; x0=w1+sp; body=''; core=st*.64
    if layout=='overlap':
        W=w88*1.04
        for i,(cx,cy) in enumerate([(x0+W*.27,cap*.27),(x0+W*.73,cap*.27),(x0+W*.27,cap*.73),(x0+W*.73,cap*.73)]):
            body+=dust_ring(cx,cy,W*.25,cap*.25,acc,core,1100,2.3,i=i,gmax=.95)
    else:
        W=w88; colw=(W-sp*.6)/2
        for c in range(2):
            cx=x0+colw/2+c*(colw+sp*.6)
            body+=dust_ring(cx,cap*.245,colw/2*.86-core/2,cap*.245-core/2,acc,core,620,2.0,i=c*2,gmax=.9)
            body+=dust_ring(cx,cap*.73,colw/2-core/2,cap*.27-core/2,acc,core,700,2.0,i=c*2+1,gmax=.9)
    x3=x0+W+sp; d3,w3=g.text(FN,'ME',SIZE,AX,track=0,x=x3,y=cap)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -6 {x3+w3+10:.1f} {cap+12:.1f}"><path d="{d1}" fill="{ink}"/>{body}<path d="{d3}" fill="{ink}"/></svg>'
for lay in ['overlap','stacked']:
    for cn,ink,acc in [('ink','#16161D',None),('cream','#F2EEE6',None),('blue','#16161D','#2B33E8'),('lime','#F2EEE6','#B6FF3B'),('orange','#16161D','#FF5A1A')]:
        open(f'{OUT}w88-dust-{lay}-{cn}.svg','w').write(word_dust(lay,ink,acc))
# the standalone mark in the same style (four rings in a square)
def mark_dust(col,core=7,dots=2600,scale=3.2):
    body=''
    for i,(cx,cy) in enumerate([(-.36,-.36),(.36,-.36),(-.36,.36),(.36,.36)]):
        body+=dust_ring(100+cx*94,100+cy*94,40.4,40.4,col,core,dots//4*1,scale,i=i,gmax=1.3)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{body}</svg>'
for cn,c in [('ink','#16161D'),('cream','#F2EEE6')]:
    open(f'{OUT}rings-dust-l-{cn}.svg','w').write(mark_dust(c,core=6,dots=4000,scale=3.6))
    open(f'{OUT}rings-dust-m-{cn}.svg','w').write(mark_dust(c,core=10,dots=2400,scale=2.6))
print('dust ok')
