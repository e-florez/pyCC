#!/usr/bin/env python3

# ------------------------------------------------------------------------------------
#   python3.x function to read file to be analyzed 
#
#
#   *** End of September 2020 by cesar-b29@hotmail.com ***
# ------------------------------------------------------------------------------------
import glob             # - Unix style pathname pattern expansion
import numpy as np      # - arrays and matrix manipulation
import pandas as pd     # -
import os               # - to check id a file or dir exits -> os.path.exists() # -  to smooth out your data


repited_list_xyz = []  # repited files (if any)
list_xyz = []  # unique files

def reading_files(list_xyz, repited_list_xyz):
    """
    *** Late September 2020 by cesar-b29@hotmail.com ***

    python3.x function to read the xyz files where there is the information to be analyze.

    Args:
        list_xyz ([list, str]): List of  files to be analyzed.
        repited_list (list, str): List of repited files in the work directory. 
      

    Returns: It shoould return 
        
    """

        # - reading files


    for input_xyz in glob.glob('*.xyz'):
        name_xyz = input_xyz[:-4]  # deleting file extention
        repited_list_xyz.append(input_xyz)  # creating an array for all xyz files

        # keeping unique xyz files
        for unique_input_xyz in repited_list_xyz:
            if unique_input_xyz not in list_xyz:
                list_xyz.append(unique_input_xyz)


    # - checking if files exist
    if len(list_xyz) > 0:
        for input_xyz in list_xyz:
            if not os.path.exists(input_xyz):
                print(f'\n*** Warinnig ***\n file {input_xyz} does not exits \n')
    else:
        exit(f' *** ERROR ***\n No file found to make the RDA \n ')

    print(f'\nA total of {len(list_xyz)} xyz were files analized\n')

    count = 0
    columns = 4
    while count < len(list_xyz):
        print(f'\t'.join(list_xyz[count:count + columns]))

        count += (columns + 1)

    return list_xyz    
        

    # -------------------------------------------------------------------------------
    # - Elements list to do radial distribution analisys
    

# def all_elements(file_xyz):
#     """ Function to get atomic pairs from a XYZ file  """
#     elements = pd.read_csv(list_xyz[0], delim_whitespace=True,
#                            skiprows=2, header=None,
#                            names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])

#     # - if XYZ file has no coordinates (by mistake)
#     if elements.shape[0] <= 1:
#         elements = []
#         print(f'\n*** WARNING *** \nNo coordinates found in {file_xyz}')
#         return elements
#         # return '*** WARNING *** No coordinates found in ', file_xyz

 