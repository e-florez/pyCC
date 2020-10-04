#!/usr/bin/env python3
# --------------------------------------------------------#
#   danianescobarv@gmail.com                              #
#   edisonffh@gmail.com                                   #
#   cesarfernando.ibarguen@gmail.com                      #
# --------------------------------------------------------#

import numpy as np

def input_from_XYZ (list_xyz) :
    """
    Number of atoms, labels and coordenates of the atoms in xyz
    Input:
        list_xyz list) : list with the names of files xyz
    Output:
        max_natoms (int) : Number max of atoms in xyz
        At_Symb (array)  : Atomic Symbol
        MXYZ (array)     : Coordinates
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
    while count < len(list_xyz):
        f = open(list_xyz[count],"r")
        natoms = int(f.readline())
        f.readline()
        MXYZ = np.zeros((max_natoms,3))
        At_Symb   = np.chararray((max_natoms))
        for i in range(natoms):
            line = f.readline()
            for j in range(4):
                if j == 0 :
                    At_Symb[i] = line.split()[0]
                else :
                    MXYZ[i,j-1] = line.split()[j] # Z + coord
        count += 1
        f.close()

    return max_natoms, At_Symb, MXYZ