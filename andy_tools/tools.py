#!/usr/bin/python3

# Programa Creado Por Andy Zapata - IMIT 2020
# Realiza el producto cruz entre 2 vectores y 
# con el vector resultante, calcula el angulo
# entre éste y otro vector 

import numpy as np
from numpy.linalg import norm
import glob # - Unix style pathname pattern expansion (Edison)
import math as mh

#=================================================================================================#
def filesxyz () :
    """
    Get names of xyz at current directory
    """
    # - Lineas tomadas del script creado por Edison: radial_distribution_analisys.py
    list_xyz = []  # unique files

    for input_xyz in glob.glob('*.xyz'):
        list_xyz = input_xyz[:-4]  # deleting file extention

    return list_xyz
#=================================================================================================# 
def LXYZ (NXYZ) :
    """
    Get Number of atoms, labels and coordenates of the atoms in xyz
    """
    natoms = 0

    g = NXYZ + ".xyz"
    f = open(g,"r")
    natoms = int(f.readline())
    print (f"Numero de atomos en",g,":",natoms)

    f.readline()
    MXYZ = np.zeros((natoms,3)) 
    LA = []
    LA.append(natoms)
    for i in range(natoms):
        line = f.readline()
        for j in range(4):
            if j == 0 :
                LA.append(line.split()[0])  #En vez de guardar el n'umero como str, se podría
            else :                          #poner el número atómico, asi se juntan los arreglos 
                MXYZ[i,j-1] = line.split()[j] # Z + coord
            
    f.close()            
    return LA, MXYZ
#=================================================================================================#
def rv (va,rmax,NALA,MXYZ) :
    """
    Return distance of all atoms to vertice and coordinates, which are lesser to rmax
    """    
    #Esta hecho solo por ahora, para tener solo un tipo de átomo
    #del vertice
    coordv = np.zeros((3))
    for i in range(NALA[0]):
        if va == NALA[i+1] :
            for j in range(3):
                coordv[j] = MXYZ[i,j]
    distv = np.zeros((NALA[0]-1,4))
    dr = np.zeros((3))
    r = 0.0
    cont = 0
    for i in range(NALA[0]) :
        for j in range(3):
            if va != NALA[i+1] :
                dr[j] = MXYZ[i,j] - coordv[j]
                if j == 2 :
                    r = dr[0]*dr[0] + dr[1]*dr[1] + dr[2]*dr[2]
                    r = mh.sqrt(r)
                    if r <= rmax :
                        for k in range(4) :
                            if k == 3 : 
                                distv[cont,k] = r
                                cont += 1
                            else :
                                distv[cont,k] = MXYZ[i,k] - coordv[k]  #Se resta coordv, para cambiar el cero de los vectores
                                
    return cont, distv
#=====================================================================================#
def angle (NAV,VR) :
    """
    Get angles between vectors
    """
    cont = 0 #número de ángulos tetha calculados
    tetha = []
    cont = 0
    print ("NAV ",NAV)
    for i in range(NAV-1) :
        l = i
        while l < NAV-1 :
            l += 1
            APB = 0.0
            for k in range(3) :
                APB += VR[i,k]*VR[l,k]
            C = 0.0
            C = APB/(VR[i,3]*VR[l,3])    
            t = 0.0
            t = mh.acos(C)
            t = t*180/mh.pi
            tetha.append(t)
            cont += 1
    return cont, tetha
