import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {abs, ArrowIcon, BrandFonts,C,fade,FrameChrome,Kicker,Logo,mix,move,Pill,ramp,Slab,SourceTab,Studio} from './design';

const Head:React.FC<{tool?:string;title:React.ReactNode;style?:React.CSSProperties}>=({tool,title,style})=><div style={{...abs,left:144,top:174,...style}}>{tool&&<Pill style={{marginBottom:23}}>{tool}</Pill>}<div style={{fontSize:68,fontWeight:600,lineHeight:1.08,letterSpacing:'-.025em'}}>{title}</div></div>;
const SourceContent:React.FC<{compact?:boolean;highlight?:number}>=({compact=false,highlight=0})=><div style={{padding:compact?'35px 38px':'42px 48px'}}><SourceTab style={{fontSize:compact?25:28}}/><div style={{height:1,background:'#ffffff15',margin:'25px 0 30px'}}/><div style={{fontSize:compact?35:47,fontWeight:600,lineHeight:1.12,marginBottom:30}}>Time tracking<br/>for your team</div><div style={{fontSize:compact?32:40,lineHeight:1.35}}><div style={{background:highlight>0?`${C.blue}18`:undefined,borderLeft:`3px solid ${highlight>0?C.blue:'transparent'}`,paddingLeft:highlight>0?15:0,marginBottom:22}}>Free trial available.</div><div style={{color:'#d0d0d8',fontSize:compact?30:36}}>A paid subscription is required after the trial.</div></div></div>;

const Leap:React.FC<{f:number}>=({f})=>{
 const bridge=ramp(f,142,189),macro=ramp(f,294,324);
 const sourceX=mix(775,165,bridge)-macro*45;
 const sourceY=mix(297,590,bridge)+macro*20;
 const sourceW=mix(1000,820,bridge),sourceH=mix(540,325,bridge);
 const intro=fade(f,4,25,144,166);
 const ribbon=fade(f,151,176);
 return <AbsoluteFill style={{perspective:1900,perspectiveOrigin:'50% 45%'}}>
 <div style={{...abs,left:144,top:229,width:560,opacity:intro,transform:`translateY(${move(f,0,30,35,0)}px)`}}><Kicker style={{marginBottom:27}}>A real decision</Kicker><div style={{fontSize:77,lineHeight:1.04,fontWeight:600,letterSpacing:'-.035em'}}>Choose a<br/>time tracker<br/>for our team.</div><div style={{marginTop:42,width:84,height:3,background:C.blue}}/></div>
 <Slab w={sourceW} h={sourceH} depth={18} light={.25+f/600} style={{left:sourceX,top:sourceY,transform:`translateZ(${mix(0,-80,bridge)}px) rotateX(${mix(0,51,bridge)}deg) rotateY(${mix(-7,0,bridge)}deg) rotateZ(${mix(0,-7,bridge)}deg) scale(${mix(.95,1,ramp(f,0,100))})`}}>
 <div style={{opacity:1-bridge}}><SourceContent highlight={f>90?1:0}/><div style={{...abs,left:48,right:48,bottom:38,display:'flex',gap:14}}>{[190,100,155].map((w,i)=><div key={i} style={{width:w,height:9,borderRadius:9,background:'#ffffff0c'}}/>)}</div></div>
 <div style={{...abs,left:42,top:45,opacity:bridge}}><Kicker style={{fontSize:25,marginBottom:24}}>The source</Kicker><div style={{fontSize:47,fontWeight:600}}>Free trial available.</div><div style={{fontSize:32,color:C.muted,marginTop:23,maxWidth:620}}>A paid subscription is required<br/>after the trial.</div></div>
 </Slab>
 <div style={{...abs,left:144,top:200,opacity:fade(f,151,174,295,314)}}><Kicker style={{marginBottom:20}}>The answer adds a promise</Kicker><div style={{fontSize:78,fontWeight:600,letterSpacing:'-.025em'}}>Beyond the source.</div></div>
 <div style={{...abs,left:144,top:198,opacity:fade(f,300,322)}}><div style={{fontSize:77,fontWeight:600,lineHeight:1.08,letterSpacing:'-.025em'}}>A confident answer<br/><span style={{color:C.muted}}>needs a source.</span></div></div>
 <div style={{...abs,left:mix(590,530,macro),top:mix(442,518,macro),width:1160,height:280,opacity:ribbon,transformStyle:'preserve-3d',transform:`translateY(${move(f,151,186,-60,0)}px) rotateY(-8deg) rotateZ(-3deg)`}}>
 <Slab w={1160} h={250} depth={13} light={f/500} fill='rgba(62,63,67,.94)' style={{transform:`rotateX(${mix(8,13,macro)}deg)`}}>
 <Kicker style={{...abs,left:40,top:28,fontSize:26}}>AI draft</Kicker>
 <div style={{...abs,left:40,top:95,fontSize:63,fontWeight:600,whiteSpace:'nowrap'}}>The best choice.</div><div style={{...abs,left:626,top:95,fontSize:63,fontWeight:600,whiteSpace:'nowrap'}}>Free forever.</div>
 <div style={{...abs,left:625,top:185,width:390,height:2,background:C.red,opacity:fade(f,190,215)}}/>
 </Slab>
 </div>
 <svg width='1920' height='1080' style={{...abs,inset:0,opacity:fade(f,205,230)}}><path d={`M ${mix(960,905,macro)} 710 L ${mix(960,905,macro)} 876`} stroke='#ffffff50' strokeWidth='1.5' strokeDasharray='5 9'/><path d={`M ${mix(985,930,macro)} 849 L 1645 849`} stroke='#ffffff1c' strokeWidth='1.5'/></svg>
 <div style={{...abs,left:mix(1020,960,macro),top:880,opacity:fade(f,210,235),fontSize:28,color:C.muted}}>No source beneath the promise.</div>
 </AbsoluteFill>;
};

