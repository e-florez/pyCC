#!/usr/bin/env python3
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
from natsort import natsorted # Simple yet flexible natural sorting in Python.
import pandas as pd # - complete data analysis tool (it can replace matplotlib or numpy, as it is built on top of both)
import numpy as np # - arrays and matrix manipulation
import matplotlib.pyplot as plt # - plotting tools
from matplotlib import rc # - runtime configuration (rc) containing the default styles for every plot element you create
rc('text', usetex=True)   # --- enable TeX mode for matplotlib

# ------------------------------------------------------------------------------------
# ------ body
# ------------------------------------------------------------------------------------
print(f'\n***********************************************************')
print(f'* comparing XYZ files through distances, angle and dihedrals*')
print(f'*************************************************************')

# - working directory

# print(f"\nCurrent working directory: {os.getcwd()}")

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

# Check if the working dir exists
if os.path.exists(working_dir) :
    # Change the current working Directory
    os.chdir(working_dir)
else:
    print(f'\n*** ERROR ***')
    exit(f"Can't change the Working Directory, {working_dir} doesn't exist")

#--------------------------------------------------------------------------
# - reading files
repited_list_xyz = []  # repited files (if any)
list_xyz = []  # unique files

if len(sys.argv) < 3:
    input_xyz =  input(f"\nlist of XYZ files to compare [Default: all .xyz]: \n")
    # - by default reading elements for the first XYZ file
    if len(input_xyz.split()) < 1 or input_xyz.lower() == 'all':
        for input_xyz in glob.glob('*.xyz'):
            repited_list_xyz.append(input_xyz)  # creating an array for all xyz files
    else:
        input_arguments = 2
        while input_arguments < len(sys.argv):
            repited_list_xyz.append(sys.argv[input_arguments])
            input_arguments += 1
else:
    if sys.argv[2] == 'all':
        for input_xyz in glob.glob('*.xyz'):
            repited_list_xyz.append(input_xyz)  # creating an array for all xyz files
    else:
        input_arguments = 2
        while input_arguments < len(sys.argv):
            repited_list_xyz.append(sys.argv[input_arguments])
            input_arguments += 1

# keeping unique xyz files
for unique_input_xyz in repited_list_xyz:
    if unique_input_xyz not in list_xyz:
        list_xyz.append(unique_input_xyz)

# list_xyz = ["w6s23.xyz"]
# list_xyz = ["w1s1.xyz", "w2s1.xyz"]
# list_xyz = ["w1s1.xyz", "w2s1.xyz", "w3s1.xyz"]
# list_xyz = ["w1s1.xyz", "w2s1.xyz", "w3s1.xyz", "w3s2.xyz"]

# - sorting the input files list
# list_xyz = natsorted(list_xyz)

# - checking if files exist
if len(list_xyz) > 0:
    for input_xyz in list_xyz:
        if not os.path.exists(input_xyz):
            print(f'\n*** Warinnig ***\n file {input_xyz} does not exits \n')
else:
    exit(f' *** ERROR ***\n No file found to make the RDA \n ')

print(f'\nA total of {len(list_xyz)} XYZ files analized\n')

count = 0
columns = 4
while count < len(list_xyz):
    print(f'\t'.join(list_xyz[count:count + columns]))

    count += columns
print()

#------------------------------------------------------------------------------------
elements = pd.read_csv(list_xyz[0], delim_whitespace=True,
                skiprows=2, header=None,
                names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])

# - if XYZ file has no coordinates (by mistake)
if elements.shape[0] <= 1:
    print(f'\n*** ERROR *** \n No coordinates found in {list_xyz[0]}')
    exit()

elements = elements['element'].tolist()

# - list of elements (uniques)
elements_uniq = []
for atom in elements:
    if atom not in elements_uniq:
        elements_uniq.append(atom)

elements_list = [atoms.capitalize() for atoms in elements_uniq]

