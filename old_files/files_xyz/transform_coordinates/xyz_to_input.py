#!/usr/bin/python3
# ------------------------------------------------------------------------------------
# July 2020
#   edisonffh@gmail.com
#
# python3.x script to transfor XYZ coordinates into Gaussian .COM or Dirac .mol files
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# ------ moules
# ------------------------------------------------------------------------------------
import sys # to get System-specific parameters
import os  # - to check id a file or dir exits -> os.path.exists()
import glob # - Unix style pathname pattern expansion
# import numpy as np # - arrays and matrix manipulation

# ------------------------------------------------------------------------------------
# ------ body
# ------------------------------------------------------------------------------------
print(f'\n****************************************************')
print(f'* Radial Distribution Analisys (RDA) for XYZ files *')
print(f'****************************************************')

# ------------------------------------------------------------------------------------
# - working directory
if len(sys.argv) <= 1:    
    tmp_dir =  input(f'\nDirectory whit the XYZ files [default: current]: ')
    tmp_dir = tmp_dir.strip()

    if tmp_dir == '.' or len(tmp_dir) < 1:
        working_dir = os.getcwd()
    else:
        working_dir = os.getcwd() + '/' + tmp_dir
else:
    if sys.argv[1] == '.':
        working_dir = os.getcwd() + '/' 
    else:
        working_dir = os.getcwd() + '/' + sys.argv[1]

print(f'\nWorking directory: {working_dir}')

# Check if working dir exists
if os.path.isdir(working_dir) :
    # Change the current working Directory
    os.chdir(working_dir)
else:
    print(f'\n*** ERROR ***')
    exit(f"Can't change the Working Directory doesn't exist \n{working_dir}\n")

# ------------------------------------------------------------------------------------
# - files to transform
list_xyz_files = []
if len(sys.argv) < 3:
    input_files =  input(f"List of XYZ files, **separated by space** [default: all]: ")

    # - by default reading elements for the first XYZ file
    if len(input_files.split()) < 1:
        for file_rda in glob.glob('*.xyz'):
            list_xyz_files.append(file_rda)
    else:
        list_xyz_files = input_files.split()
else:
    input_arguments = 2
    while input_arguments < len(sys.argv):
        list_xyz_files.append(sys.argv[input_arguments])
        input_arguments += 1

# - checking if there is any file to plot
if len(list_xyz_files) > 0:
    print(f'\nList of XYZ files:')
    count = 0
    col = 3
    while count < len(list_xyz_files):
        print(f'\t'.join(list_xyz_files[count : count + col]))
        count += (col + 1)

    for file_xyz in list_xyz_files:
        if not os.path.exists(file_xyz):
            print(f'\n*** Warinnig ***')
            print(f'file {file_xyz} does not exits in \n{working_dir}\n')
else:
    exit(f'\n *** ERROR ***\n No XYZ files found in \n{working_dir}\n')

# ------------------------------------------------------------------------------------
# OUTPUT formats

def output_format():
    """
    
    """

    
    return ()

# ------------------------------------------------------------------------------------
# - loading files to read 


output_type = output_format(xyz)


for file_xyz in list_xyz_files:
    atoms, coordinates = [], []

    # - total lines
    total_lines = sum(1 for line in open(file_xyz, 'r'))
    
    lines_counter = 1
    current_line = 1

    ext = '.xyz'

    for line in open(file_xyz, 'r'):
        read_line = [value for value in line.split()]

        if lines_counter == current_line: #first line
            num_atoms = int(read_line[0])

            # - saving the first structure
            motif = 1
            file_name = 'w' + str(int((num_atoms - 1) / 3)) + 's' + str(motif) + ext
            new_file = open(file_name, 'w')            
            
        elif lines_counter == (current_line + 1):
            # - to XYZ file
            # new_file.write('   %i\n' %(num_atoms) )
            # new_file.write(' Comments\n')            

            output_type = output_format()

            new_file.write()

        elif lines_counter > (current_line + 1) \
            and lines_counter < (current_line + num_atoms + 2):
            
            new_file.write(' %3s   %20.10f %20.10f %20.10f\n' \
                %( str(read_line[0]), \
                   float(read_line[1]), float(read_line[2]), float(read_line[3]) ) )

        else:
            # - closing previous file
            new_file.close()

            # - moving to the next set of coordinates
            current_line = lines_counter

            if lines_counter < total_lines:
                # - counting structures with the same number of atoms
                if num_atoms == int(read_line[0]):
                    motif += 1
                else:
                    motif = 1

                num_atoms = int(read_line[0])
                # - open a new file
                file_name = 'w' + str(int((num_atoms - 1) / 3)) + 's' + str(motif) + ext
                new_file = open(file_name, 'w')                
        
        lines_counter += 1

# ------------------------------------------------------------------------------------
print(f'\n****************************************************')
print(f'*** DONE ***')
print(f'****************************************************\n')
# ---------------------------- END
exit()
