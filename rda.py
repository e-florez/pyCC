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

def rda(index_dict, distances_dict, grid):
    import pandas as pd
    """


    Args:

    Return:

    """

    rmin, rmax, dr = grid

    print('\n\n --------------STARTING HERE---------------------- \n\n')

    for xyz in index_dict:
        indexes = index_dict[xyz]
        distances_df = distances_dict[xyz]
        
        # - distances matrix (no atoms or labels)
        distances_df = distances_df.loc[:, distances_df.columns != 'atoms']

        for atom_a in first_atom:
            for atom_b in second_atom:
                distance = distances_df.iloc[atom_a, atom_b]

        print(distances)

        for pair in indexes:
            




        print(' \n\n *** XXXXXXXXXX ***\n\n')
        # break
