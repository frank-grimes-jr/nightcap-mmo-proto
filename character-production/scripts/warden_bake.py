"""Resample projected donor coordinates into the suit's unique runtime UV atlas."""
from pathlib import Path
import sys
import numpy as np
from PIL import Image
out=Path(sys.argv[1]);size=2048
arrays=np.load(sys.argv[2]); old,new,positions=(arrays[n] for n in ('old','new','positions'))
color=np.asarray(Image.open(out/'Paint/Warden-donor-color.png'),float)
heat=np.asarray(Image.open(out/'Paint/Warden-donor-heat.png'),float)
source=np.dstack((color,heat))
canvas=np.zeros((size,size,4),np.uint8)
occupied=np.zeros((size,size),bool)
region_ids=np.zeros((size,size),np.uint8)
for a,b,p in zip(old,new,positions):
    # PNG pixel centers, Blender UV origin at lower left.
    dst=b*np.array([size,-size])+[-.5,size-.5]
    lo=np.maximum(np.ceil(dst.min(0)).astype(int),0);hi=np.minimum(np.floor(dst.max(0)).astype(int),size-1)
    if (hi<lo).any():continue
    x,y=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1))
    dx=x-dst[0,0];dy=y-dst[0,1]
    A,B=dst[1]-dst[0],dst[2]-dst[0]
    det=A[0]*B[1]-B[0]*A[1]
    if abs(det)<1e-8:continue
    u=(B[1]*dx-B[0]*dy)/det
    v=(-A[1]*dx+A[0]*dy)/det
    valid=(u>=-1e-5)&(v>=-1e-5)&(u+v<=1.00001)
    if not valid.any():continue
    u=u[valid,None];v=v[valid,None]
    uv=a[0]+u*(a[1]-a[0])+v*(a[2]-a[0])
    st=np.clip(uv*np.array([size,-size])+[-.5,size-.5],0,size-1.001)
    ij=np.floor(st).astype(int);fx=(st[:,0]-ij[:,0])[:,None];fy=(st[:,1]-ij[:,1])[:,None]
    sx,sy=ij.T
    pix=(1-fy)*((1-fx)*source[sy,sx]+fx*source[sy,sx+1])+fy*((1-fx)*source[sy+1,sx]+fx*source[sy+1,sx+1])
    # Low-amplitude nonrepeating oxide, continuous in world coordinates.
    pos=p[0]+u*(p[1]-p[0])+v*(p[2]-p[0])
    wave=np.sin(pos@np.array([7,17,13]))*np.cos(pos@np.array([41,23,29]))
    pix[:,:3]+=wave[:,None]*np.array([3.8,1.8,.7])
    canvas[y[valid],x[valid]]=pix.clip(0,255).astype(np.uint8)
    region_ids[y[valid],x[valid]]=1+sx//512+(sy//512)*4
    occupied[y[valid],x[valid]]=True
for _ in range(16):
    prev=occupied.copy()
    for ax,ay in [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]:
        neighbor=np.roll(prev,(ay,ax),(0,1));edge=neighbor&~occupied
        if ay>0:edge[:ay]=False
        if ay<0:edge[ay:]=False
        if ax>0:edge[:,:ax]=False
        if ax<0:edge[:,ax:]=False
        canvas[edge]=np.roll(canvas,(ay,ax),(0,1))[edge]
        occupied|=edge
Image.fromarray(canvas[:,:,:3]).save(out/'Textures/Warden-Plate.png')
Image.fromarray(canvas[:,:,3]).save(out/'Textures/Warden-Heat.png')
Image.fromarray(region_ids).save(out/'Paint/UV0-donor-region-ids.png')

