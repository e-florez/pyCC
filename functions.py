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
# ------------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# Main body
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


def reading_files_xyz():
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


def what_xyz_files(files_list_xyz, working_dir):
    """
    CHOOSING those XYZ files to analyse (by default all in working directory)

    Args:
        files_list_xyz (list str): It is a list with all XYZ file's names in the working directory
        working_dir (str): path with the working directory

    Returns:
        files_list (list str): It is a list with only those XYZ file's names to analyse.
        By default this function returns the same list with all the XYZ files found in the working directory

    by: Edison Florez <edisonffh@gmail.com>
    """
    # - avoiding an empty list
    files_list_xyz = list(filter(None, files_list_xyz))
    if len(files_list_xyz) < 1:
        # if not any(s.strip() for s in files_list_xyz):
        exit(f'\n *** ERROR ***\n Not XYZ file found in: \'{working_dir}\'')

    while True:
        input_list = input(
            f'What XYZ files do you want to analyse, separated by comma? [default: all] \n')

        input_list = input_list.split(',')

        if len(input_list[0]) == 0 or input_list[0].lower().strip() == 'all':
            return files_list_xyz

        else:

            files_list = []
            for xyz in input_list:

                # - removing any leading or trailing whitespaces
                xyz = xyz.strip()

                if xyz not in files_list_xyz:
                    print(f'** Warnnig ** file \'{xyz}\' does not exits \n')
                else:
                    files_list.append(xyz)

        # - EXITING with a not empty list
        if len(files_list) > 0:
            break

    return files_list
# ---------------------------------------------------------------------------------------


def format_xyz(file_xyz):
    # - Modules
    import pandas as pd

    """
    CHECKING if a file has the XYZ format.
    
    The formatting of the .xyz file format is as follows:
        <number of atoms>
        comment line
        <element> <X> <Y> <Z> 
    
    Args:
        file_xyz (str): XYZ file name
        
    Returns:
        a dataframe (element, x, y, z)

    by: Edison Florez <edisonffh@gmail.com>
    """

    # - if error_message == 0, not error found
    error_message = ''

    # - numbering lines
    line_number = 0

    with open(file_xyz, 'r') as f:
        # - reading line by line
        for line in f:
            line_number += 1
            values = [i for i in line.split()]

            # - firts line is number of atoms
            if line_number == 1:
                try:
                    atoms_number = int(values[0])
                except ValueError as e:
                    error_message += '\n | line 1: it must be a positive integer'
                    error_message += f'\n--- {e} ---\n'

            # - second line is a comment line. Its content does not matter
            # - third line and beyond must have: (element, x, y, z)
            elif line_number > 2:
                try:
                    assert len(values) == 4
                except AssertionError as e:
                    error_message += '\n | Not enough data for elements and coordinates. It must be: (element, x, y, z)'
                    error_message += f'\n--- {e} ---\n'

                # - checking x, y, z coordinates
                if not error_message:
                    for i in range(1, 4):
                        try:
                            float(values[i])
                        except ValueError as e:
                            error_message += '\n | coordinates (x, y, z) must be floats'
                            error_message += f'\n--- {e} ---\n'

    if not error_message and (line_number - 2) != atoms_number:
        error_message += '\n | Not enough atoms were found'
        error_message += f'\n--- Number of atoms at line 1: {atoms_number}, is not equivalent with total lines found: {line_number} lines ---\n'

    # - creating a df from a XYZ file
    if not error_message:
        df = pd.read_csv(file_xyz,
                         delim_whitespace=True,
                         skiprows=2,
                         header=None,
                         names=["element", "x-coordinate",
                                "y-coordinate", "z-coordinate"]
                         )

    else:
        df = "WARNING: check file '" + file_xyz + "'\n\n ** Error **\n" + error_message

    return df
# ---------------------------------------------------------------------------------------


def dict_coordinates_xyz(files_list_xyz):
    """
    CHECKING if those files has the XYZ format.
    CREATING a dictionary for each XYZ file with their coordinates in a pandas data frame 

    Args:
        files_list_xyz (list str): It is a list with those XYZ file's names to analyse

    Returns: 
        coordinates_xyz (dict): KEY: file.xyz (str), VALUES: pandas dataframe (element, x, y, z)
                                coordinates_xyz = {file.xyz: (element, x, y, z)}

    Technical info:
        CREATING a dictionary -> coordinates_xyz = {file.xyz: df}
        and 'df' is a data frame with four columns (element, x, y, z)
        A dataframe because is a good python object to filter and manupulate.

    by: Edison Florez <edisonffh@gmail.com>
    """

    coordinates_xyz = {}
    for file_xyz in files_list_xyz:
        coordinates_xyz[file_xyz] = format_xyz(file_xyz)

    return coordinates_xyz
# ---------------------------------------------------------------------------------------
