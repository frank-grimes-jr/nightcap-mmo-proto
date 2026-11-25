"""Original Silt Reader paint master. Pixel coordinates are measured from the top left."""
from pathlib import Path
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from xml.etree.ElementTree import Element, SubElement, tostring
from io import BytesIO
import math
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter

OUT = Path(__file__).resolve().parents[1] / 'output/dark-elf-female/silt-reader'
T, R, S = (OUT / d for d in ('Textures', 'Review', 'Paint'))
for directory in (T, R, S):
    directory.mkdir(exist_ok=True, parents=True)
N = 2048
# Inclusive paint beds. UV insets leave 18 px of dilation inside each bed.
BEDS = {
    'Wrap': (0,0,474,1430), 'Left': (475,0,1051,1430),
    'Back': (1052,0,1408,1430), 'Inside': (1409,0,2047,1430),
    'Sleeve': (0,1431,490,2047), 'Yoke': (491,1431,995,2047),
    'Clay': (996,1431,1241,2047), 'Flax': (1242,1431,1469,2047),
    'Sash': (1470,1431,1663,2047), 'Facing': (1664,1431,1855,2047),
    'Boot': (1856,1431,2047,2047)}
COLORS = {'Wrap':'#4c5068','Left':'#4a4d62','Back':'#494c61','Inside':'#494d63',
          'Sleeve':'#4c5064','Yoke':'#373c50','Clay':'#a25242','Flax':'#c2a888',
          'Sash':'#473538','Facing':'#66677c','Boot':'#513d3d'}

def png(im):
    buf=BytesIO(); im.save(buf,format='PNG'); return buf.getvalue()

