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

def distance_matrix(distances, grid):
    import numpy as np
    import pandas as pd
    """

    Args:

    Return:

    """

    ro, rf, dr = grid

    matrix_d = {}

    for xyz in distances:
        data_xyz = distances[xyz]

        num_atoms = data_xyz.shape[0]

        # - distance matrix
        #  upper triangular matrix. It means that the diagonal and the lower triangular portion are zeros
        #  The upper triangular part has the distance between every atom for a given  XYZ file
        distance_matrix = np.zeros((num_atoms, num_atoms), dtype=float)

        # - the header for the distnces matrix
        header_distance_matrix = []

        # --------------------------------------------------------------------
        # - Computing the Radial Distribution Function
        coordinates_a = np.zeros(3, dtype=float)
        coordinates_b = np.zeros(3, dtype=float)

        for atom_a in range(0, num_atoms):
            coordinates_a[0] = float(data_xyz.iloc[atom_a, 1])
            coordinates_a[1] = float(data_xyz.iloc[atom_a, 2])
            coordinates_a[2] = float(data_xyz.iloc[atom_a, 3])

            # - the header for the distnces matrix
            header_distance_matrix.append(data_xyz.iloc[atom_a, 0])

            for atom_b in range(atom_a + 1, num_atoms):
                coordinates_b[0] = float(data_xyz.iloc[atom_b, 1])
                coordinates_b[1] = float(data_xyz.iloc[atom_b, 2])
                coordinates_b[2] = float(data_xyz.iloc[atom_b, 3])

                # - computing euclidean distance
                distance = np.linalg.norm(coordinates_a - coordinates_b)

                # ------------------------------------------------
                # - computing distance matrix
                distance_matrix[atom_a, atom_b] = distance
                distance_matrix[atom_b, atom_a] = distance

                # ------------------------------------------------

        df = pd.DataFrame(distance_matrix)

        # # - inserting columns' name
        # df.columns = header_distance_matrix

        # - inserting rows' name
        df.insert(0, 'atoms', header_distance_matrix, True)

        matrix_d[xyz] = df
        # matrix_d[xyz] = distance_matrix

    return matrix_d
