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
#   César Ibargüen Becerra (github.com/cesar-ibarguen)
#   email: cesar-b29@hotmail.com
#   affiliation: University of Antioquia, Medellín-Colombia

# ------------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# Main body
# ------------------------------------------------------------------------------------

def working_directory(arg_prompt):
    import os  # - to check id a file or dir exits -> os.path.exists()

    """[summary]
    Asking or taking path of working directory from argument of prompt and
    verification of working directory

    Args:
        arg_prompt (str): argument in the prompt when was execution of program
    """

    if len(arg_prompt) <= 1 : #argument from prompt shell is not vaccum
        tmp_dir =  input(f'\nAddress of directory (whit the XYZ files) [default: empty]: ')
        tmp_dir = tmp_dir.strip()

        if tmp_dir == '.' or len(tmp_dir) < 1: #get path of current directory
            working_dir = os.getcwd()
        else:  #get full path of working directory
            if tmp_dir[0] == "/":
                working_dir = tmp_dir
            else:
                working_dir =  str(os.getcwd()) + "/" + str(tmp_dir)

    elif arg_prompt[1] == '.' : #argument from prompt shell indicate the current directory
        working_dir = os.getcwd()

    else:   #argument from prompt shell is vaccum
        if arg_prompt[1][0] == "/" :  #Full path (Since the root)
            working_dir = arg_prompt[1]
        else:                         #Path incompleted
            working_dir =  str(os.getcwd()) + "/" + str(arg_prompt[1])

    print(f'\nWorking directiry: {working_dir}')   #Working directory

    # Check if the working dir exists
    if os.path.exists(working_dir) :
        #Verification of permission of directory
        read_permission = os.access(working_dir, os.R_OK)
        write_permission = os.access(working_dir, os.W_OK)
        execution_permission = os.access(working_dir, os.X_OK)
        save_new_file_permission = os.access(working_dir, os.X_OK | os.W_OK)
        if read_permission == True and write_permission == True and\
            execution_permission == True and save_new_file_permission == True:
            # Change the current working Directory
            os.chdir(working_dir)
        else:
            print(f'\n*** ERROR ***')
            if read_permission == False:
                print(f"\n Read permission missing")
            if write_permission == False:
                print(f"\n Write permission missing")
            if execution_permission == False:
                print(f"\n Execution permission missing")
            if save_new_file_permission == False:
                print(f"\n Save new files permission missing")
            exit(f'\n*** Directory permissions insufficient ***')
    else:
        print(f'\n*** ERROR ***')
        exit(f"Can't change the Working Directory, {working_dir} doesn't exist")
#*******************************************************************************#

def reading_files_xyz():
    # - Unix style pathname pattern expansion
    import glob
    # - to check id a file or dir exits -> os.path.exists() # -  to smooth out your data
    import os
    # Simple yet flexible natural sorting in Python.
    from natsort import natsorted

    """
    The aim of this function is to read, to make a list  and sorting the XYZ files into the working directory 
      
    Args:  
        This functions does not have a argument, but it depend on working_dir (str), which 
        correspond to the path to working directory
    Returns: 
        files_list_xyz (list str): It is a list with the names of all XYZ files in working directory to be analyzed

    by: César Ibarguen-Becerra <cesar-b29@hotmail.com>
    """

    # Initializing an empty list for repited files (if any)
    repited_list_xyz = []
    list_xyz = []  # Initializing an empty list unique files

    # - reading files
    for input_xyz in glob.glob('*.xyz'):
        # creating an array for all xyz files
        repited_list_xyz.append(input_xyz)

        # keeping unique xyz files
        for unique_input_xyz in repited_list_xyz:
            if unique_input_xyz not in list_xyz:
                list_xyz.append(unique_input_xyz)

    # - sorting the input files list for a easier reading
    list_xyz = natsorted(list_xyz)

    # - checking if files exist
    if len(list_xyz) > 0:
        for input_xyz in list_xyz:
            if not os.path.exists(input_xyz):
                print(
                    f'\n*** Warinnig ***\n file {input_xyz} does not exits \n')
    else:
        exit(f' *** ERROR ***\n No file found to make the RDA \n ')

    print(f'\nA total of {len(list_xyz)} xyz files found\n')

    # - Showing those XYZ file
    count = 0
    columns = 4
    while count < len(list_xyz):
        print(f'\t'.join(list_xyz[count:count + columns]))

        count += columns

    print()

    return list_xyz
# --------------------------------------------------


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