const Guard:React.FC<{f:number}>=({f})=>{
 const p=ramp(f,12,67),scan=move(f,35,112,400,777);
 return <AbsoluteFill style={{perspective:1800}}><Head tool='guard' title='Screen incoming content.' style={{opacity:ramp(f,0,17)}}/>
 <svg width='1920' height='1080' style={{...abs,inset:0}}><path d='M 590 628 L 1320 628' stroke='#ffffff1b' strokeWidth='2'/><path d='M 620 628 L 1310 628' stroke={C.blue} strokeWidth='2' strokeDasharray='690' strokeDashoffset={690*(1-p)}/></svg>
 <Slab w={476} h={350} depth={12} style={{left:144,top:449,transform:`rotateY(${move(f,0,45,15,8)}deg) translateX(${move(f,0,40,-35,0)}px)`}}><div style={{padding:'36px 38px'}}><Kicker style={{fontSize:25,marginBottom:25}}>Source</Kicker><div style={{fontSize:39,fontWeight:600,lineHeight:1.2}}>Free trial available.</div><div style={{fontSize:32,color:C.muted,marginTop:25,lineHeight:1.3}}>A paid subscription is required after the trial.</div><SourceTab short style={{marginTop:25}}/></div></Slab>
 <Slab w={394} h={465} depth={20} light={f/150} fill='rgba(57,60,65,.94)' style={{left:765,top:391,transform:`rotateY(${move(f,0,48,-27,-8)}deg) translateZ(${move(f,0,40,-140,30)}px)`}}><div style={{display:'flex',flexDirection:'column',alignItems:'center',paddingTop:116}}><Logo size={103}/><div style={{height:1,width:250,background:'#ffffff20',margin:'40px 0 29px'}}/><Pill>guard</Pill></div><div style={{...abs,left:0,right:0,top:scan-391,height:2,background:'linear-gradient(90deg,transparent,#80bfff,transparent)',opacity:fade(f,28,44,112,130),boxShadow:'0 -20px 36px #0a84ff30'}}/></Slab>
 <Slab w={450} h={270} depth={12} style={{left:1325,top:490,transform:'rotateY(-8deg)',opacity:ramp(f,13,38)}}><div style={{padding:36}}><Kicker style={{fontSize:25,marginBottom:25}}>Before the answer</Kicker><div style={{fontSize:40,lineHeight:1.15,fontWeight:600}}>Check what<br/>comes in.</div><div style={{height:9,width:214,background:'#ffffff15',borderRadius:10,marginTop:30}}/></div></Slab>
 <div style={{...abs,left:640,top:590,width:14,height:14,borderRadius:4,background:C.blue,opacity:fade(f,28,40,119,131),transform:`translateX(${move(f,28,112,0,650)}px) rotate(45deg)`,boxShadow:'0 0 20px #0a84ff40'}}/>
 </AbsoluteFill>;
};

