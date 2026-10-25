/** Rebuild the complete movie from retained audio stems; no TTS-model download. */
import {spawnSync} from 'node:child_process';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');process.chdir(root);
function run(executable,args){const r=spawnSync(executable,args,{stdio:'inherit'});if(r.status!==0)process.exit(r.status??1)}
for(const stem of ['voiceover','music','sfx'])run('ffmpeg',['-y','-v','error','-i',`public/audio/${stem}.flac`,'-c:a','pcm_s24le',`public/audio/${stem}.wav`]);
run('python3',['scripts/mix_audio.py']);
run(process.execPath,['scripts/render.mjs',process.argv.includes('--draft')?'draft':'full']);
run(process.execPath,['scripts/mux.mjs',...(process.argv.includes('--draft')?['--draft']:[])]);
