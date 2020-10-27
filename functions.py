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
    The aim of this function is to read, to make a list  and sorting the XYZ files into the working directory 
      
    Args: 
        working_dir (str): Correspond to the path to working directory
    Returns: 
        files_list_xyz (list str): It is a list with the names of all XYZ files in working directory to be analyzed

    by: César Ibarguen-Becerra <cesar-b29@hotmail.com>
    """
    repited_list_xyz = []  # repited files (if any)
    list_xyz = []  # unique files

    import glob             # - Unix style pathname pattern expansion
    import os               # - to check id a file or dir exits -> os.path.exists() # -  to smooth out your data
    #from natsort import natsorted  # Simple yet flexible natural sorting in Python.


    # - reading files
    for input_xyz in glob.glob('*.xyz'):
        name_xyz = input_xyz[:-4]  # deleting file extention
        repited_list_xyz.append(input_xyz)  # creating an array for all xyz files

            # keeping unique xyz files
        for unique_input_xyz in repited_list_xyz:
            if unique_input_xyz not in list_xyz:
                list_xyz.append(unique_input_xyz)

    # - sorting the input files list for a easier reading 
    #    list_xyz = natsorted(list_xyz)

    # - checking if files exist
    if len(list_xyz) > 0:
        for input_xyz in list_xyz:
            if not os.path.exists(input_xyz):
                print(f'\n*** Warinnig ***\n file {input_xyz} does not exits \n')
    else:
        exit(f' *** ERROR ***\n No file found to make the RDA \n ')

    print(f'\nA total of {len(list_xyz)} xyz files were  analized\n')

    count = 0
    columns = 4
    while count < len(list_xyz):
        print(f'\t'.join(list_xyz[count:count + columns]))

        count += (columns + 1)

        return list_xyz

print(reading_files_XYZ())

# def format_files_XYZ(): 
#        """
#        [summary]

#        input: a, b, c
#        output: d

#        Args:
#            a (str): distancia
#            b ([type]): [description]
#            c ([type]): [description]
#            d ([type]): [description]
#     """
# #    pass