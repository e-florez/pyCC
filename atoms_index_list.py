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
    Finding pair of atoms into a regind definded by rmin and rmax 

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
    df_first_atom= df_label[df_label['atoms'] == input_pair[0]]
    df_second_atom= df_label[df_label['atoms'] == input_pair[1]]

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


def atoms_index_list(distances, input_pair, grid):
    """

    Args:

    Return:

    """
    

    rmin, rmax, dr = grid
    
    n = 0
    while n < (len(input_pair) - 1):        
        
        pair = []
        if n == 2:
            # - only for dihedral [A, B, C, D] to get [A, B]; [B, C]; [B, D] (instead of [C, D])
            pair.append(input_pair[n-1])
            pair.append(input_pair[n+1])
        else:
            pair.append(input_pair[n])
            pair.append(input_pair[n+1])        
        
        print(f'\n {pair}')
        
        atoms_pair = neighbors_atoms_pair(distances, pair, rmin, rmax)
        
    
        print(atoms_pair)
        
        n += 1