const claims=[{claim:'Free trial',status:'true',reason:'Supported by source',color:C.green},{claim:'Free forever',status:'false',reason:'Contradicted by source',color:C.red},{claim:'Best choice',status:'not_fact',reason:'Opinion',color:'#ccc9d6'}];
const Verdict:React.FC<{f:number}>=({f})=>{
 const settled=ramp(f,0,53),results=f>=180;
 return <AbsoluteFill><Head tool='verdict' title={results?'Know the difference.':'Check each claim against its source.'}/>
 <svg width='1920' height='1080' style={{...abs,inset:0}}>
 {[{d:'M 829 455 C 970 455, 989 575, 1100 575',at:60,color:C.blue},{d:'M 829 654 C 980 654, 981 710, 1100 710',at:90,color:C.blue}].map((path,i)=><g key={i} opacity={ramp(f,path.at,path.at+25)}><path d={path.d} stroke='#ffffff0c' strokeWidth='11' fill='none'/><path d={path.d} stroke={path.color} strokeOpacity='.65' strokeWidth='2' fill='none' strokeDasharray='370' strokeDashoffset={370*(1-ramp(f,path.at,path.at+30))}/><circle cx='1100' cy={i?710:575} r='6' fill={C.blue}/></g>)}
 </svg>
 <Slab w={685} h={172} depth={8} style={{left:144,top:564,opacity:fade(f,0,8,22,39)}}><div style={{padding:'26px 32px'}}><Kicker style={{fontSize:25,marginBottom:16}}>AI draft</Kicker><div style={{fontSize:40,fontWeight:600}}>Free forever. Best choice.</div></div></Slab>
 <div style={{...abs,left:144,top:367,width:685,perspective:1600}}>{claims.map((c,i)=>{const start=i===0?8:i===1?20:29;const enter=ramp(f,start,start+35),active=ramp(f,182+i*15,197+i*15);return <Slab key={c.claim} w={685} h={172} depth={8} light={.15+f/500} style={{top:i*197,opacity:ramp(f,start,start+12),transform:`translateX(${i===0?(1-enter)*957:0}px) translateY(${(1-enter)*(i===0?170:i===1?0:-197)}px) rotateY(${(1-enter)*(i===0?-12:8)}deg) scale(${mix(i===0?.85:1,1,enter)})`}}><div style={{padding:'29px 32px'}}><div style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}><div style={{fontSize:45,fontWeight:600}}>{c.claim}</div><div style={{opacity:active,fontSize:29,padding:'7px 15px',borderRadius:12,color:c.color,background:`${c.color}12`,border:`1px solid ${c.color}44`}}>{c.status}</div></div><div style={{fontSize:29,marginTop:18,color:active?c.color:C.muted,opacity:mix(.72,1,active)}}>{active>0?c.reason:i===0?'From the source':'From the AI draft'}</div></div></Slab>;})}</div>
 <Slab w={674} h={564} depth={11} style={{left:1101,top:367,opacity:ramp(f,0,25),transform:`perspective(1400px) rotateY(${(1-settled)*-8}deg)`}}>
 <div style={{padding:'31px 37px'}}><SourceTab style={{fontSize:28}}/><div style={{height:1,background:'#ffffff18',margin:'26px 0 29px'}}/><Kicker style={{fontSize:23,marginBottom:20}}>Source excerpt</Kicker>
 <div style={{fontSize:37,lineHeight:1.28,padding:'17px 19px',borderRadius:13,borderLeft:`3px solid ${C.blue}`,background:`${C.blue}${f>60?'14':'00'}`}}>Free trial available.</div>
 <div style={{fontSize:37,lineHeight:1.28,padding:'20px 19px',borderRadius:13,borderLeft:`3px solid ${C.blue}`,background:`${C.blue}${f>90?'14':'00'}`,marginTop:23}}>A paid subscription is required after the trial.</div>
 <div style={{fontSize:27,color:C.muted,marginTop:34}}>An opinion is not a factual condition.</div></div>
 </Slab>
 </AbsoluteFill>;
};

