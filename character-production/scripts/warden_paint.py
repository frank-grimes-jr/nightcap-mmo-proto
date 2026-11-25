"""Create native-pixel donor stencils, paint masters and elf albedo from project artwork."""
from pathlib import Path
import io, json, zipfile
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'systems-planning/assets/concept-art/dark-elf'
PROD=ROOT/'character-production'
OUT=PROD/'output/dark-elf-male/furnace-warden'
TEX=OUT/'Textures'
TEX.mkdir(parents=True,exist_ok=True)
LAY=OUT/'Paint'
LAY.mkdir(exist_ok=True)
# Points specified on a 780-pixel-wide viewing copy, transferred to the native plate.
# Order is upper-left, lower-left, lower-right, upper-right.
PATCHES=[
 ('Portrait_Hood_rim',[(493,17),(469,72),(542,52),(556,39)]),
 ('Portrait_Shoulder',[(624,148),(597,174),(739,165),(761,135)]),
 ('Portrait_Worn_edge',[(616,301),(612,321),(720,307),(721,295)]),
 ('Portrait_Grille_ember',[(519,98),(518,156),(524,151),(524,97)]),
 ('Portrait_Grille_bar',[(531,87),(530,166),(535,169),(536,88)]),
 ('Portrait_Iron',[(698,178),(692,292),(719,290),(731,179)]),
 ('Portrait_Chain',[(449,263),(445,277),(465,272),(467,260)]),
 ('Portrait_Quilt',[(346,411),(335,439),(361,448),(375,425)]),
 ('Portrait_Chest_shutter',[(430,369),(426,377),(536,371),(538,363)]),
 ('Figure_Tasset',[(167,207),(163,280),(185,289),(189,205)]),
 ('Figure_Greave',[(90,369),(80,419),(94,413),(104,378)]),
 ('Figure_Glove',[(49,231),(48,246),(61,245),(60,231)]),
 ('Authored_Rear_iron',[(698,178),(692,292),(719,290),(731,179)]),
 ('Authored_Oxide',[(617,312),(615,319),(696,311),(695,304)]),
 ('Authored_Lining',[(555,196),(553,207),(573,200),(575,188)]),
 ('Figure_Sabaton',[(189,453),(184,461),(203,468),(210,462)])]

def png(im):
    b=io.BytesIO();im.save(b,'PNG');return b.getvalue()
