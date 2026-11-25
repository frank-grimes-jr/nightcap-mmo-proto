"""Original cut-block illustrations and separated dye fields for the Ebb Cantor."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
from xml.etree.ElementTree import Element, SubElement, tostring
from io import BytesIO
import math
import numpy as np
from PIL import Image, ImageDraw

OUT=Path(__file__).resolve().parents[1]/'output/dark-elf-female/ebb-cantor'
N=2048
for folder in ('Paint','Textures','Review'):(OUT/folder).mkdir(parents=True,exist_ok=True)
def encode(im):
    b=BytesIO();im.save(b,'PNG');return b.getvalue()
def save(name,layers):
    w,h=layers[0][1].size
    comp=Image.new('RGBA',(w,h))
    for _,im in layers:comp=Image.alpha_composite(comp,im)
    comp.convert('RGB').save(OUT/'Textures'/f'{name}.png')
    root=Element('image',w=str(w),h=str(h),version='0.0.3',name=name);stack=SubElement(root,'stack')
    with ZipFile(OUT/'Paint'/f'{name}.ora','w',ZIP_DEFLATED) as z:
        z.writestr('mimetype','image/openraster',compress_type=ZIP_STORED)
        for i,(label,im) in enumerate(reversed(layers)):
            file=f'data/{i}.png';z.writestr(file,encode(im));SubElement(stack,'layer',name=label,src=file,x='0',y='0',opacity='1.0')
        z.writestr('stack.xml',tostring(root));z.writestr('mergedimage.png',encode(comp))
def layer():return Image.new('RGBA',(N,N))
def field(rects):
    y,x=np.mgrid[:N,:N].astype('float32')
    rng=np.random.default_rng(317)
    grain=(rng.uniform(-2.3,2.3,(N,N))+.95*np.cos(x*2.1)+1.2*np.sin(y*2.5+x*.3)
           +1.7*np.sin(.021*x+1.7*np.cos(y*.012))+1.2*np.cos(y*.015+x*.01))
    rgb=np.zeros((N,N,3),np.float32)
    for x0,y0,x1,y1,color in rects:rgb[y0:y1,x0:x1]=color
    return Image.fromarray(np.uint8(np.clip(rgb+grain[:,:,None],0,255))).convert('RGBA')
def bearer(draw,x,y,s,phase):
    bone='#d0c6a7';ink='#345455'
    def p(a,b):return (round(x+s*a),round(y+s*b))
    def poly(pts,color):draw.polygon([p(*q) for q in pts],fill=color)
    def line(pts,color,w):draw.line([p(*q) for q in pts],fill=color,width=max(1,round(w*s)),joint='curve')
    # A bowed profile, a wet coat split at the knees, and two walking legs.
    poly([(-9,-63),(-6,-71),(3,-74),(11,-68),(10,-63),(15,-59),(10,-57),(11,-52),(3,-51),(1,-43),(-8,-46)],bone)
    poly([(-6,-48),(4,-49),(10,-38),(14,-17),(21,5),(11,4),(5,0),(-4,8),(-15,8),(-10,-15),(-14,-27)],bone)
    if phase:
        line([(-8,3),(-15,18),(-25,30),(-17,31)],bone,5);line([(8,1),(13,17),(17,29),(24,30)],bone,5)
    else:
        line([(-6,3),(-6,17),(2,30),(9,31)],bone,5);line([(7,2),(19,16),(26,23),(33,23)],bone,5)
    line([(-1,-40),(15,-28),(20,-46),(27,-51)],bone,5)
    line([(-7,-39),(-4,-21),(4,-8)],ink,2)
    for dx in (-6,0,5):line([(dx,-12),(dx+3,1)],ink,1.4)
def procession(d,x,y,s):
    def p(a,b):return (x+s*a,y+s*b)
    def poly(pts,c):d.polygon([p(*q) for q in pts],fill=c)
    def line(pts,c,w):d.line([p(*q) for q in pts],fill=c,width=round(w*s))
    # Four pole bearers, a low shroud and negative cuts indicating the binding knots.
    for j,xx in enumerate((8,61,145,202)):bearer(d,*p(xx,0),s, j%2)
    line([(-11,-50),(235,-53)],'#cfad78',5)
    poly([(39,-57),(52,-66),(72,-68),(80,-77),(94,-79),(107,-74),(138,-74),(158,-71),(179,-61),(190,-57)],'#ae7156')
    for xx in (60,78,109,138,160):line([(xx,-67),(xx+4,-58)],'#f0cd97',2)
    for xx in (0,57,141,199):line([(xx+7,-86),(xx+2,-79)],'#8fa3a0',2)
def reed(d,x,y,height,col,wind):
    for i in range(5):
        dx=(i-2)*height*.11;h=height*(.58+.42*math.sin(i*1.91+1)**2)
        d.polygon([(x+dx*.21,y),(x+dx*.65+wind*.32,y-h*.55),(x+dx+wind,y-h),
                   (x+dx*.69+wind*.35+height*.029,y-h*.45)],fill=col)
def core():
    base=field([(0,0,N,1510,(35,63,65)),(0,1510,997,N,(42,65,66)),(997,1510,1490,N,(76,47,42)),(1490,1510,N,N,(57,45,41))])
    wash=layer();d=ImageDraw.Draw(wash)
    for edge,col in [(402,(102,139,130,22)),(602,(77,122,117,40)),(831,(15,40,48,85)),(1021,(15,36,43,155)),(1316,(79,104,97,180)),(1374,(31,52,55,200))]:
        shore=[(x,edge+16*math.sin(x*.012+.7)+7*math.sin(x*.031)) for x in range(-4,N+8,4)]
        d.polygon(shore+[(N,1509),(0,1509)],fill=col)
    relief=layer();d=ImageDraw.Draw(relief)
    for x in range(-20,N+40,89):
        reed(d,x,1151+12*math.sin(x),76+54*math.cos(x*.021)**2,'#52706b',27)
    for x in range(-175,N,326):procession(d,x,1241+9*math.sin(x*.013),1.13)
    # A low stair, submerging on one side of each procession.
    for x in range(-155,N,326):
        pts=[]
        for i in range(9):pts.extend([(x+i*19,1329-i*3),(x+(i+1)*19,1329-i*3)])
        d.line(pts,fill='#bc8762',width=4)
    finish=layer();d=ImageDraw.Draw(finish)
    for y in (1005,1016,1378,1392,1450):d.line((0,y,N,y),fill='#80928a' if y%2 else '#bc8f70',width=3)
    for i in range(0,N,13):
        for y in (1028,1413):d.line((i,y,i+5,y+1),fill='#b8aa8e',width=2)
    for x in range(20,980,42):
        for y in range(1582,1958,52):
            d.line([(x,y),(x+6,y-11),(x+15,y-15)],fill='#71837b',width=2)
    save('Ebb-Procession',[('Reed-black wools and twill',base),('Successive high-water baths',wash),('Cut block - bearers, bier and steps',relief),('Couching and sleeve picks',finish)])
def mantle():
    base=field([(0,0,1120,N,(200,190,161)),(1120,0,N,N,(138,66,47))])
    marks=layer();d=ImageDraw.Draw(marks)
    # The pall carries warp-aligned counting cords, grouped in unequal sets.
    for x in (66,83,102,177,313,328,445,629,641,655,842,860,949,967,981,1002,1046):
        pts=[(x+5*math.sin(y*.007+x),y) for y in range(0,N+8,8)]
        d.line(pts,fill='#7a8378',width=3 if x%2 else 5)
    for x in range(42,1090,101):
        for j in range(7):
            y=111+j*24+round(28*math.sin(x*.02))
            d.line((x,y,x+15+j%3*3,y+3),fill='#675e52',width=3)
    for x in range(28,1100,40):reed(d,x,1716+33*math.sin(x*.011),140+161*math.sin(x*.014)**2,'#6b7e74',52)
    bands=layer();d=ImageDraw.Draw(bands)
    for y,h,c in [(1691,14,'#776e5a'),(1727,70,'#475c57'),(1813,16,'#92624c'),(1860,8,'#414f4b'),(1945,25,'#765d50')]:
        d.rectangle((0,y,1119,y+h),fill=c)
    for x in range(14,1110,28):d.line((x,1750,x+8,1778),fill='#c7bb98',width=4)
    chart=layer();d=ImageDraw.Draw(chart)
    # Invented soundings of the funeral stair: nested banks and the white dike road.
    for j in range(31):
        pts=[]
        for y in range(-8,N+12,8):
            xc=1535+114*math.sin(y*.0035)+50*math.sin(y*.009+1.2)
            xx=xc+(j-15)*30+16*math.sin(.0057*y+j*.26)+4*math.cos(y*.021+j)
            pts.append((max(1122,min(2047,xx)),y))
        d.line(pts,fill=['#814a43','#bb8060','#ac6b53','#e1ae82'][j%4],width=2 if j%4 else 5)
    for i in range(17):
        x=1160+44*i;y=1420-35*i
        d.line([(x,y+24),(x,y),(x+44,y),(x+44,y-11)],fill='#e6c7a2',width=7)
        if i%3==1:d.ellipse((x+12,y+15,x+21,y+24),fill='#4d4640')
    # The roofless gable is deliberately interrupted by the tide stripe.
    for x,y,k in [(1400,740,1.2),(1778,1629,.62)]:
        def p(a,b):return(x+a*k,y+b*k)
        # A dismantled belfry in elevation. Separate blocks preserve the broken
        # silhouette and let the clay ground show through its central opening.
        for side,height in [(-1,6),(1,8)]:
            for row in range(height):
                xx=side*53+(row%2)*2;yy=28-row*17
                d.polygon([p(xx-12,yy),p(xx-11,yy-14),p(xx+10,yy-15),p(xx+13,yy-1)],fill='#d6ad85')
                d.line([p(xx+2,yy-13),p(xx+8,yy-3)],fill='#9e694f',width=2)
        d.line([p(-68,-77),p(-32,-98),p(-7,-113)],fill='#c8a385',width=6)
        d.line([p(-43,-52),p(49,-66)],fill='#484944',width=7)
        d.line([p(5,-57),p(5,-42)],fill='#e1b08c',width=3)
        d.polygon([p(-22,-6),p(-13,-16),p(-10,-34),p(-4,-42),p(8,-44),p(16,-36),p(19,-20),p(28,-10),p(30,-5)],fill='#493f39')
        d.line([p(-21,-6),p(30,-5)],fill='#edbc8d',width=3)
        d.ellipse([p(0,-4),p(9,4)],fill='#e4b28a')
        for j in range(6):
            d.line([p(-85-j*4,35+j*9),p(28-j*7,35+j*9),p(40-j*7,32+j*9),p(83-j*9,32+j*9)],fill='#624b40',width=3)
        for xx in (-96,-83,89,98):
            reed(d,*p(xx,53),28*k,'#c49776',10*k)
    save('Ebb-Pall',[('Ash linen and madder sailcloth',base),('Register cords and sedge',marks),('Woven hem tapes',bands),('Dike, roofless gable and soundings',chart)])
def ceramic():
    w,h=1024,512;y,x=np.mgrid[:h,:w].astype('float32');a=x/w*2*np.pi
    smoke=11*np.sin(3*a+y*.013)+6*np.sin(8*a+np.sin(y*.022))+4*np.cos(y*.20+.8*np.sin(2*a))
    foot=np.clip((y-300)/150,0,1);rng=np.random.default_rng(483)
    shade=smoke-42*foot+rng.normal(0,2.4,(h,w))
    rgb=np.array([150,91,66])+shade[:,:,None]*[1,.77,.70]
    ground=Image.fromarray(np.uint8(np.clip(rgb,0,255))).convert('RGBA')
    sgraffito=Image.new('RGBA',(w,h));d=ImageDraw.Draw(sgraffito)
    # Profile counters are cut into a brushed slip bed. The three jars turn this
    # same strip to three distinct stamps: witness, steps and sealed mouth.
    for center,style in [(720,0),(405,1),(122,2)]:
        def pts(arr):return [(center+i,204+j) for i,j in arr]
        d.polygon(pts([(-70,-40),(-46,-61),(2,-66),(60,-49),(78,-17),(68,30),(33,61),(-19,65),(-64,42),(-78,3)]),fill='#c1a786')
        if style==0:
            d.polygon(pts([(-23,41),(-22,23),(-32,9),(-36,-13),(-29,-34),(-10,-44),(14,-39),(21,-22),(20,-13),(36,0),(26,4),(27,12),(21,14),(20,22),(7,25),(3,42)]),fill='#4c4942')
            d.line(pts([(5,-18),(13,-16),(16,-18)]),fill='#dbbf96',width=3)
        elif style==1:
            for i in range(5):d.line(pts([(-48+i*14,32-i*12),(-48+i*14,20-i*12),(-34+i*14,20-i*12)]),fill='#514c43',width=6)
        else:
            d.line(pts([(-48,2),(-6,-7),(38,0),(9,12),(-20,11),(-48,2)]),fill='#514c43',width=4)
            for i in (-21,0,19):d.line(pts([(i,-12),(i+5,16)]),fill='#514c43',width=3)
        for i in range(5):d.line(pts([(-55,30+i*5),(-32+i*2,26+i*5)]),fill='#99775e',width=2)
    ticks=Image.new('RGBA',(w,h));d=ImageDraw.Draw(ticks)
    for j in range(0,w,11):
        y0=310+round(3*math.sin(j*.019))
        d.line((j,y0,j+4,y0-6),fill='#c6ae94',width=2)
    save('Ebb-Stoneware',[('Oxidised earth and thrown rings',ground),('Three cut-slip matrices',sgraffito),('Knife nicks',ticks)])
if __name__=='__main__':core();mantle();ceramic()
