#!/usr/bin/env python3.8

#--------------------------------------------------------------#
# Generating a Grid for a Frecuencies Histogram                #
# for a Radial, planar angle and Dihedral angle Distributions  #
#--------------------------------------------------------------#


def grids():    
#   import pandas as pd
    import numpy as np 
    """ [summary]
            # - This function is about to define a proper grid for constructing histograms 
            #  for interatomic distantes, planar angles and dihedral angles distribution.
    Args: 
        atoms_pairs (list): It's the full list of pairs of atoms in the system
        to perform the analysis of Radial Distribution. 
    """

    # --- BODY of the PROGRAM --- 

    print("")
    analysis = (input(f'What kind of distribution analysis do you want to Carry out? \n 0.All kinds of Analysis \n 1.RDA \
    \n 2.Plana Angle  \n 3.Dihedral Angle \n ----------------\n '))
    print("*************")

    analysis = analysis.split(' ')

    grid_parameters = []
    atoms_pairs_rda = []
    grid_atoms_trio = []
    grid_atoms_tetrad = []

    for type_analysis in analysis: 
        type_analysis = int(type_analysis)    
        if type_analysis == 0: 
            print("Radial, Angular and Dihedral distribution analysis will be performed with the default parameters ")
            print("-------------------")
            print("RDA Parameters: ro = 0.5 A, rf = 3.0 A, dr = 0.05 A ")
            print("PADA Parameters: Min Pangle = 0, Max Pangle = 180 deg, Delta_Pangle = 2 deg")
            print("DADA Parameters: Min Dangle = 0, Max Dangle = 180 deg, Delta_Dangle = 2 deg")
            print("-------------------")
            
            ro = 0.5 # As the smallest interactomic distance to be considered (in Angstrom)
            rf = 3.0 # As the largest interactomic distance to be considered
            dr = 0.05 # As  grid points for histograms
            nbins = int((rf - ro) / dr)  # number of bins for the accurences

            # Planar Angle Analysis
            min_Pangle = 0 # smallest angle between the three atoms 
            max_Pangle = 180 # Largest angle between the three atoms 
            delta_Pangle = 2.0 # grid points 
            nbins_Pangle = int((max_Pangle - min_Pangle) / delta_Pangle)

            # Dihedral Angle Analysis
            min_Dangle = 0 #  smallest angle between the three atoms 
            max_Dangle = 180 # Largest angle between the three atoms 
            delta_Dangle = 2.0 # grid points for histograms
            nbins_Dangle = int ( (max_Dangle - min_Dangle) / delta_Dangle)

            grid_rda = (ro, rf, dr)
            grid_Pa = (min_Pangle, max_Pangle, delta_Pangle)
            grid_Da = (min_Dangle, max_Dangle, delta_Dangle)
            grid_parameters.append(grid_rda)
            grid_parameters.append(grid_Pa)
            grid_parameters.append(grid_Da)

        #Paramenter to define the radial distribution analysis 
        elif type_analysis == 1:
            print("")
            print("Enter parameters for Radial Distribution Analysis: ")
            ro = float(input(f'ro = '))
            rf = float(input(f'rf = '))
            dr = float(input(f'dr = '))
            nbins = int((rf - ro) / dr)
            grid_rda = (ro, rf, dr)
            grid_parameters.append(grid_rda)


            atoms_pairs = input(f'On which pair or pairs of atoms do you want to do the analysis:  ')
            atoms_pairs = atoms_pairs.split('-')
           #R_occurrences = np.zeros(nbins, dtype=int)
            grid_pairs = (atoms_pairs)
            #atoms_parameters.append(atoms_pairs_rda)
            atoms_pairs_rda.append(grid_pairs)
            #return grid_rda 
            #print(atoms_pairs)
            #grid_pairs.append(atoms_pairs_rda)
            #atoms_pairs = 

        #Paramenter to define the angular distribution analysis
        elif type_analysis == 2:
            print("")
            print("Enter parameters for Planar Angle Analysis")
            min_Pangle = float(input(f'Min Pangle = '))
            max_Pangle = float(input(f'Max Pangle = '))
            delta_Pangle = float(input(f'Delta Pangle = '))
            nbins_Pangle = int((max_Pangle - min_Pangle) / delta_Pangle)
            #Pangle_occurrences = np.zeros(nbins_Pangle, dtype=int)
            grid_Pa = (min_Pangle, max_Pangle, delta_Pangle)
            grid_parameters.append(grid_Pa)
            atoms_trio = input(f'On which three atoms do you want to do the analysis:  ')
            atoms_trio = atoms_trio.split(',')
            grid_atoms_trio.append(atoms_trio)
            print(atoms_trio)

         #Paramenter to define the dihedral angle distribution analysis
        elif type_analysis == 3:
            print("")
            print("Enter parameters for Dihedral Analysis")
            min_Dangle = float(input(f'Min Dangle = '))
            max_Dangle = float(input(f'Max Dangle = '))
            delta_Dangle = float(input(f'Delta Dangle = '))
            nbins_Dangle = int((max_Dangle - min_Dangle) / delta_Dangle)
            Dangle_occurrences = np.zeros(nbins_Dangle, dtype=int) 
            grid_Da = (min_Dangle, max_Dangle, delta_Dangle)
            grid_parameters.append(grid_Da)
            atoms_tetrad = input(f'On which 4 atoms do you want to calculate a dihedral angle:  ')
            atoms_tetrad = atoms_tetrad.split(':')
            grid_atoms_tetrad.append(atoms_tetrad)
            print(atoms_tetrad)

    return grid_parameters, atoms_pairs_rda, grid_atoms_trio, grid_atoms_tetrad
 

new_grid = grids()
print(new_grid)