const FactsText:React.FC=()=> <div style={{padding:'30px 38px'}}><Kicker color='#9bcaff' style={{fontSize:25,marginBottom:23}}>Sourced facts</Kicker><div style={{fontSize:38,lineHeight:1.23,fontWeight:600}}>Free trial available.</div><div style={{width:'100%',height:1,background:'#ffffff15',margin:'21px 0'}}/><div style={{fontSize:35,lineHeight:1.24}}>Paid subscription required<br/>after the trial.</div><SourceTab style={{marginTop:28,fontSize:27}}/></div>;
const CompactFacts:React.FC<{w:number;h:number;style?:React.CSSProperties;light?:number}>=({w,h,style,light})=><Slab w={w} h={h} depth={12} light={light} style={style} fill='rgba(47,52,59,.98)'><FactsText/></Slab>;
const Speaker:React.FC<{f:number}>=({f})=>{
 const travel=ramp(f,10,67),fold=ramp(f,0,45);
 return <AbsoluteFill style={{perspective:1700}}><Head tool='speaker' title='Sourced facts. Less to read.'/>
 <Slab w={487} h={459} depth={12} style={{left:144,top:395,opacity:mix(1,.48,travel),transform:`rotateY(${mix(0,10,travel)}deg)`}}><div style={{padding:'34px 34px'}}><SourceTab style={{fontSize:24}}/><div style={{fontSize:36,fontWeight:600,marginTop:27,lineHeight:1.1}}>Time tracking<br/>for your team</div><div style={{fontSize:27,lineHeight:1.25,marginTop:26}}>Free trial available.</div><div style={{fontSize:25,lineHeight:1.25,marginTop:18}}>A paid subscription is required<br/>after the trial.</div>{[354,310,345].map((w,i)=><div key={i} style={{width:w,height:8,marginTop:20,background:'#ffffff12',borderRadius:10}}/>)}</div></Slab>
 <div style={{...abs,left:144,top:887,fontSize:26,color:C.muted}}>The full page stays outside.</div>
 <div style={{...abs,left:935,top:381,width:840,height:500,border:'1px solid #ffffff28',borderRadius:32,background:'#ffffff02',opacity:ramp(f,2,28)}}><div style={{...abs,top:-18,left:30,padding:'0 14px',background:C.bg,fontSize:25,color:C.muted,letterSpacing:'.06em'}}>AI CONTEXT</div><div style={{...abs,bottom:23,left:40,fontSize:27,color:C.muted}}>Within your requested size limit</div></div>
 <svg width='1920' height='1080' style={{...abs,inset:0,opacity:fade(f,28,45,110,130)}}><path d='M 625 610 L 935 610' fill='none' stroke={C.blue} strokeWidth='2' strokeDasharray='6 9'/></svg>
 <div style={{...abs,left:mix(269,976,travel),top:mix(465,431,travel),width:758,height:350,transformStyle:'preserve-3d',transform:`rotateY(${Math.sin(travel*Math.PI)*-14}deg)`}}>
 {[-1,1].map(side=><Slab key={side} w={155} h={350} depth={8} fill='rgba(49,51,55,.96)' style={{left:side===-1?-155:758,top:0,transformOrigin:side===-1?'right':'left',transform:`translateZ(-9px) rotateY(${side*mix(0,-178,fold)}deg)`,opacity:1-ramp(f,42,67)}}><div style={{padding:21}}>{[70,110,95,82,110,65,92,110].map((w,i)=><div key={i} style={{width:w,height:6,background:'#ffffff20',borderRadius:6,marginTop:25}}/>)}</div></Slab>)}
 <Slab w={758} h={135} depth={8} style={{left:0,top:350,transformOrigin:'top',transform:`translateZ(-9px) rotateX(${mix(0,176,fold)}deg)`,opacity:1-ramp(f,35,60)}}><div style={{padding:30}}>{[620,550,580].map((w,i)=><div key={i} style={{width:w,height:7,background:'#ffffff14',borderRadius:6,marginTop:14}}/>)}</div></Slab>
 <CompactFacts w={758} h={350} light={f/180} style={{left:0,top:0}}/>
 </div>
 </AbsoluteFill>;
};

