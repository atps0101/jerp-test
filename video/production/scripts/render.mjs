import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import fs from 'node:fs/promises';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const out=resolve(root,'output');await fs.mkdir(out,{recursive:true});
const mode=process.argv[2]||'full';
const serveUrl=await bundle({entryPoint:resolve(root,'entry.ts'),rootDir:root,publicDir:resolve(root,'public'),outDir:`/workspace/.cache/jerp-remotion-bundle-${mode}`,enableCaching:true});
const chromiumOptions={gl:'swiftshader',ignoreCertificateErrors:false,disableWebSecurity:false};
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium',chromiumOptions});
try{
 const composition=await selectComposition({serveUrl,id:'JerpFilm',puppeteerInstance:browser,chromiumOptions});
 console.log('COMPOSITION',JSON.stringify({width:composition.width,height:composition.height,fps:composition.fps,frames:composition.durationInFrames}));
 if(mode.startsWith('stills')){
  const frames=mode==='stills-motion'?[405,419,420,427,434,569,570,577,584,615,929,930,937,944,1110,1120,1137,1255,1260,1270,1380,1469]:[90,225,355,495,690,840,1030,1190,1400];
  for(const frame of frames){
   await renderStill({serveUrl,composition,frame,output:resolve(out,`review-${frame}.png`),puppeteerInstance:browser,chromiumOptions,imageFormat:'png',logLevel:'warn'});console.log('STILL',frame);
  }
 }else{
  const draft=mode==='draft';let last=-1;
  await renderMedia({serveUrl,composition,codec:'h264',outputLocation:resolve(out,draft?'review-draft.mp4':'silent.mp4'),puppeteerInstance:browser,chromiumOptions,concurrency:2,scale:draft?.5:1,everyNthFrame:draft?2:1,crf:draft?23:17,imageFormat:'jpeg',jpegQuality:draft?85:95,pixelFormat:'yuv420p',x264Preset:'fast',muted:true,logLevel:'warn',onProgress:p=>{const n=Math.floor(p.progress*20);if(n!==last){console.log('RENDER',Math.round(p.progress*100)+'%',p.renderedFrames,'frames');last=n;}}});
 }
}finally{await browser.close({silent:true})}
