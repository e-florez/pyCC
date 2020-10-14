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
# ------ Preamble
# ------------------------------------------------------------------------------------
# Description:

import functions  # module with all the individuals function to do analysis
message = """

**********************************************************
* Geometrical Analisys for Atomic and Molecular clusters *   
*              - files with XYZ format -                 *   
*                                                        *
* Radial, Angular and Dihedral Distribution (Histogram)  *
* Atom transfer (Stern-Limbach)                          *
*                                                        *
*                                                        *
* by:                                                    *
*    Edison Florez, Andy Zapata, Cesar Ibarguen (2020)   *
*                                                        *
**********************************************************

"""

print(message)

# ------------------------------------------------------------------------------------
# ------ modules
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# ------ Main body
# ------------------------------------------------------------------------------------

if __name__ == '__main__':

    working_dir = 'here'

    # list_files_XYZ = ["w1s1.xyz", "w2s1.xyz", "w3s1.xyz", "w6s10.xyz"]
    list_files_XYZ = ["w1s1.xyz", "w2s1.xyz"]

    # - choosing those XYZ files to analyse
    files_xyz = functions.what_xyz_files(list_files_XYZ, working_dir)

    # Choosing those XYZ files to be analyse (by default all in working directory)
    # and CHECKING if those files has the XYZ format to create a dictionary 'coordinates_XYZ'
    # for each XYZ file with their coordinates in a pandas data frame
    coordinates_XYZ = functions.dict_coordinates_xyz(files_xyz)

    for key in coordinates_XYZ:
        print('\n' + '--' * 30 +
              f'\n file: {key}\n' + '--' * 30 + '\n', coordinates_XYZ[key], '\n')
