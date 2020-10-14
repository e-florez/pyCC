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
# ------ Main body
# ------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    list_files_XYZ = ["w1s1.xyz", "w2s1.xyz", "w3s1.xyz", "w6s10.xyz"]

    coordinates_XYZ = functions.format_files_XYZ(list_files_XYZ)


