#!/usr/bin/env python3
# ------------------------------------------------------------------------------------
# July 2020
#
# python3.x script by:
#
#   name: Edison Florez (github.com/e-florez/)
#   email: edisonffh@gmail.com

# ------------------------------------------------------------------------------------
# Main body
# ------------------------------------------------------------------------------------

def neighbors_atoms_pair(distance_matrix, input_pair, rmin, rmax):
    import pandas as pd

    """
    Finding pair of atoms, neighborhood definded by rmin and rmax 

    Args:
        distance (dict): dict with a matrix distance for each XYZ file
        input_pair (list [str]): pair of atoms to get the bond distance analysis
        grid (3D tuple [float]): min and max distance and bind width to do the histogram

    Return:
        atoms_pair (list of 2D tuples [int]): list of atoms pair with a distance between rmin and rmax
    """

    # - distances matrix (no atoms or labels)
    df_dist = distance_matrix.loc[:, distance_matrix.columns != 'atoms']

    # - filtering atoms labels (one column)
    df_label = distance_matrix.loc[:, distance_matrix.columns == 'atoms']

    # - filtering for the each atom from the input pair
    df_first_atom = df_label[df_label['atoms'] == input_pair[0]]
    df_second_atom = df_label[df_label['atoms'] == input_pair[1]]

    # - getting the index (in tuples)
    first_atom = tuple(df_first_atom.index)
    second_atom = tuple(df_second_atom.index)

    # - checking what pairs are into rmin, rmax
    atoms_pair = []
    for atom_a in first_atom:
        for atom_b in second_atom:
            distance = df_dist.iloc[atom_a, atom_b]

            if (rmin <= distance) and (distance <= rmax):
                atoms_pair.append((atom_a, atom_b))

    return atoms_pair
# ---------------------------------------------------------------------------------------


def atoms_index_list(distances, input_list, grid):
    """
    For a list of max 4 elements: bond distance [A, B]; bond angle [A, B, C]; and 
    dihedral angle [A, B, C, D], we split every list in pairs and compute which of them
    are into rmin, rmax. 

    WARNING: input_list order MATTER! [A, B, C] != [A, C, B]

    For instance,
        input: [A, B, C] splits into [A, B] and [B, C] to find neighbors and returns
        atoms index for those between rmin, rmax

    Args:
        distance (dataframe): distances matrix for each XYZ file
        input_list (list [str]): list of atoms to define neighbors
        grid (3D tuple [float]): min and max distance and bind width to do the histogram


    Return:

    """
    rmin, rmax, dr = grid
    
    # - max number of elements is four; two for bond, three for angle an d three for dihedral
    input_list = input_list[:4]

    # - list of indexes 
    list_atoms_index = []
    
    # - splitting list into pair; i.e., for 
    #   bond: [A, B] we get one pair [A, B]
    #   angle: [A, B, C] we get two pairs [A, B] and [B, C] (B as a pivot)
    #   dihedral: [A, B, C, D] we get three pairs [A, B], [B, C] and [B, D] (B as a pivot)
    
    # - max number of pair 
    max_pair = range(len(input_list) - 1)
    
    n = 0
    for n in max_pair:
        if n < 2:
            pair = [input_list[n], input_list[n+1]]
        else:
            # - only for dihedral [A, B, C, D] 
            #   to get [A, B]; [B, C]; [B, D] (instead of [C, D])
            pair = [input_list[n-1], input_list[n+1]]

        # - computing list of pair into a region
        atoms_pair = neighbors_atoms_pair(distances, pair, rmin, rmax)

        # - list of lists (max 3 lists), for each pair we have a list of index
        list_atoms_index.append(atoms_pair)

    #--------------------------------
    # - groupping these indexes 
    
    # - list of tuples to compute distances, angle or dihedrals
    index_to_return = []

    # - avoiding equivalent trends; i.e.,
    #   [A, B] is equivalent to [B, A]
    #   [A, B, C] is equivalent to [C, B, A]
    #   [A, B, C, D] is equivalent to [A, B, D, C]
    duplicates_list = []

    # - bond distance: only ONE list of pair is given
    #   e.g. [A, B] gives [(1, 2), (2, 3), (5,6), ...] (only one list of several tuples)
    if len(list_atoms_index) == 1:

        # - avoiding duplicates
        for pair in list_atoms_index[0]:
            atoms_index = [pair[0], pair[1]]
            atoms_index_rev = [pair[1], pair[0]]

            if atoms_index not in duplicates_list:
                duplicates_list.append(atoms_index)
                duplicates_list.append(atoms_index_rev)
                index_to_return.append(tuple(atoms_index))

        return index_to_return

    # - Angle: [A, B, C] we'd have TWO list of several tuple, one for [A, B] and another for [B, C]
    #   first list has a key atom (pivot); 'B' is pivot atom (which defines the angle)
    for first_pair in list_atoms_index[0]:
        #   for [A, B] (first_pair), left_atom: 'A', pivot_atom: 'B'
        left_atom = first_pair[0]
        pivot_atom = first_pair[1]

        # - looking for connection through pivot atom.
        for pair1 in list_atoms_index[1]:

            # - for pair [B, C], then pivot must be iqual to 'B'
            #   and left_atom must not be iqual to C
            if (pivot_atom == pair1[0] and left_atom != pair1[1]):
                atoms_index = [left_atom, pivot_atom, pair1[1]]
                atoms_index_rev = [pair1[1], pivot_atom, left_atom]
                                
                # - avoiding duplicates
                if atoms_index not in duplicates_list:
                    duplicates_list.append(atoms_index)
                    duplicates_list.append(atoms_index_rev)
                    index_to_return.append(tuple(atoms_index))

    # - at this point we have triplets for angles
    if len(list_atoms_index) > 2:
        # - if we ask for dihedrals
        # - clearing variables for dihedrals
        duplicates_list = []
        triplet_index = list(index_to_return)
        index_to_return = []
    else:
        # - no dihedrals, then returns triplet to get only bond angle
        return index_to_return
   
    # - Dihedral: [A, B, C, D] we'd have THREE list of several tuple, 
    #   one for [A, B], one for [B, C] and another one for [B, D]
    #   'B' is pivot atom (which defines the angle)
    for triplet in triplet_index:
        # - triplets: [A, B, C]
        left = triplet[0]
        pivot = triplet[1]
        right = triplet[2]
        
        for pair in list_atoms_index[2]:
            if (pivot == pair[0] and left != pair[1] and right != pair[1]):
                atoms_index = [left, pivot, right, pair[1]]
                atoms_index_rev = [left, pivot, pair[1], right]           

                # - avoiding duplicates
                if atoms_index not in duplicates_list:
                    duplicates_list.append(atoms_index)
                    duplicates_list.append(atoms_index_rev)
                    index_to_return.append(tuple(atoms_index))

    return index_to_return
# ---------------------------------------------------------------------------------------


def atoms_index_dict(distances_dict, input_list, grid):
    """

    Args:

    Return:

    """
    # - loop over each XYZ file to get atoms index
    index_dict = {}
    for xyz in distances_dict:
        distances = distances_dict[xyz]

        # - getting atoms list to compute distance, angle or dihedral
        atoms_index = atoms_index_list(distances, input_list, grid)

        # - dictionary with atoms index according to input list
        index_dict[xyz] = atoms_index

    return index_dict
# ---------------------------------------------------------------------------------------
