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
# - working directory
print(f"\nCurrent working directory: {os.getcwd()}")

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
# - Stern-Limbach plot
# -----------------------------------------------------------

# - plotting: defining frames and designing the area to plot
fig = plt.figure(figsize=(10, 8))  # inches WxH
# fig.suptitle(f'Stern-Limbach', fontsize=25) #, fontweight='bold')

ax1 = plt.subplot()
ax1.grid()

# - legends for the main plot
# plt.xlabel('$q_1=(r_1-r_2)/2$ [Angstrom]', fontsize=18) #, fontweight='bold')
# plt.ylabel('$q_2=r_1+r_2$ [Angstrom]', fontsize=18) #, fontweight='bold')
plt.xlabel('$q_1=(r_1-r_2) /2$   $[\\AA]$', fontsize=18) #, fontweight='bold')
plt.ylabel('$q_2=r_1+r_2$   $[\\AA]$', fontsize=18) #, fontweight='bold')

# - adding an extra text on the plot
ax1.text(-0.45, 2.3, r'A $-$ X $\cdots\rightarrow$B',
        color='black', fontsize=35,
        rotation=0, va='center', bbox=dict(facecolor='white', edgecolor='none'))
ax1.text(-0.41, 2.35, '$r_1$',
        color='black', fontsize=20,
        rotation=0, va='center', bbox=dict(facecolor='white', edgecolor='none'))
ax1.text(-0.31, 2.35, '$r_2$',
        color='black', fontsize=20,
        rotation=0, va='center', bbox=dict(facecolor='white', edgecolor='none'))

ax1.text(-0.15, 2.3, r'Atom transfer $q_1\rightarrow$0',
        color='black', fontsize=14,
        rotation=0, va='center', bbox=dict(facecolor='white', edgecolor='none'))

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
        name = name.split('/')[1:]
        name = '/'.join(name)
        ax1.plot(x, y, next(linecycler), markerfacecolor='none', markeredgewidth=2, label='%s' %(name))

    ax1.xaxis.set_major_locator(plt.MaxNLocator(12))

# -----------------------------------------------------------
# - Ending the plot

plt.legend(loc=1, fontsize=16)

# ---------------------------------------------------------------------------------------------------------
# - ENDING the plots
plt.show()

print(f'\n *** DONE ***\n')
# ---------------------------- END
exit()
