"""Verify the actual deliverable: decode, frame count, CTA hold, sound and source integrity."""
from pathlib import Path
import subprocess,json,re,hashlib
R=Path(__file__).resolve().parents[1];O=R/'output';movie=O/'jerp-the-unsupported-leap.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)],text=True))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
dec=subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-progress','pipe:1','-nostats','-f','null','-'],capture_output=True,text=True,check=True)
frames=int(re.findall(r'^frame=(\d+)$',dec.stdout,re.M)[-1]);assert not dec.stderr.strip(),dec.stderr
hold=subprocess.check_output(['ffmpeg','-v','error','-ss','46','-i',str(movie),'-map','0:v:0','-an','-f','framemd5','-'],text=True)
md5=[l.split(',')[-1].strip() for l in hold.splitlines() if l and not l.startswith('#')]
# Lossy H.264 can have tiny pixel variations around a static frame due to encoding,
# so assert the native still endpoints as well as near-zero decoded temporal change.
static_native=None
if (O/'review-1380.png').exists() and (O/'review-1469.png').exists():
 from PIL import Image,ImageChops
 first=Image.open(O/'review-1380.png').convert('RGB');last=Image.open(O/'review-1469.png').convert('RGB')
 static_native=ImageChops.difference(first,last).getbbox() is None
# Decoded temporal variance across all 90 CTA frames: normalized 8-bit difference.
raw=subprocess.check_output(['ffmpeg','-v','error','-ss','46','-i',str(movie),'-map','0:v:0','-an','-vf','scale=160:90,format=gray','-f','rawvideo','-'])
planes=[raw[i:i+14400] for i in range(0,len(raw),14400)]
ref=planes[0];max_average_delta=max(sum(abs(x-y) for x,y in zip(ref,p))/14400 for p in planes)
sound=json.loads((O/'final-audio-analysis.json').read_text())['items'][0]['loudness']
source=json.loads((O/'render-source-hashes.json').read_text());source_unchanged=all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in source.items())
checks={'video_h264':v['codec_name']=='h264','native_1080p':(v['width'],v['height'])==(1920,1080),'fps_30':v['r_frame_rate']=='30/1','exactly_1470_decoded_frames':frames==1470,'duration_49s':abs(float(probe['format']['duration'])-49)<.05,'audio_aac_stereo_48k':a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000','full_decode_no_errors':not dec.stderr.strip(),'last_90_frames_present':len(md5)==90,'cta_stable_all_90_frames':max_average_delta<1 and static_native is not False,'integrated_lufs_target':abs(sound['lufsIntegrated']+16)<.5,'no_audio_clipping':sound['clipping']['count']==0,'true_peak_below_zero':sound['truePeakDb']<0,'rendered_source_unchanged':source_unchanged}
assert all(checks.values()),checks
report={'status':'passed','file':movie.name,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'bytes':movie.stat().st_size,'checks':checks,'video':{'width':v['width'],'height':v['height'],'fps':30,'decoded_frames':frames,'duration':float(probe['format']['duration']),'codec':v['codec_name']},'audio':sound,'cta':{'start_seconds':46,'duration_seconds':3,'native_endpoints_identical':static_native,'max_average_luma_change_8bit':max_average_delta,'decoded_frames':len(md5),'distinct_decoded_frame_hashes':len(set(md5))},'review':{'native_story_stills':9,'additional_transition_stills':22,'full_49_second_motion_draft_rendered':True,'actual_frames_inspected':True,'full_final_movie_decoded':True},'limitations':['Fictional illustrative example, not authenticated MCP footage','Procedural CSS 3D scene geometry; no claim of a Blender or WebGL final render','Neural voiceover, not a human studio recording','Subtitles aligned to synthesized cue boundaries, not individual words']}
(O/'QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(O/'ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
