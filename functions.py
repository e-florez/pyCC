#!/usr/bin/env python3
# ------------------------------------------------------------------------------------
# July 2020
#
# python3.x script by:
#
#   name        : Edison Florez (github.com/e-florez/)
#   email       : edisonffh@gmail.com
#   affiliation : Massey University, New Zealand
#
#   name        : Andy Zapata (github.com/AndyDanian)
#   email       : danianescobarv@gmail.com
#   affiliation : Institute of Modelling and Innovative Technology (CONICET-IMIT), Argentina
#
#   cesar-b29@hotmail.com

# ------------------------------------------------------------------------------------
# Description:

# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# ------ Main body
# ------------------------------------------------------------------------------------

import os  # - to check id a file or dir exits -> os.path.exists()
def working_directory():
    """
       [summary]

       input: a, b, c
       output: d

       Args:
           a (str): distancia
           b ([type]): [description]
           c ([type]): [description]
           d ([type]): [description]
    """

    """[summary]
    Ask or get path of working directory from variable path
    Input:
        path (string) : with or no path of working directory
    Output:
        working_dir (string) : path of working directory
    """
    """[summary]
    Change to working directory
    Input:
        working_dir (string): path of directory with .xyz
    """


    if len(path) <= 1 :
        tmp_dir =  input(f'\nDirectory (whit the XYZ files) to make the RDA [default: empty]: ')
        tmp_dir = tmp_dir.strip()

        #if tmp_dir == '.' or len(tmp_dir) < 1:
        #    working_dir = os.getcwd()
        #else:
        #    working_dir = os.getcwd() + '/' + tmp_dir
    elif path[1] == '.' :
        working_dir = os.getcwd()
        print(f'\nWorking directiry: {working_dir}')
    else:
        #working_dir = os.getcwd() + '/' + path[1]
        #La idea de pedir el path, es poner toda la dirección y
        #en el caso de hacer la evaluación dentro de la misma
        #carpeta que se esta parado se pone un .
        working_dir = path[1]
        print(f'\nWorking directiry: {working_dir}')

    # Check if the working dir exists
    if os.path.exists(working_dir) :
        # Change the current working Directory
        os.chdir(working_dir)
    else:
        print(f'\n*** ERROR ***')
        exit(f"Can't change the Working Directory, {working_dir} doesn't exist")

def reading_files_XYZ():
    """
       [summary]

       input: a, b, c
       output: d

       Args:
           a (str): distancia
           b ([type]): [description]
           c ([type]): [description]
           d ([type]): [description]
    """
    pass


def format_files_XYZ():
    """
       [summary]

       input: a, b, c
       output: d

       Args:
           a (str): distancia
           b ([type]): [description]
           c ([type]): [description]
           d ([type]): [description]
    """
    pass
