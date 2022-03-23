import pandas as pd
import numpy as np

dfxyz =\
    pd.DataFrame(np.transpose([['A','B','A','C','C','C'],\
        [0.,2.,3.,0.,1.,2.],[0.,0.,1.,0.,5.,0.],[0.,1.,0.,2.,1.,4.]]),\
        columns=['atom','x','y','z'])

df =\
    pd.DataFrame(\
        np.transpose([['A','B','A','C','C','C'],\
            [0.0,2.24,3.16,2.00,5.20,4.47],[2.24,0.0,1.73,2.24,5.10,3.00],[3.16,1.73,0.0,3.74,4.58,4.24]]),\
            columns=['atom','A','B','A'])

ncols = len(df.iloc[0,:])
nrows = len(df.iloc[:,0])
for icol in range(ncols):
    if df.columns[icol] == 'A': #filtro por label del átomo del vertice
        vector_vertice=df.iloc[:, [0,icol]].sort_values(by=['A'])
        print('\nDistancias con respecto al vertice seleccionado \n',vector_vertice,'\n')
        #Se cuenta desde el segundo átomo, ya se sabe quien es el verice, además el segundo átomo se
        #empareja con todos los posibles átomos que están a menos de 3 al verice como el segundo átomo
        irow_atom1 = 1
        while irow_atom1 < nrows and float(vector_vertice.iloc[irow_atom1+1,1]) < 3. :
            #Número de línea del átomo 1 de interes en el dataframe con las coordenadas
            nline_atom1_xyz= vector_vertice.index.values[irow_atom1]
            #theta = cos^{-1}(A . B/(|A||B|))
            #Coordenadas del primer átomo a una distancia máxima de 3 al verice
            A1 = np.zeros((3),dtype=float)
            A1[0]=dfxyz.iloc[nline_atom1_xyz,1]
            A1[1]=dfxyz.iloc[nline_atom1_xyz,2]
            A1[2]=dfxyz.iloc[nline_atom1_xyz,3]
            #contador del 2 atomo al vertice
            irow_atom2 = irow_atom1 + 1
            #Filtro por distancia máxima
            while irow_atom2 < nrows and float(vector_vertice.iloc[irow_atom2,1]) < 3. :
                #Número de línea del átomo 2 de interes en el dataframe con las coordenadas
                nline_atom2_xyz= vector_vertice.index.values[irow_atom2]
                #Coordenadas del segundo átomo a una distancia máxima de 3 al verice
                A2 = np.zeros((3),dtype=float)
                A2[0]=dfxyz.iloc[nline_atom2_xyz,1]
                A2[1]=dfxyz.iloc[nline_atom2_xyz,2]
                A2[2]=dfxyz.iloc[nline_atom2_xyz,3]
                A1pA2 = np.dot(A1,A2)
                #cos(theta)
                costheta =\
                    A1pA2/(float(vector_vertice.iloc[irow_atom1,1])\
                    *float(vector_vertice.iloc[irow_atom2,1]))
                #theta
                theta = np.arccos(costheta)
                #atomo con indice A1--A0(vertice)--A2
                label_A1 = str(vector_vertice.iloc[irow_atom1,0])\
                    + str(vector_vertice.index.values[irow_atom1])
                label_A0 = str(vector_vertice.iloc[0,0])\
                    + str(vector_vertice.index.values[0])
                label_A2 = str(vector_vertice.iloc[irow_atom2,0])\
                    + str(vector_vertice.index.values[irow_atom2])
                print('Angulo entre (',label_A1,',',label_A0,',',label_A2,') : ',theta)
                irow_atom2 += 1
            else:
                irow_atom2 = nrows
                print('\n No hay un segundo átomo a 3 al vertice ',str(vector_vertice.iloc[0,0])\
                    + str(vector_vertice.index.values[0]))
            irow_atom1 += 1
        else:
            if irow_atom1 == 1:
                print('\n No hay 2 átomos que estén a una distancia inferior de 3 al vertice')
