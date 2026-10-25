import React, {useEffect, useState} from 'react';
import {AbsoluteFill, cancelRender, continueRender, delayRender, Easing, Img, interpolate, staticFile} from 'remotion';

export const C = {bg:'#1c1c1e', surface:'#2c2c2e', ink:'#f5f5f7', muted:'#b9b9c3', blue:'#0a84ff', red:'#ff6b6b', green:'#91c5ff'};
export const ease = Easing.bezier(.23,1,.32,1);
export const spatial = Easing.bezier(.2,0,0,1);
export const ramp=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:ease});
export const mix=(a:number,b:number,t:number)=>a+(b-a)*t;
export const move=(f:number,a:number,b:number,from:number,to:number)=>mix(from,to,ramp(f,a,b));
export const fade=(f:number,a:number,b:number,c=99999,d=100000)=>ramp(f,a,b)*(1-ramp(f,c,d));
export const px=(n:number)=>`${n}px`;
export const abs:React.CSSProperties={position:'absolute'};

export const BrandFonts:React.FC=()=>{
 const [handle]=useState(()=>delayRender('Loading original JERP brand fonts'));
 useEffect(()=>{let active=true; Promise.all([
  ['Barlow','barlow-400.woff2','400'],['Barlow','barlow-600.woff2','600'],['Barlow','barlow-900.woff2','900'],['Bitcount','bitcount-latin.woff2','200'],
 ].map(async([family,file,weight])=>{const face=new FontFace(family,`url(${staticFile(`brand/${file}`)})`,{weight});await face.load();document.fonts.add(face);})).then(()=>{if(active)continueRender(handle);}).catch(e=>cancelRender(e));return()=>{active=false;};},[handle]);
 return null;
};
export const Logo:React.FC<{size?:number;style?:React.CSSProperties;orb?:boolean}>=({size=58,style,orb=false})=><div style={{display:'flex',alignItems:'center',gap:size*.14,...style}}><div style={{fontFamily:'Bitcount',fontSize:size,fontWeight:200,letterSpacing:'.04em',lineHeight:1,WebkitTextStroke:'.012em currentColor',textShadow:'.033em 0 0 currentColor, -.033em 0 0 currentColor, 0 .033em 0 currentColor, 0 -.033em 0 currentColor, .024em .024em 0 currentColor, -.024em .024em 0 currentColor, .024em -.024em 0 currentColor, -.024em -.024em 0 currentColor'}}>JERP</div>{orb&&<Img src={staticFile('brand/favicon.svg')} style={{width:size*.25,height:size*.25,marginTop:size*.02}}/>}</div>;
export const Kicker:React.FC<{children:React.ReactNode;color?:string;style?:React.CSSProperties}>=({children,color=C.muted,style})=><div style={{fontSize:28,fontWeight:600,letterSpacing:'.09em',textTransform:'uppercase',color,...style}}>{children}</div>;
export const Pill:React.FC<{children:React.ReactNode;color?:string;style?:React.CSSProperties}>=({children,color=C.blue,style})=><div style={{display:'inline-flex',alignItems:'center',gap:12,fontSize:29,lineHeight:1.1,border:`1px solid ${color}66`,borderRadius:30,padding:'12px 22px',background:`${color}13`,color,...style}}><span style={{width:7,height:7,borderRadius:'50%',background:color}}/>{children}</div>;
export const ArrowIcon:React.FC<{size?:number;style?:React.CSSProperties}>=({size=23,style})=><svg width={size} height={size} viewBox='0 0 24 24' fill='none' style={{flexShrink:0,...style}}><path d='M5 19L19 5M5 5H19V19' stroke='currentColor' strokeWidth='1.8' strokeLinecap='round' strokeLinejoin='round'/></svg>;
export const SourceTab:React.FC<{style?:React.CSSProperties;short?:boolean}>=({style,short=false})=><div style={{display:'flex',alignItems:'center',gap:13,color:'#b6d8ff',fontSize:27,...style}}><span style={{display:'inline-block',width:18,height:20,border:`1.5px solid ${C.blue}`,borderRadius:4,position:'relative'}}><span style={{position:'absolute',top:5,left:4,width:8,height:1,background:C.blue}}/><span style={{position:'absolute',top:10,left:4,width:8,height:1,background:C.blue}}/></span>{short?'Source':'northstar.example/product'}<ArrowIcon/></div>;

