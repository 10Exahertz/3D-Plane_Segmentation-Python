#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 15:36:01 2019

@author: stevenalsheimer
"""

import pandas as pd
import numpy as np
from scipy.sparse.linalg import eigsh


DF = pd.read_csv('small_example.ptx', sep = ' ', header = None,names=["x", "y", "z", "i"])
r = 98
col = 285
k=5
d_i = r*col
DF = DF[10:9000]
DF_shaved = pd.DataFrame(DF)
valll = len(DF)
DF_shaved = DF_shaved[10:(valll-k*col)]
indexNames = DF_shaved[DF_shaved['x'] == 0 ].index
DF_shaved.drop(indexNames , inplace=True)
DF_shaved = DF_shaved.reset_index(drop=False)
###This is where we start sampling the points and getting the plane###
d_thresh = 1##put back to 0.5
inliers = 0
planes = []
###Get random sampling###
for v in range(50):#200 optimal
    inliers = 0
    sample_data = DF_shaved.sample(n=1)
    sample_data = sample_data.reset_index(drop=True)
    x_1 = sample_data.loc[0,'x']
    y_1 = sample_data.loc[0,'y']
    z_1 = sample_data.loc[0,'z']
    p_1 = np.array([x_1,y_1,z_1])
    index_c = sample_data.loc[0,'index']
    EE = []
    for d in range (k):
        for i in range (k): #creates a kxk neighbor subsampling of the data set
            EE.append(DF.loc[d*col+index_c+i])#properly takes into account data dimensions
            EF = pd.DataFrame(EE)
            c_x = EF["x"].mean()
            c_y = EF["y"].mean()
            c_z = EF["z"].mean()
            P = EF - [c_x,c_y,c_z,0]
            P_p = P.drop(["i"], axis = 1)
            if d+i == (k-1)+(k-1):
                F = np.zeros((3,3))
                for d in range (k):
                    for g in range (k):
                        a = np.asarray([P_p.loc[d*col+index_c+g]])
                        prod = a * a.T
                        F = F + prod
                Eva, Eve= eigsh(F, 1, which='SM')
                #print(Eve)
                Evee = pd.DataFrame(Eve)
                #print(Evee)
                if 0 < Eva < 1:
                    planes.append([*Eve[0],*Eve[1],*Eve[2]])
planes_dat = pd.DataFrame(planes, columns = ['x','y','z'])
planes_dat = planes_dat.sort_values('x', ascending =False)
planes_dat = planes_dat.reset_index()
plane_dats = [0]
for i in range(len(planes_dat)-1):
    x = abs(planes_dat.loc[i,'x'])
    y = abs(planes_dat.loc[i,'y'])
    z = abs(planes_dat.loc[i,'z'])
    p = np.array([x,y,z])
    p_m = abs(np.sqrt(x**2+y**2+z**2))
    x2 = abs(planes_dat.loc[i+1,'x'])
    y2= abs(planes_dat.loc[i+1,'y'])
    z2= abs(planes_dat.loc[i+1,'z'])
    p2 =np.array([x2,y2,z2])
    p2_m = abs(np.sqrt(x2**2+y2**2+z2**2))
    n = np.dot(p,p2)/(p_m*p2_m)
    plane_dats.append(n)
plane_datss = pd.DataFrame(plane_dats, columns = ['n'])
planes_dat = pd.concat([planes_dat, plane_datss], axis=1, sort=False)

planes_dat.columns = ['i','x','y','z','n']
#print(planes_dat)
resultNames = planes_dat[ planes_dat['n'] > 0.9 ].index

 
# Delete these row indexes from dataFrame
planes_dat.drop(resultNames , inplace=True)
planes_dat = planes_dat.reset_index()

#for v in range(planes_dat):
    

###assign colors to planes###
for i in range(len(planes_dat)):
    r = 70+i*50
    if r > 225:
        r = 70
    b = 70+ i*30
    if b> 225:
        b = 70
    g = 70+ i*10
    if g>225:
        g = 70
    planes_dat.loc[i,'r']=r
    planes_dat.loc[i,'b']=b
    planes_dat.loc[i,'g']=g
print(planes_dat)
###Assign points to one of the created planes###
for i in range(10,len(DF)):
    x = DF.loc[i,'x']
    y = DF.loc[i,'y']
    z = DF.loc[i,'z']
    if x == 0 and y == 0 and z == 0:
        continue
    else:
        p_1 = np.array([x,y,z])
        best_value = 5
        d_thresh_p = 0.2
        for d in range(len(planes_dat)):
            nx= planes_dat.loc[d,'x']
            ny= planes_dat.loc[d,'y']
            nz= planes_dat.loc[d,'z']
            cross = np.array([nx,ny,nz])
            distance_point_to_plane = abs((np.dot(p_1,cross))/(np.sqrt(nx**2+ny**2+nz**2)))
            if distance_point_to_plane < d_thresh_p:
                if distance_point_to_plane < best_value:
                    r = planes_dat.loc[d,'r']
                    g = planes_dat.loc[d,'g']
                    b = planes_dat.loc[d,'b']
                    DF.loc[i,'r'] = r
                    DF.loc[i,'g'] = g
                    DF.loc[i,'b'] = b
                    DF.loc[i,'i'] = 1
DF = DF.fillna(0)
            
print(DF[958:4000])              
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    