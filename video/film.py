"""Deterministic 3D motion film: Python/Pillow/NumPy + FFmpeg, no external assets.
Run from any directory: python video/film.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math, subprocess, os, wave
from pathlib import Path
R=Path(__file__).resolve().parent; OUT=R/'output'; OUT.mkdir(exist_ok=True)
W,H,FPS,D=1280,720,24,30
INK=(8,12,23); WHITE=(237,243,255); MUTED=(137,157,184); MINT=(100,255,202); BLUE=(83,146,255); RED=(255,109,140)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fonts={}
def f(n,b=False):
 k=(n,b)
 if k not in fonts: fonts[k]=ImageFont.truetype(BOLD if b else FONT,n)
 return fonts[k]
def ease(x): x=max(0,min(1,x)); return x*x*(3-2*x)
def txt(d,pos,s,size=24,c=WHITE,b=False): d.text(pos,s,font=f(size,b),fill=c)
def panel(d,box,fill=(15,24,41),outline=(39,56,78),r=18): d.rounded_rectangle(box,r,fill=fill,outline=outline,width=1)
def project(p,t,center=(934,370),scale=570):
 p=np.array(p,float); a=t*.28; b=.3+math.sin(t*.21)*.15
 x=p[:,0]*math.cos(a)+p[:,2]*math.sin(a); z=-p[:,0]*math.sin(a)+p[:,2]*math.cos(a)
 y=p[:,1]*math.cos(b)-z*math.sin(b); z=p[:,1]*math.sin(b)+z*math.cos(b)
 k=scale/(z+5)
 return np.column_stack((center[0]+x*k,center[1]+y*k)),z
rng=np.random.default_rng(7); cloud=rng.normal(size=(65,3)); cloud=cloud/np.linalg.norm(cloud,axis=1)[:,None]*rng.uniform(1.5,2.3,(65,1))
def orb(d,t,mode):
 # Perspective-projected 3D latitude/longitude geometry, not a flat animation.
 for j in range(9):
  a=j*math.pi/9
  pts=[(1.7*math.cos(q)*math.cos(a),1.7*math.sin(q),1.7*math.cos(q)*math.sin(a)) for q in np.linspace(0,math.tau,100)]
  xy,z=project(pts,t)
  for i in range(len(xy)-1):
   v=int(50+65*(1-(z[i]+1.7)/3.4)); d.line([tuple(xy[i]),tuple(xy[i+1])],fill=(25,v,int(v*1.3)),width=1)
 for j in range(3):
  a=t*.4+j*1.05
  pts=[(2.1*math.cos(q),2.1*math.sin(q)*math.cos(a),2.1*math.sin(q)*math.sin(a)) for q in np.linspace(0,math.tau,140)]
  xy,z=project(pts,t);d.line([tuple(p) for p in xy],fill=[MINT,BLUE,(159,121,255)][j],width=2)
 xy,z=project(cloud,t)
 for i,p in enumerate(xy):
  if i%3==0:
   q=xy[(i+7)%len(xy)];d.line([tuple(p),tuple(q)],fill=(29,48,66),width=1)
  r=2 if z[i]>0 else 4; c=MINT if i%4==0 else BLUE
  d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill=c)
 # Front-face hub typography is composited for consistent legibility.
 panel(d,(854,329,1014,402),fill=(12,27,41),outline=(61,117,133));txt(d,(879,343),'JERP',35,MINT,True)
scenes=[('01 / THE QUESTION','Before AI answers.','Check what it knows.'),('02 / GUARD','Keep the signal.','Screen content before your AI reads it.'),('03 / VERDICT','Claims. Meet evidence.','True, false, or not a fact.'),('04 / SPEAKER','Less context.','More substance.'),('05 / THE WORKFLOW','Three tools.','One clearer answer.'),('06 / JERP','Confidence','in the Truth.')]
# Soft radial light and subtle grid, generated once.
y,x=np.mgrid[:H,:W]; glow=np.exp(-(((x-950)/470)**2+((y-330)/440)**2))
a=np.zeros((H,W,3),dtype=np.uint8)
for c,base in enumerate(INK): a[:,:,c]=base+glow*[6,15,23][c]
bg=Image.fromarray(a); dd=ImageDraw.Draw(bg)
for xx in range(0,W,64): dd.line((xx,0,xx,H),fill=(16,25,38))
for yy in range(0,H,64): dd.line((0,yy,W,yy),fill=(16,25,38))
cmd=['ffmpeg','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(OUT/'picture.mp4')]
with open(OUT/'encode.log','w') as log:
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
 for frame in range(FPS*D):
  t=frame/FPS; idx=min(5,int(t/5)); u=t%5; entry=ease(u/.7); exit=ease((5-u)/.4)
  im=bg.copy(); d=ImageDraw.Draw(im)
  txt(d,(58,30),'JERP',24,MINT,True);txt(d,(1064,36),'MCP / API',14,MUTED)
  label,l1,l2=scenes[idx]; offset=int((1-entry)*35)
  txt(d,(62,147+offset),label,14,MINT)
  txt(d,(58,199+offset),l1,46,WHITE,True)
  txt(d,(60,266+offset),l2,24,MUTED)
  orb(d,t,idx)
  if idx==0:
   for i,s in enumerate(['A confident answer.','An unsupported claim.','A source worth checking.']):
    xx=65+int(math.sin(t*1.3+i)*9); yy=377+i*66
    panel(d,(xx,yy,xx+485,yy+51));txt(d,(xx+18,yy+13),s,19,MUTED if i!=1 else RED)
  elif idx==1:
   panel(d,(62,368,563,550));txt(d,(85,388),'guard',22,MINT,True)
   txt(d,(85,431),'Content / links / actions',20)
   for i,(s,c) in enumerate([('SAFE',MINT),('UNSAFE',RED),('UNCLEAR',BLUE)]):
    xx=85+i*150;panel(d,(xx,480,xx+132,522));txt(d,(xx+14,492),s,14,c,True)
  elif idx==2:
   rows=[('TRUE','Supported by a source',MINT),('FALSE','Contradicted by a source',RED),('NOT A FACT','Opinion or marketing',BLUE)]
   for i,(s,sub,c) in enumerate(rows):
    yy=365+i*70;panel(d,(62,yy,564,yy+58));txt(d,(80,yy+18),s,15,c,True);txt(d,(252,yy+18),sub,15,MUTED)
   txt(d,(65,592),'Source + confidence + receipt',17,MINT)
  elif idx==3:
   panel(d,(62,369,565,569));txt(d,(83,387),'speaker',22,MINT,True)
   for i,s in enumerate(['Sourced facts','A defined context budget','An exportable receipt']):
    txt(d,(87,436+i*36),'+' ,20,MINT);txt(d,(115,436+i*36),s,19,WHITE)
  elif idx==4:
   for i,s in enumerate(['guard','verdict','speaker']):
    yy=368+i*66;panel(d,(62,yy,350,yy+50),outline=(46,90,103));txt(d,(85,yy+12),s,21,MINT,True)
    if i<2:d.line((205,yy+51,205,yy+64),fill=MINT,width=2)
   txt(d,(387,443),'AI',30,WHITE,True)
   d.line((351,459,377,459),fill=BLUE,width=2)
  else:
   txt(d,(62,359),'Stop guessing. Start checking.',24,WHITE)
   panel(d,(62,427,342,493),fill=MINT,outline=MINT)
   txt(d,(86,444),'getjerp.com',26,INK,True)
   txt(d,(63,529),'Connect via MCP or REST API',18,MUTED)
  txt(d,(62,661),'CONFIDENCE IN THE TRUTH',12,MUTED)
  txt(d,(1080,660),f'{idx+1:02d} / 06',13,MUTED)
  d.rectangle((0,H-3,int(W*t/D),H),fill=MINT)
  # Short dark dips join scenes; a traveling mint line supplies a directional wipe.
  if entry*exit<1:
   overlay=Image.new('RGB',(W,H),INK);im=Image.blend(overlay,im,max(.08,entry*exit))
   if u<.6:
    dd=ImageDraw.Draw(im);xx=int(W*ease(u/.6));dd.line((xx,0,xx,H),fill=MINT,width=2)
  p.stdin.write(im.tobytes())
  if frame%120==0: print(f'{frame}/{FPS*D}',flush=True)
 p.stdin.close();code=p.wait()
 if code: raise RuntimeError(f'FFmpeg exited {code}')
# Original quiet electronic bed: arpeggio, sub pulses and scene-transition air.
sr=44100; tt=np.arange(D*sr)/sr; sound=np.zeros(len(tt))
for k in range(D*2):
 start=k*.5; dt=tt-start; mask=(dt>=0)&(dt<1.8); freq=[164.81,220,246.94,329.63,440,329.63,246.94,220][k%8]
 sound[mask]+=.075*np.sin(2*np.pi*freq*dt[mask])*np.exp(-dt[mask]*3.8)*np.minimum(1,dt[mask]*45)
for k in range(0,D,5):
 dt=tt-k;mask=(dt>=0)&(dt<.7);sound[mask]+=.14*np.sin(2*np.pi*(55*dt[mask]+2*(1-np.exp(-dt[mask]*20))))*np.exp(-dt[mask]*9)
sound*=np.minimum(1,tt/1.0)*np.minimum(1,(D-tt)/1.2)
stereo=np.column_stack((sound,np.roll(sound,220)));pcm=(np.clip(stereo,-1,1)*32767).astype('<i2')
with wave.open(str(OUT/'score.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
subprocess.run(['ffmpeg','-y','-i',str(OUT/'picture.mp4'),'-i',str(OUT/'score.wav'),'-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(OUT/'jerp-marketing.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print('DONE',OUT/'jerp-marketing.mp4')
