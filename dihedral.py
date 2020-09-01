#!/usr/bin/python3.8

def dihedral(p1, p2, p3, p4):
    """ ------------------------------------------
    # August  2020
    #               cesar.ibarguen@udea.edu.co
    #
    # computing DIHEDRAL angle
    #          p3
    #         /
    #  p1----p2
    #         \
    #          p4
    # - order matters!
    # ------------------------------------------
    """
    # LIBRERIES
    import numpy as np
    import math

    #--------------- Body ------------

    # Calculate coordinates for vectors q1, q2 and q3
    q1 = np.subtract(p2, p1) # b - a
    q2 = np.subtract(p3, p2) # c - b
    q3 = np.subtract(p4, p3) # d - c

    # Calculate cross vectors
    q1_x_q2 = np.cross(q1, q2)
    q2_x_q3 = np.cross(q2, q3)

    # print(f'q1_x_q2: {q1_x_q2}')
    # print(f'q2_x_q3: {q2_x_q3}')


    # Calculate normal vectors
    n1 = q1_x_q2 / np.sqrt(np.dot(q1_x_q2, q1_x_q2))
    n2 = q2_x_q3 / np.sqrt(np.dot(q2_x_q3, q2_x_q3))

    # Orthogonal_unit_vectors(n2,q2):
    #     "Function to calculate orthogonal unit vectors"
    # Calculate unit vectors
    u1 = n2
    u3 = q2 / ( np.sqrt(np.dot(q2, q2)) )
    u2 = np.cross(u3, u1)

    # Calc_dihedral_angle(n1,u1,u2,u3)
    # Calculate cosine and sine
    cos_theta = np.dot(n1, u1)
    sin_theta = np.dot(n1, u2)

    # Calculate theta
    theta = -math.atan2(sin_theta, cos_theta)

    theta_deg = abs(np.degrees(theta))

    return theta_deg

