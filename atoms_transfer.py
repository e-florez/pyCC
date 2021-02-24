#!/usr/bin/env python3

# ------------------------------------------------------------------------------------
#   python3.x function to analyse atom transfer according to Stern-Limbach
#
#   A - X - B
#   r1 = r[AX] and r2 = r[XB]
#
#   this function compute q1 = 0.5 * (r1 - r2) and q2 = r1 + r2
#
#   see DOI: 10.1560/IJC.49.2.199 or DOI: 10.1098/rsif.2013.0518
#
#   *** February 2021 by particula94h@gmail.com ***
# ------------------------------------------------------------------------------------


def atom_transfer(index_dict, input_list, distances_dict):
    import pandas as pd
    import numpy as np

    """
    *** September 2020 by particula94h@gmail.com ***

    python3.x function to analyse atom transfer according to Stern-Limbach
        see DOI: 10.1560/IJC.49.2.199 or DOI: 10.1098/rsif.2013.0518

    for a list of three atoms A - X - B
    r1 = r[AX] and r2 = r[XB]

    this function compute q1 = 0.5 * (r1 - r2) and q2 = r1 + r2

    Args:
        transfer_list ([list, str]): List of three atoms A-X-B (order matters!) to make the analysis
        header_distance_matrix (list, str): List of atoms for the distance matrix
        data_xyz (Pandas data frame): data frame with the symbols and XYZ coordinates for each XYZ file
        distance_matrix (numpy matrix, float): distance matrix

    Returns:
        natural_bond_coordinates [(q1, q2) type: floats]:  list of tuples q1, q2 (floats)
    """
    q1_q2_coordinates = []

    for xyz in index_dict:
        indexes = index_dict[xyz]
        distances_df = distances_dict[xyz]

        # - distances matrix (no atoms or labels)
        distances_df = distances_df.loc[:, distances_df.columns != 'atoms']

        for pair in indexes:
            r1 = distances_df.iloc[pair[0], pair[1]]
            r2 = distances_df.iloc[pair[1], pair[2]]

            # - atoms transfer analysis compute q1 = 0.5 * (r1 - r2) and q2 = r1 + r2
            # q1 = np.abs(0.5 * (r2 - r1))
            q1 = (0.5 * (r1 - r2))
            q2 = r1 + r2

            q1_q2_coordinates.append((q1, q2))

    return q1_q2_coordinates
