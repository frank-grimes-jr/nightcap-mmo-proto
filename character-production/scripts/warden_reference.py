"""Make the local-only scale board from the preview screenshots and original M2 bind meshes."""
from pathlib import Path
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops
import mpyq

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT/'systems-planning/assets/concept-art/dark-elf'
REF = ROOT/'dark-elf-reference-local-20261124'
OUT = ROOT/'character-production/output/dark-elf-male/furnace-warden'
REVIEW = OUT/'Review'
REVIEW.mkdir(parents=True, exist_ok=True)
BG = (34,31,39)
font_path = 'C:/Windows/Fonts/segoeui.ttf'
def font(size): return ImageFont.truetype(font_path,size)

def compare_image(image):
    bg = Image.new('RGB',image.size,image.getpixel((0,0)))
    mask = ImageChops.difference(bg,image).convert('L').point(lambda x:255 if x>11 else 0)
    box = mask.getbbox()
    return image.crop(box)

def m2_views(archive, race):
    base = '\\'.join(['Character',race,'Male',race+'Male'])
    data,skin = [archive.read_file(base+s) for s in ('.m2','00.skin')]
    assert data[:4]==b'MD20' and skin[:4]==b'SKIN'
    nv,vo = struct.unpack_from('<II',data,60)
    # Wrath M2 vertices are 48 bytes with the position at byte zero.
    vertices = np.ndarray((nv,3),dtype='<f4',buffer=data,offset=vo,strides=(48,4)).copy()
    ni,oi,nt,ot,_,_,ns,os = struct.unpack_from('<8I',skin,4)
    index = np.frombuffer(skin,'<u2',ni,oi)
    triangles = index[np.frombuffer(skin,'<u2',nt,ot)]
    faces = []
    for j in range(ns):
        gid,level,_,_,start,count = struct.unpack_from('<6H',skin,os+48*j)
        if gid in (0,1,101,201,301,401,501,702,801,901,1001,1101,1201,1301,1501,1701,1801,2001):
            faces.extend(triangles[start:start+count].reshape((-1,3)))
    v=vertices[np.array(faces)]
    zmin,zmax=v[:,:,2].min(),v[:,:,2].max()
    for axis,horizontal in [(0,1),(1,0)]:
        # +X is anterior in the archive. Face toward the right in profile.
        ux = v[:,:,horizontal]*(-1 if axis==0 else 1)
        uy = -v[:,:,2]
        depth = v[:,:,axis].mean(axis=1)
        scale = 630/(zmax-zmin)
        xy=np.stack(((ux-ux.min())*scale+4,(uy+zmax)*scale+4),axis=2)
        canvas=Image.new('RGB',(int(np.ceil(xy[:,:,0].max()+5)),639),BG)
        pen=ImageDraw.Draw(canvas)
        norm=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0])
        norm/=np.maximum(np.linalg.norm(norm,axis=1,keepdims=True),1e-7)
        lum=(norm@np.array([.66,.32,.67])).clip(-1,1)
        for i in np.argsort(depth):
            shade=(np.array([144,137,161])*(.75+.37*lum[i])).astype('int')
            pen.polygon([tuple(p) for p in xy[i]],fill=tuple(shade))
        yield compare_image(canvas)

def board():
    archive=mpyq.MPQArchive('E:/Wow_Ascension/Data/common-2.MPQ',listfile=False)
    shots=[compare_image(Image.open(REF/'male-study/screenshots'/f'full-{a}.png').convert('RGB')) for a in [0,128]]
    panels = [shots,list(m2_views(archive,'BloodElf')),list(m2_views(archive,'NightElf'))]
    sheet=Image.new('RGB',(1860,780),(26,23,29))
    draw=ImageDraw.Draw(sheet)
    draw.text((34,19),'Male elf reference   /   crown-to-sole study',font=font(32),fill='#eee6db')
    draw.text((35,70),'Surface landmarks estimated in each rest or idle view. Datum lines at crown and sole. M2 neutral geometry, local archive.',font=font(18),fill='#bdafb2')
    marks=[(.067,.17,.28,.32,.65,.92),(.078,.18,.355,.465,.675,.929),(.082,.18,.36,.467,.68,.925)]
    for i,(name,pair) in enumerate(zip(['Hailstone  /  Dark Elf','Ascension  /  Blood Elf','Ascension  /  Night Elf'],panels)):
        start=22+i*612
        draw.text((start+14,112),name,font=font(23),fill='#ddc9a6')
        for j,img in enumerate(pair):
            # Reserve identical height across all six poses.
            img=img.resize((round(img.width*485/img.height),485),Image.Resampling.LANCZOS)
            cx=start+223+235*j
            sheet.paste(img,(int(cx-img.width/2),180))
            for k,(label,frac) in enumerate(zip(('eye','shoulder','elbow','wrist','knee','ankle'),marks[i])):
                yy=round(180+485*frac)
                x=start+(2 if j==0 else 370)
                if j==0:
                    draw.text((x,yy-9),label,font=font(12),fill='#e6c4a8')
                # Project each estimated level to a small tick outside the silhouette.
                draw.line((x+(65 if not j else 0),yy,cx-(img.width/2)+4,yy),fill='#b78e71',width=1)
            draw.line((cx-77,180,cx+77,180),fill='#988373')
            draw.line((cx-77,665,cx+77,665),fill='#988373')
            draw.text((cx-24,685),'Front' if j==0 else 'Profile',font=font(16),fill='#dacdcc')
    draw.text((35,738),'Hailstone viewer r:6:0   •   BloodElfMale.m2 and NightElfMale.m2   •   front and profile use the same source pose per figure',font=font(17),fill='#bdafb2')
    sheet.save(REVIEW/'Male-model-comparison.jpg',quality=94)
    landmark_sheet(panels,marks)

