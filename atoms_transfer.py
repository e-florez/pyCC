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


def stern_limbach(index_dict, input_list, distances_dict):
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

    coordinates_q1 = []
    coordinates_q2 = []

    for xyz in index_dict:
        indexes = index_dict[xyz]
        distances_df = distances_dict[xyz]

        # - distances matrix (no atoms or labels)
        distances_df = distances_df.loc[:, distances_df.columns != "atoms"]

        for pair in indexes:
            r1 = distances_df.iloc[pair[0], pair[1]]
            r2 = distances_df.iloc[pair[1], pair[2]]

            # - atoms transfer analysis compute q1 = 0.5 * (r1 - r2) and q2 = r1 + r2
            # q1 = np.abs(0.5 * (r2 - r1))
            # q1 = 0.5 * (r1 - r2)
            # q2 = r1 + r2

            # coordinates_q1.append(-np.abs(0.5 * (r1 - r2)))
            coordinates_q1.append(0.5 * (r1 - r2))
            coordinates_q2.append(r1 + r2)

    return {"q1": coordinates_q1, "q2": coordinates_q2}


def atom_transfer(index_dict, input_list, distances_dict):
    import numpy as np

    """[summary]
    """

    input_list = list(input_list)

    natural_bond_coordinates = stern_limbach(index_dict, input_list, distances_dict)

    triplets = "-".join(input_list)
    transfer_name = "transfer_" + "-".join(input_list) + ".dat"

    print(f"")
    print(
        f"Atoms transfer analysis ({triplets}) according to Stern-Limbach model (q1, q2):"
    )
    print(
        f"Transfer of atoms {input_list[1]} "
        + f"between {input_list[0]} and {input_list[2]}, "
        + f"where q1=0.5*(r1-r2) and q2=r1+r2, "
        + f"r1: distance[{input_list[0]}{input_list[1]}] and r2: distance[{input_list[1]}{input_list[2]}]"
    )
    print(f"")

    np.savetxt(
        transfer_name,
        natural_bond_coordinates,
        delimiter=" ",
        header="q1 [Angstrom]    q2 [Angstrom]",
        fmt="%15.10f %15.10f",
    )
