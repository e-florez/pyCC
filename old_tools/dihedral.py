#!/usr/bin/python3.8

def dihedral(p1, p2, p3, p4):
    """ ------------------------------------------
    August  2020
                cesar.ibarguen@udea.edu.co

    computing DIHEDRAL angle
            p3
            /
    p1----p2
            \
            p4
    - order matters!
    # ------------------------------------------
    """
    # # LIBRERIES
    import numpy as np
    # import math

    #--------------- Body ------------

    # Calculate coordinates for vectors q1, q2 and q3
    q1 = np.subtract(p2, p1) # b - a
    q2 = np.subtract(p3, p2) # c - b
    q3 = np.subtract(p4, p3) # d - c

    # Calculate cross vectors
    q1_x_q2 = np.cross(q1, q2)
    q2_x_q3 = np.cross(q2, q3)

    # - protecting for and zero division
    if np.linalg.norm(q1_x_q2) < 0.1 or \
        np.linalg.norm(q2_x_q3) < 0.1:
        return 0

    # Calculate normal vectors
    n1 = q1_x_q2 / np.linalg.norm(q1_x_q2)
    n2 = q2_x_q3 / np.linalg.norm(q2_x_q3)

    cos_theta = np.dot(n1, n2)

    theta = np.arccos(cos_theta)
    theta_deg = abs(np.degrees(theta))

    return theta_deg