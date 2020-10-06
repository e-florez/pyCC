#!/usr/bin/env python3
# --------------------------------------------------------#
#   danianescobarv@gmail.com                              #
#   edisonffh@gmail.com                                   #
#   cesarfernando.ibarguen@gmail.com                      #
# --------------------------------------------------------#
import pandas as pd
import numpy  as np
#---------------------------------------------------------#
# -Start: Elements list to do radial distribution analisys#
#---------------------------------------------------------#
def all_elements(file_xyz):
    """[summary]
    Function to get atomic pairs from a XYZ file,
    when it is selected all the elements and verification.
    Args:
        file_xyz (list)    : Name of the .xyz
    Return:
        element_list (list): Pairs of elements unique
    """

    #bug: Cuando en el xyz se pone en minúscula el símbolo del
    #del elemento hay diferencias, aprece que no encuentra distancias
    #o ángulos que si encuentra cuando el símbolo tiene la mayúscula

    elements = pd.read_csv(file_xyz, delim_whitespace=True,
                    skiprows=2, header=None,
                    names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])

    # - if XYZ file has no coordinates (by mistake)
    if elements.shape[0] <= 1:
        elements = []
        print(f'\n*** WARNING *** \nNo coordinates found in {file_xyz}')
        return elements
        # return '*** WARNING *** No coordinates found in ', file_xyz

    elements = elements['element'].tolist()

    # - list of elements (uniques)
    elements_uniq = []
    for atom in elements:
        if atom not in elements_uniq:
            elements_uniq.append(atom)

    elements = []
    elements = [atoms.capitalize() for atoms in elements_uniq]

    element_list = []
    atom_a = 0
    while atom_a < len(elements):
        atom_b = atom_a
        while atom_b < len(elements):
            element_list.append(elements[atom_a] + '-' + elements[atom_b])
            atom_b += 1
        atom_a += 1

    return element_list

def sort_input_pairs(elements):
    """[summary]
    Sorting uniques atomic pair A-B from an input list
    Args:
        elements (list)    : Pairs of elements from input
    Return:
        element_lsit (list): Pairs of elements unique
    """

    # - Deleting comma used to split atomic pairs (if any)
    elements = [pair.replace(',','') for pair in elements]

    cont = 0
    elements_list = []
    #When there is alone a term in elements
    if len(elements) == 1:
        elements_list = elements
    #When there are several terms in elements
    else:
        while cont < len(elements):
            pair1 = elements[cont]
            #Comparing pair1 with the other terms in elements
            if cont != len(elements)-1:
                cont1 = cont + 1
            else:
                cont1 = cont - 1
            #Comparing with pairs already accepted like different
            while cont1 < len(elements):
                if pair1 != elements[cont1] :
                    i = 0
                    cont2 = 0
                    #Comparing with A-B and B-A
                    for i in range(len(elements_list)):
                        a1p1   = pair1.split('-')[0]
                        a2p1   = pair1.split('-')[1]
                        pair1r = a2p1 + '-' + a1p1
                        if pair1 == elements_list[i] or pair1r == elements_list[i]:
                            cont2 = 1
                    if len(elements_list) == 0 or cont2 == 0 :
                        #Save unique pairs
                        elements_list.append(pair1)
                        cont1 = len(elements)
                    else:
                        cont1 += 1
                else:
                    cont1 += 1
            cont += 1

    return elements_list
#---------------------------------------------------------#
# -End: Elements list to do radial distribution analisys  #
#---------------------------------------------------------#

#---------------------------------------------------------#
# -Start: Input to Radial Distribution                    #
#---------------------------------------------------------#
def input_distribution():
    """[summary]
    Define parameter to radial distribution and plot
    Returns:
        ro    [float]         : Smallest interactomic distance
        rf    [float]         : Largest interactomic distance
        dr    [float]         : Grid points
        nbins [float]         : Number of bins for the accurences
        bond_distance [float] : Bond distance based on the previous grid for the RDA
    """
    ro = 0.6   # smallest interactomic distance
    rf = 3.5   # largest interactomic distance
    dr = 0.05  # grid points
    nbins = int((rf - ro) / dr)  # number of bins for the accurences

    # - points to use BSpline
    #bs_points = 100

    #******************************************************#
    # numpy.linspace(start, stop, num=50, endpoint=True,   #
    # retstep=False, dtype=None, axis=0)[source]           #
    # Return evenly spaced numbers over a specified        #
    # interval.                                            #
    #******************************************************#
    # - bond distance based on the previous grid for the RDA
    bond_distance = np.linspace(ro, rf, nbins)

    print(f"\n#        Parameter of Distribution                         #")

    print(f'\nRDA with {nbins} bins, grid {dr} between {ro}-{rf} Angstroms')
    #print(f'BSpline used for the RDA with {bs_points} points')

    return bond_distance, ro, rf, dr, nbins
#---------------------------------------------------------#
# -End: Input to Radial Distribution                      #
#---------------------------------------------------------#

