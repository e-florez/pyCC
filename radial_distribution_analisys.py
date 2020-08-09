#!/usr/bin/python3

# ------------------------------------------
# July 2020
#               edisonffh@gmail.com
#
# python3 script to compute bond length
# frecuency in Hg(H_2O)_n clusters
#
# ------------------------------------------

# -----------------------------------
# ------ moules
# -----------------------------------

import os.path  # - to check id a file or dir exits -> os.path.exists()
# -  to smooth out your data
from scipy.interpolate import make_interp_spline, BSpline
# - Unix style pathname pattern expansion
import glob
# - complete data analysis tool (it can replace matplotlib or numpy, as it is built on top of both)
import pandas as pd
# - arrays and matrix manipulation
import numpy as np
# - plotting
import matplotlib.pyplot as plt
# - runtime configuration (rc) containing the default styles for every plot element you create
from matplotlib import rc
rc('text', usetex=True)   # --- enable TeX mode for matplotlib

# -----------------------------------
# ------ body
# -----------------------------------
print(f'\nRadial Distribution Analisys (RDA) for XYZ files\n')

# - list for xyz files
repited_list_xyz = []  # repited files (if any)
list_xyz = []  # unique files

# - reading files
for input_xyz in glob.glob('*.xyz'):
    name_xyz = input_xyz[:-4]  # deleting file extention
    repited_list_xyz.append(input_xyz)  # creating an array for all xyz files

    # keeping unique xyz files
    for unique_input_xyz in repited_list_xyz:
        if unique_input_xyz not in list_xyz:
            list_xyz.append(unique_input_xyz)

# list_xyz = ["w1s1.xyz"]

# - checking if files exist
if len(list_xyz) > 0:
    for input_xyz in list_xyz:
        if not os.path.exists(input_xyz):
            exit(f' *** ERROR ***\n file {input_xyz} does not exits \n')
else:
    exit(f' *** ERROR ***\n any file was found in {list_xyz} \n')

# - Elements list to do radial distribution analisys
input_elements = input(
    f'List of atoms, **separated by space** [Default: all]: ')

# - by default reading elements for the first XYZ file
all_elements = False
if len(input_elements.split()) < 1 or input_elements == 'all':
    all_elements = True
    elements = pd.read_csv(list_xyz[0], delim_whitespace=True,
                           skiprows=2, header=None,
                           names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])
    elements = elements['element'].tolist()
else:
    elements = input_elements.split()

elements_list = []
# - list of elements (uniques)
for atom in elements:
    if atom not in elements_list:
        elements_list.append(atom)


elements_list = [ atom.capitalize() for atom in elements_list ]

if len(elements_list) > 0:
    print(f'\nList of atoms to make the RDA: {elements_list}')
else:
    exit(f'\n *** ERROR ***\n No atoms found \n')

# - number of atoms pair
unique_atoms = len(elements_list)

# - defining grid for the Radial Distribution Analysis (number of occurrences)
#
#    ???????????????
#
#

ro = 0.6    # smallest interactomic distance
rf = 3.5   # largest interactomic distance
dr = 0.05   # grid points
nbins = int((rf - ro) / dr)  # number of bins for the accurences

# - points to use BSpline
bs_points = 100

# - array to storage occurrences
occurrences = np.zeros((unique_atoms, unique_atoms, nbins), dtype=int)

print()
print(f'RDA with {nbins} bins, grid {dr} between {ro}-{rf} Angstroms')
print(f'BSpline used for the RDA with {bs_points} points')
print()

