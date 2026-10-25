"""Contact sheet of actual rendered frames, not preproduction mockups."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]/'output';frames=[90,225,355,495,690,840,1030,1190,1400]
b=Image.new('RGB',(1920,1208),'#141416');d=ImageDraw.Draw(b);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
d.text((18,14),'JERP / THE UNSUPPORTED LEAP / ACTUAL RENDERED FRAMES',font=font,fill='#f5f5f7')
for i,f in enumerate(frames):
 p=Image.open(R/f'review-{f}.png').convert('RGB').resize((640,360),Image.Resampling.LANCZOS);x=i%3*640;y=48+i//3*384;b.paste(p,(x,y));d.text((x+12,y+362),f'{f/30:.2f}s',font=font,fill='#b9b9c3')
b.save(R/'contact-sheet.jpg',quality=94)
