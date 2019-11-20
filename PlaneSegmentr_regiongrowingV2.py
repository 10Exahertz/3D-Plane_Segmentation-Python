#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:26:37 2019

@author: stevenalsheimer
"""

import pandas as pd
import numpy as np
from scipy.sparse.linalg import eigsh
#pd.set_option('display.max_rows', 500)


DF = pd.read_csv('small_example.ptx', sep = ' ', header = None,names=["x", "y", "z", "i"])
#print(DF)
#DF = DF[16300:19000]
r = 99#rows of dataset
c = 285#columns ""
s = 16300#start line for testing
k=3
#print(DF.iloc[:,2])
Normal = []
for x in range(10+s, 500+s):
    EE = []
    for d in range (k):
        for i in range (k): #creates a kxk neighbor subsampling of the data set
            EE.append(DF.loc[d*c+x+i])#properly takes into account data dimensions
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
                        a = np.asarray([P_p.loc[d*c+x+g]])
                        prod = a * a.T
                        F = F + prod
                Eva, Eve= eigsh(F, 1, which='SM')
                #print(Eve)
                Evee = pd.DataFrame(Eve)
                #print(Evee)
                if 0 < Eva < 0.1:
                    #print(Eva)
                    Normal.append([x,*Eve[0],*Eve[1],*Eve[2],DF.loc[(x),"x"],DF.loc[(x),"y"],DF.loc[(x),"z"],0])
                    Nm = pd.DataFrame(Normal, columns=["index","nx", "ny", "nz","x","y","z","p"])
for v in range(len(Nm)):
    index_p = Nm.loc[v,'index']
    DF.loc[index_p,'nx'] = Nm.loc[v,'nx']
    DF.loc[index_p,'ny'] = Nm.loc[v,'ny']
    DF.loc[index_p,'nz'] = Nm.loc[v,'nz']
    DF.loc[index_p,'p'] = Nm.loc[v,'p']
DF = DF.fillna(0)
                        
#print(DF.loc[2,'p'])
#p = 0
for v in range(c+1,len(DF)):
    x = DF.loc[v,'x']
    y =DF.loc[v,'y']
    z =DF.loc[v,'z']
    if x == 0 and y == 0 and z == 0:
        continue
    else:
        nx = DF.loc[v,'nx']
        ny = DF.loc[v,'ny']
        nz = DF.loc[v,'nz']
        cross_1 = np.array([nx,ny,nz])

        x2 =DF.loc[v-1,'x']
        y2 =DF.loc[v-1,'y']
        z2 =DF.loc[v-1,'z']
        nx2 =DF.loc[v-1,'nx']
        ny2 =DF.loc[v-1,'ny']
        nz2 =DF.loc[v-1,'nz']
        cross_2 = np.array([nx2,ny2,nz2])
        DiffX1 = abs(x) - abs(x2)
        DiffY1 = abs(y) - abs(y2)
        DiffZ1 = abs(z) - abs(z2)
        N = np.dot(cross_2,cross_1)

        x3 =DF.loc[v-1-c,'x']
        y3 =DF.loc[v-1-c,'y']
        z3 =DF.loc[v-1-c,'z']
        nx3 =DF.loc[v-1-c,'nx']
        ny3 =DF.loc[v-1-c,'ny']
        nz3 =DF.loc[v-1-c,'nz']
        cross_3 = np.array([nx3,ny3,nz3])
        N2 = np.dot(cross_3,cross_1)
        DiffX2 = abs(x) - abs(x3)
        DiffY2 = abs(y) - abs(y3)
        DiffZ2 = abs(z) - abs(z3)
        
        x4 =DF.loc[v-c,'x']
        y4 =DF.loc[v-c,'y']
        z4 =DF.loc[v-c,'z']
        nx4 =DF.loc[v-c,'nx']
        ny4 =DF.loc[v-c,'ny']
        nz4 =DF.loc[v-c,'nz']
        cross_4 = np.array([nx4,ny4,nz4])
        N3 = np.dot(cross_4,cross_1)
        DiffX3 = abs(x) - abs(x4)
        DiffY3 = abs(y) - abs(y4)
        DiffZ3 = abs(z) - abs(z4)
        p1 = 0
        p2 = 0
        p3 = 0
        DIST_tresh = 0.01
        ANG_thresh = 0.9
        if x2 != 0 and y2 != 0 and z2 != 0 and DiffX1 < DIST_tresh and DiffY1 <DIST_tresh and DiffZ1 < DIST_tresh and abs(N) > ANG_thresh:
            if DF.loc[v-1,'p'] == 0:
                p3 = 0
            else:
                p3 = DF.loc[v-1,'p']
        if x3 != 0 and y3 != 0 and z3 != 0 and DiffX2 < DIST_tresh and DiffY2 <DIST_tresh and DiffZ2 < DIST_tresh and abs(N2) > ANG_thresh:
            if DF.loc[v-1-c,'p'] == 0:
                p1 = 0##placement of p1 is based on the diagonal
            else:
                p1 = DF.loc[v-1-c,'p']
        if x4 != 0 and y4 != 0 and z4 != 0 and DiffX3 < DIST_tresh and DiffY3 <DIST_tresh and DiffZ3 < DIST_tresh and abs(N3) > ANG_thresh:
            if DF.loc[v-c,'p'] == 0:
                p2 = 0
            else:
                p2 = DF.loc[v-c,'p']
        ###for real points that are not in the same plane at all###        
        if x2 != 0 and y2 != 0 and z2 != 0 and not DiffX1 < DIST_tresh and not DiffY1 <DIST_tresh and not DiffZ1 < DIST_tresh and not N > ANG_thresh:
            p1 = 0
        if  x3 != 0 and y3 != 0 and z3 != 0 and not DiffX2 < DIST_tresh and not DiffY2 <DIST_tresh and not DiffZ2 < DIST_tresh and not N2 > ANG_thresh:
            p2 = 0
        if  x4 != 0 and y4 != 0 and  z4 != 0 and not DiffX3 < DIST_tresh and DiffY3 <DIST_tresh and DiffZ3 < DIST_tresh and not N3 > ANG_thresh:
            p3=0
            
        ###Compare the 3 different neighbors and label###
        if p1 == 0 and p2 == 0 and p3 == 0:
            p_max = Nm['p'].max()
            p = p_max +1
            DF.loc[v,'p'] = p
        if p1 != 0 and p2 != 0 and p3 == 0:
            DF.loc[v,'p'] = p1
            if p1 != p2:
                DF.replace({'p':{p2:p1}})
                print('yeys',p1,p2)
            ###STORE HERE EQUIVALANCY TABLE###
        if p1 != 0 and p2 == 0 and p3 != 0:
            print('yesp1p3')
            DF.loc[v,'p'] = p1
            if p1 != p3:
                DF.replace({'p':{p3:p1}})
                print(p3,p1)
            ##STORE###
        if p1 == 0 and p2 != 0 and p3 != 0:
            DF.loc[v,'p'] = p2
            if p3 != p2:
                DF.replace({'p':{p3:p2}})
                print('yes',p3,p2)
            ###STORE###
        if p1 == 0 and p2 == 0 and p3 != 0:
            DF.loc[v,'p'] = p3
        if p1 == 0 and p2 != 0 and p3 == 0:
            DF.loc[v,'p'] = p2
        if p1 != 0 and p2 == 0 and p3 == 0:
            DF.loc[v,'p'] = p1
print(DF[16800:16900])
print(len(DF['p'].unique().tolist()))
###USE IMAGE CLASS, can albel the features####
        
        
        