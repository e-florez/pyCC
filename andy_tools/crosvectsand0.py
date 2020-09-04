#!/usr/bin/python3

# Programa Creado Por Andy Zapata - IMIT 2020
# Realiza el producto cruz entre 2 vectores y 
# con el vector resultante, calcula el angulo
# entre éste y otro vector 

import tools as tl
import numpy as np

#Lectura de archivo xyz
namesxyz = tl.filesxyz()
print(f"Nombre de los xyz : ",namesxyz)

# Almacena el identificador del átomo y número de átomos 
# en un vector de (natoms + 1) x 1, el 1 de más, es que 
# en la primera posición del vector se encuentra la cantidad 
# de átomos (NALA). Además, devuelve un arreglo de número 
# de átomos x 3 con las coordenadas (MXYZ)

out = tl.LXYZ(namesxyz)
NALA = out[0]
MXYZ = np.zeros((3,NALA[0]))
MXYZ = out[1]
################################################################################
# Calculo del ángulo entre 3 átomos                                            #
################################################################################
#Pregunta el átomo del vertice del ángulo y la distancia máxima de los átomos con que 
#se quiere calcular el angulo

#print ("Átomos en",namesxyz," : ",NALA)
#vatom = input(f"Átomo del vertice del angulo (Simbolo): ") #Faltaria además darle una etiqueta para eligir
#rmax  = float(input(f"Distancia máxima al vertice : "))    #entre los mismos átomos el que se quiere, por ahora
                                                           #solo sería con vatom = Hg
vatom = "Hg"
rmax = 2.35
# Se calcula las distancias de todos los átomos con respecto
# al vertice. Falta identificar los átomos que participan en 
# el ángulo
out = tl.rv(vatom,rmax,NALA,MXYZ) 
NAV = out[0]

if NAV < 2 :
    print (f"No se calculo ángulo, ya que se necesitan almenos 2 átomos diferentes al vertice")
else : #Empieza el calculo de los ángulos
    VR1 = out[1] 
    VR  = np.zeros((NAV,4)) 
    for i in range(NAV) : 
        for j in range(4) :
            VR[i,j]  = VR1[i,j]    

    out = tl.angle(NAV,VR)
    NA  = out[0]
    VA1 = out[1]
    VA  = np.zeros((NA))
    print (f"Cantidad de angulos : ",NA)
    for i in range(NA):  
        VA[i] = float(VA1[i])
        print (f"Angulos : ",VA[i])  #Falta identificar los átomos, por ejemplo, en el orden que están en xyz

#########################################################################################
# Calculo del ángulo dihedral, que se encuentra entre cada mnolécula de H2O y el Hg     #
#########################################################################################
# Se busca los oxígenos más cercanos al Hg, según el límite rmaxo. Además, se 
# supone que las moléculas de H2O no están disociadas 
#rmaxo = float(input("Distancia máxima O a Hg : "))
rmaxo = 2.35
out = tl.SM(NALA,MXYZ,rmaxo)
NAW = out[0]

if NAW < 1 :
    print(f"No se calcula dihedro, ya que se necesita almenos una molécula de H2O")
else :
    VR1 = out[1]
    VR = np.zeros((NAW,4))
    for i in range(NAW) :
        for j in range(4) : 
            VR[i,j] = VR1[i,j]
    
    RHg1 = out[2]
    RHg = np.zeros((3))
    for i in range(3) :
        RHg[i] = RHg1[i]

# Función externa que calcula el vector perpendicular en A y B, 
# además del angulo entre el vector resultante con C, el cual 
# sería el angulo dihedral entre el plabo formado por A y B con 
# el vector C
    out = tl.dihedral(NAW,VR,RHg)

NO = int(NAW/3)
d1 = out
dihedros = np.zeros((NO))
print (f"Cantidad de dihedros : ",NO)
for i in range(NO):
    dihedros[i] = d1[i]
    print(f"dihedro : ",dihedros[i]) 
