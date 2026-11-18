# NOCTURNE icon: a night tile, a pale-gold crescent moon and a silver N that rises out of its hollow.
# python3 tools/nocturne-logo.py  -> Source/Assets/orbit-icon.png (1024 px, the app icon and the panel badge)
from PIL import Image, ImageDraw, ImageFilter
import os
S=4; W=1024*S
night=(17,21,34,255); band=(61,92,158,255); silver=(205,211,219,255); gold=(222,198,140,255); edge=(58,62,74,255)
def r(v): return int(v*S)
im=Image.new('RGBA',(W,W),(0,0,0,0))
sh=Image.new('RGBA',(W,W),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([r(102),r(114),r(922),r(934)],radius=r(176),fill=(0,0,0,80))
im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(r(6))))
box=[r(102),r(102),r(920),r(920)]
tile=Image.new('RGBA',(W,W),night); t=ImageDraw.Draw(tile)
for y in range(0,r(780)):  # a faint glow toward the top, like the sky before the night closes
    k=1-y/r(780); t.line([(0,y),(W,y)],fill=(int(17+14*k),int(21+18*k),int(34+30*k),255))
t.rectangle([0,r(790),W,r(826)],fill=silver); t.rectangle([0,r(826),W,W],fill=band)
# the crescent: a gold disc with a night disc taken out of it
moon=Image.new('L',(W,W),0); m=ImageDraw.Draw(moon)
cx,cy,R=390,430,250; m.ellipse([r(cx-R),r(cy-R),r(cx+R),r(cy+R)],fill=255)
ox,oy,Ro=500,360,225; m.ellipse([r(ox-Ro),r(oy-Ro),r(ox+Ro),r(oy+Ro)],fill=0)
tile.paste(Image.new('RGBA',(W,W),gold),(0,0),moon)
# a few stars
for x,y,s in [(700,215,9),(782,300,6),(640,140,5),(822,180,7)]:
    t.ellipse([r(x-s),r(y-s),r(x+s),r(y+s)],fill=silver)
# the N, in silver, standing in the hollow of the moon
x0,x1,y0,y1,st=520,760,380,690,62
t.rectangle([r(x0),r(y0),r(x0+st),r(y1)],fill=silver); t.rectangle([r(x1-st),r(y0),r(x1),r(y1)],fill=silver)
t.polygon([(r(x0),r(y0)),(r(x0+st*1.25),r(y0)),(r(x1),r(y1)),(r(x1-st*1.25),r(y1))],fill=silver)
mask=Image.new('L',(W,W),0); ImageDraw.Draw(mask).rounded_rectangle(box,radius=r(176),fill=255)
im.paste(tile,(0,0),mask); d=ImageDraw.Draw(im); d.rounded_rectangle(box,radius=r(176),outline=edge,width=r(5))
root=os.path.join(os.path.dirname(__file__),'..')
im.resize((1024,1024),Image.LANCZOS).save(os.path.join(root,'Source/Assets/orbit-icon.png'))
# the knob index line of the night-blue sections
idx=Image.open(os.path.join(root,'Source/Assets/skin/index_amber.png')).convert('RGBA');px=idx.load()
for y in range(idx.height):
    for x in range(idx.width):
        rr,gg,bb,a=px[x,y]
        if a>8: l=(rr+gg+bb)/3/255; px[x,y]=(int(120*l*1.5),int(160*l*1.5),int(235*l*1.5) if 235*l*1.5<255 else 255,a)
idx.save(os.path.join(root,'Source/Assets/skin/index_teal.png'))
