"""Local neural VO and original score. Run with kokoro-onnx, numpy, soundfile installed.
Model cache: JERP_TTS_MODEL_DIR or /workspace/.cache/jerp-tts-models.
No hosted TTS, no account, no external audio assets.
"""
from pathlib import Path
import os,json,subprocess,hashlib,re
import numpy as np
import soundfile as sf
import onnxruntime as ort
from kokoro_onnx import Kokoro
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'public/audio';DEST.mkdir(exist_ok=True)
CUES=DEST/'voiceover-cues';CUES.mkdir(exist_ok=True)
MODEL=Path(os.environ.get('JERP_TTS_MODEL_DIR','/workspace/.cache/jerp-tts-models'))
STORY=json.loads((ROOT/'public/story.json').read_text());SR=48000;DURATION=49
ort.disable_telemetry_events();opt=ort.SessionOptions();opt.intra_op_num_threads=3;opt.inter_op_num_threads=1;opt.log_severity_level=3
session=ort.InferenceSession(str(MODEL/'kokoro-v1.0.onnx'),sess_options=opt,providers=['CPUExecutionProvider'])
kokoro=Kokoro.from_session(session,str(MODEL/'voices-v1.0.bin'))
voice=np.zeros(SR*DURATION,dtype=np.float32);report=[];srt=[]
def stamp(t):
 m=int(round(t*1000));return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
for i,shot in enumerate(STORY['shots'],1):
 text=shot['vo'].replace('AI','A.I.').replace('JERP','Jerp')
 raw=CUES/f'{i:02d}-raw.wav';processed=CUES/f'{i:02d}.wav'
 if not raw.exists():
  print('SYNTH',i,text,flush=True)
  samples,rate=kokoro.create(text,voice='af_heart',speed=.94,lang='en-us',sentence_pause=.23,clause_pause=.1)
  sf.write(raw,samples,rate,subtype='PCM_16')
 samples,rate=sf.read(raw);duration=len(samples)/rate
 room=shot['end']-shot['start']-.58;tempo=max(1,duration/room)
 if tempo>1.25:raise RuntimeError(f'Cue {i}: required tempo {tempo:.3f} is too fast; edit pacing first')
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-af',f'atempo={tempo:.6f},afade=t=in:d=0.018,areverse,afade=t=in:d=0.045,areverse','-ar',str(SR),'-ac','1',str(processed)],check=True)
 cue,rate=sf.read(processed);start=shot['start']+.2;end=start+len(cue)/SR
 if end>shot['end']-.2:raise RuntimeError('Cue overlaps next scene')
 index=round(start*SR);voice[index:index+len(cue)]+=cue
 entry={'id':shot['id'],'text':shot['vo'],'start':round(start,3),'end':round(end,3),'raw_duration':round(duration,3),'tempo':round(tempo,4),'voice':'af_heart'};report.append(entry)
 # Exact cue envelope times; not claiming word-level forced alignment.
 text=shot['vo'];words=text.split();mid=len(words)//2
 if len(text)>65:text=' '.join(words[:mid])+'\n'+' '.join(words[mid:])
 srt.append(f'{i}\n{stamp(start)} --> {stamp(end)}\n{text}\n')
 print('CUE',entry,flush=True)
voice=voice/max(1,float(np.max(np.abs(voice)))/.85);sf.write(DEST/'voiceover.wav',voice,SR,subtype='PCM_24')
(ROOT/'output/jerp-film.srt').write_text('\n'.join(srt))
# Continuous original ambient-electronic bed. Reproducible oscillator synthesis.
rng=np.random.default_rng(131);t=np.arange(SR*DURATION)/SR;music=np.zeros((len(t),2),dtype=np.float64)
chords=[[146.832,220,261.626,329.628],[116.541,174.614,220,293.665],[130.813,196,261.626,293.665],[130.813,164.814,196,293.665]]
for idx,notes in enumerate(chords):
 start=idx*12.25;rel=t-start;env=np.clip(rel/2,0,1)*np.clip((14.5-rel)/3,0,1)
 for j,freq in enumerate(notes):
  for ch,detune in enumerate([-.001,.001]):
   oscill=np.sin(2*np.pi*freq*(1+detune)*t+j*.7)+.22*np.sin(2*np.pi*freq*2*t+.2)
   music[:,ch]+=.024*env*oscill*(.8+.2*np.sin(2*np.pi*.12*t+j))
for k in range(98):
 start=k*.5;beg=int(start*SR);n=min(int(1.5*SR),len(t)-beg);dt=np.arange(n)/SR
 freq=[293.665,440,523.251,659.255,440,349.228,523.251,440][k%8]
 env=(1-np.exp(-dt*100))*np.exp(-dt*5)
 pluck=.014*env*(np.sin(2*np.pi*freq*dt)+.18*np.sin(2*np.pi*freq*3*dt))
 pan=.25+.5*((k%3)/2);music[beg:beg+n,0]+=pluck*(1-pan);music[beg:beg+n,1]+=pluck*pan
# Restrained tactile transitions and a sonic mark; no external samples.
sfx=np.zeros_like(music)
for i,when in enumerate([4.8,9.8,13.8,18.8,24.8,30.8,36.8,41.8,45.7]):
 beg=int(when*SR);n=int(.6*SR);dt=np.arange(n)/SR;env=np.sin(np.pi*np.minimum(dt/.6,1))**2
 noise=rng.normal(0,1,n);smooth=np.convolve(noise,np.ones(9)/9,mode='same')
 breath=.023*smooth*env
 sfx[beg:beg+n,0]+=breath;sfx[beg:beg+n,1]+=np.roll(breath,240)
for when in [25.25,26.05,26.85,39.0]:
 beg=int(when*SR);n=int(.23*SR);dt=np.arange(n)/SR;tick=.022*np.sin(2*np.pi*1700*dt)*np.exp(-dt*35)
 sfx[beg:beg+n]+=tick[:,None]
for when,freq in [(14.3,587.33),(14.55,880),(46.05,587.33),(46.3,880)]:
 beg=int(when*SR);n=int(1.5*SR);dt=np.arange(n)/SR;mark=.025*np.sin(2*np.pi*freq*dt)*np.exp(-dt*3)*np.minimum(1,dt*60)
 sfx[beg:beg+n]+=mark[:,None]
fade=np.clip(t/1.4,0,1)*np.clip((49-t)/1.4,0,1)
music*=fade[:,None];sfx*=fade[:,None]
sf.write(DEST/'music.wav',music,SR,subtype='PCM_24');sf.write(DEST/'sfx.wav',sfx,SR,subtype='PCM_24')
metadata={'engine':'kokoro-onnx','voice':'af_heart','sample_rate':SR,'duration':49,'cues':report,'music':'Original deterministic additive synthesis; seed 131','model_sha256':hashlib.sha256((MODEL/'kokoro-v1.0.onnx').read_bytes()).hexdigest(),'voices_sha256':hashlib.sha256((MODEL/'voices-v1.0.bin').read_bytes()).hexdigest()}
(DEST/'provenance.json').write_text(json.dumps(metadata,indent=2)+'\n');print('AUDIO STEMS READY',flush=True)
