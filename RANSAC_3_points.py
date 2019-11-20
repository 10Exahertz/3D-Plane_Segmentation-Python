#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:30:58 2019

@author: stevenalsheimer
"""

import pandas as pd
import numpy as np


DF = pd.read_csv('small_example.ptx', sep = ' ', header = None,names=["x", "y", "z", "i"])
r = 98
c = 285
d_i = r*c
DF = DF[10:7000]
DF_shaved = pd.DataFrame(DF)
indexNames = DF_shaved[DF_shaved['x'] == 0 ].index
DF_shaved.drop(indexNames , inplace=True)
DF_shaved = DF_shaved.reset_index(drop=False)
###This is where we start sampling the points and getting the plane###
d_thresh = 1##put back to 0.5
inliers = 0
planes = []
for v in range(500):#200 optimal
    inliers = 0
    sample_data = DF_shaved.sample(n=3)
    sample_data = sample_data.reset_index(drop=True)
    x_1 = sample_data.loc[0,'x']
    y_1 = sample_data.loc[0,'y']
    z_1 = sample_data.loc[0,'z']
    p_1 = np.array([x_1,y_1,z_1])


    x_2 = sample_data.loc[1,'x']
    y_2 = sample_data.loc[1,'y']
    z_2 = sample_data.loc[1,'z']
    p_2 = np.array([x_2,y_2,z_2])


    x_3 = sample_data.loc[2,'x']
    y_3 = sample_data.loc[2,'y']
    z_3 = sample_data.loc[2,'z']
    p_3 = np.array([x_3,y_3,z_3])


    v_1 = p_1-p_2
    v_2 = p_1-p_3
    cross = np.cross(v_1,v_2)

    a = cross[0]
    b = cross[1]
    c = cross[2]

    d_thresh = 1#change back to 0.5
    inliers = 0
    for i in range(len(DF_shaved)):
        x_T = DF_shaved.loc[i,'x']
        y_T = DF_shaved.loc[i,'y']
        z_T = DF_shaved.loc[i,'z']
        p_T = np.array([x_T,y_T,z_T])
        distance_point_to_plane = abs((np.dot(p_T,cross))/(np.sqrt(a**2+b**2+c**2)))
        #print(distance_point_to_plane)
        if distance_point_to_plane < d_thresh:
            inliers += 1
          
    if inliers > 200:
        planes.append(cross)
        
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
























    

    
#print(distance_point_to_plane)
#equation_plane = 