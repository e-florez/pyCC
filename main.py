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
#   cesar-b29@hotmail.com

# ------------------------------------------------------------------------------------
# Description:

# Radial, Angle, and Dihedral Distribution Analisys (RADDA)
# 1) Bond length frequency
# 2) Angle frequency
# 3) Dihedral frequency
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# ------ modules
# ------------------------------------------------------------------------------------
import functions  # module with all the individuals function to do analysis


# ------------------------------------------------------------------------------------
# ------ Preamble
# ------------------------------------------------------------------------------------

print(f'\n****************************************************')
print(f'*    Radial, Angle, and Dihedral       *')
print(f'* Distribution Analisys for XYZ files  *')   
print(f'*              "RADDA"                 *')
print(f'****************************************************')


# ------------------------------------------------------------------------------------
# ------ Main body
# ------------------------------------------------------------------------------------

if __name__ == '__main__':

    list_xyz_file = functions.reading_files_XYZ()
    
    print()
    print(len(list_xyz_file))
    print(list_xyz_file)
    print()
    print()

