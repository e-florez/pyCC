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

# list_xyz = ["w6s41.xyz"]

# - checking if files exist

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
        atom = atom.upper()
        elements_list.append(atom)

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
# - array to storage occurrences
occurrences = np.zeros([unique_atoms, unique_atoms, nbins], dtype=int)

print(f'BSpline used for the RDA with a grid between {ro}-{rf} Angstroms\n')

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
        print(f'\n *** WARNING *** \
            \n Any data was found in {file_xyz}, please, check this files: \n')

    # - filtering to do the RDA for the atoms in the list
    data_xyz = data_xyz_all[data_xyz_all.element.isin(elements_list)]

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

            atom_b += 1
        atom_a += 1

# - Continue ONLY if any distance was found
# if sum(occurrences[0, 0, :]) < 1:
#     exit(f'\n *** ERROR *** \
#         \n No distance was found between those atoms {elements_list} \
#         \n Please, check files: {list_xyz}\n')

# ----------------------------------------------
# - to plot
fig = plt.figure()  # inches WxH, figsize=(7, 8)
fig.suptitle('Radial Distribution Analisys', fontsize=20, fontweight='bold')
ax1 = plt.subplot()
ax1.grid()

# - legends for the main plot
plt.ylabel('Number of Ocurrences', fontsize=12, fontweight='bold')
plt.xlabel('Bond Length [Angstrom]',
           fontsize=12, fontweight='bold')

# - bond distance based on  the previous grid for the RDA
bond_distance = np.linspace(ro, rf, nbins)

# - to smooth the curve (BSpline)
smooth_bond_distance = np.linspace(ro, rf, nbins * 1000)

# - plotting
atom_a = 0
while atom_a < len(elements_list):
    # - for the same type of atoms (if any)
    atoms_pair = elements_list[atom_a] + '-' + \
        elements_list[atom_a]

    # - avoiding to plot empty results
    if all_elements or len(elements_list) == 1:
        if sum(occurrences[atom_a, atom_a, :]) > 1:
            # ax1.plot(bond_distance, occurrences[atom_a,
            #                                     atom_a, :], label=r'%s' % (atoms_pair))

            # smooth curve BSpline, degree k=3, cubic
            smooth = make_interp_spline(bond_distance, occurrences[atom_a, atom_a, :], k=3)
            smooth_occurrences = smooth(smooth_bond_distance)
            ax1.plot(smooth_bond_distance,
                        smooth_occurrences, label=r'%s' % (atoms_pair))

    # - for different pair of atoms
    atom_b = atom_a + 1
    while atom_b < len(elements_list):
        atoms_pair = elements_list[atom_a] + '-' + \
            elements_list[atom_b]

        # ax1.plot(bond_distance,
        #          occurrences[atom_a, atom_b, :], label=r'%s' % (atoms_pair))
        
        # smooth curve BSpline, degree k=3, cubic
        smooth = make_interp_spline(bond_distance, occurrences[atom_a, atom_b, :], k=3)
        smooth_occurrences = smooth(smooth_bond_distance)        
        ax1.plot(smooth_bond_distance,
                 smooth_occurrences, label=r'%s' % (atoms_pair))

        atom_b += 1
    atom_a += 1

# - Put a legend below current axis
plt.legend(loc=0)

# - y axis scale
ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

# - x ticks
ax1.xaxis.set_ticks(np.arange(ro, rf, 0.2))

# - ENDING the plot
plt.show()

print(f'\n *** DONE ***\n')
# ---------------------------- END
exit()
