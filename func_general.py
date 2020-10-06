#!/usr/bin/env python3
# --------------------------------------------------------#
#   danianescobarv@gmail.com                              #
#   edisonffh@gmail.com                                   #
#   cesarfernando.ibarguen@gmail.com                      #
# --------------------------------------------------------#

import numpy as np

#---------------------------------------------------------#
# -Start: Read information in the files .xyz              #
#---------------------------------------------------------#
def input_from_XYZ (list_xyz) :
    """
    Number of atoms, labels and coordenates of the atoms in xyz
    Args:
        list_xyz list) : list with the names of files xyz
    Return:
        max_natoms (int) : Number max of atoms in xyz
        At_Symb (list)   : Atomic symbol in each xyz
        MXYZ (array)     : Coordinates in each xyz
        N_Atoms (array)  : Number of atoms in each .xyz
    """

    count1 = 0
    while count1 < len(list_xyz):
        NA = []
        f = open(list_xyz[count1],"r")
        NA.append(int(f.readline()))
        f.close
        count1 += 1
    max_natoms = max(NA)

    natoms = 0
    count = 0
    MXYZ = np.zeros((len(list_xyz),max_natoms,3))
    N_Atoms = np.zeros((len(list_xyz)))
    At_Symb = [[0 for x in range(max_natoms)] for y in range(len(list_xyz))]
    while count < len(list_xyz):
        f = open(list_xyz[count],"r")
        natoms = int(f.readline())
        N_Atoms[count] = natoms
        f.readline()
        for i in range(natoms):
            line = f.readline()
            for j in range(4):
                if j == 0 :
                    At_Symb[count][i] = line.split()[0]
                else :
                    MXYZ[count,i,j-1] = line.split()[j]
        count += 1
        f.close()

    return max_natoms, At_Symb, MXYZ, N_Atoms
#---------------------------------------------------------#
# -End: Read information in the files .xyz              #
#---------------------------------------------------------#

#---------------------------------------------------------#
# -Start: Build Distance Matrix to each .xyz              #
#---------------------------------------------------------#
def Mat_Distance(nxyz,max_natoms,N_Atoms,MXYZ):
    """[summary]
    Calculate the distance matrix associated with each
    file .xyz
    Args:
        nxyz (int)      : Number of file .xyz
        max_natoms (int): Number maximum of atoms among the .xyz
        MXYZ (array)    : Coordinate in each .xyz
        N_Atoms (array) : Number of atoms in each .xyz
    Return:
        Mat_R (array)   : Upper triangular distances matrix of each .xyz
    """

    Mat_R = np.zeros((nxyz,max_natoms,max_natoms))
    for i in range(nxyz):
        natoms = int(N_Atoms[i])
        for j in range(natoms):
            k = j + 1
            while k < natoms:
                distance_ab = np.zeros((3))
                for l in range(3):
                    distance_ab[l] = MXYZ[i,k,l]-MXYZ[i,j,l]
                    distance_ab[l] *= distance_ab[l]
                    if l > 0:
                        distance_ab[l] += distance_ab[l-1]
                Mat_R[i,j,k] = np.sqrt(distance_ab[l])
                k += 1

    return Mat_R
#---------------------------------------------------------#
# -End: Build Distance Matrix to each .xyz                #
#---------------------------------------------------------#