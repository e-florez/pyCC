#!/usr/bin/python3.6

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
# ------ script
# -----------------------------------
# - reading files & creating variables
list_xyz = []  # array for xyz files
for input_xyz in glob.glob('*.xyz'):
    fname = input_xyz[:-4]  # deleting file extention
    list_xyz.append(input_xyz)  # creating an array for all xyz files
