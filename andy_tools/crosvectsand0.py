#!/usr/bin/python3

# Programa Creado Por Andy Zapata - IMIT 2020
# Realiza el producto cruz entre 2 vectores y 
# con el vector resultante, calcula el angulo
# entre éste y otro vector 

import numpy as np
from numpy.linalg import norm

# A = [1,2,3]
# B = [3,4,2]
# C = [6,7,8]


# Set initial coordinates corresponding to w1s1 MP2
p1 = [-0.2251299774,  0.0000000026, 0.0107392362]
p2 = [1.8213760892,  0.0000000800, -0.0901652030]
p3 = [2.3259447762, -0.7989195366, 0.1773102636]
p4 = [2.3259447157,  0.7989197348, 0.1773102636]
  
# Calculate coordinates for vectors q1, q2 and q3
A = np.subtract(p2, p3) # b - a
B = np.subtract(p2, p4) # c - b
C = np.subtract(p1, p2) # d - c


D = np.cross(A,B)
print ("Vector perpendicular al plano formado por ",A," y ",B," : ",D)

#Coseno entre 2 vectores
Cos = np.dot(D,C)/norm(D)/norm(C)
angle = np.arccos(Cos)
angle = np.degrees(angle)
#print ("Ángulo en radianes entre ",D," y ",C," : ",angle)
print ("Ángulo: ",angle)
