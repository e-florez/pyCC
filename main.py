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
#   César Ibargüen Becerra (github.com/cesar-ibarguen)
#   email: cesar-b29@hotmail.com
#   affiliation: University of Antioquia, Medellín-Colombia

# ------------------------------------------------------------------------------------
# ------ Preamble
# ------------------------------------------------------------------------------------
# Description:

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
import functions  # module with all the individuals function to do analysis
import sys # module to recognise input argument form terminal (sys.argv)

# ------------------------------------------------------------------------------------
# ------ Main body
# ------------------------------------------------------------------------------------

if __name__ == '__main__':

    # - Working directory: checking permission and existence 
    working_dir = functions.working_directory(sys.argv)

    # - Function to check if XYZ files exist, list and sort them in working directory
    list_files_XYZ = functions.reading_files_xyz(working_dir)

    # - Choosing XYZ files (by default all in working directory)
    files_xyz = functions.what_xyz_files(list_files_XYZ, working_dir)

    # - Checking if those files has the XYZ format 
    #   to create a dictionary 'coordinates_XYZ' with all the XYZ file 
    #   with their coordinates in a pandas data frame
    coordinates_XYZ = functions.dict_coordinates_xyz(files_xyz)

    #-----------------------------------------------------------------------
    # At this point we have loaded all coordinates as a pandas dataframe,
    # for those XYZ file with a right format.



    # - CESAR: define a grid for each histogram: bond, angle and dihedral angle
    



    # - ANDY: Computing matrix distance for each XYZ and create a 
    #   dictionary whit a panda data frame with all distances between 
    #   all possible atomic pairs




    # - EDISON: Multihistogram analysis for bond ditribution
