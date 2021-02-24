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
import functions  # module with all the individuals function to do analysis
import sys  # module to recognise input argument form terminal (sys.argv)
import matrix_r  # module to calculate of matriz distance
import numpy as np


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

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # - grid to do a histogram analysis, rmin, rmax and bin width
    grid = (0.6, 2.5, 0.05)

    # - number of bins for the accurences
    rmin, rmax, dr = grid
    nbins = int((rmax - rmin) / dr)

    # - distance matrix
    import distance_matrix
    distances_dict = distance_matrix.distance_matrix(coordinates_XYZ, grid)

    # - atomic pairs
    # input_list = ['H', 'O']
    # input_list = ['O', 'H']
    # input_list = ['H', 'O', 'H']
    # input_list = ['O', 'Hg', 'O']
    input_list = ['O', 'H', 'O']     # Stern-Limbach
    # input_list = ['Hg', 'O', 'H', 'H']

    # - getting atoms list to compute distance, angle or dihedral
    import atoms_index_list
    index_dict = atoms_index_list.atoms_index_dict(distances_dict, input_list, grid)

    # -----------------------------------------------------------
    # - histogram analysis
    import histogram
    if len(input_list) == 2:

        # - radial (bond) distribution analysis (RDA); i.e., input_list = [A, B]
        histogram = histogram.rda(index_dict, distances_dict, grid, nbins)

        # - saving histogram
        bond_distance = np.linspace(rmin, rmax, nbins)
        pair = f'-'.join(input_list)

        # if sum(histogram) > 0:
        histogram_name = 'rda_' + pair + '.dat'
        np.savetxt(histogram_name, np.transpose([bond_distance, histogram]),
                   delimiter=' ',
                   header='distance [Angstrom]   occurrence (total=%i)'
                   % sum(histogram),
                   fmt='%.6f %28i')

    elif len(input_list) == 3:
        # - anglular distribution analysis (ADA); i.e., input_list = [A, B, C]

        # - grid = 0.1 --> 1800 = (180 - 0)/0.1
        delta_angle = 5.0
        min_angle = 0
        max_angle = 190
        nbins = int((max_angle - min_angle) / delta_angle)

        histogram = histogram.ada(
            index_dict, coordinates_XYZ, delta_angle, nbins)

        # - saving histogram
        angle_distribution = np.linspace(min_angle, max_angle, nbins)
        pair = f'-'.join(input_list)

        histogram_name = 'ada_' + pair + '.dat'
        np.savetxt(histogram_name, np.transpose([angle_distribution, histogram]),
                   delimiter=' ',
                   header='angle [Degrees]   occurrence (total=%i)'
                   % sum(histogram),
                   fmt='%.6f %28i')

        #------------------------------------------------
        # - Stern-Limbach analisys for atom tranfers

        import atoms_transfer as transfer

        input_list = list(input_list)

        natural_bond_coordinates = transfer.atom_transfer(
            index_dict, input_list, distances_dict)

        triplets = '-'.join(input_list)
        transfer_name = 'transfer_' + '-'.join(input_list) + '.dat'

        print(f'')
        print(
            f'Atoms transfer analysis ({triplets}) according to Stern-Limbach model (q1, q2):')
        print(
            f'Transfer of atoms {input_list[1]} ' +
            f'between {input_list[0]} and {input_list[2]}, ' +
            f'where q1=0.5*(r1-r2) and q2=r1+r2, ' +
            f'r1: distance[{input_list[0]}{input_list[1]}] and r2: distance[{input_list[1]}{input_list[2]}]')
        print(f'')

        np.savetxt(transfer_name, natural_bond_coordinates,
                   delimiter=' ', header='q1 [Angstrom]    q2 [Angstrom]',
                   fmt='%15.10f %15.10f')


    elif len(input_list) == 4:
        # - dihedral analysis; i.e., input_list = [A, B, C, D]

        # grid = 0.1 --> 3600 = (3600 - 0)/0.1
        delta_angle = 5.0
        min_angle = 0
        max_angle = 360

        nbins = int((max_angle - min_angle) / delta_angle)

        histogram = histogram.dada(
            index_dict, coordinates_XYZ, delta_angle, nbins)

        # - saving histogram
        angle_distribution = np.linspace(min_angle, max_angle, nbins)
        pair = f'-'.join(input_list)

        histogram_name = 'dada_' + pair + '.dat'
        np.savetxt(histogram_name, np.transpose([angle_distribution, histogram]),
                   delimiter=' ',
                   header='angle [Degrees]   occurrence (total=%i)'
                   % sum(histogram),
                   fmt='%.6f %28i')
