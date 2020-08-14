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
import sys # to get System-specific parameters
import os  # - to check id a file or dir exits -> os.path.exists()
from scipy.interpolate import make_interp_spline, BSpline # -  to smooth out your data
import glob # - Unix style pathname pattern expansion
import pandas as pd # - complete data analysis tool (it can replace matplotlib or numpy, as it is built on top of both)
import numpy as np # - arrays and matrix manipulation
import matplotlib.pyplot as plt # - plotting tools
from matplotlib import rc # - runtime configuration (rc) containing the default styles for every plot element you create
rc('text', usetex=True)   # --- enable TeX mode for matplotlib

# ------------------------------------------------------------------------------------
# ------ body
# ------------------------------------------------------------------------------------
print(f'\n****************************************************')
print(f'* Radial Distribution Analisys (RDA) for XYZ files *')
print(f'****************************************************')

# - working directory
print(f"\nCurrent working directory: {os.getcwd()}")
if len(sys.argv) <= 1:    
    tmp_dir =  input(f'\nDirectory (whit the XYZ files) to make the RDA [default: empty]: ')
    tmp_dir = tmp_dir.strip()

    if tmp_dir == '.' or len(tmp_dir) < 1:
        working_dir = os.getcwd()
    else:
        working_dir = os.getcwd() + '/' + tmp_dir
else:
    working_dir = os.getcwd() + '/' + sys.argv[1]

print(f'\nWorking directiry: {working_dir}')

# Check if New path exists
if os.path.exists(working_dir) :
    # Change the current working Directory    
    os.chdir(working_dir)
else:
    print(f'\n*** ERROR ***')
    exit(f"Can't change the Working Directory, {working_dir} doesn't exist")   

# - reading files
repited_list_xyz = []  # repited files (if any)
list_xyz = []  # unique files

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
            print(f'\n*** Warinnig ***\n file {input_xyz} does not exits \n')
else:
    exit(f' *** ERROR ***\n No file found to make the RDA \n ')

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

# -------------------------------------------------------------------------------
# - Elements list to do radial distribution analisys
elements = [] # list of elements

if len(sys.argv) < 3:
    input_elements =  input(f"List of fatoms to make the RDA, **SYMBOLS separated by space** [Default: all]: ")

    # - by default reading elements for the first XYZ file
    if len(input_elements.split()) < 1 or input_elements == 'all':
        elements = pd.read_csv(list_xyz[0], delim_whitespace=True,
                            skiprows=2, header=None,
                            names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])
        elements = elements['element'].tolist()
    else:
        elements = input_elements.split()
else:
    input_arguments = 2
    while input_arguments < len(sys.argv):
        elements.append(sys.argv[input_arguments])
        input_arguments += 1

# - list of elements (uniques)
elements_list = [] 

for atom in elements:
    if atom not in elements_list:
        elements_list.append(atom)

elements_list = [atom.capitalize() for atom in elements_list]

# - checking if there is any file to plot
if len(elements_list) < 1:
    exit(f'\n *** ERROR ***\nNo atom asked to make the RDA\n')
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
        print(f'\n*** WARNING *** \n No coordinates found in {file_xyz}')
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

        # - Put a legend below current axis
        plt.legend(loc=0)

    # - no distance found
    else:
        print(f'\n*** Warning ***')
        print(f'NO distance {pair} found in files \n\n{list_xyz}')

    atom_pair += 1

# ------------------------------------------------
# - y axis scale, for raw data
# ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0)

# - x ticks
ax1.xaxis.set_ticks(np.arange(ro, rf, 0.2))

# ------------------------------------------------------------------------------------
# - ENDING the plots
plt.show()

print(f'\n****************************************************')
print(f'*** DONE ***')
print(f'****************************************************\n')
# ---------------------------- END
exit()