def transform_to_symbols(value):
    """
    Returns the symbol for any atomic number (Z) in the periodic table (0 <= Z <= 118)

    Args:
        value (str or int): atomic number [0, 118]

    Returns:
        symbol (str): symbol from any atomic number in the periodic table
                      if 'value' is not (0, 118] it returns the same value

    by: edisonffh@gmail.com
    """

    symbols_list = {1: "H",
                    2: "He",
                    3: "Li",
                    4: "Be",
                    5: "B",
                    6: "C",
                    7: "N",
                    8: "O",
                    9: "F",
                    10: "Ne",
                    11: "Na",
                    12: "Mg",
                    13: "Al",
                    14: "Si",
                    15: "P",
                    16: "S",
                    17: "Cl",
                    18: "Ar",
                    19: "K",
                    20: "Ca",
                    21: "Sc",
                    22: "Ti",
                    23: "V",
                    24: "Cr",
                    25: "Mn",
                    26: "Fe",
                    27: "Co",
                    28: "Ni",
                    29: "Cu",
                    30: "Zn",
                    31: "Ga",
                    32: "Ge",
                    33: "As",
                    34: "Se",
                    35: "Br",
                    36: "Kr",
                    37: "Rb",
                    38: "Sr",
                    39: "Y",
                    40: "Zr",
                    41: "Nb",
                    42: "Mo",
                    43: "Tc",
                    44: "Ru",
                    45: "Rh",
                    46: "Pd",
                    47: "Ag",
                    48: "Cd",
                    49: "In",
                    50: "Sn",
                    51: "Sb",
                    52: "Te",
                    53: "I",
                    54: "Xe",
                    55: "Cs",
                    56: "Ba",
                    57: "La",
                    58: "Ce",
                    59: "Pr",
                    60: "Nd",
                    61: "Pm",
                    62: "Sm",
                    63: "Eu",
                    64: "Gd",
                    65: "Tb",
                    66: "Dy",
                    67: "Ho",
                    68: "Er",
                    69: "Tm",
                    70: "Yb",
                    71: "Lu",
                    72: "Hf",
                    73: "Ta",
                    74: "W",
                    75: "Re",
                    76: "Os",
                    77: "Ir",
                    78: "Pt",
                    79: "Au",
                    80: "Hg",
                    81: "Tl",
                    82: "Pb",
                    83: "Bi",
                    84: "Po",
                    85: "At",
                    86: "Rn",
                    87: "Fr",
                    88: "Ra",
                    89: "Ac",
                    90: "Th",
                    91: "Pa",
                    92: "U",
                    93: "Np",
                    94: "Pu",
                    95: "Am",
                    96: "Cm",
                    97: "Bk",
                    98: "Cf",
                    99: "Es",
                    100: "Fm",
                    101: "Md",
                    102: "No",
                    103: "Lr",
                    104: "Rf",
                    105: "Db",
                    106: "Sg",
                    107: "Bh",
                    108: "Hs",
                    109: "Mt",
                    110: "Ds",
                    111: "Rg",
                    112: "Cn",
                    113: "Nh",
                    114: "Fl",
                    115: "Mc",
                    116: "Lv",
                    117: "Ts",
                    118: "Og"
                    }

    try:
        symbol = symbols_list[int(value)]
    except KeyError:
        # value is not (0, 118] returns value
        symbol = value

    return symbol
# ---------------------------------------------------------------------------------------


def format_xyz(file_xyz):
    # - Modules
    import pandas as pd

    """
    CHECKING if a file has the XYZ format.

    The formatting of the .xyz file format is as follows:
    
        <number of atoms>               # only one filed (int)
        comment line                    # free format
        <element> <X> <Y> <Z>           # four fields (str/int, float, float, float)

    Args:
        file_xyz (str): XYZ file name

    Returns:
        a pandas dataframe (element, x, y, z)

    by: Edison Florez <edisonffh@gmail.com>
    """

    # - if error_message == 0, not error found
    error_message = ''

    # - numbering lines
    line_number = 0

    # - atomic number will be replaced by their symbol
    symbols = {}

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
            # - third line and beyond must have four fields: (element, x, y, z)
            elif line_number > 2:
                # - checking length, four fields
                try:
                    assert len(values) == 4
                except AssertionError as e:
                    error_message += '\n | Not enough data for elements and coordinates.'
                    error_message += '\n   It must be: (element, x, y, z)'
                    error_message += f'\n--- {e} ---\n'

                # - Four fields were found, so
                # - checking first column (element) and x, y, z coordinates
                else:
                    # - checking first column (elements), is it a str or int?
                    try:
                        int(values[0])

                    # - string
                    except ValueError:
                        # - as a string, symbol must be capitalised
                        symbols[values[0]] = values[0].capitalize()

                    # - integer (Not a 'ValueError')
                    else:
                        symbols[values[0]] = transform_to_symbols(values[0])

                    # - checking x, y, z coordinates
                    for i in range(1, 4):
                        try:
                            float(values[i])
                        except ValueError as e:
                            error_message += '\n | coordinates (x, y, z) must be floats'
                            error_message += f'\n--- {e} ---\n'

    if not error_message and (line_number - 2) != atoms_number:
        error_message += f'\n | Not enough atoms were found'
        error_message += f'\n ---Number of atoms at line 1: {atoms_number}, is not equivalent'
        error_message += f'\n    to the total number of lines found: {line_number} lines.'
        error_message += f'\n    Number of atoms (\'{atoms_number}\') plus two must be iqual'
        error_message += f'\n    to total lines (\'{line_number}\').'
        error_message += f' \'{atoms_number + 2}\' is not iqual to \'{line_number}\' ---'

    # - creating a df from a XYZ file
    if not error_message:
        df = pd.read_csv(file_xyz,
                         delim_whitespace=True,
                         skiprows=2,
                         header=None,
                         names=["element", "x-coordinate",
                                "y-coordinate", "z-coordinate"]
                         )

        # - Replacing atomic number into symbols or capitalising symbols (if any)
        df["element"] = df["element"].map(symbols)

    else:
        df = f" File \'{file_xyz}\' does not have XYZ file format\n" + \
            error_message

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
        # - creating a dataframe
        df = format_xyz(file_xyz)

        # - filtering XYZ file with errors (it will be a string, not a df)
        if isinstance(df, str):
            print(f'*** Format Error ***')
            print(df)
        else:
            coordinates_xyz[file_xyz] = df

    return coordinates_xyz
# ---------------------------------------------------------------------------------------
