#!/usr/bin/env python3
# --------------------------------------------------------#
#   danianescobarv@gmail.com                              #
#   edisonffh@gmail.com                                   #
#   cesarfernando.ibarguen@gmail.com                      #
# --------------------------------------------------------#
import sys
import func_radial as fnr
import numpy as np
import pandas as pd
#---------------------------------------------------------#
# -Start: Input to Radial Distribution                    #
#---------------------------------------------------------#
def input_distribution():
    ro = 0.6    # smallest interactomic distance
    rf = 3.5   # largest interactomic distance
    dr = 0.05   # grid points
    nbins = int((rf - ro) / dr)  # number of bins for the accurences

    # - points to use BSpline
    bs_points = 100
    return ro, rf, dr, nbins, bs_points
#---------------------------------------------------------#
# -End: Input to Radial Distribution                      #
#---------------------------------------------------------#

#---------------------------------------------------------#
# -Start: Elements list to do radial distribution analisys#
#---------------------------------------------------------#
#Bug: Falta disntinguir entre xyz
def radial_distribution (list_xyz, max_natoms, At_Symb, MXYZ):
    #***********************************************#
    #Start: Pairs of atoms                          #
    #***********************************************#
    elements = []  # list of elements
    if len(sys.argv) < 3:
        input_elements = input(f"\nAtomic pairs to make the RDA [Default: all]:\n**A-B, C-D, ... SYMBOLS** ")

        # - by default reading elements for the first XYZ file
        if len(input_elements.split()) < 1 or input_elements == 'all':
            pairs_list = fnr.all_elements(list_xyz[0])
        else:
            elements = input_elements.split()
            # - sorting atomic pairs
            pairs_list = fnr.sort_input_pairs(elements)
    else:
        if sys.argv[2] == 'all':
            pairs_list = fnr.all_elements(list_xyz[0])
        else:
            #Read pairs from argument of execution
            input_arguments = 2
            while input_arguments < len(sys.argv):
                elements.append(sys.argv[input_arguments])
                input_arguments += 1

            # - sorting atomic pairs
            pairs_list = fnr.sort_input_pairs(elements)

    # - list of atom pair from elements list
    if len(pairs_list) < 1:
        exit(f'\n *** ERROR ***\nNo atoms found to make the RDA (e.g. C-C)\n')
    else:
        print(f'\nList of atomic pairs to make the RDA: {pairs_list}')
        # - number of atoms pair, (n+1)!/2*(n-1)!
        natom_pairs = len(pairs_list)
    #***********************************************#
    #End: Pairs of atoms                            #
    #***********************************************#

    # - list of individual atoms
    elements_list = []

    for pair in pairs_list:
        for atom in pair.split('-'):
            if atom not in elements_list:
                elements_list.append(atom)

    #Defining grid to distribution  (ocurrences number, ...)
    ro, rf, dr, nbins, bs_points = input_distribution()

    #***********************************************#
    #Start: Statistical to Radial Distribution      #
    #***********************************************#
    # - array to storage occurrences for bond distances
    #    ???????????????
    #
    occurrences = np.zeros((natom_pairs, nbins), dtype=int)

    print(f'\nRDA with {nbins} bins, grid {dr} between {ro}-{rf} Angstroms')
    print(f'BSpline used for the RDA with {bs_points} points')

    # -------------------------------------------------------------------------
    # - reading coordinates for XYZ file (importing data with pandas)
    for file_xyz in list_xyz:
        num_atoms = pd.read_csv(file_xyz, nrows=1, header=None)
        num_atoms = int(num_atoms.iloc[0])

        # ------------------------------------------------------------------
        # in a nutshell:
        # with Pandas we have 'num_atoms' lines, each of them has four columns
        # 'data_xyz.iloc[i, j]', where i=0,1,...,(num_atoms-1) and j=0,1,2,3
        # As a result, we have:
        #       data_xyz.iloc[i, 0] is the element (string type)
        #       data_xyz.iloc[i, 1] is a coordinate on the x-axis (float type)
        #       data_xyz.iloc[i, 2] is a coordinate on the y-axis (float type)
        #       data_xyz.iloc[i, 3] is a coordinate on the z-axis (float type)
        # ------------------------------------------------------------------
        data_xyz_all = pd.read_csv(file_xyz, delim_whitespace=True,
                                skiprows=2, header=None,
                                names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])

        # - checking coordinates within file
        if data_xyz_all.shape[0] <= 1:
            print(f'\n*** WARNING *** \nNo coordinates found in {file_xyz}')
            continue

        # - filtering to do the RDA for the atoms in the list (case insensitive)
        data_xyz = data_xyz_all[data_xyz_all.element.str.capitalize().isin(
            elements_list)]

        # - checking if asking elements are in XYZ file
        if data_xyz.shape[0] < 1:
            print(f'\n*** Warning ***')
            print(f'No elements, from {elements_list}, found in file {file_xyz}')
            continue
            # - Warning: some elements are not in the input list
            # no_elements = data_xyz_all[~data_xyz_all.element.str.capitalize().isin(elements_list)]

        # - to show only asked atoms
        if num_atoms != data_xyz.shape[0]:
            num_atoms = data_xyz.shape[0]

        # - distance matrix
        #  upper triangular matrix. It means that the diagonal and the lower triangular portion are zeros
        #  The upper triangular part has the distance between every atom for a given  XYZ file
        distance_matrix = np.zeros((num_atoms, num_atoms), dtype=float)

        # - the header for the distnces matrix
        header_distance_matrix = []

        # --------------------------------------------------------------------
        # - Computing the Radial Distribution Function
        coordinates_a = np.zeros(3, dtype=float)
        coordinates_b = np.zeros(3, dtype=float)

        atom_a = 0
        while atom_a < num_atoms:
            coordinates_a[0] = float(data_xyz.iloc[atom_a, 1])
            coordinates_a[1] = float(data_xyz.iloc[atom_a, 2])
            coordinates_a[2] = float(data_xyz.iloc[atom_a, 3])

            # - the header for the distnces matrix
            header_distance_matrix.append(data_xyz.iloc[atom_a, 0])

            atom_b = atom_a + 1
            while atom_b < num_atoms:
                coordinates_b[0] = float(data_xyz.iloc[atom_b, 1])
                coordinates_b[1] = float(data_xyz.iloc[atom_b, 2])
                coordinates_b[2] = float(data_xyz.iloc[atom_b, 3])

                # - computing euclidean distance
                distance = np.linalg.norm(coordinates_a - coordinates_b)

                # ------------------------------------------------
                # - Radial distribution analysis
                if distance < rf:
                    # - finding atomic pair for previous distance
                    pair = str(data_xyz.iloc[atom_a, 0]) + \
                        '-' + str(data_xyz.iloc[atom_b, 0])
                    # - pair AB == BA
                    pair_rev = str(data_xyz.iloc[atom_b, 0]) + \
                        '-' + str(data_xyz.iloc[atom_a, 0])

                    # - index for pair list
                    if pair in pairs_list:
                        pair_idx = pairs_list.index(pair)
                    elif pair_rev in pairs_list:
                        pair_idx = pairs_list.index(pair_rev)
                    else:
                        atom_b += 1
                        continue

                    distance_hit = int(round((distance - ro) / dr))
                    if distance_hit > 0 and distance_hit < nbins:
                        occurrences[pair_idx, distance_hit] += 1

                # ------------------------------------------------
                # - computing distance matrix
                distance_matrix[atom_a, atom_b] = distance
                # distance_matrix[atom_b, atom_a] = distance

                # ------------------------------------------------
                atom_b += 1
            atom_a += 1
    #***********************************************#
    #End: Statistical to Radial Distribution        #
    #***********************************************#
    return natom_pairs, pairs_list, ro, rf, dr, nbins, bs_points
#---------------------------------------------------------#
# -End: Elements list to do radial distribution analisys  #
#---------------------------------------------------------#