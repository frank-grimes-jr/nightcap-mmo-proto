"""Paint the Vesper Moth vestments in editable OpenRaster layers, from empty fields."""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
from xml.etree.ElementTree import Element, SubElement, tostring
import math
from PIL import Image, ImageDraw
import numpy as np

OUT=Path(__file__).resolve().parents[1]/'output/dark-elf-female/vesper-moth'
for folder in ('Textures','Paint','Review'):(OUT/folder).mkdir(parents=True,exist_ok=True)
N=2048
GOLD='#c79863';PALE='#ecd39b';DARK='#563733';AMBER='#9f674c';TEAL='#70ceb9'
def data(im):
    b=BytesIO();im.save(b,'PNG');return b.getvalue()
def save(name,layers):
    base=Image.new('RGBA',(N,N));tree=Element('image',w=str(N),h=str(N),version='0.0.3',name=name)
    stack=SubElement(tree,'stack')
    for _,im in layers:base=Image.alpha_composite(base,im)
    base.convert('RGB').save(OUT/'Textures'/f'{name}.png')
    with ZipFile(OUT/'Paint'/f'{name}.ora','w',ZIP_DEFLATED) as f:
        f.writestr('mimetype','image/openraster',compress_type=ZIP_STORED)
        for i,(label,im) in enumerate(reversed(layers)):
            path=f'data/{i}.png';f.writestr(path,data(im));SubElement(stack,'layer',name=label,src=path,x='0',y='0',opacity='1.0')
        f.writestr('stack.xml',tostring(tree));f.writestr('mergedimage.png',data(base))
def curved(points):
    pts=np.asarray(points,float);ts=np.linspace(0,1,20)[:,None];out=[tuple(pts[0])]
    for i in range(0,len(pts)-1,3):
        a,b,c,d=pts[i:i+4]
        out.extend(map(tuple,(1-ts)**3*a+3*(1-ts)**2*ts*b+3*(1-ts)*ts**2*c+ts**3*d))
    return out
def diamond(d,x,y,w,h,fill,edge=None):
    d.polygon([(x,y-h),(x+w,y),(x,y+h),(x-w,y)],fill=fill,outline=edge,width=2)
def bez(d,pts,fill,width):d.line(curved(pts),fill=fill,width=width,joint='curve')
def moth(d,x,y,s,rich=True):
    """Veined forewings, scalloped swallowtails, skull thorax and antennae."""
    for side in (-1,1):
        def path(pts):return [(x+side*s*a,y+s*b) for a,b in pts]
        def wing(pts,fill,edge,width):
            curve=curved(path(pts));d.polygon(curve,fill=fill);d.line(curve+[curve[0]],fill=edge,width=max(1,round(width*s)),joint='curve')
        def line(pts,color,w):bez(d,path(pts),color,max(1,round(w*s)))
        gold,mid,low=(GOLD,AMBER,'#5b3653') if rich else ('#75516e','#5d3859','#442b49')
        wing([(1,6),(30,-8),(62,-37),(104,-49),(94,-24),(69,-3),(59,8),(54,4),(42,11),(34,19),(26,13),(12,18),(1,6)],low,gold,2.6)
        wing([(3,11),(26,14),(42,11),(60,6),(61,20),(49,40),(39,42),(37,34),(29,42),(23,54),(23,69),(14,84),(10,87),(16,63),(11,39),(3,11)],low,gold,2.1)
        for tip in [(99,-46),(78,-20),(57,7),(38,17),(40,39),(22,53),(13,73)]:
            ex,ey=tip;line([(2,8),(22,3),(ex*.7,ey*.75),(ex,ey)],mid,1.7)
        for xx,yy,sz in [(66,-17,6),(53,-9,4),(39,26,5),(31,33,3)]:
            diamond(d,x+side*s*xx,y+s*yy,s*sz,s*(sz+2),gold)
        line([(2,-7),(5,-19),(15,-35),(29,-35)],gold,2)
    diamond(d,x,y+23*s,4.5*s,27*s,GOLD if rich else '#71536c')
    if rich:
        d.ellipse((x-9*s,y-6*s,x+9*s,y+10*s),fill=PALE)
        for k in (-1,1):d.ellipse((x+(k*4-2.4)*s,y+.8*s,x+(k*4+2.4)*s,y+5*s),fill='#34202a')
        d.polygon([(x-6*s,y+7*s),(x+6*s,y+7*s),(x+4*s,y+14*s),(x-3*s,y+14*s)],fill=GOLD)