#---------------------------------------------------------#
#-Start: Search pairs with distance larger or equal to rf #
# into distance matrix                                    #
#---------------------------------------------------------#
def search_pairs_RM (pairs_list,max_natoms,At_Symb,N_Atoms,Mat_R,rf):
    """[summary]
    Search of atom pairs in list_pairs into distance matrix with distance
    higher than 0.0E+0 and lower or equal to rf
    Args:
        pairs_list (list): Atoms pairs list selected
        max_natoms (int) : Number maximum of atoms among .xyz
        At_Symb (array)  : Number of atoms and Atomic symbol
                            in each .xyz
        Mat_R (array)    : Upper triangular distances matriz associated with each .xyz
        N_Atoms (array)  : Number of atoms in each .xyz
        rf (float)       : Largest interatomic distance
    Returns:
        dist_pairs_l (array): Distance between atoms to each pair in list_pairs
    """

    num_xyz = int(len(Mat_R))
    dim3 = max_natoms*max_natoms - int((max_natoms*max_natoms)/2) #rest the half of distances matrix
    dist_pairs_l = np.zeros((num_xyz,len(pairs_list),dim3))

    for i in range(num_xyz):
        for l in range(len(pairs_list)):
            il = 0
            n_atoms = int(N_Atoms[i])
            for j in range(n_atoms):
                k = j + 1
                while k < n_atoms:
                    pair_ab = str(At_Symb[i][j]) + '-' + \
                        str(At_Symb[i][k])
                    pair_ba = str(At_Symb[i][k]) + '-' + \
                        str(At_Symb[i][j])
                    #Compare with each pair of list_pairs: A-B, B-A
                    if pair_ab in pairs_list[l] or pair_ba in pairs_list[l]:
                        distance_ab = Mat_R[i,j,k]
                        #Save pairs with distance > 0 and <= rf
                        if distance_ab <= rf and distance_ab != 0.0E+0 :
                            dist_pairs_l[i,l,il] = distance_ab
                            il += 1
                    k += 1

    return dist_pairs_l
#---------------------------------------------------------#
#-End: Search pairs with rf into distance matrix          #
#---------------------------------------------------------#

#---------------------------------------------------------#
#-Start: Statistical to Radial Distribution and save      #
#---------------------------------------------------------#
def statistical_radial (list_xyz,pairs_list,dist_pairs_l,max_natoms,ro,dr,nbins):
    """[summary]
    Calculate of ocurrences of distance of the different pairs atoms in pairs_list
    into of the grid for RDA
    Args:
        list_xyz (list)      : Name of the files .xyz
        pairs_list (list)    : Atoms pairs list selected unique
        dist_pairs_l (array) : Distance of atoms pairs in pairs_list
        max_natoms (int)     : Maximum number of atoms among the .xyz
        ro    [float]        : Smallest interactomic distance
        dr    [float]        : Grid of points
        nbins [float]        : Number of bins for the accurences

    Returns:
        ocurrences [array]      : Total occurrences by distance of each of the atom pairs
        occurr_each_xyz [array] : Total occurrences by distance of each of the atom pairs into each xyz
    """
    # - array to storage occurrences for bond distances
    #    ???????????????
    #
    occurr_each_xyz = np.zeros((len(list_xyz), len(pairs_list), nbins), dtype=int)
    occurrences = np.zeros((len(pairs_list), nbins), dtype=int)

    #Calculate of ocurrences
    for i in range(len(list_xyz)):
        for j in range(len(pairs_list)):
            for k in range(max_natoms):
                if dist_pairs_l[i,j,k] > 0.0E+0 :
                    distance_hit = int(round((dist_pairs_l[i,j,k] - ro) / dr))
                    if distance_hit > 0 and distance_hit < nbins:
                        #Bond_distance doesn't start since 0.0 then
                        #it is neccesary rest 1 to distance_hit
                        occurrences[j, distance_hit-1] += 1
                        occurr_each_xyz[i, j, distance_hit-1] += 1

    return occurrences, occurr_each_xyz
#----------------------------------------------------------#
#-End: Statistical to Radial Distribution                  #
#----------------------------------------------------------#

#----------------------------------------------------------#
#-Start: Save Information from Radial Distribution Analysis#
#----------------------------------------------------------#
def save_rda(list_xyz,pairs_list,bond_distance,occurrences,occurr_each_xyz) :
    """[summary]
    Save information of ocurrences of radial distribution analysis into
    .txt by each interaction
    Args:
        list_xyz [list]         : Name of the files .xyz
        pairs_list [list]       : Atoms pairs list selected unique
        bond_distance [float]   : Bond distance based on the previous grid for the RDA
        ocurrences [array]      : Total occurrences by distance of each of the atom pairs
        occurr_each_xyz [array] : Total occurrences by distance of each of the atom pairs into each xyz
    """

    # - saving
    atom_pair = 0

    while atom_pair < len(pairs_list):
        # - atom pair from the list
        pair = pairs_list[atom_pair]
        total_bond = sum(occurrences[atom_pair, :])

        # - plotting only if any distance is found
        if total_bond > 0:
            # - saving RDA

            rda_name = 'rda_' + pair + '.dat'
            np.savetxt(rda_name, np.transpose([bond_distance, occurrences[atom_pair, :]]),
                    delimiter=' ',
                    header='distance [Angstrom]   occurrence (total=%i)' % total_bond,
                    fmt='%.6f %28i')
        else:
            print(f'\n*** Warning ***')
            print(f'No distance {pair} found in XYZ files\n')

        df = pd.DataFrame(np.round(bond_distance, decimals=3), columns = ['#R[A]'])
        df['Tot occ'] = occurrences[atom_pair, :]
        for i in range(len(list_xyz)):
            df[list_xyz[i].replace('.xyz','')] = np.transpose(occurr_each_xyz[i,atom_pair,:])

        rda_split_name = 'rda_split_' + pair + '.dat'
        df.to_csv(rda_split_name, sep="\t", index=False)

        atom_pair += 1
#----------------------------------------------------------#
#-Start: Save Information from Radial Distribution Analysis#
#----------------------------------------------------------#