# - reading coordinates for XYZ file (importing data with pandas)
for file_xyz in list_xyz:
    # ------------------------------------------------------------------
    # in a nutshell:
    # with Pandas we have 'num_atoms' lines, each of them has four columns
    # 'data_xyz.iloc[i,j]', where i=0,1,...,(num_atoms-1) and x=0,1,2,3
    # As a result, we have:
    #       data_xyz.iloc[i, 0] is the element (string type)
    #       data_xyz.iloc[i, 1] is a coordinate on the x-axis (float type)
    #       data_xyz.iloc[i, 2] is a coordinate on the y-axis (float type)
    #       data_xyz.iloc[i, 3] is a coordinate on the z-axis (float type)
    # ------------------------------------------------------------------
    num_atoms = pd.read_csv(file_xyz, nrows=1, header=None)
    num_atoms = int(num_atoms.iloc[0])

    data_xyz_all = pd.read_csv(file_xyz, delim_whitespace=True,
                               skiprows=2, header=None,
                               names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])

    # - checking coordinates within file
    if data_xyz_all.shape[0] <= 1:
        print(f'\n *** WARNING *** \n data was found in {file_xyz}, please, check this files: \n')

    # - filtering to do the RDA for the atoms in the list (case insensitive)
    data_xyz = data_xyz_all[data_xyz_all.element.str.capitalize().isin(elements_list)]

    # - Warning elements not in the input list
    no_elements = data_xyz_all[~data_xyz_all.element.str.capitalize().isin(elements_list)]
    print(f'*** Warning ***')
    print(f'element {elements_list} not found {file_xyz} \n')
    print(no_elements.to_string(index=False, float_format='%.10f'))

    # - to show only asked atoms
    if num_atoms != data_xyz.shape[0]:
        num_atoms = data_xyz.shape[0]

    # - Distance between two atoms
    coordinates_a = np.zeros(3, dtype=float)
    coordinates_b = np.zeros(3, dtype=float)

    atom_a = 0
    while atom_a < num_atoms:
        # for atom_a
        element_a = elements_list.index(str(data_xyz.iloc[atom_a, 0]))

        coordinates_a[0] = float(data_xyz.iloc[atom_a, 1])
        coordinates_a[1] = float(data_xyz.iloc[atom_a, 2])
        coordinates_a[2] = float(data_xyz.iloc[atom_a, 3])

        atom_b = atom_a + 1
        while atom_b < num_atoms:
            # for atom_b
            element_b = elements_list.index(str(data_xyz.iloc[atom_b, 0]))

            coordinates_b[0] = float(data_xyz.iloc[atom_b, 1])
            coordinates_b[1] = float(data_xyz.iloc[atom_b, 2])
            coordinates_b[2] = float(data_xyz.iloc[atom_b, 3])

            # computing euclidean distance
            distance = np.linalg.norm(coordinates_a - coordinates_b)

            if distance <= rf:
                # Radial distribution analysis
                distance_hit = int(round((distance - ro) / dr))
                if distance_hit > 0 and distance_hit < nbins:
                    occurrences[element_a, element_b, distance_hit] += 1

                    # print(
                    #     f'atom pair: {elements_list[element_a]} - {elements_list[element_b]}')
                    # print(occurrences)
                    # print()

            atom_b += 1
        atom_a += 1

# print('shape', occurrences[:, :, :])

# exit()

# atom_a = 0
# while atom_a < len(elements_list):
#     element_a = elements_list[atom_a]
#     atom_b = atom_a + 1
#     while atom_b < len(elements_list):
#         element_b = elements_list[atom_b]
#         print(
#             f'atom pair: {elements_list[atom_a]} - {elements_list[atom_b]}')
#         print(occurrences[atom_a, atom_b, :])
#         print()
#         print('sum atoms', atom_a, atom_b, sum(occurrences[atom_a, atom_b, :]))
#         print()
#         # print('shape', occurrences[:, :, :])

#         atom_b += 1
#     atom_a += 1

# exit()

# ----------------------------------------------

# - bond distance based on  the previous grid for the RDA
bond_distance = np.linspace(ro, rf, nbins)
# - to smooth the curve (BSpline)
smooth_bond_distance = np.linspace(ro, rf, nbins * bs_points)

