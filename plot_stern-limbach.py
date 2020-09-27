#!/usr/bin/env python3

# ---------------------------------------------------------------------------------------------------------
# ------ moules
# ---------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker  # - ticks
import numpy as np
import sys # to get System-specific parameters
import os # contains some useful functions on pathnames
import glob # - Unix style pathname pattern expansion
from scipy.interpolate import interp1d
from itertools import cycle # - lines style in a for loop

# ---------------------------------------------------------------------------------------------------------
# ------ body
# ---------------------------------------------------------------------------------------------------------
print(f'\nPlotting Radial Distribution Analisys (pfile)\n')

# -----------------------------------------------------------
# - working directory
print(f"\nCurrent working directory: {os.getcwd()}")

##### if uncomment the section to change the working dir, must change
##### len(sys.argv) < 3
##### input_arguments =

# if len(sys.argv) <= 1:
#     tmp_dir =  input(f'\nDirectory (whit the XYZ files) to make the pfile [default: empty]: ')
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
# - pfile files to plot
plot_files = []
if len(sys.argv) < 2:
    input_files =  input(f"List of files to plot, **separated by space** [Default: all '.dat']: ")

    # - by default reading elements for the first XYZ file
    if len(input_files.split()) < 1:
        for pfiles in glob.glob('*.dat'):
            plot_files.append(pfiles)
    else:
        plot_files = input_files.split()
else:
    input_arguments = 1
    while input_arguments < len(sys.argv):
        plot_files.append(sys.argv[input_arguments])
        input_arguments += 1

# - checking if there is any file to plot
if len(plot_files) > 0:
    # print(f'\nList of files:\n\n{plot_files}\n')
    print(f'\nList of files:\n')
    print('\n'.join(plot_files))
    for pfiles in plot_files:
        if not os.path.exists(pfiles):
            exit(f'\n*** Warinnig ***\n file {pfiles} does not exits \n')
else:
    exit(f'\n *** ERROR ***\n No files found to plot\n')

# -----------------------------------------------------------
# - plotting: defining frames and designing the area to plot
# - Stern-Limbach plot
fig = plt.figure(figsize=(10, 8))  # inches WxH
# fig.suptitle(f'Stern-Limbach for {transfer_list[0]}--{transfer_list[1]}$\cdots${transfer_list[2]}', fontsize=20) #, fontweight='bold')
fig.suptitle(f'Stern-Limbach', fontsize=25) #, fontweight='bold')

ax1 = plt.subplot(111)
ax1.grid()

# - legends for the main plot
plt.xlabel('$q_1=(r_1-r_2)/2$ [Angstrom]', fontsize=18) #, fontweight='bold')
plt.ylabel('$q_2=r_1+r_2$ [Angstrom]', fontsize=18) #, fontweight='bold')

# -markers
lines = ['o', '^', 'v', '<', '>', 's', 'd'] #, 'h', 'p', 'D', 'H']
linecycler = cycle(lines)

# -----------------------------------------------------------
# - loading files to read and plot them
for pfile in plot_files:
    name = pfile.split('/')[:-1]
    name = '/'.join(name)

    x, y = [], []
    for line in open(pfile, 'r'):
        # skipping the header
        if line.startswith("#"):
            label = [header.title() for header in line.split()]
            label_x = ' '.join(label[1:3])
            continue

        values = [float(s) for s in line.split()]
        x.append(values[0])
        y.append(values[1])

    if pfile == 'water_hexamer/transfer_O-H-O.dat':
        m, b = np.polyfit(x, y, 1)
        ax1.plot(x, m*np.array(x) + b, '-', linewidth=3, color='black', label='%s' %(name))
    else:
        ax1.plot(x, y, next(linecycler), markerfacecolor='none', markeredgewidth=2, label='%s' %(name))

    ax1.xaxis.set_major_locator(plt.MaxNLocator(12))

# -----------------------------------------------------------
# - Ending the plot

plt.legend(loc=0, fontsize=18)
# Put a legend below current axis
# plt.legend(loc='lower center', bbox_to_anchor=(1.32, 0.6, 0.0, 0.0),
#             fancybox=True, shadow=True, ncol=1, fontsize=11)

# # - Shrink current axis's height by 10% on the bottom
# box = ax1.get_position()
# ax1.set_position([box.x0, box.y0, box.width * 0.7, box.height])

# ---------------------------------------------------------------------------------------------------------
# - ENDING the plots
plt.show()

print(f'\n *** DONE ***\n')
# ---------------------------- END
exit()
