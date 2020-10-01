#!/usr/bin/env python3
# ------------------------------------------------------------------------------------
# July 2020
#   edisonffh@gmail.com
# September 2020
#   danianescobarv@gmail.com
# ------------------------------------------------------------------------------------

import os  # - to check id a file or dir exits -> os.path.exists()
import pandas as pd # - complete data analysis tool (it can replace matplotlib or numpy, as it is built on top of both)

def working_path (path):
    """[summary]
    Get path of working directory from variable path or ask
    Input:
        path (string) : with or no path of working directory
    Output:
        working_dir (string) : path of working directory
    """

    if len(path) <= 1 :
        tmp_dir =  input(f'\nDirectory (whit the XYZ files) to make the RDA [default: empty]: ')
        tmp_dir = tmp_dir.strip()

        if tmp_dir == '.' or len(tmp_dir) < 1:
            working_dir = os.getcwd()
        else:
            working_dir = os.getcwd() + '/' + tmp_dir
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
    Input:
        working_dir (string): path of directory with .xyz
    """
    # Check if the working dir exists
    if os.path.exists(working_dir) :
        # Change the current working Directory
        os.chdir(working_dir)
    else:
        print(f'\n*** ERROR ***')
        exit(f"Can't change the Working Directory, {working_dir} doesn't exist")


def all_elements(file_xyz):
    """[summary]
    Function to get atomic pairs from a XYZ file,
    when it is selected all the elements and verification.
    Input:
        file_xyz (list): name of the .xyz
    Output:
        element_list (list): pairs of elements unique
    """

    #bug: Cuando en el xyz se pone en minúscula el símbolo del
    #del elemento hay diferencias, aprece que no encuentra distancias
    #o ángulos que si encuentra cuando el símbolo tiene la mayúscula

    elements = pd.read_csv(file_xyz, delim_whitespace=True,
                    skiprows=2, header=None,
                    names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])

    # - if XYZ file has no coordinates (by mistake)
    if elements.shape[0] <= 1:
        elements = []
        print(f'\n*** WARNING *** \nNo coordinates found in {file_xyz}')
        return elements
        # return '*** WARNING *** No coordinates found in ', file_xyz

    elements = elements['element'].tolist()

    # - list of elements (uniques)
    elements_uniq = []
    for atom in elements:
        if atom not in elements_uniq:
            elements_uniq.append(atom)

    elements = []
    elements = [atoms.capitalize() for atoms in elements_uniq]

    element_list = []
    atom_a = 0
    while atom_a < len(elements):
        #element_list.append(elements[atom_a] + '-' + elements[atom_a]) no es necesaría
        atom_b = atom_a
        while atom_b < len(elements):
            element_list.append(elements[atom_a] + '-' + elements[atom_b])
            atom_b += 1
        atom_a += 1

    return element_list

def sort_input_pairs(elements):
    """[summary]
    Sorting uniques atomic pair A-B from an input list
    Input:
        elements (list): pairs of elements from input
    Output:
        element_lsit (list): pairs of elements unique
    """

    # - Deleting comma used to split atomic pairs (if any)
    elements = [pair.replace(',','') for pair in elements]

    cont = 0
    elements_list = []
    if len(elements) == 1:
        elements_list = elements
    else:
        while cont < len(elements):
            pair1 = elements[cont]
            if cont != len(elements)-1:
                cont1 = cont + 1
            else:
                cont1 = cont - 1
            while cont1 < len(elements):
                if pair1 != elements[cont1] :
                    i = 0
                    cont2 = 0
                    for i in range(len(elements_list)):
                        a1p1   = pair1.split('-')[0]
                        a2p1   = pair1.split('-')[1]
                        pair1r = a2p1 + '-' + a1p1
                        if pair1 == elements_list[i] or pair1r == elements_list[i]:
                            cont2 = 1
                    if len(elements_list) == 0 or cont2 == 0 :
                        elements_list.append(pair1)
                        cont1 = len(elements)
                    else:
                        cont1 += 1
                else:
                    cont1 += 1
            cont += 1

    return elements_list