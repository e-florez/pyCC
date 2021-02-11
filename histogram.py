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

import numpy


def rda(index_dict, distances_dict, grid, nbins):
    import pandas as pd
    import numpy as np
    """
    Args:
    Return:
    """

    rmin, rmax, dr = grid

    occurrences = np.zeros(nbins, dtype=int)

    for xyz in index_dict:
        indexes = index_dict[xyz]
        distances_df = distances_dict[xyz]

        # - distances matrix (no atoms or labels)
        distances_df = distances_df.loc[:, distances_df.columns != 'atoms']

        for pair in indexes:
            distance = distances_df.iloc[pair[0], pair[1]]

            distance_hit = int(round((distance - rmin) / dr))
            if distance_hit > 0 and distance_hit < nbins:
                occurrences[distance_hit] += 1

    return occurrences
# ---------------------------------------------------------------------------------------


def angle(atom_A, atom_B, atom_C):
    import numpy as np
    """
    Computing plane angle between three atoms A-B-C

    Args:

    Return:

    """
    # - Distance between each side atoms and the central one
    d_AB = np.subtract(atom_A, atom_B)
    d_BC = np.subtract(atom_C, atom_B)

    # - norm
    n_AB = np.linalg.norm(d_AB)
    n_BC = np.linalg.norm(d_BC)

    # - cosine throuth dot product
    Cos = np.dot(d_AB, d_BC) / n_AB / n_BC

    # - angle in rad
    angle = np.arccos(Cos)

    return np.degrees(angle)
# ---------------------------------------------------------------------------------------


def ada(index_dict, coordinates_XYZ, delta_angle, nbins):
    import pandas as pd
    import numpy as np
    """

    Args:

    Return:

    """

    occurrences = np.zeros(nbins, dtype=int)

    for xyz in index_dict:
        indexes = index_dict[xyz]
        df = coordinates_XYZ[xyz]

        # - distances matrix (no atoms or labels)
        coordinates = df.loc[:, df.columns != 'element']

    for pair in indexes:
        coordinates_A = coordinates.iloc[pair[0]]
        atom_A = coordinates_A.to_numpy()

        coordinates_B = coordinates.iloc[pair[1]]
        atom_B = coordinates_B.to_numpy()

        coordinates_C = coordinates.iloc[pair[2]]
        atom_C = coordinates_C.to_numpy()

        # - computing angle A-B-C (using dot product)
        angle_deg = angle(atom_A, atom_B, atom_C)

        angle_hit = int(round((angle_deg) / delta_angle))
        if angle_hit > 0 and angle_hit < nbins:
            occurrences[angle_hit] += 1

    return occurrences
# ---------------------------------------------------------------------------------------


def dada(index_dict, coordinates_XYZ, delta_angle, nbins):
    import pandas as pd
    import numpy as np
    import dihedral
    """

    Args:

    Return:

    """

    occurrences = np.zeros(nbins, dtype=int)

    for xyz in index_dict:
        indexes = index_dict[xyz]
        df = coordinates_XYZ[xyz]

        # - distances matrix (no atoms or labels)
        coordinates = df.loc[:, df.columns != 'element']

    for pair in indexes:
        coordinates_A = coordinates.iloc[pair[0]]
        atom_A = coordinates_A.to_numpy()

        coordinates_B = coordinates.iloc[pair[1]]
        atom_B = coordinates_B.to_numpy()

        coordinates_C = coordinates.iloc[pair[2]]
        atom_C = coordinates_C.to_numpy()

        coordinates_D = coordinates.iloc[pair[3]]
        atom_D = coordinates_D.to_numpy()

        # - computing dihedral angle A-B-C-D
        angle_deg = dihedral.dihedral(atom_A, atom_B, atom_C, atom_D)

        angle_hit = int(round((angle_deg) / delta_angle))
        if angle_hit > 0 and angle_hit < nbins:
            occurrences[angle_hit] += 1

    return occurrences
# ---------------------------------------------------------------------------------------
