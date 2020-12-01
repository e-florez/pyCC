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

        print('\n NEW-------- \n')

        new_df = df[df['atoms'] == atom_pair[0]]

        print(f'\n File {xyz}, pair: ' + '-'.join(atom_pair) + '\n')

        # print(new_df[atom_pair[1]])

        new_df = new_df[atom_pair[1]]

        print(new_df)

        print('\n LAST-------- \n')

        last_df = new_df[(new_df > rmin) & (new_df < rmax)]

        last_df = pd.DataFrame(last_df)

        print(last_df)

        # last_df = last_df.to_string(index=False)

        # print(last_df)

        # print('\n ------ \n')

        # for index, column in last_df.iteritems():
        #     print(f'{index}\txxxxxx\t {column}')

        # for

        print('---')
        # break
