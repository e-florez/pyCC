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

import matrix_r  # module to calculate of matriz distance
import sys  # module to recognise input argument form terminal (sys.argv)
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

    # -----------------------------------------------------------------------
    # At this point we have loaded all coordinates as a pandas dataframe,
    # for those XYZ file with a right format.

    # - CESAR: define a grid for each histogram: bond, angle and dihedral angle

    # - ANDY: Computing matrix distance for each XYZ and create a
    #   dictionary whit a panda data frame with all distances between
    #   all possible atomic pairs
    # R_Matrix = matrix_r.Distance_Matrix(files_xyz, coordinates_XYZ)

    # - EDISON: Multihistogram analysis for bond ditribution

    # - grid to do a histogram analysis, rmin, rmax and bin width
    grid = (0.5, 3.0, 0.01)

    # - distance matrix
    import distance_matrix
    distances_dict = distance_matrix.distance_matrix(coordinates_XYZ, grid)

    # - atomic pairs
    input_list = ['H', 'O']
    # input_list = ['H', 'O', 'H']
    # input_list = ['Hg', 'O', 'H', 'H']

    # - loop over each XYZ file to get atoms index
    index_dict = {}
    for xyz in distances_dict:
        distances = distances_dict[xyz]

        # - getting atoms list to compute distance, angle or dihedral
        import atoms_index_list
        atoms_index = atoms_index_list.atoms_index_list(distances, input_list, grid)

        # - dictionary with atoms index according to input list
        index_dict[xyz] = atoms_index

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # - index starts at zero.
        tmp = []
        for t in atoms_index:
            tmp2 = []
            for s in t:
                tmp2.append(s+1)
            tmp.append(tuple(tmp2))

        print(f'file: {xyz}')
        print(f'requiring: {input_list}\n')
        # print(atoms_index)
        print(tmp)
        print('\n\n')
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # - histogram analysis
    if len(input_list) == 2:
        # - bond distance analysis; i.e., input_list = [A, B]
        import rda
        rda.rda(index_dict, distances_dict, grid)

    elif len(input_list) == 3:
        # - anglular analysis; i.e., input_list = [A, B, C]
        pass
    elif len(input_list) == 4:
        # - dihedral analysis; i.e., input_list = [A, B, C, D]
        pass