pairs_list = []
atom_a = 0
while atom_a < len(elements_list):
    pairs_list.append(elements_list[atom_a] + '-' + elements_list[atom_a])
    atom_b = atom_a + 1
    while atom_b < len(elements_list):
        pairs_list.append(elements_list[atom_a] + '-' + elements_list[atom_b])
        atom_b += 1
    atom_a += 1

atom_pairs = len(pairs_list)


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------
# - bond distance based on  the previous grid for the RDA

def save_distance():

    bond_distance = np.linspace(ro, rf, nbins)

    # - saving
    atom_pair = 0
    while atom_pair < len(pairs_list):
        # - atom pair from the list
        pair = pairs_list[atom_pair]
        total_bond = sum(occurrences[atom_pair, :])

        # - plotting only if any distance is found
        if total_bond > 0:
            # - saving RDA

            rda_name = 'rda_' + name_xyz + '_' + pair + '.dat'
            np.savetxt(rda_name, np.transpose([bond_distance, occurrences[atom_pair, :]]),
                        delimiter=' ', header='distance [Angstrom]   occurrence (total=%i)' % total_bond,
                        fmt='%.6f %28i')
        # - no distance found
        # else:
        #     print(f'\n*** Warning ***')
        #     print(f'NO distance {pair} found in XYZ files\n')

        atom_pair += 1

#---------------------------------------------------------------------------------------
# - bond angle based on the previous grid for the RDA

def save_angle():
    # print(f'')
    # print(f'Angular Distribution Analisys for:')
    # print(f'')
    # print(f'   {angle_list[1]}')
    # print(f'  /  \\')
    # print(f' {angle_list[0]}    {angle_list[2]}')
    # print(f'')

    bond_angle = np.linspace(min_angle, max_angle, nbins_angle)

    total_angles = sum(occurrences_angle)

    ada_name =  'ada_' + name_xyz + '_' + '-'.join(angle_list) + '.dat'

    if total_angles > 0:
        np.savetxt(ada_name, np.transpose([bond_angle, occurrences_angle]),
                    delimiter=' ', header='Angle [degrees]   occurrence (total=%i)' % total_angles,
                    fmt='%.6f %28i')
    # else:
    #     print(f'\n*** Warning ***')
    #     print(f'NO angle {ada_name} found in XYZ files\n')


#-------------------------------------------------------------------
# - dihedral angle
def save_dihedral():
    # print(f'')
    # print(f'Angular Distribution Analisys for Dihedral angle:')
    # print(f'')
    # print(f'          {dihedral_list[2]}')
    # print(f'         /')
    # print(f'  {dihedral_list[0]}----{dihedral_list[1]}')
    # print(f'         \\')
    # print(f'          {dihedral_list[3]}')
    # print(f'')

    bond_angle = np.linspace(min_dihedral_angle, max_dihedral_angle, nbins_dihedral_angle)

    total_dihedral_angles = sum(occurrences_dihedral_angle)

    dihedral_ada_name = 'dada_' + name_xyz + '_' + '-'.join(dihedral_list) + '.dat'

    if total_dihedral_angles > 0:
        np.savetxt(dihedral_ada_name, np.transpose([bond_angle, occurrences_dihedral_angle]),
                    delimiter=' ', header='Angle [degrees]   occurrence (total=%i)' \
                                                        % total_dihedral_angles,
                    fmt='%.6f %28i')
    # else:
    #     print(f'\n*** Warning ***')
    #     print(f'NO dihedral angle {ada_name} found in XYZ files\n')

# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# - defining grid for the Radial Distribution Analysis (number of occurrences)
ro = 0.6    # smallest interactomic distance
rf = 3.5   # largest interactomic distance
dr = 0.05  # grid points
nbins = int((rf - ro) / dr)  # number of bins for the accurences

# - points to use BSpline
bs_points = 100

# - array to storage occurrences for bond distances
# occurrences = np.zeros((atom_pairs, nbins), dtype=int)

print(f'\nRDA with {nbins} bins, grid {dr} between {ro}-{rf} Angstroms')
print(f'BSpline used for the RDA with {bs_points} points')

