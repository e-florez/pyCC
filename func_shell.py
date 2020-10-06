#!/usr/bin/env python3
# ------------------------------------------------------------------------------------
#   danianescobarv@gmail.com
#   edisonffh@gmail.com
#   cesarfernando.ibarguen@gmail.com
# ------------------------------------------------------------------------------------

import os  # - to check id a file or dir exits -> os.path.exists()

#---------------------------------------------------------#
# -Start: Working Directory                               #
#---------------------------------------------------------#
def working_path (path):
    """[summary]
    Get path of working directory from variable path or ask
    Args:
        path (string) : with or no path of working directory
    Return:
        working_dir (string) : path of working directory
    """

    if len(path) <= 1 :
        tmp_dir =  input(f'\nDirectory (whit the XYZ files) to make the RDA [default: empty]: ')
        tmp_dir = tmp_dir.strip()

        if tmp_dir == '.' or len(tmp_dir) < 1:
            working_dir = os.getcwd()
        else:
            print(f"\n*** ERROR ***")
            exit(f"Path of Working Directory, {working_dir}")
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

    return working_dir

def cd_path (working_dir) :
    """[summary]
    Change to working directory
    Args:
        working_dir (string): path of directory with .xyz
    """
    # Check if the working dir exists
    if os.path.exists(working_dir) :
        # Change the current working Directory
        os.chdir(working_dir)
    else:
        print(f'\n*** ERROR ***')
        exit(f"Can't change the Working Directory, {working_dir} doesn't exist")
#---------------------------------------------------------#
# -End: Working Directory                                 #
#---------------------------------------------------------#