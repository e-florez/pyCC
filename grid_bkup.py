#!/usr/bin/env python3.8

#---------------------------------------------------------#
# Generating a Grid for a Frecuency Histogram             #
# for a Radial, planar angle and Dihedral  Distributions  #
#---------------------------------------------------------#

def grid_rda2():
    print("Enter parameters ro, rf, dr for the RDA grid: ")
    ro = float(input(f'ro = '))
    rf = float(input(f'rf ='))
    dr = float(input(f'dr ='))
    nbins = int((rf - ro) / dr)
   #R_occurrences = np.zeros(nbins, dtype=int)
    grid_rda = (ro, rf, dr)
    return grid_rda 
    #atoms_pairs = 
    # a np just with nbins




def Grids():    
#   import pandas as pd
    import numpy as np 
    """ [summary]
            # - This function is about to define a proper grid for constructing histograms 
            #  for interatomic distantes, planar angles and dihedral angle distributions.
    Args: 
        atoms_pairs (list): It's the full list of pairs of atoms in the system
        to perform the analysis of Radial Distribution
    """

    # --- BODY of the PROGRAM --- 

    print("")
    analysis = (input(f'What kind of distribution analysis do you want to Carry out? \n 0.All kind of Analysis \n 1.RDA \
    \n 2.Plana Angle  \n 3.Dihedral Angle \n ----------------\n '))
    print("*************")

    analysis = analysis.split(' ')

    results = []

    for element in analysis: 
        element = int(element)    
        if element == 0: 
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

        elif element == 1:
            

            print("Enter parameters for Radial Distribution Analysis: ")
            ro = float(input(f'ro = '))
            rf = float(input(f'rf ='))
            dr = float(input(f'dr ='))
            nbins = int((rf - ro) / dr)
            R_occurrences = np.zeros(nbins, dtype=int)
            grid_rda = (ro, rf, dr)
            #return grid_rda 
            results.append(grid_rda)
            #return grid_rda2()
            #atoms_pairs = 
            # a np just with nbins

        elif element == 2:
            print("Enter parameters for Planar Angle Analysis")
            min_Pangle = float(input(f'Min Pangle = '))
            max_Pangle = float(input(f'Max Pangle = '))
            delta_Pangle = float(input(f'Delta Pangle = '))
            nbins_Pangle = int((max_Pangle - min_Pangle) / delta_Pangle)
            Pangle_occurrences = np.zeros(nbins_Pangle, dtype=int)
            grid_Pa = (min_Pangle, max_Pangle, delta_Pangle)
            results.append(grid_Pa)
          
            #return grid_Pa


        elif element == 3:
            print("")
            print("Enter parameters for Dihedral Analysis")
            min_Dangle = float(input(f'Min Dangle = '))
            max_Dangle = float(input(f'Max Dangle = '))
            delta_Dangle = float(input(f'Delta Dangle = '))
            nbins_Dangle = int((max_Dangle - min_Dangle) / delta_Dangle)
            Dangle_occurrences = np.zeros(nbins_Dangle, dtype=int) 
            grid_Da = (min_Dangle, max_Dangle, delta_Dangle)
            results.append(grid_Da)

    return results

     #   grid_rda = (ro, rf, dr)
     #   grid_Pa = (min_Pangle, max_Pangle, delta_Pangle)
     #   grid_Da = (min_Dangle, max_Dangle, delta_Dangle)

     # return grid_rda, grid_Pa, grid_Da
#print(ro, rf, dr)
new_grid = Grids()
print(new_grid)