# - array to storage occurrences for angles, [0, 180] degrees
# grid = 0.1 --> 1800 = (180 - 0)/0.1
delta_angle = 5.0
min_angle = 0
max_angle = 190
nbins_angle = int ( (max_angle - min_angle) / delta_angle)

# occurrences_angle = np.zeros(nbins_angle, dtype=int)

# - array to storage occurrences for DIHEDRAL angles, [0, 360] degrees
# grid = 0.1 --> 3600 = (3600 - 0)/0.1
delta_angle = 5.0
min_dihedral_angle = 0
max_dihedral_angle = 360

nbins_dihedral_angle = int ( (max_dihedral_angle - min_dihedral_angle) / delta_angle)

# occurrences_dihedral_angle = np.zeros(nbins_dihedral_angle, dtype=int)

list_rda = []
list_ada = []
list_dada = []

# - saving ocurrences arrays for each XYZ file into a Dictionary
histogram_dictionary = {}

# -------------------------------------------------------------------------
# - reading coordinates for XYZ file (importing data with pandas)
for file_xyz in list_xyz:

    name_xyz = file_xyz[:-4]  # deleting file extention

    rda = name_xyz + "_distance"
    ada = name_xyz + "_angle"
    dada = name_xyz + "_dihedral"

    # - list of files to analise
    list_rda.append(rda)  # distances
    list_ada.append(ada)  # plane angles
    list_dada.append(dada)  # dihedral angles

    # - initializing main arrays to save distributions
    occurrences = np.zeros((atom_pairs, nbins), dtype=int)
    occurrences_angle = np.zeros(nbins_angle, dtype=int)
    occurrences_dihedral_angle = np.zeros(nbins_dihedral_angle, dtype=int)

    # - importing data from XYZ
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

    #--------------------------------------------------------------------
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

            #------------------------------------------------
            # - Radial distribution analysis
            if distance < rf:
                # - finding atomic pair for previous distance
                pair = str(data_xyz.iloc[atom_a, 0]) + '-' + str(data_xyz.iloc[atom_b, 0])
                # - pair AB == BA
                pair_rev = str(data_xyz.iloc[atom_b, 0]) + '-' + str(data_xyz.iloc[atom_a, 0])

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

            #------------------------------------------------
            # - computing distance matrix
            distance_matrix[atom_a, atom_b] = distance
            # distance_matrix[atom_b, atom_a] = distance

            #------------------------------------------------
            atom_b += 1
        atom_a += 1

    histogram_dictionary[rda] = occurrences

    #--------------------------------------------------------------------------------
    # - computing angle 1-C-2
    #       C
    #      / \
    #     1   2
    # - order matters!

    max_distance = 2.5
    min_distance = 0.1
    coordinates_central = np.zeros(3, dtype=float)
    coordinates_first = np.zeros(3, dtype=float)
    coordinates_second = np.zeros(3, dtype=float)

    angle_list = ["H", "O", "H"]
    # angle_list = ["H", "O", "Hg"]
    # angle_list = ["O", "Hg", "O"]

    # print(f'')
    # print(f'Angular Distribution Analisys for:')
    # print(f'')
    # print(f'   {angle_list[1]}')
    # print(f'  /  \\')
    # print(f' {angle_list[0]}    {angle_list[2]}')
    # print(f'')

    first_atom = angle_list[0]
    central_atom = angle_list[1]
    second_atom = angle_list[2]

    # - atom index from XYZ file
    list_idx_central_atom = [i for i, x in enumerate(header_distance_matrix) \
                                    if x == central_atom]
    list_idx_first_atom = [i for i, x in enumerate(header_distance_matrix) \
                                if x == first_atom]
    list_idx_second_atom = [i for i, x in enumerate(header_distance_matrix) \
                                if x == second_atom]

    for central in list_idx_central_atom:
        coordinates_central[0] = float(data_xyz.iloc[central, 1])
        coordinates_central[1] = float(data_xyz.iloc[central, 2])
        coordinates_central[2] = float(data_xyz.iloc[central, 3])

        # - avoiding to count the same pair in reverse orden
        # - i.e. angle A-X-B = B-X-A, so for angle AB = BA
        list_pair_angle = []

        for first in list_idx_first_atom:

            if central == first:
                continue

            if distance_matrix[central, first] > min_distance \
                and distance_matrix[central, first] < max_distance:
                pass
            elif distance_matrix[first, central] > min_distance \
                and distance_matrix[first, central] < max_distance:
                pass
            else:
                continue

            coordinates_first[0] = float(data_xyz.iloc[first, 1])
            coordinates_first[1] = float(data_xyz.iloc[first, 2])
            coordinates_first[2] = float(data_xyz.iloc[first, 3])

            # - vectorial distance between the central and first atom
            central_first = np.subtract(coordinates_central, coordinates_first)

            for second in list_idx_second_atom:

                if first == second:
                    continue

                pair_angle = str(first) + str(second)
                pair_angle_rev = str(second) + str(first)

                if pair_angle in list_pair_angle \
                    or pair_angle_rev in list_pair_angle:
                    continue
                else:
                    list_pair_angle.append(pair_angle)
                    list_pair_angle.append(pair_angle_rev)

                if distance_matrix[central, second] > min_distance \
                    and distance_matrix[central, second] < max_distance:
                    pass
                elif distance_matrix[second, central] > min_distance \
                    and distance_matrix[second, central] < max_distance:
                    pass
                else:
                    continue

                coordinates_second[0] = float(data_xyz.iloc[second, 1])
                coordinates_second[1] = float(data_xyz.iloc[second, 2])
                coordinates_second[2] = float(data_xyz.iloc[second, 3])

                # - vectorial distance between the central and second atom
                central_second = np.subtract(coordinates_central, coordinates_second)

                #-----------------------------------------------------------------------
                # - computing angle first-central-second (using dot product)
                norm_second = np.linalg.norm(central_second)
                norm_first = np.linalg.norm(central_first)
                Cos = np.dot(central_first, central_second) / norm_first / norm_second

                angle = np.arccos(Cos)
                angle_deg = np.degrees(angle)

                angle_hit = int(round( (angle_deg) / delta_angle) )
                if angle_hit > 0 and angle_hit < nbins_angle:
                    occurrences_angle[angle_hit] += 1

                # print(angle_deg)

    histogram_dictionary[ada] = occurrences_angle

    #--------------------------------------------------------------------
    # - computing DIHEDRAL angle X-YAB
    #          2
    #         /
    #   1----C
    #         \
    #          3
    # - order matters!

    max_distance = 2.5
    min_distance = 0.1

    coordinates_first = np.zeros(3, dtype=float)
    coordinates_central = np.zeros(3, dtype=float)
    coordinates_second = np.zeros(3, dtype=float)
    coordinates_third = np.zeros(3, dtype=float)

    dihedral_list = ["Hg", "O", "H", "H"]

    # print(f'')
    # print(f'Angular Distribution Analisys for Dihedral angle:')
    # print(f'')
    # print(f'          {dihedral_list[2]}')
    # print(f'         /')
    # print(f'  {dihedral_list[0]}----{dihedral_list[1]}')
    # print(f'         \\')
    # print(f'          {dihedral_list[3]}')
    # print(f'')

    first_atom = dihedral_list[0]
    central_atom = dihedral_list[1]
    second_atom = dihedral_list[2]
    third_atom = dihedral_list[3]

    # - atom index from XYZ file
    list_idx_central_atom = [i for i, x in enumerate(header_distance_matrix) \
                                    if x == central_atom]
    list_idx_first_atom = [i for i, x in enumerate(header_distance_matrix) \
                                if x == first_atom]
    list_idx_second_atom = [i for i, x in enumerate(header_distance_matrix) \
                                if x == second_atom]
    list_idx_third_atom = [i for i, x in enumerate(header_distance_matrix) \
                                if x == third_atom]

    for first in list_idx_first_atom:
        coordinates_first[0] = float(data_xyz.iloc[first, 1])
        coordinates_first[1] = float(data_xyz.iloc[first, 2])
        coordinates_first[2] = float(data_xyz.iloc[first, 3])

        for central in list_idx_central_atom:

            if central == first:
                continue

            if distance_matrix[central, first] > min_distance \
                and distance_matrix[central, first] < max_distance:
                pass
            elif distance_matrix[first, central] > min_distance \
                and distance_matrix[first, central] < max_distance:
                pass
            else:
                continue

            coordinates_central[0] = float(data_xyz.iloc[central, 1])
            coordinates_central[1] = float(data_xyz.iloc[central, 2])
            coordinates_central[2] = float(data_xyz.iloc[central, 3])

            # - vectorial distance between the central and first atom
            central_first = np.subtract(coordinates_first, coordinates_central)

            # - initial value to choose the min
            min_second = 10000

            for second in list_idx_second_atom:

                if first == second or central == second:
                    continue

                if distance_matrix[central, second] > min_distance \
                    and distance_matrix[central, second] < max_distance:
                    distance_second = distance_matrix[central, second]
                elif distance_matrix[second, central] > min_distance \
                    and distance_matrix[second, central] < max_distance:
                    distance_second = distance_matrix[second, central]
                else:
                    continue

                if min_second != min(min_second, distance_second):
                    min_second = min(min_second, distance_second)

                    choose_second = second

                    coordinates_second[0] = float(data_xyz.iloc[second, 1])
                    coordinates_second[1] = float(data_xyz.iloc[second, 2])
                    coordinates_second[2] = float(data_xyz.iloc[second, 3])

            # - vectorial distance between the central and second atom
            central_second = np.subtract(coordinates_central, coordinates_second)

            # - initial value to choose the min
            min_third = 10000

            for third in list_idx_third_atom:

                if first == third or central == third or choose_second == third:
                    continue

                if distance_matrix[central, third] > min_distance \
                    and distance_matrix[central, third] < max_distance:
                    distance_third = distance_matrix[central, third]
                elif distance_matrix[third, central] > min_distance \
                    and distance_matrix[third, central] < max_distance:
                    distance_third = distance_matrix[third, central]
                else:
                    continue

                if min_third != min(min_third, distance_third):
                    min_third = min(min_third, distance_third)

                    coordinates_third[0] = float(data_xyz.iloc[third, 1])
                    coordinates_third[1] = float(data_xyz.iloc[third, 2])
                    coordinates_third[2] = float(data_xyz.iloc[third, 3])

            # - vectorial distance between the central and third atom
            central_third = np.subtract(coordinates_central, coordinates_third)

            #--------------------------------------------------------------
            # - computing dihedral angle (using cross product)

            import dihedral as dh

            p1 = coordinates_first
            p2 = coordinates_central
            p3 = coordinates_second
            p4 = coordinates_third

            dihedral_angle_deg = dh.dihedral(p1, p2, p3, p4)

            dihedral_angle_hit = int(round( (dihedral_angle_deg) / delta_angle) )
            if dihedral_angle_hit > 0 and dihedral_angle_hit < nbins_angle:
                occurrences_dihedral_angle[dihedral_angle_hit] += 1

            # print()
            # print(f'dihedral: {dihedral_angle_deg}')
            # print()

    histogram_dictionary[dada] = occurrences_dihedral_angle

    #--------------------------------------------------------------------
    #--------------------------------------------------------------------

