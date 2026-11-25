"""Publish an asset plate, mip contact sheet and abbreviated equipment index."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np
R=Path(__file__).resolve().parents[1]/'output/dark-elf-male/furnace-warden/Review'
O=R.parent
def font(size,bold=False,serif=False):
    name=('georgiab' if bold else 'georgia') if serif else ('segoeuib' if bold else 'segoeui')
    return ImageFont.truetype('C:/Windows/Fonts/'+name+'.ttf',size)
def fitted(img,w,h):
    img=img.crop(img.getbbox());img.thumbnail((w,h),Image.Resampling.LANCZOS);return img
def backdrop(w,h):
    yy,xx=np.ogrid[:h,:w];fall=np.exp(-((xx/w-.36)/.82)**2-((yy/h-.38)/.76)**2)
    a=np.array([23,21,29])+fall[:,:,None]*np.array([35,31,35])
    return Image.fromarray(a.astype('uint8'))
def paste(a,filename,box):
    im=fitted(Image.open(R/filename).convert('RGBA'),box[2],box[3])
    a.paste(im,(box[0]+(box[2]-im.width)//2,box[1]+(box[3]-im.height)//2),im)
def publish():
    board=backdrop(1632,1080);d=ImageDraw.Draw(board)
    d.text((65,41),'N I G H T C A P     /     C H A R A C T E R   S T U D I E S',font=font(16,True),fill='#c4a791')
    d.text((60,79),'Furnace Warden',font=font(65,False,True),fill='#f0e7db')
    d.text((66,167),'Male Dark Elf   /   Lava-forged plate',font=font(23),fill='#d1bdb1')
    d.line((65,220,1566,220),fill='#76635e',width=1)
    paste(board,'Three-quarter.png',(45,236,620,786))
    paste(board,'Helmet-detail.png',(720,249,404,465))
    paste(board,'Uncovered-head.png',(1161,249,400,465))
    d.text((733,733),'Closed forge hood',font=font(26,False,True),fill='#eee0d4')
    d.text((1165,733),'Uncovered head',font=font(26,False,True),fill='#eee0d4')
    d.line((726,798,1567,798),fill='#76635e')
    tap=Image.open(R/'Front.png').convert('RGBA');tap=fitted(tap,180,128);tap.save(R/'Figure-128.png')
    board.paste(tap,(740,844),tap)
    d.text((884,845),'Bind pose',font=font(24,False,True),fill='#eee0d4')
    d.text((884,897),'1.820 m barefoot     /     53 bones',font=font(20),fill='#ccb8aa')
    d.text((884,938),'Figure at left shown at 128 pixels high.',font=font(17),fill='#b0a1a2')
    board.save(R/'Furnace-Warden.jpg',quality=95,subsampling=0)
    # Show actual downsampled atlas data and isolated portrait-size detail.
    proof=backdrop(1160,520);d=ImageDraw.Draw(proof)
    d.text((24,16),'Runtime paint at reduced texture sizes',font=font(28),fill='#ede0d4')
    src=Image.open(O/'Textures/Warden-Plate.png')
    for i,sz in enumerate([2048,1024,512,256]):
        im=src.resize((sz,sz),Image.Resampling.BOX);im.thumbnail((256,256))
        proof.paste(im,(23+285*i,88))
        d.text((23+285*i,368),f'{sz} × {sz}',font=font(22),fill='#d7c7ba')
    d.text((23,440),'Albedo   /   UV0    •    16 px edge extension at 2048',font=font(17),fill='#ccb6a0')
    proof.save(R/'Plate-mips.jpg',quality=94)
if __name__=='__main__':publish()