def landmark_sheet(panels,marks):
    """Normalize on the center of the skull so tall ear tips cannot set the scale."""
    sheet=Image.new('RGB',(1560,752),(26,23,29));d=ImageDraw.Draw(sheet)
    d.text((28,20),'Crown, joint levels and ear rake',font=font(30),fill='#eee6db')
    d.text((28,68),'Front and profile   /   470 px from central crown to sole   /   dots are visual estimates',font=font(17),fill='#c3adb1')
    # Coordinates are inspected fractions across each independently cropped silhouette.
    xrows=[[(.51,.30,.12,.12,.28,.23),(.53,.41,.16,.81,.68,.72)],
           [(.51,.21,.085,.055,.29,.31),(.69,.53,.43,.74,.49,.43)],
           [(.51,.22,.085,.065,.30,.31),(.73,.62,.52,.76,.53,.48)]]
    labels=('Eye','Shoulder','Elbow','Wrist','Knee','Ankle')
    for i,(pair,title) in enumerate(zip(panels,['Hailstone Dark Elf','Ascension Blood Elf','Ascension Night Elf'])):
        d.text((22+i*518,112),title,font=font(21),fill='#dfc6aa')
        for j,img in enumerate(pair):
            rgb=np.array(img,dtype=int)
            # Most frequent colour on the border is the render background.
            colors,counts=np.unique(np.vstack([rgb[0],rgb[-1],rgb[:,0],rgb[:,-1]]),axis=0,return_counts=True)
            fg=np.max(np.abs(rgb-colors[counts.argmax()]),axis=2)>14
            # Use a narrow window over the skull. Profile centers are in front of the ears.
            fx=(.50 if j==0 else [.48,.60,.69][i])
            lo=max(0,int(img.width*(fx-.025)));hi=min(img.width,int(img.width*(fx+.025))+1)
            crown=int(np.nonzero(fg[:,lo:hi].any(axis=1))[0][0])
            s=470/(img.height-1-crown);im=img.resize((round(img.width*s),round(img.height*s)),Image.Resampling.LANCZOS)
            cx=140+i*518+j*241;left=cx-im.width//2;top=190-round(crown*s)
            sheet.paste(im,(left,top))
            d.line((cx-68,190,cx+68,190),fill='#907b77')
            d.line((cx-68,660,cx+68,660),fill='#907b77')
            for k,(xf,yf) in enumerate(zip(xrows[i][j],marks[i])):
                px=left+int(im.width*xf);py=top+int(im.height*yf)
                d.ellipse((px-3,py-3,px+3,py+3),fill='#f1c38f',outline='#563b36')
                if j==0:
                    lab=22+i*518
                    d.line((lab+52,py,px-4,py),fill='#b39178')
                    d.text((lab,py-9),labels[k],font=font(12),fill='#ead0b1')
            d.text((cx-21,684),'Front' if j==0 else 'Profile',font=font(16),fill='#d1bdb3')
    sheet.save(REVIEW/'Male-landmarks.jpg',quality=95)

def reference_board():
    sheet=Image.new('RGB',(1520,1100),(24,22,28))
    d=ImageDraw.Draw(sheet)
    panels=[(ART/'furnace-warden.png',(24,70,915,675),'Furnace Warden  /  silhouette, visor, iron and shutters'),
            (ART/'character-plate.png',(940,70,560,280),'Character plate  /  facial planes and skin'),
            (ART/'armor-finishes.png',(940,420,560,280),'Finish study  /  cool roll into plum'),
            (REF/'screenshots/dark-elf.png',(20,770,660,265),'Hailstone DAF  /  native-scale value grouping'),
            (REF/'shaman-chests.jpg',(700,770,800,265),'Ascension shaman chests  /  fastener and link rhythm')]
    d.text((24,12),'Furnace Warden   /   reference board',font=font(30),fill='#e9dfd1')
    for path,(x,y,w,h),label in panels:
        im=Image.open(path).convert('RGB');im.thumbnail((w,h))
        sheet.paste(im,(x,y));d.text((x,y+im.height+6),label,font=font(17),fill='#c7b7a3')
    sheet.save(REVIEW/'Design-board.jpg',quality=93)

if __name__=='__main__':
    reference_board()
    board()

