#!/usr/bin/python3.8
# ------------------------------------------------------------------------------------
# July 2020
#   edisonffh@gmail.com
#
# python3.8 script to compute bond length frecuency; a Radial Distribution Analisys (RDA)
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# ------ moules
# ------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------
# ------ body
# ------------------------------------------------------------------------------------
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

# - savig list as a pandas df
df = pd.DataFrame(list_xyz, columns=['files'])

# - sorting df and re indexing
df = df.sort_values(by='files', ascending=True).reset_index(drop=True)

# - trasposing data to print out
list_xyz_to_print = df.T.to_string(index=False, header=False).split('.xyz')

print(f'A total of {len(list_xyz)} XYZ files analized')
print(f'\nFiles (xyz): \n')

# - printing files for the RDA (five columns)
num_files = 0
while num_files < len(list_xyz_to_print):
    print(f'\t\t'.join(list_xyz_to_print[num_files:num_files + 5]).strip())

    num_files += 6
print()

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

elements_list = [atom.capitalize() for atom in elements_list]

if len(elements_list) < 1:
    exit(f'\n *** ERROR ***\nAny atom was asked to make the RDA\n')
else:
    # - list of atom pair from elements list
    pairs_list = []
    atom_a = 0
    while atom_a < len(elements_list):
        atom_b = atom_a + 1
        pair = str(elements_list[atom_a]) + '-' + str(elements_list[atom_a])
        pairs_list.append(pair)
        while atom_b < len(elements_list):
            pair = str(elements_list[atom_a]) + '-' + str(elements_list[atom_b])
            pairs_list.append(pair)

            atom_b += 1
        atom_a += 1

    print(f'\nList of atomic pairs to make the RDA: {pairs_list}')
    # - number of atoms pair, (n+1)!/2*(n-1)!
    atom_pairs = len(pairs_list)

# -------------------------------------------------------------------------------
# - defining grid for the Radial Distribution Analysis (number of occurrences)
ro = 0.6    # smallest interactomic distance
rf = 3.5   # largest interactomic distance
dr = 0.05   # grid points
nbins = int((rf - ro) / dr)  # number of bins for the accurences

# - points to use BSpline
bs_points = 100

# - array to storage occurrences
#    ???????????????
#
occurrences = np.zeros((atom_pairs, nbins), dtype=int)

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
    # 'data_xyz.iloc[i,j]', where i=0,1,...,(num_atoms-1) and x=0,1,2,3
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
        print(f'\n*** WARNING *** \n any coordinates were found in {file_xyz}')
        continue

    # - filtering to do the RDA for the atoms in the list (case insensitive)
    data_xyz = data_xyz_all[data_xyz_all.element.str.capitalize().isin(
        elements_list)]

    # - checking if asking elements are in XYZ file
    if data_xyz.shape[0] < 1:
        print(f'\n*** Warning ***')
        print(f'elements from {elements_list} were not found in file {file_xyz}')
        continue
        # - Warning: some elements are not in the input list
        # no_elements = data_xyz_all[~data_xyz_all.element.str.capitalize().isin(elements_list)]

    # - to show only asked atoms
    if num_atoms != data_xyz.shape[0]:
        num_atoms = data_xyz.shape[0]

    # - Distance between two atoms
    coordinates_a = np.zeros(3, dtype=float)
    coordinates_b = np.zeros(3, dtype=float)

    atom_a = 0
    while atom_a < num_atoms:
        coordinates_a[0] = float(data_xyz.iloc[atom_a, 1])
        coordinates_a[1] = float(data_xyz.iloc[atom_a, 2])
        coordinates_a[2] = float(data_xyz.iloc[atom_a, 3])

        atom_b = atom_a + 1
        while atom_b < num_atoms:
            coordinates_b[0] = float(data_xyz.iloc[atom_b, 1])
            coordinates_b[1] = float(data_xyz.iloc[atom_b, 2])
            coordinates_b[2] = float(data_xyz.iloc[atom_b, 3])

            # computing euclidean distance
            distance = np.linalg.norm(coordinates_a - coordinates_b)

            if distance <= rf:
                # - finding atomic pair for previous distance
                pair = str(data_xyz.iloc[atom_a, 0]) + '-' + str(data_xyz.iloc[atom_b, 0])
                # - pair AB == BA
                pair_rev = str(data_xyz.iloc[atom_b, 0]) + '-' + str(data_xyz.iloc[atom_a, 0])
                
                # - index for pair list
                if pair in pairs_list:
                    pair_idx = pairs_list.index(pair)
                elif pair_rev in pairs_list:
                    pair_idx = pairs_list.index(pair_rev)

                # Radial distribution analysis
                distance_hit = int(round((distance - ro) / dr))
                if distance_hit > 0 and distance_hit < nbins:
                    occurrences[pair_idx, distance_hit] += 1

            atom_b += 1
        atom_a += 1

# ----------------------------------------------
# - bond distance based on  the previous grid for the RDA
bond_distance = np.linspace(ro, rf, nbins)
# - to smooth the curve (BSpline)
smooth_bond_distance = np.linspace(ro, rf, nbins * bs_points)

# ----------------------------------------------
# - plotting & saving
atom_pair = 0
while atom_pair < len(pairs_list):
    # - atom pair from the list
    pair = pairs_list[atom_pair]
    total_bond = sum(occurrences[atom_pair, :])

    # - plotting only if any distance is found
    if total_bond > 0:
        # - saving RDA
        np.savetxt(pair + '_rda' + '.dat', np.transpose([bond_distance, occurrences[atom_pair, :]]),
                    delimiter=' ', header='distance [Angstrom]   occurrence (total=%i)' % total_bond,
                    fmt='%.6f %28i')

        # - to plot
        fig = plt.figure()  # inches WxH, figsize=(7, 8)
        fig.suptitle('Radial Distribution Analisys \n' + r'\small{Total distances= %i}' % total_bond,
                        fontsize=20, fontweight='bold')
        ax1 = plt.subplot()
        ax1.grid()

        # - legends for the main plot
        plt.ylabel('Relative Number of Ocurrences', fontsize=12, fontweight='bold')
        plt.xlabel('Bond Length [Angstrom]', fontsize=12, fontweight='bold')

        # - smooth curve BSpline, degree k=3, cubic
        smooth = make_interp_spline(bond_distance, occurrences[atom_pair, :], k=3)
        smooth_occurrences = smooth(smooth_bond_distance)
        ax1.plot(smooth_bond_distance, smooth_occurrences / total_bond, label='%s' % (pair))

        # - raw data, not Bspline fitting
        # ax1.plot(bond_distance, occurrences[pair_idx, :], label=r'%s' % (pair))
        # - y axis scale
        # ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

        # - Put a legend below current axis
        plt.legend(loc=0)
        # - x ticks
        ax1.xaxis.set_ticks(np.arange(ro, rf, 0.2))

    # - no distance found
    else:
        print(f'\n*** Warning ***')
        print(f' no distance was found for pair {pair} in files {file_xyz}')

    atom_pair += 1

# ------------------------------------------------------------------------------------
# - ENDING the plots
plt.show()

print(f'\n *** DONE ***\n')
# ---------------------------- END
exit()
