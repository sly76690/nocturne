# NOCTURNE icon, in the family of the O6 and O8 badges: "NO", a condensed N and the ring O with its satellite.
# python3 tools/nocturne-logo.py  -> Source/Assets/orbit-icon.png (1024 px, the app icon and the panel badge)
from PIL import Image, ImageDraw, ImageFilter
import os
S=4; W=1024*S
night=(70,104,176,255); grey=(200,206,212,255); dark=(29,30,31,255); edge=(58,58,60,255)
def r(v): return int(v*S)
im=Image.new('RGBA',(W,W),(0,0,0,0))
sh=Image.new('RGBA',(W,W),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([r(102),r(114),r(922),r(934)],radius=r(176),fill=(0,0,0,70))
im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(r(6))))
box=[r(102),r(102),r(920),r(920)]
tile=Image.new('RGBA',(W,W),(0,0,0,0)); t=ImageDraw.Draw(tile)
t.rectangle([0,0,W,r(730)],fill=dark); t.rectangle([0,r(730),W,r(826)],fill=grey); t.rectangle([0,r(826),W,W],fill=night)
mask=Image.new('L',(W,W),0); ImageDraw.Draw(mask).rounded_rectangle(box,radius=r(176),fill=255)
im.paste(tile,(0,0),mask); d=ImageDraw.Draw(im); d.rounded_rectangle(box,radius=r(176),outline=edge,width=r(5))
# the N: condensed, same stroke and height as the 6 and the 8 of the family, in night blue
x0,x1,top,bot,st=258,421,258,582,54
d.rounded_rectangle([r(x0),r(top),r(x0+st),r(bot)],radius=r(18),fill=night)
d.rounded_rectangle([r(x1-st),r(top),r(x1),r(bot)],radius=r(18),fill=night)
d.polygon([(r(x0+4),r(top+6)),(r(x0+st+6),r(top)),(r(x1-4),r(bot-6)),(r(x1-st-6),r(bot))],fill=night)
# the O: the ring in light grey, its satellite in night blue with a dark halo
cx,cy=612,421
d.ellipse([r(cx-167),r(cy-167),r(cx+167),r(cy+167)],fill=grey); d.ellipse([r(cx-110),r(cy-110),r(cx+110),r(cy+110)],fill=dark)
sx,sy=cx+97,cy-97
d.ellipse([r(sx-44),r(sy-44),r(sx+44),r(sy+44)],fill=dark); d.ellipse([r(sx-28),r(sy-28),r(sx+28),r(sy+28)],fill=night)
root=os.path.join(os.path.dirname(__file__),'..')
im.resize((1024,1024),Image.LANCZOS).save(os.path.join(root,'Source/Assets/orbit-icon.png'))
