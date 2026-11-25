"""Compose the outfit plate and matched-scale costume comparison from Blender renders."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter

R=Path(__file__).resolve().parents[1]/'output/dark-elf-female/vesper-moth/Review'
def font(file,size):return ImageFont.truetype('C:/Windows/Fonts/'+file+'.ttf',size)
def label(draw,x,y,txt,size=16,color='#dbcbb7',gap=2):
    ft=font('bahnschrift',size)
    for letter in txt:
        draw.text((x,y),letter,fill=color,font=ft,anchor='lt');x+=draw.textlength(letter,font=ft)+gap
def paste(canvas,img,rect):
    x,y,w,h=rect;im=img.crop(img.getbbox());ratio=min(w/im.width,h/im.height)
    im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS)
    canvas.paste(im,(round(x+(w-im.width)/2),round(y+(h-im.height)/2)),im)
def plate():
    w,h=1460,925;y,x=np.mgrid[:h,:w]
    k=np.clip(1-np.hypot((x-338)/620,(y-306)/870),0,1)
    im=Image.fromarray(np.uint8(np.array([29,27,34])+k[:,:,None]*[62,49,61]))
    d=ImageDraw.Draw(im);d.rectangle((690,0,w,h),fill='#25232b')
    label(d,48,38,'NIGHTCAP',20,'#f3dfbc',4);label(d,463,44,'CHARACTER ART',13)
    d.line((48,78,643,78),fill='#897b80')
    shadow=Image.new('RGBA',im.size);sd=ImageDraw.Draw(shadow)
    sd.ellipse((226,841,472,864),fill=(8,5,13,140))
    shadow=shadow.filter(ImageFilter.GaussianBlur(9));im.paste(shadow,(0,0),shadow)
    paste(im,Image.open(R/'Portrait-light.png').convert('RGBA'),(47,96,600,759))
    d=ImageDraw.Draw(im);d.line((48,873,643,873),fill='#897b80')
    label(d,48,891,'FULL REGALIA',13);label(d,492,891,'BIND POSE',13)
    label(d,739,45,'FEMALE DARK ELF    /    WARLOCK',15,'#c9b39b',2.2)
    d.text((730,94),'Vesper Moth',font=font('georgia',91),anchor='lt',fill='#f1dfc1')
    d.line((739,208,1410,208),fill='#736369')
    paste(im,Image.open(R/'Reliquary.png').convert('RGBA'),(707,242,732,439))
    d.line((739,700,1410,700),fill='#736369')
    d.text((740,732),'Blackberry silk, chased gold and witchglass',font=font('georgiai',27),fill='#e3d4be',anchor='lt')
    for j,(c,n) in enumerate([('#4e2d49','SILK'),('#833c54','LINING'),('#372f3c','HORN'),('#c39862','GOLD'),('#299e88','WITCHGLASS')]):
        xx=740+j*136;d.rectangle((xx,814,xx+119,834),fill=c)
        label(d,xx,855,n,12,'#d0c2b2',1.2)
    im.save(R/'Vesper-Moth.jpg',quality=95,subsampling=0)
    comp=Image.new('RGB',(1150,810),'#77727f');d=ImageDraw.Draw(comp)
    for i,(p,title) in enumerate([(R.parents[1]/'silt-reader/Review/Front.png','Silt Reader'),(R/'Front.png','Vesper Moth')]):
        paste(comp,Image.open(p).convert('RGBA'),(i*575+18,36,539,673))
        d.line((i*575+44,735,i*575+529,735),fill='#bbb2ac')
        d.text((i*575+44,755),title,font=font('georgia',29),fill='#fff3df',anchor='lt')
    comp.save(R/'Costume-comparison.jpg',quality=93)
if __name__=='__main__':plate()