/** Six CSS planes form an actual prism. The top, underside and four edges share a world transform. */
export const Slab:React.FC<{w:number;h:number;depth?:number;children?:React.ReactNode;style?:React.CSSProperties;fill?:string;light?:number;radius?:number}>=({w,h,depth=10,children,style,fill='rgba(48,48,51,.95)',light=.5,radius=28})=>{
 const edge=`linear-gradient(90deg,rgba(255,255,255,.2),rgba(90,100,112,.32),rgba(255,255,255,.08))`;
 return <div style={{position:'absolute',width:w,height:h,transformStyle:'preserve-3d',...style}}>
 <div style={{...abs,inset:0,borderRadius:radius,background:'#202023',transform:`translateZ(-${depth}px)`,boxShadow:'0 48px 70px rgba(0,0,0,.32)'}}/>
 <div style={{...abs,left:radius,top:0,width:w-radius*2,height:depth,background:edge,transformOrigin:'top',transform:'rotateX(-90deg)'}}/>
 <div style={{...abs,left:radius,top:h,width:w-radius*2,height:depth,background:edge,transformOrigin:'top',transform:'rotateX(-90deg)'}}/>
 <div style={{...abs,left:0,top:radius,width:depth,height:h-radius*2,background:edge,transformOrigin:'left',transform:'rotateY(90deg)'}}/>
 <div style={{...abs,left:w,top:radius,width:depth,height:h-radius*2,background:edge,transformOrigin:'left',transform:'rotateY(90deg)'}}/>
 <div style={{...abs,inset:0,borderRadius:radius,background:fill,border:'1px solid rgba(255,255,255,.2)',boxShadow:'inset 0 2px 1px rgba(255,255,255,.12), inset 0 -2px 6px rgba(0,0,0,.22)',overflow:'hidden',backfaceVisibility:'hidden'}}>
  <div style={{...abs,inset:0,pointerEvents:'none',background:`radial-gradient(ellipse at ${light*100}% -50%,rgba(255,255,255,.16),transparent 67%),linear-gradient(125deg,rgba(255,255,255,.025),transparent 50%)`}}/>{children}
 </div></div>;
};

export const Studio:React.FC<{f:number}>=({f})=>{
 const t=Math.min(f,1380);return <AbsoluteFill style={{background:C.bg,overflow:'hidden'}}>
 <div style={{...abs,width:1600,height:1100,top:-720,left:mix(-350,250,t/1380),borderRadius:'50%',background:'radial-gradient(ellipse,rgba(255,255,255,.18),transparent 68%)',transform:'rotate(-12deg)'}}/>
 <div style={{...abs,width:1300,height:800,top:570,left:mix(500,200,t/1380),borderRadius:'50%',background:'radial-gradient(ellipse,rgba(90,104,128,.09),transparent 66%)'}}/>
 <div style={{...abs,inset:0,background:'radial-gradient(ellipse at 50% 35%,transparent 25%,rgba(0,0,0,.26) 100%)'}}/>
 <div style={{...abs,left:144,right:144,bottom:146,height:1,background:'linear-gradient(90deg,transparent,rgba(255,255,255,.09),transparent)'}}/>
 </AbsoluteFill>;
};
export const FrameChrome:React.FC<{f:number;shot:string;chapter:string}>=({f,shot,chapter})=><>
 <Logo size={50} style={{...abs,left:144,top:68,opacity:fade(f,0,20,1250,1260)}}/>
 <div style={{...abs,right:144,top:77,display:'flex',gap:20,alignItems:'center',opacity:fade(f,0,20,1250,1260)}}><span style={{fontSize:24,color:'#9999a4',letterSpacing:'.09em'}}>THE UNSUPPORTED LEAP</span><span style={{width:32,height:1,background:'#5e5e65'}}/><span style={{fontSize:27,color:C.muted}}>{shot}</span></div>
 {f<1260&&<div style={{...abs,left:144,right:144,bottom:67,display:'flex',justifyContent:'space-between',alignItems:'center'}}><div style={{fontSize:26,color:'#a6a6b1'}}>Illustrative example · fictional vendor</div><div style={{fontSize:25,color:'#898992'}}>{chapter}</div></div>}
 </>;
