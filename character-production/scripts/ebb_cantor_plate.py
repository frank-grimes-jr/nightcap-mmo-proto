"""Compose the character plate, block proofs, and matched silhouette review."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np
O=Path(__file__).resolve().parents[1]/'output/dark-elf-female/ebb-cantor';R=O/'Review'
def font(name,sz):return ImageFont.truetype('C:/Windows/Fonts/'+name+'.ttf',sz)
def text(d,p,s,n,color,face='bahnschrift'):d.text(p,s,font=font(face,n),fill=color,anchor='lt')
def caps(d,p,s,n,color):
    x,y=p;f=font('bahnschrift',n)
    for char in s:
        d.text((x,y),char,font=f,fill=color,anchor='lt');x+=d.textlength(char,font=f)+1.9
def place(canvas,obj,box,crop=True):
    if crop:obj=obj.crop(obj.getbbox())
    x,y,w,h=box;f=min(w/obj.width,h/obj.height)
    obj=obj.resize((round(obj.width*f),round(obj.height*f)),Image.Resampling.LANCZOS)
    canvas.paste(obj,(round(x+(w-obj.width)/2),round(y+(h-obj.height)/2)),obj)
def pic(n):return Image.open(R/(n+'.png')).convert('RGBA')
def plate():
    x,y=np.meshgrid(np.arange(1480),np.arange(945))
    k=np.clip(1-np.hypot((x-316)/620,(y-318)/850),0,1)
    im=Image.fromarray(np.uint8(np.array([33,45,45])+k[:,:,None]*[47,50,46]));d=ImageDraw.Draw(im)
    d.rectangle((684,0,1480,945),fill='#e7e2d5')
    caps(d,(47,35),'NIGHTCAP',22,'#f0e7d4');caps(d,(438,40),'CHARACTER STUDY',13,'#c9cbc1')
    d.line((47,74,637,74),fill='#92988c')
    sh=Image.new('RGBA',im.size);sd=ImageDraw.Draw(sh);sd.ellipse((201,857,453,876),fill=(14,19,20,120))
    sh=sh.filter(ImageFilter.GaussianBlur(9));im.paste(sh,(0,0),sh)
    place(im,pic('Three-quarter'),(38,91,604,778))
    d.line((47,889,637,889),fill='#92988c');caps(d,(47,906),'FEMALE DARK ELF',13,'#dad9c9')
    caps(d,(500,906),'BIND POSE',13,'#dad9c9')
    caps(d,(734,40),'KNELLWATER POLDER',16,'#865444')
    text(d,(726,85),'Ebb Cantor',89,'#233737','georgia')
    text(d,(735,191),'Vestments for binding the drowned',27,'#5a6157','georgiai')
    d.line((736,243,1427,243),fill='#a8a394')
    place(im,pic('Vessels'),(720,258,724,440),False)
    d.line((736,714,1427,714),fill='#a8a394')
    caps(d,(736,737),'THE FUNERAL ROAD',14,'#78503e')
    core=Image.open(O/'Textures/Ebb-Procession.png')
    cloth=core.crop((258,1122,990,1338)).resize((690,143),Image.Resampling.LANCZOS)
    im.paste(cloth,(736,771))
    im.save(R/'Ebb-Cantor.jpg',quality=96,subsampling=0)
def proof():
    im=Image.new('RGB',(1400,845),'#ece7dc');d=ImageDraw.Draw(im)
    text(d,(48,40),'The cantor’s blocks',52,'#243532','georgia')
    caps(d,(48,123),'PRINT AND SLIP PROOFS',15,'#745a47')
    procession=Image.open(O/'Textures/Ebb-Procession.png')
    chart=Image.open(O/'Textures/Ebb-Pall.png');pots=Image.open(O/'Textures/Ebb-Stoneware.png')
    im.paste(procession.crop((180,1032,1484,1400)).resize((1304,303)),(48,167))
    text(d,(49,482),'Four bearers carry a shrouded body along the exposed steps.',22,'#3c4841','georgiai')
    im.paste(chart.crop((1270,578,1530,904)).resize((229,261)),(48,549))
    im.paste(pots.crop((15,125,828,285)).resize((836,165)),(444,569))
    text(d,(297,577),'The roofless',22,'#3c4841','georgia');text(d,(297,610),'bell gable',22,'#3c4841','georgia')
    text(d,(444,751),'Three kiln stamps identify the sealed mouth, the stair and the witness.',22,'#3c4841','georgiai')
    im.save(R/'Block-proofs.jpg',quality=96,subsampling=0)
def comparison():
    im=Image.new('RGB',(1200,775),'#e5e0d4');d=ImageDraw.Draw(im)
    for j,(p,label) in enumerate([(O.parent/'vesper-moth/Review/Front.png','Vesper Moth'),(R/'Front.png','Ebb Cantor')]):
        src=Image.open(p).convert('RGBA');alpha=src.getchannel('A')
        sil=Image.new('RGBA',src.size,'#354343');sil.putalpha(alpha)
        place(im,sil,(j*600+38,27,520,635))
        d.line((j*600+42,690,j*600+554,690),fill='#959687')
        text(d,(j*600+42,711),label,30,'#283936','georgia')
    im.save(R/'Silhouettes.jpg',quality=92)
if __name__=='__main__':plate();proof();comparison()