def garment():
    layers=[]
    def layer(name):
        im=Image.new('RGBA',(N,N)); layers.append((name,im)); return ImageDraw.Draw(im)
    d=layer('01 | Vat-dyed fields')
    for name,rect in BEDS.items(): d.rectangle(rect,fill=COLORS[name])
    d=layer('02 | Dye clouds')
    x,y=np.meshgrid(np.arange(N,dtype=np.float32),np.arange(N,dtype=np.float32))
    a=np.uint8(np.clip(8+4*np.sin(.023*x+.008*y)+4*np.cos(.007*x-.013*y),0,18))
    layers[-1][1].paste((181,153,156), (0,0,N,N), Image.fromarray(a))
    d=layer('03 | Warp shadows and wet hem')
    for name in ('Wrap','Left','Back','Inside'):
        x0,_,x1,y1=BEDS[name]
        for i in range(x0,x1+1):
            t=(i-x0)/(x1-x0)
            high=1165+33*math.sin(i*.021)+15*math.sin(i*.041)+8*math.sin(i*.115)
            for j in range(12):
                d.line((i,high+j*2,i,high+(j+1)*2),fill=(54,44,57,28+j*6))
            d.line((i,high+24,i,y1),fill=(54,44,57,98))
            d.line((i,high+42,i,y1),fill=(53,48,56,85))
            d.line((i,1390,i,y1),fill=(45,39,48,135))
    d=layer('04 | Lining selvage')
    for i in (1016,1023,1040,1220):
        d.line((i,1431,i,2048),fill=(238,165,110,100),width=3)
    d=layer('05 | Broken flood register, left of front slit')
    # Rows wrap around the seam from the outside front onto its neighbour.
    for row,(yy,start,end) in enumerate([(1042,118,441),(1072,137,448),(1108,106,458),(1176,292,447)]):
        for i in range(start,end):
            if (i+row*7)%87 in (1,2,3,4): continue
            h=yy+round(2*math.sin(i*.038)+math.sin(i*.081))
            d.line((i,h,i,h+5+(row%2)),fill=(185,163,139,185))
    d.line([(447,1108),(474,1109)],fill=(181,154,131,173),width=6)
    d.line([(475,1109),(503,1108),(527,1110),(543,1109)],fill=(181,154,131,173),width=6)
    for i in [151,178,204,232,270,305,360,396,420]:
        d.line((i,1052,i-1,1060),fill=(184,167,149,144),width=3)
    for j in range(865,1310):
        seam=340+round((j-1050)*.024)
        d.line((seam,j,seam+2,j),fill=(48,47,58,172))
        if j%13<6:d.point((seam+4,j),fill=(156,145,145,122))
    d=layer('06 | Darn and abrasion')
    patch=[(217,1206),(312,1199),(320,1267),(308,1279),(223,1283)]
    d.polygon(patch,fill=(96,86,88,255))
    for i in range(228,307,6): d.line((i,1210,i+5,1271),fill=(155,139,126,88),width=2)
    d=layer('07 | Needle and binding')
    for y0 in (1211,1271):
        for i in range(228,309,9):
            d.line((i,y0-(i-228)*.075,i+4,y0+3-(i-228)*.075),fill=(202,178,145,205),width=2)
    for name in ('Flax','Sash','Facing','Yoke'):
        x0,y0,x1,y1=BEDS[name]
        for i in range(x0,x1+1,10):
            for j in (y0+38,y1-37):
                d.line((i,j,i+5,j+1),fill=(196,170,140,160),width=2)
    tile=Image.new('RGBA',(24,24),(0,0,0,0)); td=ImageDraw.Draw(tile)
    for j in range(0,24,4):
        for i in range(-24,48,8):
            k=i+(j//4)*4
            for shift in (-24,0,24):
                td.line((k+shift,j,k+shift+4,j+2), fill=(221,211,201,16),width=1)
                td.line((k+shift+2,j+2,k+shift+5,j+3),fill=(20,17,25,18))
    tile.save(S/'Wool-repeat.png')
    repeat=Image.new('RGBA',(72,72),(76,80,104,255))
    for j in range(3):
        for i in range(3): repeat.alpha_composite(tile,(i*24,j*24))
    repeat.resize((360,360),Image.Resampling.NEAREST).save(R/'Wool-3x3.png')
    grain=np.tile(np.array(tile),(86,86,1))[:N,:N].copy()
    layers.append(('08 | Wool picks, 6–7 percent coverage opacity',Image.fromarray(grain)))
    final=Image.new('RGBA',(N,N))
    for _,im in layers: final=Image.alpha_composite(final,im)
    final.convert('RGB').save(T/'SiltReader-BaseColor.png')
    tree=Element('image',{'version':'0.0.3','w':str(N),'h':str(N),'name':'Silt Reader'}); stack=SubElement(tree,'stack')
    with ZipFile(S/'SiltReader.ora','w',compression=ZIP_DEFLATED) as f:
        f.writestr('mimetype','image/openraster',compress_type=ZIP_STORED)
        for i,(name,im) in enumerate(reversed(layers)):
            path=f'data/{i}.png'; f.writestr(path,png(im))
            SubElement(stack,'layer',{'name':name,'src':path,'x':'0','y':'0','opacity':'1.0','composite-op':'svg:src-over'})
        f.writestr('stack.xml',tostring(tree)); f.writestr('mergedimage.png',png(final))
    pattern=final.convert('RGB').resize((700,700)); d=ImageDraw.Draw(pattern)
    for name,(x0,y0,_,_) in BEDS.items(): d.text((x0*700/N+5,y0*700/N+8),name,fill='white')
    pattern.save(R/'Panel-map.png')
    scrap=Image.new('RGB',(320,128),'#b49f83'); d=ImageDraw.Draw(scrap)
    for i,w in enumerate([199,183,204,0,67]):
        if w:d.line([(36,24+i*17),(36+w*.6,22+i*17),(36+w,24+i*17)],fill='#454452',width=4)
    scrap.save(S/'Register-scrap.png')

def anatomy_maps():
    u,v=np.meshgrid(np.arange(512)/512,np.arange(512)/512)
    r=np.hypot(u-.5,v-.50); th=np.arctan2(v-.5,u-.5)
    iris=np.full((512,512,3),[156,140,145],np.float32)
    light=(.55+.19*np.sin(55*th+38*r)+.13*np.cos(87*th-19*r))*np.clip((.37-r)*32,0,1)
    iris[r<.37]=np.array([65,36,32])+light[r<.37,None]*[172,112,48]
    iris[r<.133]=[30,22,31]
    Image.fromarray(iris.astype('uint8')).save(T/'Copper-Iris.png')
    ear=np.zeros((512,512,3))+[101,77,108]
    bowl=np.exp(-((v-.46)/.23)**2)*np.sin(np.pi*u)**.55
    helix=np.exp(-((v-.16)/.13)**2)*np.sin(np.pi*u)**.65
    ear+=bowl[:,:,None]*np.array([-26,-23,-15])+helix[:,:,None]*np.array([25,12,13])
    Image.fromarray(ear.astype('uint8')).save(T/'Auricle.png')
    tones=5*np.cos(2*np.pi*(u*9+.12*np.sin(v*2*np.pi)))+4*np.cos(2*np.pi*(u*3+v*.17))+1.6*np.sin(2*np.pi*u*49)
    Image.fromarray(np.uint8(np.clip(np.array([207,197,178])+tones[:,:,None],0,255))).save(T/'Ivory-Locks.png')

if __name__=='__main__':
    garment()
    anatomy_maps()