#=================================================================================================#
def SM (NALA,MXYZ,rmaxo) :
    """
    Search water molecules, which are lesser to rmaxo to Hg
    """
    coordv = np.zeros((3))
    for i in range(NALA[0]):
        if "Hg" == NALA[i+1] :
            for j in range(3):
                coordv[j] = MXYZ[i,j]
    distv = np.zeros((NALA[0]-1,4))
    dr = np.zeros((3))
    r = 0.0
    cont = 0
    for i in range(NALA[0]) :
        for j in range(3):
            if "Hg" != NALA[i+1] :
                dr[j] = MXYZ[i,j] - coordv[j]
                if j == 2 :
                    r = dr[0]*dr[0] + dr[1]*dr[1] + dr[2]*dr[2]
                    r = mh.sqrt(r)
                    if r <= rmaxo :
                        for k in range(4) :
                            if k == 3 : 
                                distv[cont,k] = r
                                cont += 1
                                #Busco H más cercanos a O, distancia < 1.5
                                if 'O' in NALA[i+1] :
                                    for ii in range(NALA[0]):
                                        for jj in range(3):
                                            if 'Hg' != NALA[ii+1] and 'O' != NALA[ii+1] :
                                                dr[jj] = MXYZ[ii,jj] - MXYZ[i,jj]
                                                if jj == 2 :
                                                    r = dr[0]*dr[0] + dr[1]*dr[1] + dr[2]*dr[2]
                                                    r = mh.sqrt(r)
                                                    if r <= 1.5 :  #El valor 1.5 es para garantizar los H que se disocian del H2O
                                                        for kk in range(4):
                                                            if kk == 3 :                                                                
                                                                distv[cont,kk] = r
                                                                #print (NALA[ii+1]," : ",distv[cont,:])
                                                                cont += 1
                                                            else:
                                                                distv[cont,kk] = MXYZ[ii,kk]
                            else :
                                distv[cont,k] = MXYZ[i,k] 
    return cont, distv, coordv
#=================================================================================================#
def dihedral (NAW,VR,RHg) :
    """
    Calculate dihedral between water molecule and Hg with Praxeolitic formule
    https://en.wikipedia.org/wiki/Talk%3ADihedral_angle
    https://www.it-swarm.dev/es/python/angulo-diedrico-torsion-desde-cuatro-puntos-en-coordenadas-cartesianas-en-python/1042912628/
    """
    #        H
    #       /|
    # Hg\  O |<- El ángulo dihedral, describe la torsión del vector señalado
    #    \---H
    #
    NO = 0
    NO = int(NAW/3)
    #print ("# O : ",NO)
    #Vectores O->H, H->H, H->Hg
    voh = np.zeros((NO,3))
    vhh = np.zeros((NO,3))
    vhhg= np.zeros((NO,3))
    cont = 0
    for i in range(NO):
        l = i+i*2
        for k in range(3) :
            voh[cont,k] = -1.0*(VR[l+1,k] - VR[l,k])   #Distancia O->H
            vhh[cont,k] = VR[l+2,k] - VR[l+1,k]        #Distancia H->H
            vhhg[cont,k] = RHg[k] - VR[l+2,k]      #Distancia H-Hg
        cont += 1

    #Normalizo vector H->H
    nhh = 0.0
    for i in range(NO):
        dr = 0.0
        r = 0.0
        for j in range(3):
            dr = vhh[i,j]*vhh[i,j]
            r += dr
        nhh = mh.sqrt(r)
        for j in range(3) :
            vhh[i,j] = vhh[i,j]/nhh 
    # vOHvHH Proyección de O->H en H->H y resto componente que alignea a H->H
    # vHHgvHH Proyección de H->Hg en H->H y resto componente que alignea a H->H
    dih = np.zeros((NO))
    cont = 0
    for i in range(NO) :
        droh  = roh = 0.0
        drhhg = rhhg = 0.0
        vOHvHH = np.zeros((3))
        vHHgvHH = np.zeros((3))
        x = 0.0
        y = 0.0
        y1 = np.zeros((3))
        for j in range(3): #Producto punto o proyección
            droh   = voh[i,j]*vhh[i,j]
            roh  += droh
            drhhg  = vhhg[i,j]*vhh[i,j]
            rhhg += drhhg
        for j in range(3): #Resto
            vOHvHH[j] = voh[i,j] - roh*vhh[i,j] 
            vHHgvHH[j] = vhhg[i,j] - rhhg*vhh[i,j] 
    # El ángulo entre vOHvHH y vHHgvHH en un plano es el ángulo de torsión
            x += vOHvHH[j]*vHHgvHH[j]
        y1 = np.cross(vhh[i,:],vOHvHH)
        for j in range(3):
            y +=  y1[j]*vHHgvHH[j]
        dih[cont] = np.arctan2(y,x)*180/mh.pi
        cont += 1
    return dih
