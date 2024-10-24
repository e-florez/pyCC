#!/usr/bin/python3.8

# ------------------------------------------
# August  2020
#               cesar-ibarguen@udea.edu.co 
# 		cesar-b29@hotmail.com  github user: cesar-ibarguen 
#
# It is short python3.8 script to compute dihedral
# angles in degrees for given sets of four atoms. 
# The final aim is to determine dihedral angles
# between  a Hg atom and a water molecule.
#
# ------------------------------------------
# LIBRERIES

import os.path # - to check id a file or dir exits -> os.path.exists()
# -  to smooth out your data
import glob 

#import pandas as pd
# - arrays and matrix manipulation

import numpy as np
# - plotting

import math

#--------------- Body ------------
# Set initial values for arrays
p1 = np.zeros(3)
p2 = np.zeros(3)
p3 = np.zeros(3)
p4 = np.zeros(3)

# Set initial coordinates corresponding to w1s1 MP2
p1[:] = [-0.2251299774,  0.0000000026, 0.0107392362]
p2[:] = [1.8213760892,  0.0000000800, -0.0901652030]
p3[:] = [2.3259447762, -0.7989195366, 0.1773102636]
p4[:] = [2.3259447157,  0.7989197348, 0.1773102636]

# Calculate coordinates for vectors q1, q2 and q3
q1 = np.subtract(p2,p1) # b - a
q2 = np.subtract(p3,p2) # c - b
q3 = np.subtract(p4,p3) # d - c

# Calculate cross vectors
q1_x_q2 = np.cross(q1,q2)
q2_x_q3 = np.cross(q2,q3)

# Calculate normal vectors
n1 = q1_x_q2/np.sqrt(np.dot(q1_x_q2,q1_x_q2))
n2 = q2_x_q3/np.sqrt(np.dot(q2_x_q3,q2_x_q3))

# Orthogonal_unit_vectors(n2,q2):
#     "Function to calculate orthogonal unit vectors"
# Calculate unit vectors
u1 = n2
u3 = q2/(np.sqrt(np.dot(q2,q2)))
u2 = np.cross(u3,u1)

# Calc_dihedral_angle(n1,u1,u2,u3)
# Calculate cosine and sine
cos_theta = np.dot(n1,u1)
sin_theta = np.dot(n1,u2)

# Calculate theta
theta = -math.atan2(sin_theta,cos_theta)  

theta_deg = np.degrees(theta)

# Results
print("theta (rad) = %8.3f"%theta)
print("theta (deg) = %8.3f"%theta_deg)

exit()
