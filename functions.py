#!/usr/bin/env python3
# ------------------------------------------------------------------------------------
# July 2020
#
# python3.x script by:
#
#   name: Edison Florez (github.com/e-florez/)
#   email: edisonffh@gmail.com
#   affiliation: Massey University, New Zealand
#
#   danianescobarv@gmail.com
#
#   cesar-b29@hotmail.com

# ------------------------------------------------------------------------------------
# Description:

# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# ------ Main body
# ------------------------------------------------------------------------------------

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
    pass


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


def format_files_XYZ(list_files_XYZ):
    """
        Function to choose those XYZ files to be analyse (by default all in working directory)
        and to CHECK if those files has the XYZ format to create a dictionary for each XYZ file
        with their coordinates in a pandas data frame 
 
        Args:
            list_files_XYZ (list str): It is a list with XYZ file's names 
            coordinates_XYZ (dict): It is a dictionary whit KEY: file_XYZ, VALUES: pandas dataframe (Sym, x, y, z)

        Input: 
           'list_files_XYZ' with all the XYZ files in the working directory
            
        Output: 
           'list_files_XYZ' with the XYZ files for the analysis (may be the same as input)
    """
    print(list_files_XYZ)
