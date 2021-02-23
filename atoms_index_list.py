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

    # - checking inputs
    # if len(input_pair) != 2:
    # return atoms_pair

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
                # atoms_pair.append((atom_a+1, atom_b+1))

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

    list_atoms_index = []
    n = 0
    while n < (len(input_list) - 1):

        pair = []
        if n == 2:
            # - only for dihedral [A, B, C, D] to get [A, B]; [B, C]; [B, D] (instead of [C, D])
            pair.append(input_list[n-1])
            pair.append(input_list[n+1])
        else:
            pair.append(input_list[n])
            pair.append(input_list[n+1])

        n += 1

        # - computing list of pair into a region
        atoms_pair = neighbors_atoms_pair(distances, pair, rmin, rmax)

        list_atoms_index.append(atoms_pair)

    # list of tuples to compute distances, angle or dihedrals
    index_to_return = []

    # - avoiding equivalent trends; i.e.,
    #   [A, B] is equivalent to [B, A]
    #   [A, B, C] is equivalent to [C, B, A]
    #   [A, B, C, D] is equivalent to [A, B, D, C]
    duplicates_list = []

    # - list of lists (max 3 lists), for each pair we have a list of index
    if len(list_atoms_index) == 1:
        # - bond distance

        # - avoiding duplicates
        for pair0 in list_atoms_index[0]:

            atoms_index = [pair0[0], pair0[1]]
            atoms_index_rev = [pair0[1], pair0[0]]

            # - avoiding duplicates
            if atoms_index not in duplicates_list:
                duplicates_list.append(atoms_index)
                duplicates_list.append(atoms_index_rev)
                index_to_return.append(tuple(atoms_index))

        return index_to_return

    # - the first list has a key atom (pivot). For [A, B, C] or [A, B, C, D],
    #   'B' is pivot atom (which defines the angle)
    firts_list = list_atoms_index[0]

    #   for [A, B] (first_pair) we use 'B' (pivot)
    for first_pair in firts_list:

        #   for [A, B] (first_pair), left_atom: 'A', pivot_atom: 'B'
        pivot_atom = first_pair[1]
        left_atom = first_pair[0]

        # - looking for connection through pivot atom.
        for pair1 in list_atoms_index[1]:

            # - for pair [B, C], then pivot must be iqual to 'B'
            #   and left_atom must not be iqual to C
            if (pivot_atom == pair1[0] and left_atom != pair1[1]):

                # - only for dihedral
                if len(list_atoms_index) > 2:
                    for pair2 in list_atoms_index[2]:

                        if (pivot_atom == pair2[0]
                            and left_atom != pair2[1]
                                and pair1[1] != pair2[1]):

                            atoms_index = [left_atom, pivot_atom,
                                           pair1[1], pair2[1]]
                            atoms_index_rev = [left_atom, pivot_atom,
                                               pair2[1], pair1[1]]
                else:
                    atoms_index = [left_atom, pivot_atom, pair1[1]]
                    atoms_index_rev = [pair1[1], pivot_atom, left_atom]

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

        # # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # # - index starts at zero.
        # tmp = []
        # for t in atoms_index:
        #     tmp2 = []
        #     for s in t:
        #         tmp2.append(s+1)
        #     tmp.append(tuple(tmp2))

        # print(f'file: {xyz}')
        # print(f'requiring: {input_list}\n')
        # # print(atoms_index)
        # print(tmp)
        # print('\n\n')
        # # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    return index_dict
# ---------------------------------------------------------------------------------------