# ----------------------------------------------
# - plotting & saving
atom_a = 0
while atom_a < len(elements_list):
    # - for the same type of atoms (if any)
    atoms_pair = elements_list[atom_a] + '-' + \
        elements_list[atom_a]

    total_bond = sum(occurrences[atom_a, atom_a, :])

    # - avoiding to plot empty results
    if all_elements or len(elements_list) == 1:
        if total_bond > 0:

            # - saving RDA
            np.savetxt(atoms_pair + '_rda' + '.dat',
                       np.transpose(
                           [bond_distance, occurrences[atom_a, atom_a, :]]),
                       delimiter=' ',
                       header='distance [Angstrom]   occurrence (total=%i)' % total_bond,
                       fmt='%.6f %28i')

            # - to plot
            fig = plt.figure()  # inches WxH, figsize=(7, 8)
            fig.suptitle('Radial Distribution Analisys \n' + r'\small{Total distances= %i}' % total_bond,
                         fontsize=20, fontweight='bold')
            ax1 = plt.subplot()
            ax1.grid()

            # - legends for the main plot
            plt.ylabel('Relative Number of Ocurrences',
                       fontsize=12, fontweight='bold')
            plt.xlabel('Bond Length [Angstrom]',
                       fontsize=12, fontweight='bold')

            # ax1.plot(bond_distance, occurrences[atom_a,
            #                                     atom_a, :], label=r'%s' % (atoms_pair))

            # smooth curve BSpline, degree k=3, cubic
            smooth = make_interp_spline(
                bond_distance, occurrences[atom_a, atom_a, :], k=3)
            smooth_occurrences = smooth(smooth_bond_distance)
            ax1.plot(smooth_bond_distance,
                     smooth_occurrences / total_bond, label='%s' % (atoms_pair))

            # - Put a legend below current axis
            plt.legend(loc=0)
            # - y axis scale
            # ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            # - x ticks
            ax1.xaxis.set_ticks(np.arange(ro, rf, 0.2))

    # - for different pair of atoms
    atom_b = atom_a + 1
    while atom_b < len(elements_list):
        atoms_pair = elements_list[atom_a] + '-' + \
            elements_list[atom_b]

        total_bond = sum(occurrences[atom_a, atom_b, :])

        # - saving RDA
        np.savetxt(atoms_pair + '_rda' + '.dat',
                   np.transpose(
                       [bond_distance, occurrences[atom_a, atom_b, :]]),
                   delimiter=' ',
                   header='distance [Angstrom]   occurrence (total=%i)' % total_bond,
                   fmt='%.6f %28i')

        if total_bond > 0:

            # # - saving RDA
            # np.savetxt(atoms_pair + '_rda' + '.dat',
            #            np.transpose(
            #                [bond_distance, occurrences[atom_a, atom_b, :]]),
            #            delimiter=' ',
            #            header='distance [Angstrom]   occurrence (total=%i)' % total_bond,
            #            fmt='%.6f %28i')

            # - to plot
            fig = plt.figure()  # inches WxH, figsize=(7, 8)
            fig.suptitle('Radial Distribution Analisys \n' + r'\small{Total distances= %i}' % total_bond,
                         fontsize=20, fontweight='bold')
            ax1 = plt.subplot()
            ax1.grid()

            # - legends for the main plot
            plt.ylabel('Relative Number of Ocurrences',
                       fontsize=12, fontweight='bold')
            plt.xlabel('Bond Length [Angstrom]',
                       fontsize=12, fontweight='bold')

            # ax1.plot(bond_distance,
            #          occurrences[atom_a, atom_b, :], label=r'%s' % (atoms_pair))

            # smooth curve BSpline, degree k=3, cubic
            smooth = make_interp_spline(
                bond_distance, occurrences[atom_a, atom_b, :], k=3)
            smooth_occurrences = smooth(smooth_bond_distance)
            ax1.plot(smooth_bond_distance,
                     smooth_occurrences / total_bond, label='%s' % (atoms_pair))

            # - Put a legend below current axis
            plt.legend(loc=0)
            # - y axis scale
            # ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            # - x ticks
            ax1.xaxis.set_ticks(np.arange(ro, rf, 0.2))

        atom_b += 1
    atom_a += 1

# - ENDING the plots
plt.show()

print(f'\n *** DONE ***\n')
# ---------------------------- END
exit()
