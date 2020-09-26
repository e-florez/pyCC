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
    """


