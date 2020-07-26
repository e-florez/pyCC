#!/usr/bin/python3.6

# ------------------------------------------
# July 2020
#               edisonffh@gmail.com
#
# python3.6 script to compute bond length
# frecuency in Hg(H_2O)_n clusters
#
# ------------------------------------------

# -----------------------------------
# ------ moules
# -----------------------------------
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
# --- enable TeX mode for matplotlib
rc('text', usetex=True)

# -----------------------------------
# ------ body
# -----------------------------------

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

# list_xyz = ["w6s1.xyz"]

# - to plot
fig = plt.figure()  # inches WxH, figsize=(7, 8)
fig.suptitle('Histogram Analisys', fontsize=20, fontweight='bold')
ax1 = plt.subplot()
ax1.grid()

# - legends for the main plot
plt.ylabel('Ocurrence', fontsize=12, fontweight='bold')
plt.xlabel('Bond Distance [Angstrom]',
           fontsize=12, fontweight='bold')

# - defining grid for the Histogram Analysis (number of occurences)
ro = 0.0    # smallest interactomic distance
rf = 15.0   # largest interactomic distance
dr = 0.1   # grid points
nbins = int((rf - ro) / dr)  # number of bins for the accurences
# - array to storage occurences
occurences = np.zeros(nbins, dtype=int)

# - reading coordinates fro XYZ file (importing data with pandas)
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

    data_xyz = pd.read_csv(file_xyz, delim_whitespace=True,
                           skiprows=2, header=None,

                           names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])

    # # - list of elements  ### mercury = data_xyz[data_xyz['element'] == 'Hg']
    # elements = data_xyz['element'].tolist()
    # elements_list = []
    # for atom in elements:
    #     if atom not in elements_list:
    #         elements_list.append(atom)

    # - Distance between two atoms
    coordinates_a = np.zeros(3, dtype=float)
    coordinates_b = np.zeros(3, dtype=float)

    atom_a = 0
    while atom_a < num_atoms:
        # for atom_a
        coordinates_a[0] = float(data_xyz.iloc[atom_a, 1])
        coordinates_a[1] = float(data_xyz.iloc[atom_a, 2])
        coordinates_a[2] = float(data_xyz.iloc[atom_a, 3])

        atom_b = atom_a + 1
        while atom_b < num_atoms:
            # for atom_b
            coordinates_b[0] = float(data_xyz.iloc[atom_b, 1])
            coordinates_b[1] = float(data_xyz.iloc[atom_b, 2])
            coordinates_b[2] = float(data_xyz.iloc[atom_b, 3])

            # computing euclidean distance
            distance = np.linalg.norm(coordinates_a - coordinates_b)

            # atoms_pair = str(data_xyz.iloc[atom_a, 0]) + '-' + \
            #     str(data_xyz.iloc[atom_b, 0])

            # Histogram analysis
            distance_hit = int(round((distance - ro) / dr))
            if distance_hit > 0 and distance_hit < nbins:
                occurences[distance_hit] += 1

            atom_b += 1
        atom_a += 1

# - plotting
bond_distance = np.linspace(ro, rf, nbins)
ax1.plot(bond_distance, occurences)

# - ENDING the plot
plt.show()

# ---------------------------- END
exit()
