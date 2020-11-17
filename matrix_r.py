#!/usr/bin/env python3

#---------------------------------------------------------#
# -Start: Build Distance Matrix to each .xyz              #
#---------------------------------------------------------#
def Distance_Matrix(files_xyz,coordinates_XYZ):
    import pandas as pd
    import numpy as np
    """[summary]
    Computing distance matrix for each XYZ and create a dictionary whit
    a panda data frame with all distances between all possible atomic pair
    Args:
        files_xyz (list)             : It is a list with those XYZ file's names to analyse
        coordinates_XYZ (dictionary) :  KEY: file.xyz (str),
                                        VALUES: pandas dataframe (element, x, y, z)
                                        coordinates_xyz = {file.xyz: (element, x, y, z)}
    Return:
        R_Matrix (dictonary)   : KEY: file.xyz (str),
                                VALUES: pandas dataframe (Distance between atoms)
                                R_Matrix = {file.xyz: (distance_iatom_jatom)}
    """
    nfiles_xyz = len(files_xyz) #Number of files .xyz
    R_Matrix = {}
    for ifile in range(nfiles_xyz):
        XYZ = pd.DataFrame(coordinates_XYZ[files_xyz[ifile]],\
            columns=['x-coordinate','y-coordinate','z-coordinate'])
        natoms=len(XYZ['x-coordinate'])   #Number of atoms
        temporal_R_Matrix = np.zeros((natoms,natoms),dtype=float)
        #Computing distance matrix
        for iatom in range(natoms):
            for jatom in range(natoms):
                distance_ab_x = XYZ['x-coordinate'][jatom] - XYZ['x-coordinate'][iatom]
                distance_ab_x *= distance_ab_x
                distance_ab_y = XYZ['y-coordinate'][jatom] - XYZ['y-coordinate'][iatom]
                distance_ab_y *= distance_ab_y
                distance_ab_z = XYZ['z-coordinate'][jatom] - XYZ['z-coordinate'][iatom]
                distance_ab_z *= distance_ab_z
                temporal_R_Matrix[jatom,iatom] =\
                    np.sqrt(distance_ab_x+distance_ab_y+distance_ab_z)
        df = pd.DataFrame(temporal_R_Matrix)
        #Save distance matrix in dictonary
        R_Matrix[files_xyz[ifile]] = df
    return R_Matrix
#---------------------------------------------------------#
# -End: Build Distance Matrix to each .xyz                #
#---------------------------------------------------------#
