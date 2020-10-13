#!/usr/bin/env python3
# --------------------------------------------------------#
#   danianescobarv@gmail.com                              #
#   edisonffh@gmail.com                                   #
#   cesarfernando.ibarguen@gmail.com                      #
# --------------------------------------------------------#
import sys
import func_radial as fnr #¿por qué?
#---------------------------------------------------------#
# -Start: Elements list to do radial distribution analisys#
#---------------------------------------------------------#
#Bug: Falta disntinguir entre xyz
def radial_distribution (list_xyz, max_natoms, At_Symb, N_Atoms, Mat_R):
    """[summary]
    Main function of the radial distribution
    Args:
        list_xyz (list)  : Name of the files .xyz
        max_natoms (int) : Maximun number of atoms among the .xyz
        At_Symb (list)   : Atomic symbol of atoms in each of the .xyz
        N_Atoms (array)  : Atom number in each of the .xyz
        Mat_R (array)    : Upper triangular distance Matrix of each of the .xyz
    Returns:
        [type]: [description]
    """
    print(f"\n###############################################################")
    print(f"#           Start Radial Distribution Analysis                #")
    print(f"###############################################################")
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

    #Defining grid to distribution  (ocurrences number, ...)
    bond_distance, ro, rf, dr, nbins = \
        fnr.input_distribution()

    #Search pairs with dr into distance matrix
    dist_pairs_l = \
        fnr.search_pairs_RM(pairs_list,max_natoms,At_Symb,N_Atoms,Mat_R,rf)

    #Statistical to Radial Distribution
    occurrences, occurr_each_xyz = \
        fnr.statistical_radial(list_xyz,pairs_list,dist_pairs_l,max_natoms,ro,dr,nbins)

    #Save information
    fnr.save_rda(list_xyz,pairs_list,bond_distance,occurrences,occurr_each_xyz)

    print(f"\n###############################################################")
    print(f"#           End Radial Distribution Analysis                  #")
    print(f"###############################################################")
    return pairs_list
#---------------------------------------------------------#
# -End: Elements list to do radial distribution analisys  #
#---------------------------------------------------------#
