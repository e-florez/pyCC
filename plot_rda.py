#!/usr/bin/python3.8

# ---------------------------------------------------------------------------------------------------------
# ------ moules
# ---------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker  # - ticks
import numpy as np
import sys # to get System-specific parameters
import os # contains some useful functions on pathnames
import glob # - Unix style pathname pattern expansion
from scipy.interpolate import make_interp_spline, BSpline # - to smooth out your data

# ---------------------------------------------------------------------------------------------------------
# ------ body
# ---------------------------------------------------------------------------------------------------------
print(f'\nPlotting Radial Distribution Analisys (RDA)\n')

# -----------------------------------------------------------
# - working directory
print(f"\nCurrent working directory: {os.getcwd()}")

##### if uncomment the section to change the working dir, must change 
##### len(sys.argv) < 3
##### input_arguments = 

# if len(sys.argv) <= 1:    
#     tmp_dir =  input(f'\nDirectory (whit the XYZ files) to make the RDA [default: empty]: ')
#     tmp_dir = tmp_dir.strip()

#     if tmp_dir == '.' or len(tmp_dir) < 1:
#         working_dir = os.getcwd()
#     else:
#         working_dir = os.getcwd() + '/' + tmp_dir
# else:
#     working_dir = os.getcwd() + '/' + sys.argv[1]

# print(f'\nWorking directiry: {working_dir}')

# # Check if New path exists
# if os.path.exists(working_dir) :
#     # Change the current working Directory    
#     os.chdir(working_dir)
# else:
#     print(f'\n*** ERROR ***')
#     exit(f"Can't change the Working Directory, {working_dir} doesn't exist")   

# -----------------------------------------------------------
# - RDA files to plot
rda_files = []
if len(sys.argv) < 2:
    input_files =  input(f"List of files to plot RDA, **separated by space** [Default: all '.dat']: ")

    # - by default reading elements for the first XYZ file
    if len(input_files.split()) < 1:
        for file_rda in glob.glob('*.dat'):
            rda_files.append(file_rda)
    else:
        rda_files = input_files.split()
else:
    input_arguments = 1
    while input_arguments < len(sys.argv):
        rda_files.append(sys.argv[input_arguments])
        input_arguments += 1

# - checking if there is any file to plot
if len(rda_files) > 0:
    print(f'\nList of files:\n\n{rda_files}\n')
    for file_rda in rda_files:
        if not os.path.exists(file_rda):
            print(f'\n*** Warinnig ***\n file {file_rda} does not exits \n')
else:
    exit(f'\n *** ERROR ***\n No files found to plot\n')

# -----------------------------------------------------------
# - plotting: defining frames and designing the area to plot
fig = plt.figure(figsize=(10, 8))  # inches WxH
fig.suptitle('Radial Distribution Analisys', fontsize=20) #, fontweight='bold')

ax1 = plt.subplot(111)
ax1.grid()

# - legends for the main plot
plt.ylabel('Relative Number of Ocurrences', fontsize=12) #, fontweight='bold')
plt.xlabel('Bond Distance [Angstrom]', fontsize=12) #, fontweight='bold')

# - ticks for the x-axis
ax1.xaxis.set_major_locator(plticker.MultipleLocator(base=0.2))

# -----------------------------------------------------------
# - loading files to read and plot them
for rda in rda_files:
    x, y = [], []
    for line in open(rda, 'r'):
        # skipping the header
        if line.startswith("#"):
            continue

        values = [float(s) for s in line.split()]
        x.append(values[0])
        y.append(values[1])

    # total number of distances
    total = sum(y)

    # - to smooth the curve (BSpline)
    smooth_x = np.linspace(x[0], x[-1], len(x)*100)

    # smooth curve BSpline, degree k=3, cubic
    smooth = make_interp_spline(x, y, k=3)
    smooth_y = smooth(smooth_x)

    # - Bspline fitting
    ax1.plot(smooth_x, smooth_y / total, label=' %s \n Total distances= %i' %(rda, total))
    
    # - raw data, no Bspline fitting
    # ax1.plot(x, y, label='%s' %rda)

# -----------------------------------------------------------
# - Ending the plot

# plt.legend(loc=0)
# Put a legend below current axis
plt.legend(loc='lower center', bbox_to_anchor=(1.32, 0.6, 0.0, 0.0),
            fancybox=True, shadow=True, ncol=1, fontsize=11)

# - Shrink current axis's height by 10% on the bottom
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.7, box.height])

# ---------------------------------------------------------------------------------------------------------
# - ENDING the plots
plt.show()

print(f'\n *** DONE ***\n')
# ---------------------------- END
exit()