const Answer:React.FC<{f:number}>=({f})=>{
 const open=ramp(f,24,50),morph=ramp(f,0,27),end=ramp(f,138,150);
 return <AbsoluteFill><Head title='An answer you can inspect.' style={{top:190,opacity:ramp(f,5,22)*(1-end)}}/>
 <div style={{...abs,left:935,top:381,width:840,height:500,border:'1px solid #ffffff28',borderRadius:32,opacity:1-ramp(f,0,18)}}><div style={{...abs,top:-18,left:30,padding:'0 14px',background:C.bg,fontSize:25,color:C.muted}}>AI CONTEXT</div></div>
 <Slab w={mix(758,1000,morph)} h={mix(350,489,morph)} depth={12} light={.4+f/300} fill='rgba(47,52,59,.98)' style={{left:mix(976,144,morph),top:mix(431,355,morph),opacity:1-end,transform:`perspective(1700px) rotateY(${Math.sin(morph*Math.PI)*9}deg)`}}><div style={{...abs,inset:0,opacity:1-ramp(f,8,18)}}><FactsText/></div><div style={{padding:'40px 47px',opacity:ramp(f,12,27)}}><Kicker style={{fontSize:26,marginBottom:32}}>Your AI · sourced answer</Kicker><div style={{fontSize:53,lineHeight:1.22,fontWeight:600,letterSpacing:'-.01em'}}>The page offers a free trial.</div><div style={{fontSize:49,lineHeight:1.25,marginTop:24,color:'#e1e1e8'}}>A paid subscription is<br/>required afterward.</div><div style={{marginTop:39,display:'inline-flex',padding:'15px 20px',border:`1px solid ${C.blue}77`,borderRadius:13,background:`${C.blue}10`}}><SourceTab style={{fontSize:29}}/></div></div></Slab>
 <svg width='1920' height='1080' style={{...abs,inset:0,opacity:open*(1-end)}}><path d='M 628 744 C 1010 744, 1090 545, 1203 545' stroke={C.blue} strokeWidth='2' fill='none'/><circle cx='1203' cy='545' r='5' fill={C.blue}/></svg>
 <Slab w={572} h={425} depth={10} light={.7} style={{left:mix(1204,960,end),top:mix(417,620,end),opacity:open*(1-end),transformOrigin:'0 0',transform:`perspective(1500px) rotateY(${mix(-18,0,open)}deg) translateX(${(1-open)*-50}px) scale(${1-end})`}}><div style={{padding:'33px 35px'}}><Kicker color='#9bcaff' style={{fontSize:24,marginBottom:27}}>The original source</Kicker><div style={{fontSize:36,lineHeight:1.28}}>Free trial available.</div><div style={{width:55,height:2,background:C.blue,margin:'25px 0'}}/><div style={{fontSize:36,lineHeight:1.28}}>A paid subscription is required after the trial.</div><SourceTab style={{fontSize:24,marginTop:29}}/></div></Slab>
 <div style={{...abs,left:144,right:144,top:430,textAlign:'center',fontSize:92,fontWeight:600,lineHeight:1.1,letterSpacing:'-.035em',opacity:ramp(f,142,150)}}>No source, no claim.</div>
 <div style={{...abs,left:952,top:612,width:16,height:16,borderRadius:'50%',background:C.blue,opacity:ramp(f,140,150)}}/>
 </AbsoluteFill>;
};
const Closing:React.FC<{f:number}>=({f})=>{
 const brand=ramp(f,38,60),cta=ramp(f,101,120);
 return <AbsoluteFill>
 <div style={{...abs,left:952,top:612,width:16,height:16,borderRadius:'50%',background:C.blue,opacity:1-ramp(f,0,18),transform:`scale(${1-ramp(f,0,18)})`}}/>
 <div style={{...abs,left:144,right:144,top:move(f,37,62,430,243),textAlign:'center',fontSize:92,fontWeight:600,lineHeight:1.1,letterSpacing:'-.035em',opacity:1-ramp(f,41,58)}}>No source, no claim.</div>
 <div style={{...abs,inset:0,display:'flex',flexDirection:'column',alignItems:'center',opacity:brand,transform:`translateY(${(1-brand)*30}px)`}}><Logo size={240} orb style={{marginTop:247}}/><div style={{fontSize:54,fontWeight:400,marginTop:36,letterSpacing:'-.01em'}}>Confidence in the Truth</div><div style={{fontSize:32,color:C.muted,marginTop:29,opacity:cta}}>Stop guessing. Start checking.</div><div style={{display:'flex',alignItems:'center',gap:35,marginTop:48,opacity:cta}}><div style={{fontSize:33,fontWeight:600,padding:'21px 44px',borderRadius:22,background:C.blue,boxShadow:'inset 0 1px 0 #ffffff55'}}>Try Free <ArrowIcon size={27} style={{marginLeft:24,verticalAlign:'middle'}}/></div><div style={{fontSize:34,color:'#d4d4dc'}}>getjerp.com</div></div></div>
 </AbsoluteFill>;
};

