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
                                R_Matrix = {file.xyz: (              iatom
                                                        jatom   distance_jatom_iatom)}
    """
    nfiles_xyz = len(files_xyz) #Number of files .xyz
    R_Matrix = {} #Dictonary with distances matrix
    for ifile in range(nfiles_xyz):
        natoms=len(coordinates_XYZ[files_xyz[ifile]]['x-coordinate']) #Number of atoms
        temporal_R_Matrix = np.zeros((natoms,natoms),dtype=float)
        label=[]
        #Computing distance matrix
        for iatom in range(natoms): #Colums
            #Labels of columns and rows : str(element) + str(iatom)
            label.append(coordinates_XYZ[files_xyz[ifile]]['element'][iatom] + str(iatom))
            jatom = iatom
            while jatom < natoms: #Rows
                distance_ab_x  = coordinates_XYZ[files_xyz[ifile]]['x-coordinate'][jatom]\
                                - coordinates_XYZ[files_xyz[ifile]]['x-coordinate'][iatom]
                distance_ab_x *= distance_ab_x
                distance_ab_y  = coordinates_XYZ[files_xyz[ifile]]['y-coordinate'][jatom]\
                                - coordinates_XYZ[files_xyz[ifile]]['y-coordinate'][iatom]
                distance_ab_y *= distance_ab_y
                distance_ab_z  = coordinates_XYZ[files_xyz[ifile]]['z-coordinate'][jatom]\
                                - coordinates_XYZ[files_xyz[ifile]]['z-coordinate'][iatom]
                distance_ab_z *= distance_ab_z
                #Distance between atoms
                temporal_R_Matrix[jatom][iatom] =\
                    np.sqrt(distance_ab_x+distance_ab_y+distance_ab_z)
                #Symmetric term
                temporal_R_Matrix[iatom][jatom] = temporal_R_Matrix[jatom][iatom]
                jatom += 1
        #Dateframe with distances
        df=pd.DataFrame(temporal_R_Matrix,columns=[label])
        #First column of df
        df.insert(loc=0, column='atom', value=np.transpose(label))
        #Save df in dictonary
        R_Matrix[files_xyz[ifile]] = df
        print(R_Matrix[files_xyz[ifile]])
    return R_Matrix
#---------------------------------------------------------#
# -End: Build Distance Matrix to each .xyz                #
#---------------------------------------------------------#
