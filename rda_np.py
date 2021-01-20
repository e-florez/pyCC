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

def rda(distances, atom_pair, grid):
    import pandas as pd
    import numpy as np

    """
    Asking or taking path of working directory from argument of prompt and
    verification of working directory

    Args:
        distance (dict): dict with a matrix distance for each XYZ file
        atom_pair (list [str]): pair of atoms to get the bond distance analysis
        grid (3D tuple [float]): min and max distance and bind width to do the histogram

    Return:

    """

    rmin, rmax, dr = grid

    print('\n\n --------------STARTING HERE---------------------- \n\n')

    for xyz in distances:
        df = distances[xyz]
        print(df)

        df2 = df.loc[:, df.columns == 'atoms']

        # - from pandas DF to numpy array
        df = df.loc[:, df.columns != 'atoms']

        df = df.to_numpy()

        print(f'\n *********** \n')
        print(df2)

        print(' \n\n *** XXXXXXXXXX ***\n\n')
        # break
