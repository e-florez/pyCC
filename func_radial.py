#!/usr/bin/env python3
# --------------------------------------------------------#
#   danianescobarv@gmail.com                              #
#   edisonffh@gmail.com                                   #
#   cesarfernando.ibarguen@gmail.com                      #
# --------------------------------------------------------#

import pandas as pd

#---------------------------------------------------------#
# -Start: Elements list to do radial distribution analisys#
#---------------------------------------------------------#
def all_elements(file_xyz):
    """[summary]
    Function to get atomic pairs from a XYZ file,
    when it is selected all the elements and verification.
    Args:
        file_xyz (list): name of the .xyz
    Return:
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
    Args:
        elements (list): pairs of elements from input
    Return:
        element_lsit (list): pairs of elements unique
    """

    # - Deleting comma used to split atomic pairs (if any)
    elements = [pair.replace(',','') for pair in elements]

    cont = 0
    elements_list = []
    #When there is alone a term in elements
    if len(elements) == 1:
        elements_list = elements
    #When there are several terms in elements
    else:
        while cont < len(elements):
            pair1 = elements[cont]
            #Comparing pair1 with the other terms in elements
            if cont != len(elements)-1:
                cont1 = cont + 1
            else:
                cont1 = cont - 1
            #Comparing with pairs already accepted like different
            while cont1 < len(elements):
                if pair1 != elements[cont1] :
                    i = 0
                    cont2 = 0
                    #Comparing with A-B and B-A
                    for i in range(len(elements_list)):
                        a1p1   = pair1.split('-')[0]
                        a2p1   = pair1.split('-')[1]
                        pair1r = a2p1 + '-' + a1p1
                        if pair1 == elements_list[i] or pair1r == elements_list[i]:
                            cont2 = 1
                    if len(elements_list) == 0 or cont2 == 0 :
                        #Save unique pairs
                        elements_list.append(pair1)
                        cont1 = len(elements)
                    else:
                        cont1 += 1
                else:
                    cont1 += 1
            cont += 1

    return elements_list
#---------------------------------------------------------#
# -End: Elements list to do radial distribution analisys  #
#---------------------------------------------------------#