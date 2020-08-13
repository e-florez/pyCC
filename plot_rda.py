#!/usr/bin/python3.8

# -----------------------------------
# ------ moules
# -----------------------------------
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker  # - ticks
import numpy as np
import sys # to get System-specific parameters
import os # contains some useful functions on pathnames
# -  to smooth out your data
from scipy.interpolate import make_interp_spline, BSpline

# -----------------------------------
# ------ body
# -----------------------------------
print(f'\nPlotting Radial Distribution Analisys (RDA)\n')

# # - RDA files to plot
# if len(sys.argv) <= 1:
#     rda_input =  input(f"List of files to plot RDA, **separated by space** [Default: all '.dat']: ")

# # - by default reading elements for the first XYZ file
# all_elements = False
# if len(input_elements.split()) < 1 or input_elements == 'all':
#     all_elements = True
#     elements = pd.read_csv(list_xyz[0], delim_whitespace=True,
#                            skiprows=2, header=None,
#                            names=["element", "x-coordinate", "y-coordinate", "z-coordinate"])
#     elements = elements['element'].tolist()
# else:
#     elements = input_elements.split()

rda_files = []
input_arguments = 1
while input_arguments < len(sys.argv):
    rda_files.append(sys.argv[input_arguments])
    input_arguments += 1

if len(rda_files) > 0:
    print(f'\nList of files to plot RDA: {rda_files}\n')
else:
    exit(f'\n *** ERROR ***\n No files found \n')

# - plotting
fig = plt.figure() #figsize=(10, 8))  # inches WxH
fig.suptitle('Radial Distribution Analisys', fontsize=20) #, fontweight='bold')

ax1 = plt.subplot(111)
ax1.grid()

# - legends for the main plot
plt.ylabel('Relative Number of Ocurrences', fontsize=12) #, fontweight='bold')
plt.xlabel('Bond Distance [Angstrom]', fontsize=12) #, fontweight='bold')

ax1.xaxis.set_major_locator(plticker.MultipleLocator(base=0.2))

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

    ax1.plot(smooth_x, smooth_y / total, label=' %s \n Total distances= %i' %(rda, total))
    # ax1.plot(x, y, label='%s' %rda)

    # - Put a legend below current axis
    plt.legend(loc=0)


# - ENDING the plots
plt.show()

print(f'\n *** DONE ***\n')
# ---------------------------- END
exit()