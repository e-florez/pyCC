#!/usr/bin/python3

# Programa Creado Por Andy Zapata - IMIT 2020
# Realiza el producto cruz entre 2 vectores y 
# con el vector resultante, calcula el angulo
# entre éste y otro vector 

import numpy as np
from numpy.linalg import norm

A = [1,2,3]
B = [3,4,2]
C = [6,7,8]

D = np.cross(A,B)
print ("Vector perpendicular al plano formado por ",A," y ",B," : ",D)

#Coseno entre 2 vectores
Cos = np.dot(D,C)/norm(D)/norm(C)
angle = np.arccos(Cos)
print ("Ángulo en radianes entre ",D," y ",C," : ",angle)