def save_layers(layers):
    root=ET.Element('image',{'w':'2048','h':'2048','version':'0.0.3','name':'Warden surface donors'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(LAY/'Warden-donor-layers.ora','w') as z:
        z.writestr('mimetype','image/openraster')
        for j,(name,im) in enumerate(layers):
            file='data/'+name+'.png'
            ET.SubElement(stack,'layer',{'name':name,'src':file,'x':str(j%4*512),'y':str(j//4*512),'opacity':'1.0'})
            z.writestr(file,png(im))
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        z.writestr('mergedimage.png',png(atlas))
source=Image.open(ART/'furnace-warden.png').convert('RGB')
atlas=Image.new('RGB',(2048,2048))
mask=Image.new('L',atlas.size)
layers=[];rows=[];rng=np.random.default_rng(9201)
y,x=np.mgrid[0:512,0:512]/511
for j,(name,points) in enumerate(PATCHES):
    quad=[round(c*source.width/780) for pt in points for c in pt]
    region=source.transform((512,512),Image.Transform.QUAD,quad,resample=Image.Resampling.BICUBIC)
    a=np.asarray(region,dtype=float)
    # Restrict value range of donor lighting while retaining hue and small tool marks.
    broad=np.asarray(region.filter(ImageFilter.GaussianBlur(55)),dtype=float)
    a=a-.24*(broad-np.median(broad,axis=(0,1)))
    grain=rng.normal(0,1.25,(512,512,1))
    if j in (0,1,5,8,9,10,12,15):
        roll=13*np.exp(-((.22*x+y-.29)/.25)**2)-8*y
        a+=roll[:,:,None]
    if j in (0,1,2,4,5,6,8,9,10,12,15):
        # Iron remains dark beneath the broad pale roll, especially on the shell sides.
        a=(np.maximum(a,0)/255)**1.12*244
    if j==12:a=a*np.array([.81,.86,.94])+np.array([2,3,7])
    if j==13:a=a*np.array([1.36,1.07,.78])+np.array([12,7,2])
    if j==14:a=a*.56+4
    if j==7:
        # Quilted padding follows a bias seam on the body shell.
        stitch=np.minimum(abs(np.sin((x+y)*np.pi*5)),abs(np.sin((x-y)*np.pi*5)))
        a=(np.array([63,38,49])+.26*(a-np.median(a,axis=(0,1))))*(.68+.32*np.minimum(1,stitch*4))[:,:,None]
    if j==3:
        heat=.19+.81*np.exp(-((y-.70)/.32)**2)
        a=a*.65+np.array([109,49,9])*heat[:,:,None]
        mask.paste(Image.fromarray(np.uint8(heat*229)),(1536,0))
    im=Image.fromarray((a+grain).clip(0,255).astype('uint8'))
    tile=(j%4*512,j//4*512)
    atlas.paste(im,tile);layers.append((name,im))
    rows.append(dict(layer=name,source='furnace-warden.png',native_quad_TL_BL_BR_TR=quad,destination_top_left_px=tile,size=[512,512],method='masked quadrilateral resample, broad-light attenuation, grain and local paint'))
atlas.save(LAY/'Warden-donor-color.png');mask.save(LAY/'Warden-donor-heat.png');save_layers(layers)
# Map original male facial planes into the skin palette sampled from the concept.
face=Image.open(ART/'character-plate.png').convert('RGB')
swatches=[]
for px,py in [(250,57),(267,58),(275,49),(283,57)]:
    cx=round(px*1536/400);cy=round(py*1536/400)
    swatches.append(np.asarray(face.crop((cx-3,cy-3,cx+4,cy+4))).mean((0,1)))
male=np.asarray(Image.open(PROD/'textures/male-facial-skin-albedo-2048-v01.png').convert('RGB'),float)
lum=male@np.array([.299,.587,.114])
colors=np.array([[21,19,30],swatches[0],swatches[1],swatches[2],swatches[3],[154,140,163],[187,170,187]])
skin=np.stack([np.interp(lum,[0,68,107,143,164,192,240],colors[:,i]) for i in range(3)],axis=-1)
skin=skin*np.array([.83,.84,.90])+np.array([-1,-1,2])
Image.fromarray(skin.clip(0,255).astype('uint8')).save(TEX/'DarkElf-Skin.png')
# Existing scalp strips have root-to-tip UVs, preserving painted strand direction.
hair=np.asarray(Image.open(PROD/'textures/chestnut-hair-clumps-v02.png').convert('L').resize((512,512)),float)/255
hair=np.clip(hair*1.45,0,1)
ivory=(np.array([104,96,110])+hair[:,:,None]*np.array([141,140,120])).clip(0,255)
Image.fromarray(ivory.astype('uint8')).save(TEX/'DarkElf-Ivory.png')
ey,ex=np.mgrid[-1:1:512j,-1:1:512j];rad=np.hypot(ex,ey);theta=np.arctan2(ey,ex)
spokes=np.cos(theta*89+2*np.sin(theta*19)+rad*18)*.5+.5
glow=np.clip(1-np.abs(rad-.26)*5,0,1)
eye=np.zeros((512,512,3))+np.array([169,155,155])
iris=rad<.371
eye[iris]=np.array([75,37,20])+((.49+.51*spokes)*glow)[iris,None]*np.array([170,126,39])
eye[rad<.131]=[24,16,22]
eye[np.hypot(ex+.086,ey+.105)<.040]=[250,219,162]
Image.fromarray(eye.astype('uint8')).save(TEX/'DarkElf-Amber.png')
(LAY/'donors.json').write_text(json.dumps(dict(suit=rows,skin_palette_rgb=np.round(swatches,1).tolist(),skin_source='character-plate.png, palette only; male-facial-skin-albedo-2048-v01.png, UV-local male paint; scalar luminance remap',hair='Nightcap chestnut-hair-clumps-v02.png to ivory ramp'),indent=2))

