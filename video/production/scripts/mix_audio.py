"""Ducked, two-pass loudness-normalized mix. Uses only authored local stems."""
import subprocess,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'public/audio';O=R/'output'
graph='[0:a]highpass=f=75,lowpass=f=10500,acompressor=threshold=0.12:ratio=2.2:attack=8:release=100:makeup=1.1,volume=2.2,asplit[v][sc];[1:a]volume=0.45[bed];[bed][sc]sidechaincompress=threshold=0.025:ratio=5:attack=25:release=350:makeup=1[duck];[2:a]volume=0.85[sfx];[v][duck][sfx]amix=inputs=3:normalize=0:duration=longest,afade=t=out:st=48.65:d=0.35[mix]'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(A/'voiceover.wav'),'-i',str(A/'music.wav'),'-i',str(A/'sfx.wav'),'-filter_complex',graph,'-map','[mix]','-ar','48000','-ac','2','-c:a','pcm_s24le',str(O/'premix.wav')],check=True)
first=subprocess.run(['ffmpeg','-hide_banner','-i',str(O/'premix.wav'),'-af','loudnorm=I=-16:TP=-1.2:LRA=8:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
measured=json.loads(re.findall(r'\{\s*"input_i".*?\}',first.stderr,re.S)[-1]);(O/'mix-loudness-pass1.json').write_text(json.dumps(measured,indent=2))
filt='loudnorm=I=-16:TP=-1.2:LRA=8:linear=true:print_format=json:'+':'.join(f'{a}={measured[b]}' for a,b in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])
second=subprocess.run(['ffmpeg','-y','-hide_banner','-i',str(O/'premix.wav'),'-af',filt,'-ar','48000','-ac','2','-c:a','pcm_s24le',str(O/'master-audio.wav')],capture_output=True,text=True,check=True)
report=json.loads(re.findall(r'\{\s*"input_i".*?\}',second.stderr,re.S)[-1]);(O/'mix-loudness-pass2.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
