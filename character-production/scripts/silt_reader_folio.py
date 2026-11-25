"""Print plates from Blender review frames, preserving the model's rendered pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np
import math
import json

O=Path(__file__).resolve().parents[1]/'output/dark-elf-female/silt-reader'
R=O/'Review'
def font(name,size):return ImageFont.truetype('C:/Windows/Fonts/'+name+'.ttf',size)
def ink(d,pos,s,size=18,fill='#303139',family='bahnschrift'):
    d.text(pos,s,font=font(family,size),fill=fill,anchor='lt')
def space(d,x,y,s,size,color,gap=2):
    f=font('bahnschrift',size)
    for char in s:
        d.text((x,y),char,font=f,fill=color,anchor='lt');x+=d.textlength(char,font=f)+gap
def frame(name):return Image.open(R/(name+'.png')).convert('RGBA')
def place(im,obj,box,crop=True):
    if crop:obj=obj.crop(obj.getbbox())
    x,y,w,h=box;factor=min(w/obj.width,h/obj.height)
    obj=obj.resize((round(obj.width*factor),round(obj.height*factor)),Image.Resampling.LANCZOS)
    im.paste(obj,(round(x+(w-obj.width)/2),round(y+(h-obj.height)/2)),obj)
def folio():
    W,H=1480,940; x,y=np.meshgrid(np.arange(W),np.arange(H))
    light=np.clip(1.05-np.hypot((x-402)/730,(y-390)/920),0,1)
    bg=np.array([46,49,60])+light[:,:,None]*[59,55,55]
    im=Image.fromarray(bg.astype('uint8'));d=ImageDraw.Draw(im)
    d.rectangle((822,0,W,H),fill='#e8e3d9')
    space(d,46,36,'NIGHTCAP',22,'#f3e8d4',4)
    space(d,566,43,'CHARACTER ART',13,'#ded6c9',1.8)
    d.line((46,75,776,75),fill='#999493')
    # Two soft contact marks locate the soles without affecting the character render.
    shadow=Image.new('RGBA',im.size);sd=ImageDraw.Draw(shadow)
    sd.ellipse((277,837,514,855),fill=(19,18,25,108))
    shadow=shadow.filter(ImageFilter.GaussianBlur(10));im.paste(shadow,(0,0),shadow)
    place(im,frame('Three-quarter'),(54,90,705,760))
    d=ImageDraw.Draw(im);d.line((46,871,776,871),fill='#999493')
    ink(d,(46,891),'Three-quarter view',19,'#f3e8d4','georgiai')
    ink(d,(592,893),'STATIC BIND POSE',14,'#e2d9ce')
    space(d,866,46,'KNELLWATER  /  FIELD DRESS',15,'#715446',2)
    ink(d,(861,91),'Silt Reader',82,'#252936','georgia')
    ink(d,(868,192),'Female Dark Elf',27,'#5e5359','georgiai')
    d.line((867,246,1435,246),fill='#b5a99e')
    place(im,frame('Uncovered-head'),(847,260,606,458),False)
    d=ImageDraw.Draw(im);d.line((867,722,1435,722),fill='#b5a99e')
    ink(d,(869,749),'Peat-indigo wool wrap with a flax cuff, clay lining',20,'#37353b','georgia')
    ink(d,(869,778),'and a brass plumb weight at the sash.',20,'#37353b','georgia')
    colors=['#4c5068','#373c50','#a25242','#c2a888','#a98758']
    for i,(color,label) in enumerate(zip(colors,['WOOL','YOKE','CLAY','FLAX','BRASS'])):
        xx=868+i*115;d.rectangle((xx,842,xx+104,865),fill=color)
        space(d,xx,880,label,12,'#504b4d',1.5)
    im.save(R/'Silt-Reader.jpg',quality=95,subsampling=0)
    plate=Image.new('RGB',(1250,710),'#767581');d=ImageDraw.Draw(plate)
    for j,n in enumerate(['Front','Profile','Rear']):
        place(plate,frame(n),(j*410+14,26,398,608));ink(d,(j*410+28,658),n,26,'#fff0de','georgia')
    plate.save(R/'Turnaround.jpg',quality=93)
def color_study():
    unlit=frame('Unlit');unlit=unlit.crop(unlit.getbbox())
    unlit.thumbnail((150,128),Image.Resampling.LANCZOS)
    grey=ImageOps.grayscale(unlit).convert('RGBA');grey.putalpha(unlit.getchannel('A'))
    im=Image.new('RGB',(630,232),'#dcd8d1');d=ImageDraw.Draw(im)
    for i,(name,obj) in enumerate([('Local color',unlit),('Value',grey),('Cool key',frame('Cool-128'))]):
        place(im,obj,(i*210+15,20,180,128));ink(d,(i*210+24,171),name,19)
    im.save(R/'Palette-128.png')
def landmarks():
    # Scaled orthographic camera images with the same metric vertical axis and eye-line.
    im=Image.new('RGB',(1060,510),'#e8e2d7');d=ImageDraw.Draw(im)
    ink(d,(30,24),'Head landmarks',39,family='georgia')
    scale=300/.35
    def proj(x,z,cx):return (cx+x*scale,230-(z-1.563)*scale)
    for cx,n,coords in [(220,'Head-front',[(.033,1.583),(.074,1.577),(.155,1.621),(.064,1.608),(0,1.486)]),
                         (580,'Head-profile',[(-.135+.052,1.583),(-.074+.052,1.576),(.006+.052,1.621),(-.105+.052,1.606),(-.139+.052,1.486)])]:
        obj=frame(n).resize((300,300))
        if n=='Head-profile':coords=[(-x,z) for x,z in coords]
        im.paste(obj,(cx-150,80),obj)
        cy=proj(0,1.583,cx)[1]
        d.line((cx-166,cy,cx+166,cy),fill='#ac8872');d.line((cx,87,cx,372),fill='#b4a390')
        for j,(x,z) in enumerate(coords):
            xx,yy=proj(x,z,cx);d.ellipse((xx-3,yy-3,xx+3,yy+3),fill='#bb683d');ink(d,(xx+4,yy-12),str(j+1),12,'#70371c')
        ink(d,(cx-110,389),n.replace('Head-','').capitalize(),19,family='georgiai')
    for i,line in enumerate(['1   Copper iris','2   Ear root','3   Swept tip','4   Temple hairline','5   Jaw tip']):
        ink(d,(790,120+i*39),line,20)
    ink(d,(34,460),'Front and profile share the same eye-line and orthographic scale.',19)
    im.save(R/'Head-landmarks.png')
def cutting():
    data=json.loads((O/'Paint'/'Cut-stations.json').read_text())
    im=Image.new('RGB',(1450,860),'#e8e3d8');d=ImageDraw.Draw(im)
    ink(d,(42,30),'Silt Reader',49,family='georgia');space(d,347,52,'CUTTING STUDY',18,'#72574a')
    d.line((42,105,1408,105),fill='#aba298')
    items=list(data.items());centers=[145,361,591,780]
    for i,(name,sections) in enumerate(items[:4]):
        cx=centers[i];scale=365
        def edge(r,sgn):
            v,w,left,right=r
            h=(left[2]+right[2])/2
            return (cx+sgn*w*scale/2,700-(h-.12)*scale)
        ps=[edge(r,-1) for r in sections]+[edge(r,1) for r in reversed(sections)]
        d.polygon(ps,fill=['#65687d','#68697c','#5e6174','#767587'][i],outline='#444654',width=2)
        d.line((cx,380,cx,612),fill='#d5c4a8',width=2)
        d.polygon([(cx,618),(cx-5,605),(cx+5,605)],fill='#d5c4a8')
        ink(d,(cx-83,735),['Outside front','Left side','Joined back','Inside front'][i],19,family='georgia')
        ink(d,(cx-83,768),f'{max(r[1] for r in sections)*100:.1f} cm at widest',15)
    d.line((900,136,900,798),fill='#aba298')
    ink(d,(939,150),'Other pieces',27,family='georgia')
    for j,(name,rows) in enumerate(items[4:]):
        title=name.split('| ')[1].replace(' l','',1) if name.endswith(' l') else name.split('| ')[1]
        ink(d,(939,213+j*53),title,17)
        ink(d,(1290,213+j*53),f'{max(r[1] for r in rows)*100:.1f} cm',17)
        d.line((938,240+j*53,1396,240+j*53),fill='#c4bbb0')
    ink(d,(939,574),'Widths follow the bound cloth surface.',17,family='georgiai')
    ink(d,(939,606),'Arrows follow the hanging warp.',17,family='georgiai')
    tile=Image.open(O/'Paint'/'Wool-repeat.png').resize((96,96),Image.Resampling.NEAREST)
    box=Image.new('RGBA',(96,96),'#4c5068');box.alpha_composite(tile)
    im.paste(box,(940,664));d.rectangle((939,663,1036,760),outline='#967e67',width=2)
    ink(d,(1062,680),'One repeat',20,family='georgia');ink(d,(1062,717),'24 × 24 atlas pixels',17)
    im.save(R/'Cutting-study.png')
if __name__=='__main__':
    folio();color_study();landmarks();cutting()
