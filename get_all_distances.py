#!/usr/bin/python3.6

# ------------------------------------------
# July 2020
#               edisonffh@gmail.com
#
# python3.6 script to compute bond length
# frecuency in Hg(H_2O)_n clusters
#
# ------------------------------------------

# -----------------------------------
# ------ moules
# -----------------------------------
# - Unix style pathname pattern expansion
import glob
# - complete data analysis tool (it can replace matplotlib or numpy, as it is built on top of both)
import pandas as pd
# - arrays and matrix manipulation
import numpy as np
# - plotting
import matplotlib.pyplot as plt
# - runtime configuration (rc) containing the default styles for every plot element you create
from matplotlib import rc
# --- enable TeX mode for matplotlib
rc('text', usetex=True)

# -----------------------------------
# ------ body
# -----------------------------------

# - list for xyz files
repited_list_xyz = []  # repited files (if any)
list_xyz = []  # unique files

# - reading files
for input_xyz in glob.glob('*.xyz'):
    name_xyz = input_xyz[:-4]  # deleting file extention
    repited_list_xyz.append(input_xyz)  # creating an array for all xyz files

    # keeping unique xyz files
    for unique_input_xyz in repited_list_xyz:
        if unique_input_xyz not in list_xyz:
            list_xyz.append(unique_input_xyz)

list_xyz = ["w6s1.xyz"]

# - reading coordinates fro XYZ file
for file_xyz in list_xyz:
    atoms = pd.read_csv(file_xyz, nrows=1, header=None)
    # importing data with pandas (skipping comments line; rsecond row)
    data_xyz = pd.read_csv(file_xyz, delim_whitespace=True,
                           skiprows=2, header=None)

    # print(f'\n file: {file_xyz}\n atoms: {int(atoms.iloc[0])}')
    # print(f'Pandas data is: \n{data_xyz.iloc[0,:]}\n')
    # print(f'Pandas data is: \n{data_xyz.iloc[1,:]}\n')