/** A traveling glass edge reveals the next stage while the previous stage remains in space. */
const PlaneCut:React.FC<{f:number;reverse?:boolean;before:React.ReactNode;children:React.ReactNode}>=({f,reverse=false,before,children})=>{
 const frame=useCurrentFrame();
 const p=ramp(f,0,14),edge=reverse?1920*(1-p):1920*p;
 return <AbsoluteFill>{p<1&&<AbsoluteFill style={{transform:`perspective(2200px) translateZ(${-30*p}px)`}}>{before}</AbsoluteFill>}<AbsoluteFill style={{clipPath:reverse?`inset(0 0 0 ${(1-p)*100}%)`:`inset(0 ${(1-p)*100}% 0 0)`}}><Studio f={frame}/>{children}</AbsoluteFill>{p<1&&<div style={{...abs,left:edge-1,top:135,width:3,height:790,background:'linear-gradient(transparent,rgba(255,255,255,.5) 25%,rgba(255,255,255,.2) 75%,transparent)',boxShadow:'-28px 0 60px 20px #ffffff05'}}/>}</AbsoluteFill>;
};

export const JerpFilm:React.FC=()=>{
 const f=useCurrentFrame();
 const shot=f<150?'01':f<300?'02':f<420?'03':f<570?'04':f<750?'05':f<930?'06':f<1110?'07':f<1260?'08':'09';
 const chapter=f<150?'The real task':f<300?'The unsupported leap':f<420?'Confidence needs evidence':f<570?'Before the answer':f<930?'Claims → sources':f<1110?'Compact, traceable context':'An answer you can inspect';
 return <AbsoluteFill style={{fontFamily:'Barlow',color:C.ink,fontWeight:400,overflow:'hidden',background:C.bg}}><BrandFonts/><Studio f={f}/>{f<420?<Leap f={f}/>:f<570?<PlaneCut f={f-420} before={<Leap f={419}/>}><Guard f={f-420}/></PlaneCut>:f<930?<PlaneCut f={f-570} before={<Guard f={149}/>}><Verdict f={f-570}/></PlaneCut>:f<1110?<PlaneCut f={f-930} reverse before={<Verdict f={359}/>}><Speaker f={f-930}/></PlaneCut>:f<1260?<Answer f={f-1110}/>:<Closing f={Math.min(f-1260,120)}/>}<FrameChrome f={f} shot={shot} chapter={chapter}/></AbsoluteFill>;
};