# exit()

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
# - plotting: defining frames and designing the area to plot
def plot_histogram(dictionary, x_axis, x_label, subtitle):
    """

    """

    x = x_axis
    x_label = x_label
    subtitle = subtitle

    # - plotting: defining frames and designing the area to plot
    fig = plt.figure(figsize=(10, 6))  # inches WxH
    fig.suptitle('Distribution Analisys \n' + subtitle, fontsize=20) #, fontweight='bold')

    ax1 = plt.subplot(111)
    ax1.grid()

    # - legends for the main plot
    plt.ylabel('Relative Number of Ocurrences', fontsize=12) #, fontweight='bold')
    # plt.xlabel('Bond Distance [Angstrom]', fontsize=12) #, fontweight='bold')

    files_to_plot = list(dictionary.keys())

    # - renaming for file names with PATH included
    new_names = []
    for item in files_to_plot:
        new_names.append(item.split('/')[-1])

    count = 0
    while count < len(files_to_plot):

        name_file = new_names[count]
        file_xyz = name_file.split('_')[0]

        y = list(dictionary.values())[count]
        if len(x) < 1:
            x = np.linspace(0, 100, len(y) - 1)

        # total number of distances
        total = sum(y)

        # - to smooth the curve (BSpline)
        smooth_x = np.linspace(x[0], x[-1], len(x)*100)

        # smooth curve BSpline, degree k=3, cubic
        smooth = make_interp_spline(x, y, k=3)
        smooth_y = smooth(smooth_x)

        # - Bspline fitting
        ax1.plot(smooth_x, smooth_y / total, label=' %s \n Total= %i' %(file_xyz, total))

        count += 1
    # ------------------------------------
    ax1.xaxis.set_major_locator(plt.MaxNLocator(12))

    plt.xlabel(x_label, fontsize=12) #, fontweight='bold')
    # plt.xlabel('No label', fontsize=12) #, fontweight='bold')
    # -----------------------------------------------------------
    # - Ending the plot

    # plt.legend(loc=0)
    # Put a legend below current axis
    plt.legend(loc='lower center', bbox_to_anchor=(1.32, 0.6, 0.0, 0.0),
                fancybox=True, shadow=True, ncol=1, fontsize=11)

    # - Shrink current axis's height by 10% on the bottom
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 0.7, box.height])

    # - ENDING the plots
    return plt.show()
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

