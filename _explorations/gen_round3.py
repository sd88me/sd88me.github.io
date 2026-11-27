import importlib.util
import pathlib; S=str(pathlib.Path(__file__).parent)+'/'
def load(n,p):
    spec=importlib.util.spec_from_file_location(n,S+p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
s2=load('s2','gen_symbols.py'); g=s2.g
OUT=S+'round3/sym/'
def small_sand(col): return s2.sand('rings',col,dots=2600,seed=11)
def lock(col,name,font='BricolageGrotesque[opsz,wdth,wght].ttf',axes={'wght':600,'opsz':96,'wdth':100},sz=104,track=-20,symcol=None):
    d,w=g.text(font,'sd88me',sz,axes,track=track,x=150,y=112)
    W=150+w+20
    open(OUT+name+'.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 150"><g transform="translate(10,12) scale(.63)">{small_sand(symcol or col)}</g><path d="{d}" fill="{col}"/></svg>')
lock('#15201D','lock-specimen',font='InstrumentSans[wdth,wght].ttf',axes={'wght':600,'wdth':100},track=-30)
lock('#1B2430','lock-resonance',symcol='#1F5FBF')
lock('#FFF8EC','lock-orbit')
for n,c in [('mark-cream','#F4EEDF'),('mark-ink','#15201D'),('mark-blue','#1F5FBF')]:
    open(OUT+n+'.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{small_sand(c)}</svg>')
print('ok')
def lockp(col,name,font='BricolageGrotesque[opsz,wdth,wght].ttf',axes={'wght':600,'opsz':96,'wdth':100},track=-20,symcol=None):
    d,w=g.text(font,'sd88me',104,axes,track=track,x=150,y=112); W=150+w+20
    open(OUT+name+'.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 150"><g transform="translate(10,12) scale(.63)">{s2.peaks(symcol or col,sw=3.4,levels=6)}</g><path d="{d}" fill="{col}"/></svg>')
lockp('#1B2430','lockp-resonance',symcol='#1F5FBF')
lockp('#15201D','lockp-specimen',font='InstrumentSans[wdth,wght].ttf',axes={'wght':600,'wdth':100},track=-30)
lockp('#F4EEDF','lockp-cream')
lock('#F4EEDF','lock-cream')
for n,c,sw in [('peaks-ink','#15201D',2.6),('peaks-cream','#F4EEDF',2.6),('peaks-green','#2F6B4F',2.6)]:
    open(OUT+n+'.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{s2.peaks(c,sw=sw)}</svg>')
for n,c in [('rings-ink','#15201D'),('rings-cream','#F4EEDF'),('rings-orange','#E8642C')]:
    open(OUT+n+'.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{s2.sand("rings",c)}</svg>')
# stamps in new palette
open(OUT+'stamp-rings-green.svg','w').write(s2.stamp_sym('sand-rings','#F4EEDF','#F4EEDF','#2F6B4F'))
open(OUT+'stamp-peaks-orange.svg','w').write(s2.stamp_sym('peaks','#15201D','#15201D','#E8642C'))
open(OUT+'seal-rings-blue.svg','w').write(s2.seal('sand-rings','#F4EEDF','#F4EEDF','#1F4E8C'))
open(OUT+'seal-peaks-ink.svg','w').write(s2.seal('peaks','#F4EEDF','#E9A23B','#15201D'))
print('ok2')
for n,c in [('peaks-small-ink','#15201D'),('peaks-small-cream','#F4EEDF')]:
    open(OUT+n+'.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{s2.peaks(c,sw=9,levels=3)}</svg>')
