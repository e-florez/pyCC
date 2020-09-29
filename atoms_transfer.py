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
#   *** September 2020 by particula94h@gmail.com ***
# ------------------------------------------------------------------------------------

import numpy as np
# ------------------------------------------------------------------------------------


def atom_transfer(transfer_list, header_distance_matrix, data_xyz, distance_matrix):
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

    max_distance = 2.0
    min_distance = 0.5

    coordinates_first = np.zeros(3, dtype=float)
    coordinates_central = np.zeros(3, dtype=float)
    coordinates_second = np.zeros(3, dtype=float)

    first_atom = transfer_list[0]
    central_atom = transfer_list[1]
    second_atom = transfer_list[2]

    # - atom index from XYZ file
    list_idx_central_atom = [i for i, x in enumerate(header_distance_matrix)
                             if x == central_atom]
    list_idx_first_atom = [i for i, x in enumerate(header_distance_matrix)
                           if x == first_atom]
    list_idx_second_atom = [i for i, x in enumerate(header_distance_matrix)
                            if x == second_atom]

    # - list to save all (q1, q2) pairs
    natural_bond_coordinates = []

    for central in list_idx_central_atom:
        coordinates_central[0] = float(data_xyz.iloc[central, 1])
        coordinates_central[1] = float(data_xyz.iloc[central, 2])
        coordinates_central[2] = float(data_xyz.iloc[central, 3])

        # - initial value to choose the min
        min_first = 10000

        choose_first = 0
        for first in list_idx_first_atom:

            if central == first:
                continue

            if distance_matrix[central, first] > min_distance \
                    and distance_matrix[central, first] < max_distance:
                distance_first = distance_matrix[central, first]
            elif distance_matrix[first, central] > min_distance \
                    and distance_matrix[first, central] < max_distance:
                distance_first = distance_matrix[first, central]
            else:
                continue

            if min_first != min(min_first, distance_first):
                min_first = min(min_first, distance_first)
                choose_first = first

                coordinates_first[0] = float(data_xyz.iloc[first, 1])
                coordinates_first[1] = float(data_xyz.iloc[first, 2])
                coordinates_first[2] = float(data_xyz.iloc[first, 3])

        # - vectorial distance between the central and first atom
        central_first = np.subtract(coordinates_central, coordinates_first)

        r1 = np.linalg.norm(central_first)

        if r1 > max_distance:
            continue

        # - initial value to choose the min
        min_second = 10000

        for second in list_idx_second_atom:

            if choose_first == second or central == second:
                continue

            if distance_matrix[central, second] > min_distance \
                    and distance_matrix[central, second] < max_distance:
                distance_second = distance_matrix[central, second]
            elif distance_matrix[second, central] > min_distance \
                    and distance_matrix[second, central] < max_distance:
                distance_second = distance_matrix[second, central]
            else:
                continue

            if min_second != min(min_second, distance_second):
                min_second = min(min_second, distance_second)

                coordinates_second[0] = float(data_xyz.iloc[second, 1])
                coordinates_second[1] = float(data_xyz.iloc[second, 2])
                coordinates_second[2] = float(data_xyz.iloc[second, 3])

        # - vectorial distance between the central and second atom
        central_second = np.subtract(coordinates_central, coordinates_second)

        r2 = np.linalg.norm(central_second)

        if r2 > max_distance:
            continue

        # - atoms transfer analysis compute q1 = 0.5 * (r1 - r2) and q2 = r1 + r2
        q1 = 0.5 * (r1 - r2)
        q2 = r1 + r2

        # if q2 < 2:
        #     print(central_first)
        #     print(central_second)

        natural_bond_coordinates.append((q1, q2))

    return natural_bond_coordinates