def make():
    yy,xx=np.mgrid[0:N,0:N].astype(np.float32)
    weave=(1.3*np.sin((xx+yy)*1.54)+1.1*np.cos((xx*.5-yy)*1.8)+1.1*np.sin(xx*.031+yy*.012))
    def dye(rects):
        a=np.zeros((N,N,3),np.float32)
        for x0,y0,x1,y1,rgb in rects:
            u=(xx[y0:y1,x0:x1]-x0)/(x1-x0)
            flow=3.4*np.cos(u*6*np.pi+yy[y0:y1,x0:x1]*.002)+6*np.sin(np.pi*u)**2
            a[y0:y1,x0:x1]=np.array(rgb)+flow[:,:,None]
        a+=weave[:,:,None]
        return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')
    def blank():return Image.new('RGBA',(N,N))
    fields=[(0,0,474,1431,(48,29,52)),(474,0,1052,1431,(55,28,49)),(1052,0,1409,1431,(48,26,47)),(1409,0,2048,1431,(50,28,53)),
            (0,1431,491,2048,(57,30,54)),(491,1431,996,2048,(57,29,53)),(996,1431,1242,2048,(115,39,61)),
            (1242,1431,1470,2048,(72,40,52)),(1470,1431,1664,2048,(52,35,41)),(1664,1431,1856,2048,(90,52,61)),(1856,1431,2048,2048,(47,32,41))]
    dam=blank();d=ImageDraw.Draw(dam)
    for row,y in enumerate(range(50,1420,121)):
        for x in range(-60+(row%2)*62,2050,124):moth(d,x,y,.43,False)
    border=blank();d=ImageDraw.Draw(border)
    for x in range(-84,2140,84):
        for y,h in [(1340,62),(1290,27)]:
            pts=[(x-42,y),(x-26,y-2),(x-14,y-h*.74),(x,y-h),(x+14,y-h*.74),(x+26,y-2),(x+42,y)]
            bez(d,pts,GOLD if h>30 else AMBER,4 if h>30 else 2)
        diamond(d,x,1321,8,15,AMBER);diamond(d,x,1321,3,8,PALE)
        for k in (-1,1):
            bez(d,[(x,1374),(x+9*k,1352),(x+36*k,1347),(x+36*k,1335),(x+36*k,1322),(x+24*k,1320),(x+26*k,1333)],'#a67a58',3)
    for y,w in [(1266,2),(1383,5),(1392,3),(1398,1)]:d.line((0,y,N,y),fill=GOLD,width=w)
    for x0,x1 in [(0,490),(491,995),(1242,1469),(1470,1663),(1664,1855),(1856,2047)]:
        for y in (1468,1480,1984,1995):d.line((x0,y,x1,y),fill=GOLD,width=3)
        for x in range(x0+10,x1,29):
            diamond(d,x,1967,8,13,AMBER);diamond(d,x,1967,3,7,GOLD)
    save('Vesper-Brocade',[('Blackberry silk and weave',dye(fields)),('Woven moth repeat',dam),('Hem arches and couched braid',border)])
    # Full-length embroidery beds for front, rear, hip leaves and sleeve falls.
    spans=[(0,704),(704,1296),(1296,1744),(1744,2048)]
    ground=dye([(a,0,b,N,color) for (a,b),color in zip(spans,[(60,25,54),(67,29,54),(91,37,61),(73,33,59)])])
    brod=blank();deco=blank();detail=blank()
    for idx,(a,b) in enumerate(spans):
        cx=(a+b)/2;half=(b-a)/2
        d=ImageDraw.Draw(brod)
        for row,y in enumerate(range(48,2030,94)):
            for x in range(a+40+(row%2)*39,b-22,82):diamond(d,x,y,10,24,'#633950')
        d=ImageDraw.Draw(deco)
        for sign in (-1,1):
            for margin,color,width in [(.081,AMBER,8),(.11,PALE,3),(.155,AMBER,2)]:
                x=cx+sign*half*(1-margin)
                d.line((x,12,x,2036),fill=color,width=width)
            for row in range(7):
                y=92+row*272
                def p(x,h):return (cx+sign*x*half,y+h)
                bez(d,[p(.88,0),p(.80,81),p(.39,86),p(.39,150),p(.39,206),p(.67,212),p(.67,171)],GOLD,5 if idx<2 else 3)
                bez(d,[p(.865,20),p(.82,81),p(.57,104),p(.52,139)],PALE,2)
                bez(d,[p(.40,154),p(.22,134),p(.22,108),p(.29,94)],AMBER,3)
                diamond(d,*p(.67,168),half*.018,12,PALE);diamond(d,*p(.29,94),half*.014,9,GOLD)
        d=ImageDraw.Draw(detail)
        for j,(y,f) in enumerate([(384,.90),(1070,.73),(1660,.48)]):
            s=half/124*f
            d.ellipse((cx-58*s,y-88*s,cx+58*s,y+84*s),outline=AMBER,width=3)
            d.ellipse((cx-53*s,y-80*s,cx+53*s,y+78*s),outline='#8f6354',width=2)
            for k in range(24):
                t=k*math.pi/12;px=cx+62*s*math.cos(t);py=y+92*s*math.sin(t)
                d.ellipse((px-2,py-2,px+2,py+2),fill=PALE)
            moth(d,cx,y,s)
            diamond(d,cx,y-100*s,6*s,13*s,TEAL)
        for y in (748,1400,1900):
            diamond(d,cx,y,half*.12,40,GOLD);diamond(d,cx,y,half*.085,31,'#492b48');diamond(d,cx,y,half*.033,20,TEAL)
            d.line((cx,y+42,cx,y+68),fill=AMBER,width=2)
    save('Vesper-Orphrey',[('Silk dye',ground),('Cut velvet pile',brod),('Couched gold vines',deco),('Death moths and reliquary seals',detail)])
if __name__=='__main__':make()