# - deleting empty arrays
rda_dictionary = {}
new_pairs_list = []

atom_pair = 0
while atom_pair < len(pairs_list):
    for data_file in list_rda:
        distance_array = histogram_dictionary[data_file]

        if sum(distance_array[atom_pair, :]) > 0:
            file_name = data_file + '_' + pairs_list[atom_pair]
            new_pairs_list.append(pairs_list[atom_pair]) # del pair whit no distance
            rda_dictionary[file_name] = distance_array[atom_pair, :]

    atom_pair += 1

#-------------------------------------------
# - plotting RDA

# - deleting duplicates
pairs_list = []
for pair in new_pairs_list:
    if pair not in pairs_list:
        pairs_list.append(pair)

for pair in pairs_list:
    dict_to_plot = {}
    for data_file in list_rda:
        file_name = data_file + '_' + pair

        try:
            dict_to_plot[file_name] = rda_dictionary[file_name]
        except KeyError:
            continue

    dictionary = dict_to_plot
    x_axis = np.linspace(ro, rf, nbins)
    x_label = 'Bond Distance [Angstrom]'
    subtitle = pair

    plot_histogram(dictionary, x_axis, x_label, subtitle)

#-------------------------------------------
# - plotting ADA

ada_dictionary = {}
for data_file in list_ada:
    distance_array = histogram_dictionary[data_file]
    if sum(distance_array) > 0:
        ada_dictionary[data_file] = distance_array

dictionary = ada_dictionary
x_axis = np.linspace(min_angle, max_angle, nbins_angle)
x_label = 'Angle [Degrees]'
subtitle = '-'.join(angle_list)

plot_histogram(dictionary, x_axis, x_label, subtitle)

#-------------------------------------------
# - plotting DADA

dada_dictionary = {}
for data_file in list_dada:
    distance_array = histogram_dictionary[data_file]
    if sum(distance_array) > 0:
        dada_dictionary[data_file] = distance_array

dictionary = dada_dictionary
x_axis = np.linspace(min_dihedral_angle, max_dihedral_angle, nbins_dihedral_angle)
x_label = 'Dihedral Angle [Degrees]'
subtitle = '-'.join(dihedral_list)

plot_histogram(dictionary, x_axis, x_label, subtitle)

print(f'\n****************************************************')
print(f'*** DONE ***')
print(f'****************************************************\n')
# ---------------------------- END
exit()
