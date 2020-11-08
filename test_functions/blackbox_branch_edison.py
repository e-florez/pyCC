#!/usr/bin/env python3
# ------------------------------------------------------------------------------------
# September 2020
#   danianescobarv@gmail.com
# python3.6 script to try functions in function.py:
# 1) def working_path (path)
# 2) def cd_path (working_dir)
# 3) def all_elements(file_xyz)
# 4) def sort_input_pairs(elements)
# ------------------------------------------------------------------------------------

import unittest
import functions as fn
import os
import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal # <-- for testing dataframes
import numpy as np

class Test(unittest.TestCase):
    def test_functions1(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        file_xyz = 'check_format.xyz'
        df = pd.read_csv("check_format.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        df1 = fn.format_xyz(file_xyz)
        for i in range(6):
            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        print("\n...Ok : functions.dict_coordinates_xyz ")
        print("\n        No hay problemas con la lectura del formato")
    def test_functions2(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        file_xyz = 'check_format.xyz'
        df = pd.read_csv("check_format.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        os.remove(file_xyz)
        f = open("check_format.xyz","w")
        f.write('6 \n')
        f.write(' \n')
        f.write('h  0.000 0.000 0.000\n')
        f.write('o  1.000 0.000 0.200\n')
        f.write('hg 1.000 3.000 0.300\n')
        f.write('c  2.000 0.500 0.400\n')
        f.write('n  1.500 3.300 0.500\n')
        f.write('f  3.500 0.000 0.600')
        f.close()

        df1 = fn.format_xyz(file_xyz)
        diferencias = 0
        for i in range(6):
            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        print("\n...Ok : functions.dict_coordinates_xyz ")
        print("\n         Acepta la lectura del simbolos atómico en minúscula,")
        print("           además los devuelve en el formato estandar")
    def test_functions3(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        print("\n...Error1 : functions.dict_coordinates_xyz ")
        print("\n          No se pone la etiqueta de 1 átomos")

        f = open("check_format1.xyz","w")
        f.write('6 \n')
        f.write(' \n')
        f.write('h  0.000 0.000 0.000\n')
        f.write('o  1.000 0.000 0.200\n')
        f.write(' 1.000 3.000 0.300\n')
        f.write('c  2.000 0.500 0.400\n')
        f.write('n  1.500 3.300 0.500\n')
        f.write('f  3.500 0.000 0.600')
        f.close()
        file_xyz = 'check_format1.xyz'

        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        df1 = fn.format_xyz(file_xyz)
        print('\n',df,'\n Descripción del Error \n ****',df1)
#        for i in range(6):
#            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
    def test_functions4(self):
        """[summary]
        
        """

        print("\n*****************************************************************")
        print("\n...Error2 : functions.dict_coordinates_xyz ")
        print("\n          No se pone la coordenada y de 1 átomos")

        f = open("check_format1.xyz","w")
        f.write('6 \n')
        f.write(' \n')
        f.write('h  0.000 0.000 0.000\n')
        f.write('o  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300\n')
        f.write('c  2.000 0.500 0.400\n')
        f.write('n  1.500 3.300 0.500\n')
        f.write('f  3.500  0.600')
        f.close()
        file_xyz = 'check_format1.xyz'

        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        df1 = fn.format_xyz(file_xyz)
        diferencias = 0
        print('\n',df,'\n Descripción del Error \n ****',df1)
#        for i in range(6):
#            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
    def test_functions5(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        print("\n...Error3 : functions.dict_coordinates_xyz ")
        print("\n          Simbolo atómico no designado de 2 caracteres")
        f = open("check_format1.xyz","w")
        f.write('6 \n')
        f.write(' \n')
        f.write('Y  0.000 0.000 0.000\n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300\n')
        f.write('C  2.000 0.500 0.400\n')
        f.write('N  1.500 3.300 0.500\n')
        f.write('Ya  3.500 0.000 0.600')
        f.close()
        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        file_xyz = 'check_format1.xyz'
        df1 = fn.format_xyz(file_xyz)
        for i in range(6):
            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
        print(' ...Ok : functions.dict_coordinates_xyz')
        print('*********WARNING**************')
        print('Se aceptan simbolos no designados a átomos')
    def test_functions6(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        print("\n...Error4 : functions.dict_coordinates_xyz ")
        print("\n          No se pone la cantidad de átomos en la primera línea")
        f = open("check_format1.xyz","w")
        f.write(' \n')
        f.write(' \n')
        f.write('Y  0.000 0.000 0.000\n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300\n')
        f.write('C  2.000 0.500 0.400\n')
        f.write('N  1.500 3.300 0.500\n')
        f.write('Hg  3.500 0.000 0.600')
        f.close()
        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        file_xyz = 'check_format1.xyz'
        df1 = fn.format_xyz(file_xyz)
        print('\n',df,'\n Descripción del Error \n ****',df1)
#        for i in range(6):
#            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
    def test_functions7(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        print("\n...Error5 : functions.dict_coordinates_xyz ")
        print("\n          No se pone la cantidad total correcta de átomos")
        f = open("check_format1.xyz","w")
        f.write('1 \n')
        f.write(' \n')
        f.write('Y  0.000 0.000 0.000\n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300\n')
        f.write('C  2.000 0.500 0.400\n')
        f.write('N  1.500 3.300 0.500\n')
        f.write('Hg  3.500 0.000 0.600')
        f.close()
        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        file_xyz = 'check_format1.xyz'
        df1 = fn.format_xyz(file_xyz)
        print('\n',df,'\n Descripción del Error \n ****',df1)
#        for i in range(6):
#            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
    def test_functions8(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        print("\n...Error6 : functions.dict_coordinates_xyz ")
        print("\n           String donde van las coordenadas")
        f = open("check_format1.xyz","w")
        f.write('6 \n')
        f.write(' \n')
        f.write('Y  0.000 aaee 0.000\n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300\n')
        f.write('C  2.000 0.500 0.400\n')
        f.write('N  1.500 3.300 0.500\n')
        f.write('Hg  3.500 0.000 0.600')
        f.close()
        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        file_xyz = 'check_format1.xyz'
        df1 = fn.format_xyz(file_xyz)
        print('\n',df,'\n Descripción del Error \n ****',df1)
#        for i in range(6):
#            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
    def test_functions9(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        print("\n...Error7 : functions.dict_coordinates_xyz ")
        print("\n           Simbolo atómico no designado con mas de 2 caracteres")
        f = open("check_format1.xyz","w")
        f.write('6 \n')
        f.write(' \n')
        f.write('Y  0.000 0.000 0.000\n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300\n')
        f.write('C  2.000 0.500 0.400\n')
        f.write('N  1.500 3.300 0.500\n')
        f.write('Aeee  3.500 0.000 0.600')
        f.close()
        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        file_xyz = 'check_format1.xyz'
        df1 = fn.format_xyz(file_xyz)
        for i in range(6):
            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
        print(' ...Ok : functions.dict_coordinates_xyz')
        print('*********WARNING**************')
        print('Se aceptan simbolos no designados a átomos con más de 3 caracteres')
    def test_functions91(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        print("\n...Error8 : functions.dict_coordinates_xyz ")
        print("\n           Linea en blanco entre átomos")
        f = open("check_format1.xyz","w")
        f.write('7 \n')
        f.write(' \n')
        f.write('Y  0.000 0.000 0.000\n')
        f.write('                    \n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300\n')
        f.write('C  2.000 0.500 0.400\n')
        f.write('N  1.500 3.300 0.500\n')
        f.write('Hg  3.500 0.000 0.600')
        f.close()
        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        file_xyz = 'check_format1.xyz'
        df1 = fn.format_xyz(file_xyz)
        print('\n',df,'\n Descripción del Error \n ****',df1)
#        for i in range(6):
#            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
    def test_functions92(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        print("\n...Error9 : functions.dict_coordinates_xyz ")
        print("\n           String en donde va la cantidad de átomos")
        f = open("check_format1.xyz","w")
        f.write('aaaa \n')
        f.write(' \n')
        f.write('Y  0.000 0.000 0.000\n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300\n')
        f.write('C  2.000 0.500 0.400\n')
        f.write('N  1.500 3.300 0.500\n')
        f.write('Hg  3.500 0.000 0.600')
        f.close()
        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        file_xyz = 'check_format1.xyz'
        df1 = fn.format_xyz(file_xyz)
        print('\n',df,'\n Descripción del Error \n ****',df1)
#        for i in range(6):
#            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
    def test_functions93(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        f = open("check_format1.xyz","w")
        f.write('6 \n')
        f.write(' \n')
        f.write('Y  1 0.000 0.000\n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300\n')
        f.write('C  2.000 0.500 0.400\n')
        f.write('N  1.500 3.300 0.500\n')
        f.write('Hg  3.500 0.000 0.600')
        f.close()
        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        file_xyz = 'check_format1.xyz'
        df1 = fn.format_xyz(file_xyz)
        for i in range(6):
            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        print("\n...Ok : functions.dict_coordinates_xyz ")
        print("\n        Se aceptan coordenadas en enteros")

        os.remove(file_xyz)
    def test_functions94(self):
        """[summary]
        
        """
        print("\n*****************************************************************")
        print("\n...Error10 : functions.dict_coordinates_xyz ")
        print("\n           Un columna más en las coordenadas de 1 átomo")
        f = open("check_format1.xyz","w")
        f.write('aaaa \n')
        f.write(' \n')
        f.write('Y  0.000 0.000 0.000\n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Sc 1.000 3.000 0.300 0.000 \n')
        f.write('C  2.000 0.500 0.400\n')
        f.write('N  1.500 3.300 0.500\n')
        f.write('Hg  3.500 0.000 0.600')
        f.close()
        df = pd.read_csv("check_format1.xyz",
                            delim_whitespace=True,
                            skiprows=2,
                            header=None,
                            names=["element", "x-coordinate",
                            "y-coordinate", "z-coordinate"]
                            )
        file_xyz = 'check_format1.xyz'
        df1 = fn.format_xyz(file_xyz)
        print('\n',df,'\n Descripción del Error \n ****',df1)
#        for i in range(6):
#            pd.testing.assert_series_equal(df1.iloc[1],df.iloc[1],check_dtype=False)
        os.remove(file_xyz)
if __name__ == '__main__':
    f = open("check_format.xyz","w")
    f.write('6 \n')
    f.write(' \n')
    f.write('H  0.000 0.000 0.000\n')
    f.write('O  1.000 0.000 0.200\n')
    f.write('Hg 1.000 3.000 0.300\n')
    f.write('C  2.000 0.500 0.400\n')
    f.write('N  1.500 3.300 0.500\n')
    f.write('F  3.500 0.000 0.600')
    f.close()
    unittest.main()
    print("\n Everything passed")

    check_format.xyz